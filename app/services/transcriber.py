from transformers import pipeline

pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small",
    return_timestamps=True   
)

def transcribe(audio_path):
    result = pipe(audio_path)
    return result["text"]

def transcribe_audio(audio_path):
    result = pipe(audio_path)
    return result["chunks"]
