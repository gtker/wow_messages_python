from writer import Writer


def print_addon_array(s: Writer):
    s.write_block("""
@dataclasses.dataclass
class AddonArray:
    data: list[Addon]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        raise Exception('read for AddonArray is unimplemented. Create an issue on Github if this is relevant for you.')

    def write(self, fmt, data):
        for d in self.data:
            fmt, data = d.write(fmt, data)

        return fmt, data

    def size(self):
        size = 0
        for d in self.data:
            size += d.size()
            
        return size
""")

    s.double_newline()
