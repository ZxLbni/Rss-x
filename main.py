import os
import requests
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Pyrogram Client Setup
api_id = int(os.environ.get("API_ID", 29382018))
api_hash = os.environ.get("API_HASH", "4734a726c04620c61ec0a28a1ae0d57f")
bot_token = os.environ.get("BOT_TOKEN", "8027197031:AAHhjRgVcA5QlfcryW6EAm2PrIUHS3kMXoU")
channel_id = os.environ.get("CHANNEL_ID", "-1002616383974")  # Use channel username or ID

bot = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Flask Server to Keep Alive
app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is alive!'

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))

@bot.on_message(filters.command("post") & filters.private)
async def post_to_channel(client, message):
    try:
        api_url = "https://nsfw-noob-api.vercel.app/xnxx/10/desi"
        response = requests.get(api_url)
        
        if response.status_code != 200:
            await message.reply("API থেকে ডাটা লোড করতে সমস্যা হয়েছে ❌")
            return

        data = response.json().get("data", [])
        
        if not data:
            await message.reply("কোন কন্টেন্ট খুঁজে পাওয়া যায়নি 😢")
            return

        for item in data:
            name = item.get("name", "No Title")
            desc = item.get("description", "No Description")
            date = item.get("upload_date", "Unknown Date")
            thumbnail = item.get("thumbnail", "")
            content_url = item.get("content_url", "#")

            # Create Caption
            caption = f"**📌 {name}**\n\n{desc}\n\n**আপলোড তারিখ:** {date}"

            # Create Inline Button
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🎥 ভিডিও দেখুন", url=content_url)]
            ])

            # Send to Channel
            await client.send_photo(
                chat_id=channel_id,
                photo=thumbnail,
                caption=caption,
                reply_markup=keyboard
            )

        await message.reply("সব কন্টেন্ট সফলভাবে পোস্ট করা হয়েছে ✅")

    except Exception as e:
        await message.reply(f"একটি error হয়েছে: {str(e)}")
        print(f"Error: {e}")

if __name__ == "__main__":
    # Start Flask Server in a Thread
    Thread(target=run_flask).start()
    
    # Start Pyrogram Bot
    print("Bot is running...")
    bot.run()
