from generator.util import world_version_is_vanilla, world_version_is_tbc, \
    world_version_is_wrath
from generator.writer import Writer
import model


def print_aura_mask(s: Writer, v: model.WorldVersion):
    block = ""
    if world_version_is_vanilla(v):
        block = """
@dataclasses.dataclass
class AuraMask:
    fields: dict[int]

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
"""
    elif world_version_is_tbc(v):
        block = """
@dataclasses.dataclass
class AuraMask:
    fields: dict[int, tuple[int, int]]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        mask = await read_int(reader, 8)

        fields = {}
        for index in range(0, 64):
            if mask & 1 << index:
                first = await read_int(reader, 2)
                second = await read_int(reader, 1)
                fields[index] = (first, second)

        return AuraMask(fields=fields)

    def write(self, fmt, data):
        mask = 0
        for i, _ in enumerate(self.fields):
            mask |= 1 << i

        fmt += 'Q'
        data.append(mask)

        for (first, second) in self.fields:
            fmt += "HB"
            data.append(first)
            data.append(second)

        return fmt, data

    def size(self):
        return 4 + len(self.fields) * 3
"""
    elif world_version_is_wrath(v):
        block = """
@dataclasses.dataclass
class AuraMask:
    fields: dict[int]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        mask = await read_int(reader, 8)

        fields = {}
        for index in range(0, 64):
            if mask & 1 << index:
                first = await read_int(reader, 4)
                second = await read_int(reader, 1)
                fields[index] = (first, second)

        return AuraMask(fields=fields)

    def write(self, fmt, data):
        mask = 0
        for i, _ in enumerate(self.fields):
            mask |= 1 << i

        fmt += 'Q'
        data.append(mask)

        for (first, second) in self.fields:
            fmt += "IB"
            data.append(first)
            data.append(second)

        return fmt, data

    def size(self):
        return 4 + len(self.fields) * 5

"""
    else:
        raise Exception("invalid version")

    s.write_block(block)

    s.double_newline()
