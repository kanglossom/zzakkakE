from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Schedule
from .serializers import ScheduleSerializer

# API 기능이 있는 폴더 - 일정 입력, 조회, 삭제 등

# @api_view는 Django REST Framework의 데코레이터.
# 여기서는 POST만 허용한다는 뜻.
# 참고로 POST는 데이터를 '보내는' 용도. - 등록, 생성

# 다음과 같은걸 API 뷰라고 함.
# 일정입력 데이터 받아주는 친구
@api_view(['POST']) # POST니까 데이터를 서버로 보낸다는 것
def create_schedule(request):
    serializer = ScheduleSerializer(data=request.data)
    # 유효성검사
    if serializer.is_valid(): # 형식에 맞다면
        serializer.save() # 저장
        return Response({"message":"일정 등록 완료!"}) # 성공적으로 저장
    return Response(serializer.errors) # 유효하지 않다면 에러

# 일정 조회 관련된거
@api_view(['GET']) # GET, 즉 일정 조회만 가능
def get_schedules(request):
    schedules = Schedule.objects.all().order_by('date')
    # 스케줄 모델에 저장된 모든 일정을 불러오고 date 필드를 기준으로 오름차순 정렬
    serializer = ScheduleSerializer(schedules, many=True)
    return Response(serializer.data)

# 일정 삭제 관련
@api_view(['POST'])
def delete_schedule(request):
    title = request.data.get('title')
    user = request.data.get('user')

    try :
        schedule = Schedule.objects.get(title=title, discord_user=user)
        schedule.delete()
        return Response({"message":"일정 삭제 완료!"})
    except Schedule.DoesNotExist:
        return Response({"error":"일정을 찾을 수 없음"}, status=404)