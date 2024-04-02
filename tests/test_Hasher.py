import pytest
from src.modules.Hasher import Hasher


@pytest.fixture
def hasher_instance():
    return Hasher()


def test_hasher_hash(hasher_instance):
    message = bytearray(b'sdngj3bj2hf2n43gnejkfbbwqfekr')
    expected_hash = '0d29fef8145d2730d0c1a00da0a953c1'  # Replace with the expected hash for your specific input

    result = hasher_instance.hash(message)

    assert result == expected_hash


def test_hasher_extend():
    message = bytearray(b'Test message')
    result = Hasher.extend(message)

    assert len(result) % 64 == 0
    assert result[:len(message)] == message


def test_hasher_left_rotate():
    input_value = 0b11000000110000001100000011000000
    amount = 2
    expected_output = 0b11000000110000001100000011

    result = Hasher.leftRotate(input_value, amount)

    assert result == expected_output