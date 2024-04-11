from pyrogram import Client, filters
import ffmpeg
import os

# Create a Pyrogram Client
api_id = "10471716"
api_hash = "f8a1b21a13af154596e2ff5bed164860"
bot_token = "6999401413:AAHgF1ZpUsCT5MgWX1Wky7GbegyeHvzi2AU"

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Function to remove audio from video
def remove_audio(input_file, output_file):
    ffmpeg.input(input_file).output(output_file, **{'c:v': 'copy', 'an': None}).run(overwrite_output=True)

# Start command handler
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Hello! Send me a video and reply '/remove' to remove the audio.")

# Remove command handler
@app.on_message(filters.command("remove"))
def remove_audio_handler(client, message):
    if message.reply_to_message and message.reply_to_message.video:
        video_message = message.reply_to_message
        video_file_id = video_message.video.file_id
        video_file = client.download_media(video_file_id)
        output_file = "output_" + os.path.basename(video_file)

        try:
            remove_audio(video_file, output_file)
            message.reply_document(document=output_file)
            os.remove(output_file)
        except Exception as e:
            print("Error:", e)
            message.reply_text("An error occurred while processing the video.")
    else:
        message.reply_text("Please reply to a video message with '/remove' to remove the audio.")

# 
# Run the bot
app.run()
