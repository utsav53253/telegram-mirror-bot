import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.document:
        file = await update.message.document.get_file()
        file_path = os.path.join(DOWNLOAD_FOLDER, update.message.document.file_name)
        await file.download_to_drive(file_path)
        await update.message.reply_text("File received. Upload feature coming next.")

    elif update.message.text:
        link = update.message.text
        await update.message.reply_text("Downloading link...")

        filename = link.split("/")[-1]
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)

        r = requests.get(link)
        with open(file_path, "wb") as f:
            f.write(r.content)

        await update.message.reply_text("Link downloaded successfully.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))

app.run_polling()
