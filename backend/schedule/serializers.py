from rest_framework import serializers
from .models import Schedule

# 모델 <-> JSON 변환기

# 시리얼라이저의 필요 이유(장고 REST 프레임워크에서 제공함.)
# 디스코드 봇은 사람처럼 눈으로 DB를 읽을 수 있는게 아님
# JSON으로 소통함.
# 따라서 필요함.

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule # Schedule 모델과 연결
        fields = '__all__' # 모든 필드(title, date, discord_user)를 자동으로 포함시킴
    