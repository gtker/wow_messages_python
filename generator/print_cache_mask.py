from writer import Writer


def print_cache_mask(s: Writer):
    s.write_block("""
@dataclasses.dataclass
class CacheMask:
    fields: dict[int, int]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        mask = await read_int(reader, 4)

        fields = {}
        for index in range(0, 32):
            if mask & 1 << index:
                fields[index] = await read_int(reader, 2)

        return AuraMask(fields=fields)

    def write(self, fmt, data):
        mask = 0
        for key in self.fields:
            mask |= 1 << key

        fmt += 'I'
        data.append(mask)

        fmt += f"{len(self.fields)}H"
        data.extend(list(self.fields.values()))

        return fmt, data

    def size(self):
        return 4 + len(self.fields) * 2
""")

    s.double_newline()