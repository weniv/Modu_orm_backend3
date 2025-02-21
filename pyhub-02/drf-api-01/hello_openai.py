# 장고 외부 스크립트에서 장고 초기화 코드
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()

# 이제 모든 장고 요소에 접근 가능 !!!

from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "당신은 파이썬/장고 웹서비스 개발 고수입니다."},
        {"role": "user", "content": "blog 서비스를 위한 포스팅 모델을 설계해주세요."},
    ],
    # stream=True,
)

print(completion.choices[0].message)
