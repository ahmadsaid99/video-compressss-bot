import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def compress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video
    file = await video.get_file()
    await file.download_to_drive("input.mp4")

    subprocess.run([
        "ffmpeg", "-i", "input.mp4",
        "-vcodec", "libx264",
        "-crf", "28",
        "output.mp4"
    ])

    await update.message.reply_video(video=open("output.mp4", "rb"))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.VIDEO, compress))
app.run_polling()