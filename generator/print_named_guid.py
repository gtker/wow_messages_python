from writer import Writer


def print_named_guid(s: Writer):
    s.write_block("""
@dataclasses.dataclass
class NamedGuid:
    guid: int
    name: typing.Optional[int]

    @staticmethod
    async def read(reader: asyncio.StreamReader) -> Aura:
        guid = await read_int(reader, 4)

        if guid != 0:
            name = await read_cstring(reader)

        return Aura(
            guid=guid,
            name=name,
        )

    def write(self, _fmt, _data):
        if self.guid != 0:
            _fmt += f"Q{len(self.name)}sB"
            _data.extend([self.guid, self.name, 0])
        else:
            _fmt += 'Q'
            _data.append(self.guid)

        return _fmt, _data

    def size(self) -> int:
        if guid != 0:
            return len(self.name) + 8
        else:
            return 8

""")

    s.double_newline()