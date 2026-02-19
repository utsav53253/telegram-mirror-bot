import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text

    await update.message.reply_text("Downloading...")

    # Download using aria2
    subprocess.run(["aria2c", "-x", "8", "-s", "8", link])

    await update.message.reply_text("Download completed (test mode).")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
