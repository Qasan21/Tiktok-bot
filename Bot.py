# --- Keep Alive Hissəsi ---
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Telegram Bot Hissəsi ---
import telebot
import os
import requests

TOKEN = os.environ.get('8441531405:AAGp_G5tY0Li-SwI9fWh72PGyqilAjrhEnk')  # Tokeni Koyeb environment variable-dan götürür
bot = telebot.TeleBot(TOKEN)

# --- TikTok/Instagram Downloader ---
def download_video(url):
    # Sadə demo: TikTok üçün üçüncü tərəf API
    api_url = f"https://www.tikwm.com/api/?url={url}"
    r = requests.get(api_url).json()
    if r.get("data") and r["data"].get("play"):
        return r["data"]["play"]
    return None

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Salam! Mən TikTok və Instagram videolarını yükləyə bilirəm. Link göndər! 😎")

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    url = message.text.strip()
    if "tiktok.com" in url or "instagram.com" in url:
        bot.send_message(message.chat.id, "⏳ Videonu yoxlayıram...")
        video_link = download_video(url)
        if video_link:
            bot.send_message(message.chat.id, f"✅ Video hazırdır: {video_link}")
        else:
            bot.send_message(message.chat.id, "❌ Videonu yükləmək alınmadı. Başqa link yoxla!")
    else:
        bot.send_message(message.chat.id, "⚠️ Zəhmət olmasa düzgün TikTok/Instagram linki göndər!")

# --- Botu oyadırıq və işə salırıq ---
keep_alive()
bot.polling()
