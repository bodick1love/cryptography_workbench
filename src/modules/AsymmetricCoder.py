class AsymmetricCoder:
    def __init__(self, p=61, q=53):
        self.p = p
        self.q = q

        self.__generateKeys()

    def __generateKeys(self):
        n = self.p * self.q

        phi = (self.p - 1) * (self.q - 1)

        e = 65537
        d = self.modinv(e, phi)

        self.publicKey = (e, n)
        self.__privateKey = (d, n)

    def modinv(self, a, m):
        m0, x0, x1 = m, 0, 1
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        return x1 + m0 if x1 < 0 else x1

    def encryption(self, data: bytes) -> list[int]:
        e, n = self.publicKey
        cipher = [pow(byte, e, n) for byte in data]

        return cipher

    def decryption(self, cipher: list[int]) -> bytes:
        d, n = self.__privateKey
        decrypted_bytes = [pow(char, d, n) for char in cipher]

        return bytes(decrypted_bytes)

    def setP(self, p):
        self.p = p
        self.__generateKeys()

    def setQ(self, q):
        self.q = q
        self.__generateKeys()