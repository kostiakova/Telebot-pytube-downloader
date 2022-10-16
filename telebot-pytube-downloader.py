import random
import pytube
from aiogram import  Dispatcher, Bot, types
from aiogram.utils import executor
from glob import glob

token = "5084563840:AAEPCiX5oa8JScbexo2eUidZ00Y95Z0DuDE"
bot = Bot(token)
dp = Dispatcher(bot)
sending = ""

async def onStart(_):
    print("Bot is on-line!")

list_mp3 = glob('/home/kostinus/Videos/*')

@dp.message_handler(commands=["start"])
async def onStart(message:types.Message):
    await bot.send_message(message.from_user.id, "This is bot, developed by KostiaKova.\nThe easiest form of this class bots.\nSource code: ")

@dp.message_handler(commands=['random'])
async def command_start(message:types.Message):
    await  bot.send_audio(message.from_user.id, audio=open(random.choice(list_mp3), "rb"))

@dp.message_handler(commands=["send"])
async def Sending(message:types.Message):
    with open("res.txt", "r") as fr:
        string_name = fr.read(100)
        fr.close()
    await bot.send_audio(message.from_user.id, audio=open("/home/kostinus/Videos/"+string_name+".mp3", "rb"))

@dp.message_handler(lambda message: True)
async def checkingMsgs(message:types.Message):
    link = message.text
    yt = pytube.YouTube(link)
    name = yt.title
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(output_path="/home/kostinus/Videos",
                    filename=name+".mp3")
    print(name)
    sending = name
    print(sending)
    with open("res.txt", "w") as fw:
        fw.write(sending)
        fw.close()


executor.start_polling(dp, skip_updates=True, on_startup=onStart)