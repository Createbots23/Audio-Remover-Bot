from pyrogram import Client, filters
import subprocess

API_ID = '10471716'
API_HASH = 'f8a1b21a13af154596e2ff5bed164860'
BOT_TOKEN = '6999401413:AAHgF1ZpUsCT5MgWX1Wky7GbegyeHvzi2AU'

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def is_video_document(_, message):
    if message.document:
        mime_type = message.document.mime_type
        return mime_type.startswith('video/')
    return False

@app.on_message(filters.command('start'))
def start(_, update):
    update.reply_text("Hello! Send me a video file or document and I'll remove the audio and send it back to you.")

@app.on_message(filters.video | (filters.document & filters.create(is_video_document)))
def remove_audio(_, update):
    try:
        file_id = update.message.video.file_id if update.message.video else update.message.document.file_id
        file_path = app.download_media(file_id)
        output_file = f"{file_path}_no_audio.mp4"
        subprocess.run(["avconv", "-i", file_path, "-c", "copy", "-an", output_file], check=True)
        update.reply_video(output_file)
    except Exception as e:
        print(f"An error occurred: {e}")
        update.reply_text("Sorry, something went wrong while processing the video.")

@app.on_message(filters.command(["help", "error"]))
def help_command(_, update):
    update.reply_text("I'm just a simple bot that removes audio from videos. Send me a video file or document and I'll take care of the rest.")

app.run()
