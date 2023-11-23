from writer import Writer


def print_inspect_talent_gear_mask(s: Writer):
    s.write_block("""
@dataclasses.dataclass
class InspectTalentGearMask:
    fields: dict[int, InspectTalentGear]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        mask = await read_int(reader, 4)

        fields = {}
        for index in range(0, 32):
            if mask & 1 << index:
                a = InspectTalentGear.read(reader)
                fields[index] = a

        return InspectTalentGearMask(fields=fields)

    def write(self, fmt, data):
        mask = 0
        for i, _ in enumerate(self.fields):
            mask |= 1 << i

        fmt += 'I'
        data.append(mask)

        for a in self.fields:
            fmt, data = a.write(fmt, data)

        return fmt, data

    def size(self):
        size = 4
        for f in self.fields:
            size += f.size()
        return size
""")

    s.double_newline()
