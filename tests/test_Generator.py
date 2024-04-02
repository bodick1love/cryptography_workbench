import pytest
from src.modules.Generator import Generator


@pytest.fixture
def generator_instance():
    return Generator(m=100, a=5, c=3, x0=7)


def test_generate(generator_instance):
    result = generator_instance.generate(5)
    assert len(result) == 6
    assert result[0] == 7


def test_countT():
    test_data = [1, 2, 3, 4, 5, 2]
    result = Generator.countT(test_data)
    assert result == 5


def test_setters(generator_instance):
    generator_instance.setM(50)
    assert generator_instance._Generator__m == 50

    generator_instance.setA(10)
    assert generator_instance._Generator__a == 10

    generator_instance.setC(2)
    assert generator_instance._Generator__c == 2

    generator_instance.setX0(15)
    assert generator_instance._Generator__x0 == 15