# 이렇게 test 코드가 fail이 뜨게 먼저 구성을 해놓고
# 그리고 함수 작성을 시작합니다.

import unittest


def replace_cto_to_ceo(text):
    pass


def check_ceo_exists(text):
    pass


class TestTitle(unittest.TestCase):
    def test_replace_cto_to_ceo(self):
        """CTO를 CEO로 변경하는 테스트"""
        # 기본 케이스 테스트
        self.assertEqual(replace_cto_to_ceo("weniv CTO mural"), "weniv CEO mural")
        # CTO가 없는 경우 테스트
        self.assertEqual(replace_cto_to_ceo("weniv mural"), "weniv mural")
        # 여러 개의 CTO가 있는 경우 테스트
        self.assertEqual(replace_cto_to_ceo("CTO weniv CTO"), "CEO weniv CEO")

    def test_check_ceo_exists(self):
        """CEO 존재 여부 확인 테스트"""
        # CEO가 있는 경우 테스트
        self.assertTrue(check_ceo_exists("weniv CEO mural"))
        # CEO가 없는 경우 테스트
        self.assertFalse(check_ceo_exists("weniv CTO mural"))
        # 대소문자 정확히 일치하는 경우만 테스트
        self.assertFalse(check_ceo_exists("weniv ceo mural"))


if __name__ == "__main__":
    unittest.main()
