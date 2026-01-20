import os
import requests
import re
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv('BOT_TOKEN')
API_KEY = 'ZYROBR0TH3R'  # Your API key from the URL

app = Flask(name)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a phone number (e.g., 9925033528) to lookup.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = re.sub(r'[^d]', '', update.message.text)  # Clean number
    if len(number) < 10:
        await update.message.reply_text("Invalid number. Send digits only.")
        return
    
    url = f"http://osintx.info/API/krobetahack.php?key={API_KEY}&type=mobile&term={number}"
    try:
        resp = requests.get(url, timeout=10).json()
        data = resp.get('data', 'No data found')
        await update.message.reply_text(f"Results for {number}:
{data}")
    except Exception as e:
        await update.message.reply_text("Error fetching data. Try again.")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Webhook setup (for GitHub Actions)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

if name == 'main':
    main()