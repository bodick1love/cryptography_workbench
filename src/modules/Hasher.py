import math


class Hasher:
    def __init__(self):
        # Define an initial buffer that contains an intermediate value
        self.__initBuffer = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]

        # Define the four auxiliary functions that produce one 32-bit word
        self.__F = lambda x, y, z: (x & y) | (~x & z)
        self.__G = lambda x, y, z: (x & z) | (y & ~z)
        self.__H = lambda x, y, z: x ^ y ^ z
        self.__I = lambda x, y, z: y ^ (x | ~z)

        # Define const array
        self.__T = [int(2 ** 32 * abs(math.sin(i))) for i in range(1, 65)]

        # Define the number of left rotations for each round of processing
        self.__rotateBy = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4

    def hash(self, msg: bytearray) -> str:
        msg = Hasher.extend(msg)

        state = self.__initBuffer.copy()
        for i in range(0, len(msg), 64):    # Process the message in 64-byte blocks
            block = msg[i:i+64]

            a, b, c, d = self.processBlock(block, state.copy())

            # Updating state with new values
            state[0] = (state[0] + a) % 2**32
            state[1] = (state[1] + b) % 2**32
            state[2] = (state[2] + c) % 2**32
            state[3] = (state[3] + d) % 2**32

        # Format the output
        digit = sum(buffer_content << (32*i) for i, buffer_content in enumerate(state))    # Placing each bit at its place
        raw = digit.to_bytes(16, byteorder='little')    # Convert the digit to a 16-byte array
        return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))   # Format the byte array as a 32-character hexadecimal string

    @staticmethod
    def toByteArray(filename: str) -> bytearray:
        with open(filename, 'rb') as file:  # Open file in binary mode
            data = file.read()

        return bytearray(data)

    @staticmethod
    def extend(msg: bytearray) -> bytearray:
        msg_bit_len = len(msg) * 8 % 2**32

        msg.append(0x80)
        while len(msg) % 64 != 56:
            msg.append(0)

        msg += msg_bit_len.to_bytes(8, byteorder='little')

        return msg

    @staticmethod
    def leftRotate(x: int, amount: int) -> int:
        x %= 2**32
        return (x << amount | x >> (32 - amount)) % 2**32

    def processBlock(self, block: bytearray, state: list[int]) -> list[int]:
        # Extract the values of a, b, c, and d from the state
        a, b, c, d = state

        for i in range(64):     # Process the block in 64 rounds, updating the state for each round
            if 0 <= i < 16:
                f = self.__F(b, c, d)
                idx = i
            elif 16 <= i < 32:
                f = self.__G(b, c, d)
                idx = (5*i + 1) % 16
            elif 32 <= i < 48:
                f = self.__H(b, c, d)
                idx = (3*i + 5) % 16
            else:
                f = self.__I(b, c, d)
                idx = (7*i) % 16

            to_rotate = a + f + self.__T[i] + int.from_bytes(block[4 * idx: 4 * idx + 4], byteorder='little')
            new_a = (b + self.leftRotate(to_rotate, self.__rotateBy[i])) & (2 ** 32 - 1)

            a, b, c, d = d, new_a, b, c

        return [a, b, c, d]