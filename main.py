import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # If user sends a Telegram file
    if update.message.document:
        await update.message.reply_text("Receiving file...")

        file = await update.message.document.get_file()
        file_name = update.message.document.file_name
        file_path = os.path.join(DOWNLOAD_FOLDER, file_name)

        await file.download_to_drive(file_path)

        await update.message.reply_text("File saved on server successfully.")

    # If user sends a link
    elif update.message.text:
        link = update.message.text.strip()

        await update.message.reply_text("Downloading from link...")

        try:
            filename = link.split("/")[-1]
            if not filename:
                filename = "downloaded_file"

            file_path = os.path.join(DOWNLOAD_FOLDER, filename)

            # Memory safe download
            with requests.get(link, stream=True) as r:
                r.raise_for_status()
                with open(file_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

            await update.message.reply_text("Link downloaded successfully.")

        except Exception as e:
            await update.message.reply_text(f"Download failed: {str(e)}")


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))

print("Bot is running...")
app.run_polling()
