import random
import pytube
from aiogram import Dispatcher, Bot, types
from aiogram.utils import executor
from glob import glob
import os

current_path = os.getcwd()
token = open(current_path+"\\res\\api.txt", "r").readline()
bot = Bot(str(token))
dp = Dispatcher(bot)
sending = ""

async def onStartInit(_):
    print("Bot is on-line!")

list_mp3 = glob(current_path + "current_path + '\\*")

@dp.message_handler(commands=["start"])
async def onStart(message:types.Message):
    await bot.send_message(message.from_user.id, "This is bot, developed by KostiaKova.\nThe easiest form of this class bots.\nSource code:\n"
                                                 "https://github.com/kostiakova/telebot-pytube-downloader.git")

@dp.message_handler(commands=['random'])
async def Random(message:types.Message):
    await  bot.send_audio(message.from_user.id, audio=open(random.choice(list_mp3), "rb"))

@dp.message_handler(commands=["send"])
async def Sending_downloaded(message:types.Message):
    with open(current_path + "\\res\\last_downloading.txt", "r") as fr:
        string_name = fr.read(100)
        fr.close()
    await bot.send_audio(message.from_user.id, audio=open(current_path+"\\res\\audios\\"+string_name+".mp3", "rb"))

@dp.message_handler(lambda message: True)
async def checkingAllMsgs(message:types.Message):
    print(message.text)
    if "www" in message.text:
        link: str = message.text
        yt = pytube.YouTube(link)
        name: str = yt.title
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(output_path=current_path+"\\res\\audios\\", filename=name+".mp3")
        print(name)
        with open(current_path + "\\res\\last_downloading.txt", "w") as fw:
            fw.write(name)
            fw.close()
        print("Downloading is DONE!!!")
        await bot.send_message(message.from_user.id, "Downloading is Well DONE!")
        print("Proceeding to sending")
        await bot.send_message(message.from_user.id, "Proceeding to Sending")
        try:
            await Sending_downloaded(message)
        except:
            print("Didn't Send :(")
            await bot.send_message(message.from_user.id, "I didn't Send it:(")

    else:
        await bot.send_message(message.from_user.id, "This message isn't link")

@dp.message_handler(commands=["stop"])
def Stop():
    exit()

executor.start_polling(dp, skip_updates=True, on_startup=onStartInit)
