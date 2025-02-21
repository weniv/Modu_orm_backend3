def mysum(a, b):
    return a * 10 + b


class Calculator:
    def add(self, x, y):
        """..."""
        return x + y

    def subtract(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        if y == 0:
            raise ValueError("0으로 나눌 수 없습니다")
        return x / y
