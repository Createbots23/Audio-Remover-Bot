from pyrogram import Client, filters
import ffmpeg
import os

# Create a Pyrogram Client
# Create a Pyrogram Client
api_id = "10471716"
api_hash = "f8a1b21a13af154596e2ff5bed164860"
bot_token = "6999401413:AAHgF1ZpUsCT5MgWX1Wky7GbegyeHvzi2AU"


app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Function to remove audio from video
def remove_audio(input_file, output_file):
    (
        ffmpeg
        .input(input_file)
        .output(output_file, **{'c:v': 'copy', 'an': None})
        .run(overwrite_output=True)
    )

# Function to send status message
def send_status_message(message, text):
    message.reply_text(text)

# Start command handler
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Hello! Send me any video file, and I'll remove the audio.")

# Process all video files
@app.on_message(filters.video)
def process_video(client, message):
    # Notify user that processing has started
    send_status_message(message, "Processing started. Please wait...")

    video_file_id = message.video.file_id
    video_file = client.download_media(video_file_id)
    output_file = "output_" + os.path.basename(video_file)

    try:
        remove_audio(video_file, output_file)
        # Send the processed video back to the user
        message.reply_video(video=output_file)
        # Notify user that processing is complete
        send_status_message(message, "Processing completed.")
        # Delete the temporary output file
        os.remove(output_file)
    except Exception as e:
        print("Error:", e)
        send_status_message(message, "An error occurred while processing the video.")

# Run the bot
app.run()
