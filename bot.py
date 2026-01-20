# bot.py
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Use env var

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send a number to look up. Example: 9925033528")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.message.text.strip()

    # API request
    url = f"http://osintx.info/API/krobetahack.php?key=ZYROBR0TH3R&type=mobile&term={number}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("Error fetching data from API.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
