from rest_framework import serializers
from .models import Todo


# 조회 : 데이터 변환
# 생성/수정 : 데이터 유효성 검사와 데이터베이스로의 저장 <= 장고 Form과 유사
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        # 노출할 필드를 명시
        fields = ["pk", "message", "is_completed"]
        # fields = '__all__'
