import pytest


# runserver 서버를 띄우지 않아도 됩니다.
@pytest.mark.it("대문 페이지는 항상 200 응답을 반환해야 한다.")
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
