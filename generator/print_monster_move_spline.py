from writer import Writer


def print_monster_move_spline(s: Writer):
    s.write_block("""
@dataclasses.dataclass
class MonsterMoveSpline:
    splines: list[Vector3d]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        def packed_to_vec(packed: int) -> Vector3d:
            x = float(packed & 0x7FF) / 4
            y = float((packed >> 11) & 0x7FF) / 4
            z = float((packed >> 22) & 0x3FF) / 4
            return Vector3d(x=x, y=y, z=z)

        amount_of_splines = await read_int(reader, 4)

        if amount_of_splines == 0:
            return MonsterMoveSpline(splines=[])

        splines = [await Vector3d.read(reader)]

        for i in range(1, amount_of_splines): # subtract the 'real' one
            packed = await read_int(reader, 4)
            splines.append(packed_to_vec(packed))

        return MonsterMoveSpline(splines=splines)

    def write(self, fmt, data):
        def vec_to_packed(vec: Vector3d) -> int:
            packed = 0
            packed |= int(vec.x / 0.25) & 0x7FF
            packed |= (int(vec.y / 0.25) & 0x7FF) << 11
            packed |= (int(vec.z / 0.25) & 0x3FF) << 22
            return packed
        amount_of_splines = len(self.splines)
        fmt += 'I'
        data.append(amount_of_splines)

        if amount_of_splines == 0:
            return fmt, data

        fmt, data = self.splines[0].write(fmt, data)

        for i in range(1, amount_of_splines):
            packed = vec_to_packed(self.splines[i])
            fmt += 'I'
            data.append(packed)

        return fmt, data

    def size(self):
        if len(self.splines) == 0:
            return 4

        return 4 + 3 * 4 + (len(self.splines) - 1) * 4
""")

    s.double_newline()
