import discord # 디스코드 모듈
from discord import app_commands # 이게 슬래쉬 명령어
from discord.ext import commands # 이게 디코봇 기능임 그냥 (기존방식)
import requests # Django 서버에 HTTP 요청 보내는 친구
import asyncio # 비동기 프로그래밍 - 여러작업 동시에 할 수 있도록!
from dotenv import load_dotenv # .env 파일에서 토큰 가져오는 친구
import os # 환경변수 가져오기

load_dotenv() # 얘가 6줄에 의해 작동함
TOKEN = os.getenv("DISCORD_BOT_TOKEN") # 얘가 7줄에 의해 작동함
# .env에 저장된 TOKEN 값 불러오는거임

intents = discord.Intents.default()
# 걍 최소 필요한 코드라고 이해하자
bot = commands.Bot(command_prefix=None, intents=intents)
# 역시 이것도 그냥 필요한 코드라고 생각하자 봇 객체를 만든거임

# 봇이 로그인을 했음을 알리는 이벤트
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync() # 슬래시 명령어 사용하겠다는거임
        print(f'✅ 명령어 {len(synced)}개 등록됨: {[cmd.name for cmd in synced]}')
    except Exception as e:
        print(f'❌ 명령어 등록 실패: {e}')
    print(f'로그인완료: {bot.user}')


# /일정입력 [제목] [날짜]
@bot.tree.command(name="add_schedule", description="일정을 등록합니다")
# 이건 제목 = / 눌렀을 때 뜨는 명령어 이름, 설명 = 말그대로 옆에 무슨기능인지 나오는 설명임
@app_commands.describe(제목="일정 제목", 날짜="날짜 (YYYY-MM-DD)")
# 이건 입력할때 입력창에 보면 각각 필드를 눌렀을 때 어떤 형식으로 입력하는지 알려주는거임
# 이 밑에있는 함수가 실제 입력값 받아서 넘어가는 부분인거야
async def 일정입력(interaction: discord.Interaction, 제목: str, 날짜: str):
    try:
        data = {
            "title" : 제목,
            "date" : 날짜,
            "discord_user": str(interaction.user)
        }
        # data로 묶여서 서버에 넘어갈 준비 완료

        res = requests.post("http://127.0.0.1:8000/schedule/create/", json=data)
        # Django 서버로 HTTP POST 요청 보냄!
        if res.status_code == 200:
            await interaction.response.send_message("일정등록 완료")
            # 등록이 완료되었을 때 봇이 보내는 메세지가 바로 여기
        else :
            await interaction.response.send_message("등록 실패")
            # 등록에 실패했을 때 봇이 보내는 메세지가 여기!
    except Exception as e:
        await interaction.response.send_message(f"에러발생 {e}")

# /일정확인
@bot.tree.command(name="view_schedule", description="등록된 일정을 전부 확인합니다")
async def 일정확인(interaction: discord.Interaction):
    try: 
        res = requests.get("http://127.0.0.1:8000/schedule/")
        if res.status_code != 200:
            await interaction.response.send_message("서버가 응답을 안해요")
            return
        
        data = res.json()
        if not data:
            await interaction.response.send_message("등록된 일정이 없다능")
            return
        msg = "\n".join([f"{item['date']}-{item['title']}"for item in data])
        await interaction.response.send_message(f"등록된 일정:\n{msg}")
    
    except Exception as e:
        await interaction.response.send_message(f"서버에러: {e}")

bot.run(TOKEN) # 봇 실행~
