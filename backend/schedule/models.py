from django.db import models

# DB 구조 정의
class Schedule(models.Model):
    title = models.CharField(max_length=100) # 일정 이름
    date = models.DateField() # 일정 날짜
    discord_user = models.CharField(max_length=100) # 디스코드 유저 ID

    def __str__(self):
        return f"{self.title} - {self.date}" # "자료구조 과제 - 2025-06-02"