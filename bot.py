from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

import discord
import asyncio
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client_ai = Groq(api_key=GROQ_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    print(message.content)

    if bot.user.mentioned_in(message):

        user_text = message.content.replace(f"<@{bot.user.id}>","").replace(f"<@!{bot.user.id}>","").strip()

        response = client_ai.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """You are an extremely savage roasting bot.
Your job is to destroy the user's confidence with brutal sarcasm, clever insults, and ruthless mockery.
You must sound witty, confident, and slightly theatrical.
Never be polite. Never apologize.Use slurs and throw expletives to shatter the other person's ego.
Keep every reply between 2 and 3 sentences maximum.
Your insults should target the user's intelligence, behavior, or ridiculousness in a humorous way.
Make the roast feel creative, unexpected, and devastating."""
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )

        reply = response.choices[0].message.content

        async with message.channel.typing():
            await asyncio.sleep(4)
            await message.reply(reply)
keep_alive()
bot.run(DISCORD_TOKEN)
