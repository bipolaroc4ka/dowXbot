from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    filters
)
import os
import yt_dlp

# Your BotFather token
BOT_TOKEN = "You Token"

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Hello! Send me a link to a tweet with a video, and I'll download it for you."
    )

async def download_twitter_video(update: Update, context: CallbackContext):
    message = update.message.text

    if "x.com" in message:
        await update.message.reply_text("Downloading video, this may take some time...")
        try:
            # Unique filename for the video
            output_file = "twitter_video.mp4"

            # yt_dlp configuration
            ydl_opts = {
                "outtmpl": output_file,
                "format": "best[ext=mp4]",
            }

            # Download the video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([message])

            # Send the video back to the user
            with open(output_file, "rb") as video:
                await update.message.reply_video(video)

            # Remove the file after sending
            os.remove(output_file)

        except Exception as e:
            await update.message.reply_text(f"Error: {e}")
    else:
        await update.message.reply_text("Please send a link to a tweet with a video.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers for commands and messages
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_twitter_video))

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
