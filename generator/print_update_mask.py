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
        highest_key = max(self.fields, default=0)
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

        for key in sorted(self.fields):
            if isinstance(self.fields[key], float):
                fmt += 'f'
            else:
                fmt += 'I'
            data.append(self.fields[key])

        return fmt, data

    def size(self):
        highest_key = max(self.fields, default=0)
        amount_of_blocks = highest_key // 32

        extra = highest_key % 32
        if extra != 0:
            extra = 1
        else:
            extra = 0

        return 1 + (extra + amount_of_blocks + len(self.fields)) * 4
""")

    s.double_newline()

    s.open("class UpdateMaskValue(enum.IntEnum):")

    for value in update_mask:
        name = f"{value.object_type.name}_{value.name}"
        match value.data_type:
            case model.UpdateMaskDataTypeGUIDArrayUsingEnum(content=content):
                for enumerator in content.definer.enumerators:
                    s.wln(f"{name}_{enumerator.name} = {value.offset + int(enumerator.value.value) * 2}")
            case model.UpdateMaskDataTypeArrayOfStruct(content=content):
                amount_of_items = value.size // content.size
                mask = content.update_mask_struct
                for i in range(0, amount_of_items):
                    for word_index, word in enumerate(mask.members):
                        for member_index, member in enumerate(word):
                            val = value.offset + i * content.size + word_index
                            extra = member.member.name.upper()

                            if member.size == 4:
                                s.wln(f"{name}_{i}_{extra} = {val}")
                            elif member.size == 8:
                                s.wln(f"{name}_{i}_{extra}_LOW = {val}")
                                s.wln(f"{name}_{i}_{extra}_HIGH = {val + 1}")
                            else:
                                s.wln(f"{name}_{i}_{extra}_{member_index} = {val}")

            case _:
                s.wln(f"{name} = {value.offset}")

    s.close()
    s.double_newline()
