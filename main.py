import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Media Downloader Engine (Cobalt API)
API_URL = "https://api.cobalt.tools/"

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 **স্বাগতম Downloader Bot-এ!**\n\n"
        "যেকোনো ভিডিও বা ছবির লিংক পাঠান:\n"
        "• 🎵 TikTok (Watermark ছাড়া)\n"
        "• 📸 Instagram (Reels & HD Photo)\n"
        "• 📘 Facebook Videos\n"
        "• ▶️ YouTube Videos\n\n"
        "শুধু লিংক পেস্ট করুন!"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

# Link Handle Command
async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.startswith(("http://", "https://")):
        await update.message.reply_text("❌ অনুগ্রহ করে সঠিক ভিডিও বা ছবির লিংক দিন।")
        return

    msg = await update.message.reply_text("⏳ প্রসেস করা হচ্ছে, একটু অপেক্ষা করুন...")

    try:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "url": url,
            "videoQuality": "max"
        }

        response = requests.post(API_URL, json=payload, headers=headers)
        data = response.json()

        if response.status_code == 200 and "url" in data:
            download_link = data["url"]
            await update.message.reply_text(
                f"✅ **ডাউনলোড রেডি!**\n\n🔗 [এখানে ক্লিক করে ডাউনলোড করুন]({download_link})", 
                parse_mode="Markdown"
            )
            await msg.delete()

        elif "picker" in data:
            # multiple images/videos carousel
            for item in data["picker"]:
                item_url = item.get("url")
                if item_url:
                    await update.message.reply_text(f"🔗 [ডাউনলোড লিংক]({item_url})", parse_mode="Markdown")
            await msg.delete()

        else:
            await msg.edit_text("❌ লিঙ্কটি সাপোর্ট করছে না বা ভিডিও খুঁজে পাওয়া যায়নি।")

    except Exception as e:
        await msg.edit_text("❌ প্রসেস করতে সমস্যা হয়েছে। আবার চেষ্টা করুন।")

if __name__ == '__main__':
    TOKEN = os.environ.get("BOT_TOKEN")
    if TOKEN:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_media))
        print("Bot Run Hochhe...")
        app.run_polling()
      
