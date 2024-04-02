import pytest
from src.modules.Coder import Coder
from src.modules.Hasher import Hasher


@pytest.fixture
def coder_instance():
    my_hasher = Hasher()

    key = bytes.fromhex(my_hasher.hash(bytearray(b'SecretKey123')))
    return Coder(key)


def test_coder_encrypt_file_decrypt_file(coder_instance, tmp_path):
    plaintext = b'Test message'

    input_file_path = tmp_path / "input_file.txt"
    with open(input_file_path, 'wb') as input_file:
        input_file.write(plaintext)

    encrypted_file_path = tmp_path / "encrypted_file.txt"
    coder_instance.encryptFile(input_file_path, encrypted_file_path)

    decrypted_file_path = tmp_path / "decrypted_file.txt"
    coder_instance.decryptFile(encrypted_file_path, decrypted_file_path)

    with open(decrypted_file_path, 'rb') as decrypted_file:
        decrypted_content = decrypted_file.read()
        assert decrypted_content == b'\x13\xfc\xe9\x07\xe3\xe2\xd9\x93'


def test_coder_setters(coder_instance):
    new_w = 16
    new_r = 4
    new_b = 8
    new_key = b'NewKey456'

    coder_instance.setW(new_w)
    coder_instance.setR(new_r)
    coder_instance.setB(new_b)
    coder_instance.setK(new_key)

    assert coder_instance._Coder__w == new_w
    assert coder_instance._Coder__r == new_r
    assert coder_instance._Coder__b == new_b
    assert coder_instance._Coder__key == new_key
