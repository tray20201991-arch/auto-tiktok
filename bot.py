import requests, random, time, os
import telebot

TOKEN = "8093135920:AAGqzb8HIOE1Pda1vIoyFlGXx1xtOVPc490"
CHANNEL_ID = "@st00rg"
bot = telebot.TeleBot(TOKEN)

# حسابات تيك توك نسحب منها - بدون موقع tikwm
TIKTOK_USERS = ["funnyvideos", "comedy", "memes", "footballtiktok"]

def get_videos_from_tiktok():
    # نستخدم API مجاني ما محجوب من بايثون اني وير
    try:
        username = random.choice(TIKTOK_USERS)
        # نستخدم رابط مباشر بدون tikwm
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://www.tiktok.com/@{username}"
        # هنا نرجع فيديو تجريبي لان التحميل المباشر محجوب، نستخدم تيليجرام مباشرة
        # الحل البديل: ننشر رابط تيك توك مع وصف
        return [f"https://www.tiktok.com/@{username}/video/7123456789"]
    except:
        return []

print(f"🚀 بدأ النشر لقناة {CHANNEL_ID}")

while True:
    try:
        # نشر رسالة تجريبية لتأكد البوت شغال
        caption = f"""😂 فيديو مضحك جديد

#مضحك #تيك_توك #st00rg

تابعونا: {CHANNEL_ID}"""
        
        # نجرب ننشر فيديو من حسابات عامة
        bot.send_message(CHANNEL_ID, caption)
        print("✅ نشر تم")
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        if "not enough rights" in str(e).lower() or "chat not found" in str(e).lower():
            print("تأكد البوت ادمن بالقناة @st00rg")
    
    time.sleep(300) # 5 دقايق
