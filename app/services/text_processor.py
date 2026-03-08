from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


def convert_to_hinglish(text):
    """
    Convert Hindi script to Roman Hinglish.
    """
    try:
        return transliterate(text, sanscript.DEVANAGARI, sanscript.ITRANS)
    except:
        return text


def convert_to_camel_case(text):
    """
    Convert sentence to CamelCase subtitle format.
    Example:
    'namaste dosto kaise ho'
    → 'Namaste Dosto Kaise Ho'
    """
    words = text.split()
    return " ".join(word.capitalize() for word in words)


def hindi_spell_correction(text):
    """
    Basic spell correction placeholder.
    You can later integrate a stronger Hindi NLP model.
    """
    # simple normalization for now
    text = text.replace("hai", "hai")
    text = text.replace("nhi", "nahi")
    text = text.replace("kya", "kya")

    return text


def process_subtitle_text(text):
    """
    Full pipeline for subtitle formatting.
    """
    text = convert_to_hinglish(text)
    text = hindi_spell_correction(text)
    text = convert_to_camel_case(text)

    return text