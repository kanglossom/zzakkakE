import discord
from discord import app_commands
from discord.ext import commands
import requests
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

print(f"TOKEN: {TOKEN}")

# TOKEN =

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)
# tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    await bot.tree.sync() # 슬래시 명령어가 디스코드에 등록됨
    print(f'로그인완료: {bot.user}')


# /일정입력 [제목] [날짜]
@bot.tree.command(name="일정입력", description="일정을 등록합니다")
@app_commands.describe(제목="일정 제목", 날짜="날짜 (YYYY-MM-DD)")
async def 일정입력(interaction: discord.Interaction, 제목: str, 날짜: str):
    data = {
        "title" : 제목,
        "date" : 날짜,
        "discord_user": str(interaction.user)
    }

    res = requests.post("http://127.0.0.1:8000/schedule/create/", json=data)
    if res.status_code == 200:
        await interaction.response.send_message("일정 등록 완료")
    else :
        await interaction.response.send_message("등록 실패")



bot.run(TOKEN)