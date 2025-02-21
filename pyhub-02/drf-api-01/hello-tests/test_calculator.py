import unittest

from calculator import Calculator, mysum


class TestMySum(unittest.TestCase):
    def test_1(self):
        self.assertEqual(mysum(1, 2), 12)
        self.assertEqual(mysum(2, 3), 23)


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        """두 숫자의 덧셈을 테스트"""
        self.assertEqual(self.calc.add(3, 5), 8)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(-1, -1), -2)

    def test_subtract(self):
        """두 숫자의 뺄셈을 테스트"""
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(1, 2), -1)
        self.assertEqual(self.calc.subtract(-1, -1), 0)

    def test_multiply(self):
        """두 숫자의 곱셈을 테스트"""
        self.assertEqual(self.calc.multiply(3, 5), 15)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
        self.assertEqual(self.calc.multiply(-2, -2), 4)

    def test_divide(self):
        """두 숫자의 나눗셈을 테스트"""
        self.assertEqual(self.calc.divide(6, 2), 3)
        self.assertEqual(self.calc.divide(5, 2), 2.5)
        self.assertEqual(self.calc.divide(-6, 2), -3)

    def test_divide_by_zero(self):
        """0으로 나눌 때 ValueError 발생 테스트"""
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)


# 구현하기 전에 테스트를 먼저 작성하고
# 테스트 실패를 먼저 확인합니다.
if __name__ == "__main__":
    unittest.main()
