import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from diary.tests.factories import PostFactory


@pytest.mark.it(
    "게시물 목록 조회. 비인증 조회가 가능해야하며, 생성한 포스팅의 개수만큼 응답을 받아야 합니다."
)
@pytest.mark.django_db
def test_post_list(client):
    # post_list = [PostFactory() for __ in range(10)]
    post_list = PostFactory.create_batch(10)

    url: str = reverse("diary:api-v1:post-list")
    response: Response = client.get(url)
    assert status.HTTP_200_OK == response.status_code  # Expected, Actual
    assert len(post_list) == len(response.data)
