import unittest


def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


class TestTitle(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)

    def test_subtract(self):
        self.assertEqual(subtract(1, 2), -2)


class TestTitleTwo(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)

    def test_subtract(self):
        self.assertEqual(subtract(1, 2), -2)


if __name__ == "__main__":
    unittest.main()
