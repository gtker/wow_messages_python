import model
from writer import Writer


def print_update_mask_read(s: Writer, update_mask: list[model.UpdateMask]):
    s.wln("@staticmethod")
    s.open("async def read(reader: asyncio.StreamReader):")
    s.wln("amount_of_blocks = await read_int(reader, 1)")
    s.newline()
    s.wln("blocks = []")

    s.open("for _ in range(0, amount_of_blocks):")
    s.wln("blocks.append(await read_int(reader, 4))")
    s.close()  # for _ in range
    s.newline()

    s.wln("fields = {}")
    s.open("for block_index, block in enumerate(blocks):")
    s.open("for bit in range(0, 32):")

    s.open("if block & 1 << bit:")
    s.wln("value = await read_int(reader, 4)")
    s.wln("key = block_index * 32 + bit")
    s.wln("fields[key] = value")
    s.close()  # if block & 1

    s.close()  # for bit in range
    s.close()  # for block_index, block
    s.newline()

    s.wln("return UpdateMask(fields=fields)")

    s.close()  # async def read

    s.newline()


def print_update_mask_write(s: Writer, update_mask: list[model.UpdateMask]):
    s.open("def write(self, fmt, data):")

    s.wln("highest_key = max(self.fields)")
    s.wln("amount_of_blocks = highest_key // 32")
    s.newline()

    s.wln("fmt += 'B'")
    s.wln("data.append(amount_of_blocks)")
    s.newline()

    s.wln("blocks = [0] * amount_of_blocks")
    s.newline()

    s.open("for key in self.fields:")
    s.wln("block = key // 32")
    s.wln("index = key % 32")
    s.wln("blocks[block] |= 1 << index")
    s.close()  # for key in self.fields
    s.newline()

    s.wln("fmt += f'{len(blocks)}I'")
    s.wln("data.extend(blocks)")
    s.newline()

    s.open("for value in self.fields.values():")
    s.wln("fmt += 'I'")
    s.wln("data.append(value)")
    s.close()  # for value in self.fields
    s.newline()

    s.wln("return fmt, data")

    s.close()  # def write

    s.double_newline()


def print_update_mask(s: Writer, update_mask: list[model.UpdateMask]):
    s.wln("@dataclasses.dataclass")
    s.open("class UpdateMask:")

    s.wln("fields: dict[int, int]")
    s.newline()

    print_update_mask_read(s, update_mask)

    print_update_mask_write(s, update_mask)

    s.close()  # class UpdateMask
