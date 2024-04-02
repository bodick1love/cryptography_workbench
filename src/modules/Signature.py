from Crypto.Hash import SHA256
from Crypto.Signature import DSS
from Crypto.PublicKey import DSA


class Signer:
    def __init__(self, key_path="supersecretprivatekey"):
        self.key = DSA.import_key(open(key_path).read())
        self.processor = DSS.new(self.key, 'fips-186-3')

    def verify(self, data: bytes, signature: bytes) -> bool:
        h = SHA256.new(data)
        try:
            self.processor.verify(h, signature)
            return True
        except ValueError:
            return False

    def sign(self, data: bytes) -> bytes:
        h = SHA256.new(data)
        signature = self.processor.sign(h)

        return signature

    @staticmethod
    def generateKey():
        key = DSA.generate(2048)
        return key

    def setKey(self, key_path):
        self.key = DSA.import_key(open(key_path).read())
        self.processor = DSS.new(self.key, 'fips-186-3')