from django.urls import path
from . import views

# 이 앱 (shedule)에서 쓰는 URL 경로들

urlpatterns = [
    path('create/', views.create_schedule),
    path('get/', views.get_schedules),
    path('delete/', views.delete_schedule),
]

