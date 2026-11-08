with open("prompt.txt", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

import os
import telebot
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bienvenue sur DIENG PREDICT VIP - FC26 Penalty. Envoie-moi un match : Ex: Real Madrid vs Barcelone - PENALTY")

@bot.message_handler(func=lambda m: True)
def predict(message):
    user_text = message.text
    bot.reply_to(message, "Analyse en cours...")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ]
        )
        result = response.choices[0].message.content
        bot.reply_to(message, result)
    except Exception as e:
        bot.reply_to(message, f"Erreur : {e}")

print("Bot lancé...")
bot.infinity_polling()
