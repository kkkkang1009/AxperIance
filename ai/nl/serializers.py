from rest_framework import serializers
from .models import Filmrate

class FilmrateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filmrate # 모델 설정
        fields = ('content','rate') # 필드 설정
