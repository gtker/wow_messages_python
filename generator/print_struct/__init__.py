import model
from model import Container
from print_struct.print_read import print_read
from print_struct.print_size import print_size
from print_struct.print_write import print_write
from print_struct.util import type_to_python_str
from writer import Writer


def print_struct(s: Writer, container: Container):
    s.wln("@dataclasses.dataclass")
    s.wln(f"class {container.name}:")
    s.inc_indent()

    print_members_definitions(s, container)

    print_read(s, container)

    print_write(s, container)

    print_size(s, container)

    s.dec_indent()  # class
    s.newline()


def print_members_definitions(s: Writer, container: Container):
    for member in container.members:
        print_member_definition(s, member, False)

    s.newline()


def print_member_definition(s: Writer, member: model.StructMember, optional: bool):
    match member:
        case model.StructMemberDefinition(
            _tag,
            model.Definition(
                data_type=data_type,
                name=name,
                used_as_size_in=used_as_size_in,
                constant_value=constant_value,
                size_of_fields_before_size=size_of_fields_before_size,
            ),
        ):
            if (
                used_as_size_in is not None
                or size_of_fields_before_size is not None
                or constant_value is not None
            ):
                return

            if optional:
                s.wln(f"{name}: typing.Optional[{type_to_python_str(data_type)}]")
            else:
                s.wln(f"{name}: {type_to_python_str(data_type)}")

        case model.StructMemberIfStatement(_tag, model.IfStatement(members=members)):
            for member in members:
                print_member_definition(s, member, True)

        case model.StructMemberOptional(_tag, model.OptionalMembers(members=members)):
            for member in members:
                print_member_definition(s, member, True)

        case _:
            raise Exception("invalid struct member")
