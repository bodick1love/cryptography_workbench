class Generator:
    def __init__(self, m: int, a: int, c: int, x0: int):
        self.__m = m
        self.__a = a
        self.__c = c
        self.__x0 = x0

    def generate(self, n: int) -> list[int]:
        x = [self.__x0]
        for i in range(n):
            next_val = (self.__a * x[-1] + self.__c) % self.__m
            x.append(next_val)

        return x

    @staticmethod
    def countT(x: list[int]) -> int | None:
        visited = set()
        for i in range(len(x)):
            if x[i] in visited:
                return i
            else:
                visited.add(x[i])

    def setM(self, m: int):
        self.__m = m

    def setA(self, a: int):
        self.__a = a

    def setC(self, c: int):
        self.__c = c

    def setX0(self, x0: int):
        self.__x0 = x0