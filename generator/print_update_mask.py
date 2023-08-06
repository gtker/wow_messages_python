import model
from writer import Writer


def print_update_mask(s: Writer, update_mask: list[model.UpdateMask]):
    s.write_block("""
@dataclasses.dataclass
class UpdateMask:
    fields: dict[int, int]
    
    @staticmethod
    async def read(reader: asyncio.StreamReader):
        amount_of_blocks = await read_int(reader, 1)

        blocks = []
        for _ in range(0, amount_of_blocks):
            blocks.append(await read_int(reader, 4))

        fields = {}
        for block_index, block in enumerate(blocks):
            for bit in range(0, 32):
                if block & 1 << bit:
                    value = await read_int(reader, 4)
                    key = block_index * 32 + bit
                    fields[key] = value

        return UpdateMask(fields=fields)

    def write(self, fmt, data):
        highest_key = max(self.fields)
        amount_of_blocks = highest_key // 32
        if highest_key % 32 != 0:
            amount_of_blocks += 1

        fmt += 'B'
        data.append(amount_of_blocks)

        blocks = [0] * amount_of_blocks

        for key in self.fields:
            block = key // 32
            index = key % 32
            blocks[block] |= 1 << index

        fmt += f'{len(blocks)}I'
        data.extend(blocks)

        for value in self.fields.values():
            fmt += 'I'
            data.append(value)

        return fmt, data

    def size(self):
        highest_key = max(self.fields)
        amount_of_blocks = highest_key // 32

        extra = highest_key % 32
        if extra != 0:
            extra = 1
        else:
            extra = 0

        return 1 + (extra + amount_of_blocks + len(self.fields)) * 4
""")

    s.double_newline()
