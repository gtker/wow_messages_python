from writer import Writer


def print_achievement_in_progress_array(s: Writer):
    s.write_block("""
@dataclasses.dataclass
class AchievementInProgressArray:
    data: list[AchievementInProgress]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        data = []
        achievement = await read_int(reader, 4)

        while achievement != -1:
            counter = await read_packed_guid(reader)

            player = await read_packed_guid(reader)

            timed_criteria_failed = await read_bool(reader, 4)

            progress_date = await read_int(reader, 4)

            time_since_progress = await read_int(reader, 4)

            time_since_progress2 = await read_int(reader, 4)
            
            data.append(AchievementInProgress(
                                              achievement=achievement,
                                              counter=counter,
                                              player=player,
                                              timed_criteria_failed=timed_criteria_failed,
                                              progress_date=progress_date,
                                              time_since_progress=time_since_progress,
                                              time_since_progress2=time_since_progress2,
                                              ))

            achievement = await read_int(reader, 4)

        return AchievementInProgressArray(data=data)

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
