from transformers import pipeline
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-medium",
    return_timestamps=True
)


def convert_to_hinglish(text):
    """
    Converts Hindi (Devanagari) text to Hinglish (Roman script).
    If text is already English, it returns unchanged.
    """
    try:
        return transliterate(text, sanscript.DEVANAGARI, sanscript.ITRANS)
    except:
        return text


def transcribe(audio_path):
    lang = detect_language(audio_path)
    pipe = get_pipeline(lang)
    result = pipe(audio_path)

    text = result["text"]

    # Convert Hindi → Hinglish
    text = convert_to_hinglish(text)

    return text


def transcribe_audio(audio_path):
    lang = detect_language(audio_path)
    pipe = get_pipeline(lang)
    result = pipe(audio_path)

    chunks = result["chunks"]

    # Convert Hindi → Hinglish for each chunk
    for chunk in chunks:
        chunk["text"] = convert_to_hinglish(chunk["text"])

    return chunks