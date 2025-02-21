import pytest
from calculator import Calculator


@pytest.fixture
def calculator():
    return Calculator()


def test_add(calculator):
    """두 숫자의 덧셈을 테스트"""
    assert calculator.add(3, 5) == 8
    assert calculator.add(-1, 1) == 0
    assert calculator.add(-1, -1) == -2


def test_subtract(calculator):
    """두 숫자의 뺄셈을 테스트"""
    assert calculator.subtract(5, 3) == 2
    assert calculator.subtract(1, 2) == -1
    assert calculator.subtract(-1, -1) == 0


def test_multiply(calculator):
    """두 숫자의 곱셈을 테스트"""
    assert calculator.multiply(3, 5) == 15
    assert calculator.multiply(-2, 3) == -6
    assert calculator.multiply(-2, -2) == 4


def test_divide(calculator):
    """두 숫자의 나눗셈을 테스트"""
    assert calculator.divide(6, 2) == 3
    assert calculator.divide(5, 2) == 2.5
    assert calculator.divide(-6, 2) == -3


def test_divide_by_zero(calculator):
    """0으로 나눌 때 ValueError 발생 테스트"""
    with pytest.raises(ValueError):
        calculator.divide(10, 0)
