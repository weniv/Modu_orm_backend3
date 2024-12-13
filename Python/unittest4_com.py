import unittest


def cto_to_ceo(s: str) -> str:
    return s.replace("CTO", "CEO")


def has_ceo(s: str) -> bool:
    return "CEO" in s


class TestTitle(unittest.TestCase):
    """
    주의해야 할 점:
        1. test 함수의 이름은 test로 시작해야 합니다.
        2. test 함수의 실행은 정의 순서대로 이뤄지는 것이 아니라, 알파벳 순서대로 이뤄집니다.
        3. test 함수의 첫 번째 인자는 self여야 합니다.
    """

    def test_cto_ceo(self):
        self.assertEqual(cto_to_ceo("weniv CTO mural"), "weniv CEO mural")

    def test_has_ceo(self):
        self.assertFalse(has_ceo("weniv CTO mural"))
        self.assertTrue(has_ceo("weniv CEO mural"))


if __name__ == "__main__":
    unittest.main()
