import requests
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from SONALI_MUSIC import app

# 🔑 अपनी OpenAI API key यहां डालो
OPENAI_API_KEY = "https://api.openai.com/v1/chat/completions"

def ask_ai(query):
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": query}],
            "max_tokens": 200
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return f"API Error: {response.text}"
    except Exception as e:
        return f"Error: {e}"

@app.on_message(filters.command("ask"))
async def ask_handler(client, message):
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply_text("**Please provide a query.**")

    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    reply = ask_ai(query)

    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("ᴧηsᴡєʀ ʙʏ", url="https://t.me/Sonali_music_bot")]]
    )
    await message.reply_text(reply, reply_markup=button)

@app.on_message(filters.mentioned & filters.group)
async def ask_group_handler(client, message):
    query = message.text.replace(f"@{client.me.username}", "").strip()
    if not query:
        return await message.reply_text("**Please provide a query.**")

    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    reply = ask_ai(query)

    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("ᴧηsᴡєʀ ʙʏ", url="https://t.me/Sonali_music_bot")]]
    )
    await message.reply_text(reply, reply_markup=button)
