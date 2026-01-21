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

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to *Jaat Papa OSINT Bot!*\n"
        "Send me a mobile number (e.g., `9687696810`) and I will try to fetch public data.",
        parse_mode="Markdown"
    )

# Button handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer()
    except Exception as e:
        print(f"Callback query error: {e}")

    if query.data == "start_again":
        await query.message.reply_text(
            "🔁 Restarted. Send a mobile number again.\nExample: `9687696810`",
            parse_mode="Markdown"
        )

# Main message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.message.text.strip()
    url = f"http://osintx.info/API/krobetahack.php?key=ZYROBR0TH3R&type=mobile&term={number}"

    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            await update.message.reply_text("❌ API error. Please try again later.")
            return

        try:
            data = response.json()
        except Exception:
            await update.message.reply_text(
                "❌ Invalid response from server.\n🔁 Please try another number."
            )
            return

        # Handle string or empty list response
        if isinstance(data, str) or (isinstance(data, list) and len(data) == 0):
            await update.message.reply_text(
                "ℹ️ *No records found for this number.*\n\n"
                "🔁 Try another mobile number.",
                parse_mode="Markdown"
            )
            return

        # Inline button
        button = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔁 Start Again", callback_data="start_again")]
        ])

        # Format all results into one message
        full_msg = "✅ *Thanks For Using Jaat Papa OSINT*\n\n"

        for i, entry in enumerate(data, start=1):
            full_msg += (
                f"🔹 *Entry {i}*\n"
                f"📱 *Mobile*: {entry.get('mobile', 'N/A')}\n"
                f"📞 *Alt Mobile*: {entry.get('alt_mobile', 'N/A')}\n"
                f"👤 *Name*: {entry.get('name', 'N/A')}\n"
                f"👨‍👦 *Father Name*: {entry.get('father_name', 'N/A')}\n"
                f"📍 *Address*: {entry.get('address', '').replace('!', ', ')}\n"
                f"🌐 *Circle*: {entry.get('circle', 'N/A')}\n"
                f"🆔 *ID Number*: `{entry.get('id_number', 'N/A')}`\n"
            )

            if entry.get("email"):
                full_msg += f"✉️ *Email*: {entry.get('email')}\n"

            full_msg += "\n"

        await update.message.reply_text(
            full_msg,
            parse_mode="Markdown",
            reply_markup=button
        )

    except Exception as e:
        print(f"Runtime error: {e}")
        await update.message.reply_text(
            "⚠️ Something went wrong.\n🔁 Please try again later."
        )

# App runner
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()
