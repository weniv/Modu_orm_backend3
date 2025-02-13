from django import forms
from rest_framework import serializers

from .models import Song

# forms.Form
# forms.ModelForm

# serializers.Serializer
# serializers.ModelSerializer


# 직렬화의 책임
#  - 여러 View에서 동일한 직렬화 로직을 재사용
#  - 직렬화 로직 변경이 필요한 경우, Serializer만 수정하면 되기에 유지보수성 향상
class SongSerializer(serializers.ModelSerializer):
    title_length = serializers.IntegerField(read_only=True)

    # title_length = serializers.SerializerMethodField(method_name="get_title_length")
    #
    # def get_title_length(self, obj) -> int:
    #     return len(obj.title)

    class Meta:
        model = Song
        fields = ["title", "title_length"]
