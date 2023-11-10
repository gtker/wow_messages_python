from writer import Writer


def print_variable_item_random_property(s: Writer):
    s.write_block("""
@dataclasses.dataclass
class VariableItemRandomProperty:
    first: int
    second: typing.Optional[int]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        first = await read_int(reader, 4)
        
        second = None
        if first != 0:
            second = await read_int(reader, 4)

        return VariableItemRandomProperty(first=first, second=second)

    def write(self, fmt, data):
        fmt += 'I'
        data.append(first)
        
        if second is not None:
            fmt += 'I'
            data.append(second)

        return fmt, data

    def size(self):
        if second is not None:
            return 8
        else:
            return 4
""")

    s.double_newline()
