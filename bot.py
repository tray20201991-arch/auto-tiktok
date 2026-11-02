import telebot, requests, io
TOKEN = "8093135920:AAFGm0JYeytgv4SBpRV-PeYbbiBrmjER0Ew"
CHANNEL = "@st00rg"
bot = telebot.TeleBot(TOKEN)

# هذا فيديو مضمون 100% يشتغل بتيليجرام وبيه صوت
url = "https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4"
data = requests.get(url, timeout=30).content

print(f"Size: {len(data)}")
f = io.BytesIO(data)
f.name = "video.mp4"

bot.send_video(CHANNEL, f, caption="فيديو مضحك جديد 😂\n\n#مضحك #تيك_توك #st00rg\nتابعونا: @st00rg", supports_streaming=True)
print("OK posted!")
