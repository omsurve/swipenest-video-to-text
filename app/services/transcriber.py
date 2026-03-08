from faster_whisper import WhisperModel

# Load Faster-Whisper model once (better performance)
model = WhisperModel(
    "large-v3",
    device="cpu",        # change to "cuda" if you have GPU
    compute_type="int8"  # good balance of speed and memory for CPU
)


def detect_language(audio_path):
    """
    Detect language of the audio using Faster-Whisper.
    Returns language code like 'en', 'hi', etc.
    """
    segments, info = model.transcribe(audio_path, beam_size=1)

    # Faster-Whisper automatically detects language
    language = info.language

    return language


def transcribe(audio_path):
    """
    Return full transcription text (string).
    Keeps same behavior as previous implementation.
    """
    segments, info = model.transcribe(audio_path)

    text = " ".join([segment.text.strip() for segment in segments])

    return text


def transcribe_audio(audio_path):
    """
    Return transcription chunks with timestamps.
    Structure matches your previous 'chunks' output
    so subtitle generator will still work.
    """
    segments, info = model.transcribe(audio_path)

    chunks = []

    for segment in segments:
        chunks.append({
            "timestamp": (segment.start, segment.end),
            "text": segment.text.strip()
        })

    return chunks