import asyncio
import os
import config
import sys
import logging
from aiogram.enums import ParseMode, ChatAction
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from pytube import YouTube
from aiogram.types import BufferedInputFile

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer('Для скачивания видео пропишите /download "ссылка"')

@dp.message(Command('download'))
async def command_download_handler(message: Message):
    user_info = f"User ID: {message.from_user.id}\n"
    user_info += f"Username: {message.from_user.username}\n"
    user_info += f"First name: {message.from_user.first_name}\n"
    user_info += f"Last name: {message.from_user.last_name}\n"
    user_info += f"Language code: {message.from_user.language_code}\n"
    user_info += f"\n"

    with open('user_info.txt', 'a') as f:
        f.write(user_info)
    try:
        video_url = message.text.split()[1]
        save_path = "./video"

        await message.answer("Загрузка...")

        yt = YouTube(video_url)
        stream = yt.streams.filter(resolution='720p', progressive=True).first()
        video_file = stream.download(output_path=save_path)

        await message.answer(f"Видео '{yt.title}' успешно загружено!")

        await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_VIDEO)

        with open(video_file, 'rb') as file:
            video = BufferedInputFile(file.read(), filename="cool_video.mp4")
            await bot.send_video(chat_id=message.chat.id, video=video)

        os.remove(video_file)

        print("Видео успешно отправлено и удалено с сервера.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")
async def main():
    global dp
    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())