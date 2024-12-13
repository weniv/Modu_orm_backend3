import unittest
import requests


def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


class TestTitle(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)

    def test_subtract(self):
        self.assertEqual(subtract(1, 2), -2)


class TestAPI(unittest.TestCase):
    def test_add(self):
        url = "https://eduapi.weniv.co.kr/397/blog/"
        data = requests.get(url)
        self.assertEqual(len(data.text), 3749)

    # 이런 테스트를 만들 수 있습니다. 만약 blog였다면
    # 1. 글을 작성하는 api test
    # 2. 작성한 글이 제대로 웹 페이지에 노출되는지 확인하는 api test
    # 3. 작성된 웹 페이지의 구조가 제대로 되어있는지 확인하는 api test
    # ...


if __name__ == "__main__":
    unittest.main()
