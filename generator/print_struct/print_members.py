import model
from model import Container
from print_struct.util import type_to_python_str
from writer import Writer


def print_members_definitions(s: Writer, container: Container):
    non_optional = Writer()
    non_optional.inc_indent()

    optionals = Writer()
    optionals.inc_indent()

    for member in container.members:
        print_member_definition(non_optional, optionals, member, False)

    s.append(non_optional)
    s.append(optionals)

    s.newline()


def print_member_definition(
        non_optional: Writer, optionals: Writer, member: model.StructMember, optional: bool
):
    match member:
        case model.StructMemberDefinition(
            _tag,
            model.Definition(
                data_type=data_type,
                name=name,
                used_as_size_in=used_as_size_in,
                constant_value=constant_value,
                size_of_fields_before_size=size_of_fields_before_size,
                tags=tags,
            ),
        ):
            if (
                    used_as_size_in is not None
                    or size_of_fields_before_size is not None
                    or constant_value is not None
            ):
                return

            if optional:
                optionals.wln(
                    f"{name}: typing.Optional[{type_to_python_str(data_type)}] = None"
                )
            else:
                non_optional.wln(f"{name}: {type_to_python_str(data_type)}")

        case model.StructMemberIfStatement(_tag, struct_member_content=statement):
            print_member_if_statement(non_optional, optionals, statement)

        case model.StructMemberOptional(_tag, model.OptionalMembers(members=members)):
            for member in members:
                print_member_definition(non_optional, optionals, member, True)

        case _:
            raise Exception("invalid struct member")


def print_member_if_statement(
        non_optional: Writer, optionals: Writer, statement: model.IfStatement
):
    for member in statement.members:
        print_member_definition(non_optional, optionals, member, True)

    for elseif in statement.else_if_statements:
        print_member_if_statement(non_optional, optionals, elseif)

    for member in statement.else_members:
        print_member_definition(non_optional, optionals, member, True)
