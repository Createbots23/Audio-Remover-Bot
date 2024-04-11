from pyrogram import Client, filters
from pyrogram.types import Message
from moviepy.editor import VideoFileClip

# Initialize Pyrogram client
api_id = 10471716
api_hash = 'f8a1b21a13af154596e2ff5bed164860'
bot_token = '6999401413:AAHgF1ZpUsCT5MgWX1Wky7GbegyeHvzi2AU'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Function to remove audio from video file
def remove_audio(video_path):
    video = VideoFileClip(video_path)
    video_without_audio = video.without_audio()
    video_without_audio_path = "video_without_audio.mp4"
    video_without_audio.write_videofile(video_without_audio_path, codec="libx264", audio_codec="aac")
    video.close()
    return video_without_audio_path

# Start command handler
@app.on_message(filters.command("start"))
def start_command(client, message):
    message.reply_text("Welcome to the bot! Send me a video file or document and I will remove the audio for you.")


# Main handler
@app.on_message(filters.private & filters.video)
def process_video(client, message):
    video_file = message.video.download()
    video_without_audio_path = remove_audio(video_file)
    message.reply_video(video_without_audio_path)
    # Clean up files
    os.remove(video_file)
    os.remove(video_without_audio_path)

# Run the bot
app.run()
