import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import yt_dlp
import os
from config import TOKEN  # Tokeni config.py-dən oxuyuruq

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 🔹 Videonu yükləyən funksiya
async def download_video(url):
    output_path = "video.mp4"
    ydl_opts = {
        "outtmpl": output_path,
        "format": "mp4/best",
        "quiet": True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path

# 🔹 /start komandası
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Salam! 👋 Link at, sənin üçün videonu çəkim. (TikTok/Instagram)")

# 🔹 İstifadəçi link atanda
@dp.message()
async def link_handler(message: types.Message):
    url = message.text.strip()
    if "tiktok.com" in url or "instagram.com" in url:
        await message.answer("⏳ Videonu yükləyirəm, gözlə...")
        try:
            video_path = await download_video(url)
            await message.answer_video(video=open(video_path, "rb"))
            os.remove(video_path)  # Videonu silirik ki, yaddaş dolmasın
        except Exception as e:
            await message.answer(f"⚠️ Xəta baş verdi: {e}")
    else:
        await message.answer("⚠️ Zəhmət olmasa TikTok və ya Instagram linki at!")

# 🔹 Botu işə salırıq
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
