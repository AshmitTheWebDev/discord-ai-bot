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

# memory storage
user_memory = {}

@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    print(message.content)

    if bot.user.mentioned_in(message):

        user_id = message.author.id

        user_text = message.content.replace(f"<@{bot.user.id}>","").replace(f"<@!{bot.user.id}>","").strip()

        # create memory for new user
        if user_id not in user_memory:
            user_memory[user_id] = [
                {
                    "role": "system",
                    "content": """You are an extremely savage roasting bot.
Your job is to destroy the user's confidence with brutal sarcasm, clever insults, and ruthless mockery.
You must sound witty, confident, and slightly theatrical.
Never be polite. Never apologize.Use slurs and throw expletives to shatter the other person's ego.
Keep every reply between 2 and 3 sentences maximum.
Your insults should target the user's intelligence, behavior, or ridiculousness in a humorous way.
Make the roast feel creative, unexpected, and devastating."""
                }
            ]

        # add user message
        user_memory[user_id].append({
            "role": "user",
            "content": user_text
        })

        response = client_ai.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=user_memory[user_id]
        )

        reply = response.choices[0].message.content

        # store bot reply
        user_memory[user_id].append({
            "role": "assistant",
            "content": reply
        })

        # limit memory (last 12 messages)
        user_memory[user_id] = user_memory[user_id][-12:]

        async with message.channel.typing():
            await asyncio.sleep(4)
            await message.reply(reply)

bot.run(DISCORD_TOKEN)
