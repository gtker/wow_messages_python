from model import Definer
from writer import Writer


def print_enum(s: Writer, enum: Definer):
    s.wln(f"class {enum.name}(enum.Enum):")
    s.inc_indent()

    for enumerator in enum.enumerators:
        s.wln(f"{enumerator.name} = {enumerator.value.value}")

    s.newline()

    s.dec_indent()  # class
    s.newline()


def print_flag(s: Writer, enum: Definer):
    s.wln(f"class {enum.name}(enum.Flag):")
    s.inc_indent()

    for enumerator in enum.enumerators:
        s.wln(f"{enumerator.name} = {enumerator.value.value}")

    s.newline()

    s.dec_indent()  # class
    s.newline()
