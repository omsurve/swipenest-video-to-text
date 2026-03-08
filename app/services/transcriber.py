from transformers import pipeline
from app.services.text_processor import process_subtitle_text


# Load Whisper model once (important for performance)
pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-large-v3",
    return_timestamps=True
)


def transcribe(audio_path):
    """
    Transcribe full audio and return processed text.
    """
    result = pipe(audio_path)

    text = result["text"]

    # Apply subtitle processing (Hinglish + spell correction + CamelCase)
    text = process_subtitle_text(text)

    return text


def transcribe_audio(audio_path):
    """
    Transcribe audio with timestamps and return chunks.
    """
    result = pipe(audio_path)

    chunks = result["chunks"]

    # Process each subtitle chunk
    for chunk in chunks:
        chunk["text"] = process_subtitle_text(chunk["text"])

    return chunks