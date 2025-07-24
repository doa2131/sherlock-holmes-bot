import discord
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

user_states = {}

async def type_slowly(channel, text, delay=0.05):
    async with channel.typing():
        await asyncio.sleep(len(text) * delay)
    await channel.send(text)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = str(message.author.id)
    content = message.content.strip()

    if content == "/셜록홈즈와 대화하기":
        user_states[user_id] = "대화시작"
        await type_slowly(message.channel,
            "🕵️‍♂️ 셜록 홈즈: 오셨습니까? 오는 길은 어떠셨는지. "
            "뭐, 워낙 이름을 널리 알리신 탐정이시니 그리 힘들진 않으셨을 거라 믿습니다.\n\n"
            "**선택지: '나에게 초대장을 보낸 이유는 무엇이죠?'**"
        )
        return

    if user_states.get(user_id) == "대화시작" and "초대장" in content:
        user_states[user_id] = "왓슨대체"
        await type_slowly(message.channel,
            "🕵️‍♂️ 셜록 홈즈: 소문은 들으셨겠지만 최근 화이트채플의 거리가 피로 물들고 있습니다. "
            "그런데, 제 믿음직한 조수인 왓슨은 지금 자리를 비웠군요. "
            "그래서 수소문 끝에 당신을 찾아 편지를 보냈습니다. "
            "당신은 왓슨을 대신할 만한 실력을 갖추고 있나요?\n\n"
            "**선택지: '물론이지.' 또는 '아직 더 고민을 해봐야겠어.'**"
        )
        return

    if user_states.get(user_id) == "왓슨대체":
        if "고민" in content:
            user_states.pop(user_id)
            await type_slowly(message.channel,
                "🕵️‍♂️ 셜록 홈즈: 그렇군요. 아쉽지만 다른 분을 찾아봐야겠군요.\n\n"
                "`[셜록 홈즈와의 대화가 종료되었습니다.]`"
            )
            return
        elif "물론" in content:
            user_states[user_id] = "퀴즈제시"
            await type_slowly(message.channel,
                "🕵️‍♂️ 셜록 홈즈: 당신이 내 오른팔이 될 수 있는지 시험해보도록 하지.\n"
                "문제입니다. 한 남자가 방 안에서 깨진 창문을 발견했습니다. "
                "바닥에는 유리 조각, 물, 그리고 금붕어가 있었습니다.\n"
                "무슨 일이 있었던 걸까요?\n\n"
                "**선택지: '창문'**"
            )
            return

    if user_states.get(user_id) == "퀴즈제시":
        if "창문" in content:
            user_states.pop(user_id)
            await type_slowly(message.channel,
                "🕵️‍♂️ 셜록 홈즈: 휼륭하군요, 당신이라면 믿고 의뢰를 함께 하겠습니다.\n\n"
                "`[셜록 홈즈와의 대화가 종료되었습니다. 레스트레이드 경감을 찾아가 의뢰를 수락하세요.]`"
            )
            return

# 렌더(Render) 환경변수 사용
TOKEN = os.environ.get("DISCORD_TOKEN")
client.run(TOKEN)
