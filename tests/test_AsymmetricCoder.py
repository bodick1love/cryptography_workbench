from src.modules.AsymmetricCoder import AsymmetricCoder


def test_asymmetric_coder_encryption_decryption():
    coder = AsymmetricCoder(p=61, q=53)

    plaintext = b'Test message'
    encrypted_data = coder.encryption(plaintext)
    decrypted_data = coder.decryption(encrypted_data)

    assert decrypted_data == plaintext


def test_asymmetric_coder_setters():
    coder = AsymmetricCoder(p=61, q=53)

    new_p = 67
    new_q = 59

    coder.setP(new_p)
    coder.setQ(new_q)

    assert coder.p == new_p
    assert coder.q == new_q


def test_asymmetric_coder_modinv():
    coder = AsymmetricCoder()

    a = 17
    m = 3120
    expected_output = 2753

    result = coder.modinv(a, m)

    assert result == expected_output