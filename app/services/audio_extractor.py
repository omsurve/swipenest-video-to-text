import subprocess
import os

def extract_audio(video_path, output_audio_path):

    os.makedirs("audio", exist_ok=True)

    command = [
        "ffmpeg",
        "-i", video_path,
        "-ac", "1",        # mono
        "-ar", "16000",    # 16kHz
        "-vn",             # no video
        output_audio_path
    ]

    try:
        subprocess.run(command, check=True)
        print("✅ Audio extracted successfully!")

    except subprocess.CalledProcessError as e:
        print("❌ FFmpeg failed:", e)
