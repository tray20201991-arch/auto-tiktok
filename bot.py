import os
import logging
from pyrogram import Client, filters
from pyrogram.types import (
    Message, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    CallbackQuery
)
import yt_dlp

# إعدادات التسجيل
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# بيانات البوت وحساب التليجرام
API_ID = int(os.getenv("API_ID", "24340324"))  # حط الـ API ID مالك هنا أو اتركه افتراضي
API_HASH = os.getenv("API_HASH", "c4146a48fdf8f4ff682ac4a6217e2e77")  # الـ API Hash مالك
BOT_TOKEN = "8608740193:AAEK0S6kUN6ZaGC5QTPr7gxw0Wpi3doiMfM"  # توكن البوت الخاص بك

app = Client("InternalSearchBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"هلا بيك يا **{user_name}** ⚡️\n\n"
        "أني بوت البحث والتحميل الداخلي المتطور 🔥\n"
        "🔹 **فقط دز اسم الشيء الي تريد تبحث عنه أو رابطه هنا بالدردشة، وراح أجيبلك النتائج مع الصور وأزرار التحميل المائية المرتبة!**"
    )
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 البوت يعمل بأعلى كفاءة", callback_data="about_bot")]
    ])
    await message.reply_text(welcome_text, reply_markup=keyboard)

@app.on_callback_query(filters.regex("about_bot"))
async def about_callback(client, callback_query):
    await callback_query.answer("البوت جاهز للبحث والتحميل بأعلى جودة 🔥", show_alert=True)

# البحث والتحميل حصراً داخل البوت
@app.on_message(filters.text & ~filters.command(["start"]))
async def internal_search_and_download(client, message: Message):
    query = message.text.strip()
    processing_msg = await message.reply_text("🔍 **جاري البحث والتحليل بأعلى دقة، انتظرني لحظات...**")

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch3', # يجيب أفضل 3 نتائج مطابقة بدقة عالية
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            entries = info.get('entries', [info])

            if not entries:
                await processing_msg.edit_text("❌ ما لقيت أي نتائج تطابق بحثك، جرب كلمة بحث أخرى.")
                return

            await processing_msg.delete()

            # عرض النتائج بشكل بطاقات داخل البوت مع أزرار مائية وتفاعلية
            for entry in entries:
                title = entry.get('title', 'بدون عنوان')
                duration = entry.get('duration_string', 'غير معروف')
                uploader = entry.get('uploader', 'قناة غير معروفة')
                thumbnail = entry.get('thumbnail')
                webpage_url = entry.get('webpage_url')
                
                caption = (
                    f"🎬 **{title}**\n\n"
                    f"👤 **القناة:** `{uploader}`\n"
                    f"⏱ **المدة:** `{duration}`\n"
                    f"🔗 **الرابط:** {webpage_url}\n\n"
                    "👇 **اختر طريقة التحميل بأعلى جودة:**"
                )

                # أزرار مائية مرتبة بتصميم أنيق
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔥 تحميل فيديو (أعلى جودة مقفولة)", callback_data=f"dl_vid|{webpage_url}")],
                    [InlineKeyboardButton("🎵 تحويل إلى صوت MP3 (نقاء تام)", callback_data=f"dl_aud|{webpage_url}")]
                ])

                if thumbnail:
                    await message.reply_photo(photo=thumbnail, caption=caption, reply_markup=keyboard)
                else:
                    await message.reply_text(caption, reply_markup=keyboard)

    except Exception as e:
        await processing_msg.edit_text(f"⚠️ حدث خطأ أثناء البحث: `{str(e
