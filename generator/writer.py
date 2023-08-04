class Writer:
    __inner = ""
    __indentation = 0

    def w(self, s: str):
        for _ in range(0, self.__indentation):
            self.__inner += "    "

        self.__inner += s

    def wln(self, s):
        self.w(s)
        self.newline()

    def newline(self):
        self.__inner += "\n"

    def prepend(self, s):
        s.__inner += self.__inner
        self.__inner = s.__inner

    def append(self, s):
        self.__inner += s.__inner

    def inner(self):
        assert self.__indentation == 0
        return self.__inner

    def inc_indent(self):
        if self.__indentation == 255:
            raise AssertionError("indentation overflow")

        self.__indentation += 1

    def dec_indent(self):
        if self.__indentation == 0:
            raise AssertionError("indentation underflow")

        self.__indentation -= 1
