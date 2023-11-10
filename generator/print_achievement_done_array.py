from writer import Writer


def print_achievement_done_array(s: Writer):
    s.write_block("""
@dataclasses.dataclass
class AchievementDoneArray:
    data: list[AchievementDone]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        data = []
        achievement = await read_int(reader, 4)

        while achievement != -1:
            time = await read_int(reader, 4)
            data.append(AchievementDone(achievement=achievement, time=time))

            achievement = await read_int(reader, 4)

        return AchievementDoneArray(data=data)

    def write(self, fmt, data):
        for d in self.data:
            fmt, data = d.write(fmt, data)

        fmt += "i"
        data.append(-1)

        return fmt, data

    def size(self):
        size = 4
        for d in self.data:
            size += d.size()
        return size
""")

    s.double_newline()
