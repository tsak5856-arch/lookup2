# bot.py

import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to *Jaat Papa OSINT Bot!*\n"
        "Send me a mobile number (e.g., `9687696810`) and I will try to fetch public data.",
        parse_mode="Markdown"
    )


# Handle inline button presses
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "start_again":
        await query.message.reply_text(
            "🔁 Restarted. Send a mobile number again.\nExample: `9687696810`",
            parse_mode="Markdown"
        )


# Handle phone number messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.message.text.strip()
    url = f"http://osintx.info/API/krobetahack.php?key=ZYROBR0TH3R&type=mobile&term={number}"

    try:
        response = requests.get(url)

        if response.status_code != 200:
            await update.message.reply_text("❌ Error fetching data from API.")
            return

        data = response.json()

        if not data:
            await update.message.reply_text("ℹ️ No data found for this number.")
            return

        # Inline button
        button = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔁 Start Again", callback_data="start_again")]
        ])

        for entry in data:
            msg = (
                "✅ *Thanks For Using Jaat Papa OSINT*\n\n"
                f"📱 *Mobile*: {entry.get('mobile')}\n"
                f"📞 *Alt Mobile*: {entry.get('alt_mobile')}\n"
                f"👤 *Name*: {entry.get('name')}\n"
                f"👨‍👦 *Father Name*: {entry.get('father_name')}\n"
                f"📍 *Address*: {entry.get('address', '').replace('!', ', ')}\n"
                f"🌐 *Circle*: {entry.get('circle')}\n"
                f"🆔 *ID Number*: `{entry.get('id_number')}`\n"
            )

            if entry.get("email"):
                msg += f"✉️ *Email*: {entry.get('email')}\n"

            await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=button)

    except Exception as e:
        await update.message.reply_text(f"❗ Error: {e}")


# Main app runner
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))  # to handle buttons
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()
