import math


class Coder:
    def __init__(self, key: bytes, w=32, r=8, b=16):
        # RC5/32/8/16
        self.__key = key
        self.__w = w
        self.__r = r
        self.__b = b

        self.__mod = 2 ** w
        self.__mask = self.__mod - 1
        self.__w8 = w // 8
        self.__w4 = w // 4
        self.__c = b // self.__w8
        self.__t = int(2 * (r + 1))

        # Constants
        self.__setConstants()

        # Process Key
        self.__keyAlign()
        self.__keyExtend()
        self.shuffle()

    def __setConstants(self):
        if self.__w == 16:
            self.__P = 0xb7e1
            self.__Q = 0x9e37
        elif self.__w == 32:
            self.__P = 0xb7e15163
            self.__Q = 0x9e3779b9
        else:
            self.__P = 0xb7e151628aed2a6b
            self.__Q = 0x9e3779b97f4a7c15

    def lshift(self, val, n):
        n %= self.__w
        return ((val << n) & self.__mask) | ((val & self.__mask) >> (self.__w - n))

    def rshift(self, val, n):
        n %= self.__w
        return ((val & self.__mask) >> n) | (val << (self.__w - n) & self.__mask)

    def __keyAlign(self):
        self.__c = 1 if self.__b == 0 else math.ceil(self.__b / self.__w8)
        L = [0] * self.__c
        for i in range(self.__b - 1, -1, -1):
            L[i // self.__w8] = (L[i // self.__w8] << 8) + self.__key[i]
        self.__L = L

    def __keyExtend(self):
        self.__s_key = [(self.__P + i * self.__Q) % self.__mod for i in range(self.__t)]

    def shuffle(self):
        i, j, A, B = 0, 0, 0, 0
        for k in range(3 * max(self.__c, self.__t)):
            A = self.__s_key[i] = self.lshift((self.__s_key[i] + A + B), 3)
            B = self.__L[j] = self.lshift((self.__L[j] + A + B), A + B)
            i = (i + 1) % self.__t
            j = (j + 1) % self.__c

    def encryptBlock(self, data):
        A = int.from_bytes(data[:self.__w8], byteorder='little')
        B = int.from_bytes(data[self.__w8:], byteorder='little')

        A = (A + self.__s_key[0]) % self.__mod
        B = (B + self.__s_key[1]) % self.__mod
        for i in range(1, self.__r + 1):
            A = (self.lshift((A ^ B), B) + self.__s_key[2 * i]) % self.__mod
            B = (self.lshift((A ^ B), A) + self.__s_key[2 * i + 1]) % self.__mod

        return A.to_bytes(self.__w8, byteorder='little')

    def encryptFile(self, inpFileName, outFileName):
        with open(inpFileName, 'rb') as inp, open(outFileName, 'wb') as out:
            run = True
            while run:
                text = inp.read(self.__w4)
                if not text:
                    break
                if len(text) != self.__w4:
                    text = text.ljust(self.__w4, b'\x00')
                    run = False
                text = self.encryptBlock(text)
                out.write(text)

    def decryptBlock(self, data):
        A = int.from_bytes(data[:self.__w8], byteorder='little')
        B = int.from_bytes(data[self.__w8:], byteorder='little')
        for i in range(self.__r, 0, -1):
            B = self.rshift(B - self.__s_key[2 * i + 1], A) ^ A
            A = self.rshift(A - self.__s_key[2 * i], B) ^ B

        B = (B - self.__s_key[1]) % self.__mod
        A = (A - self.__s_key[0]) % self.__mod

        return A.to_bytes(self.__w8, byteorder='little') + B.to_bytes(self.__w8, byteorder='little')

    def decryptFile(self, inpFileName, outFileName):
        with open(inpFileName, 'rb') as inp, open(outFileName, 'wb') as out:
            run = True
            while run:
                text = inp.read(self.__w4)
                if not text:
                    break
                if len(text) != self.__w4:
                    run = False
                text = self.decryptBlock(text)
                if not run:
                    text = text.rstrip(b'\x00')
                out.write(text)

    def setW(self, w):
        self.__w = w
        self.__mod = 2 ** w
        self.__w8 = w // 8
        self.__setConstants()

    def setR(self, r):
        self.__r = r
        self.__t = int(2 * (r + 1))

    def setB(self, b):
        self.__b = b
        self.__c = b // self.__w8
        self.__keyAlign()
        self.__keyExtend()
        self.shuffle()

    def setK(self, k: bytes):
        self.__key = k
        self.__keyAlign()
        self.__keyExtend()
        self.shuffle()
