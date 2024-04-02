import pytest
from src.modules.Signature import Signer


@pytest.fixture
def signer_instance(tmp_path):
    key = Signer.generateKey()
    with open(tmp_path / "key.pem", 'wb') as key_file:
        key_file.write(key.export_key())
    return Signer(tmp_path / "key.pem")


def test_signer_sign_and_verify(tmp_path):
    key_path = tmp_path / "test_private_key.pem"
    key = Signer.generateKey()
    with open(key_path, 'wb') as key_file:
        key_file.write(key.export_key())

    signer = Signer(key_path)

    plaintext = b'Test message'
    signature = signer.sign(plaintext)
    verified = signer.verify(plaintext, signature)

    assert verified


def test_signer_set_key(signer_instance, tmp_path):
    new_key = Signer.generateKey()
    with open(tmp_path / "key.pem", 'wb') as key_file:
        key_file.write(new_key.export_key())
    signer_instance.setKey(tmp_path / "key.pem")

    plaintext = b'Test message'
    signature = signer_instance.sign(plaintext)
    verified = signer_instance.verify(plaintext, signature)

    assert verified