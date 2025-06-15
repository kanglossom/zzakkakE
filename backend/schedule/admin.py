from django.contrib import admin
from .models import Schedule

# 관리자 페이지에 모델 등록
admin.site.register(Schedule)
# Shedule 모델을 관리자 페이지에서 관리할 수 있도록 등록