import model
from model import Container
from print_struct.print_members import print_members_definitions
from print_struct.print_read import print_read
from print_struct.print_size import print_size
from print_struct.print_write import print_write
from writer import Writer


def print_struct(s: Writer, container: Container):
    s.wln("@dataclasses.dataclass")
    s.wln(f"class {container.name}:")
    s.inc_indent()

    print_members_definitions(s, container)

    print_read(s, container)

    match container.object_type:
        case model.ObjectTypeMsg(opcode=opcode):
            print_write(s, container, model.ObjectTypeCmsg("CMsg", opcode))
            print_write(s, container, model.ObjectTypeSmsg("SMsg", opcode))
        case _:
            print_write(s, container, container.object_type)

    print_size(s, container)

    s.dec_indent()  # class
    s.newline()
