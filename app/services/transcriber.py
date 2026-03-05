from transformers import pipeline, WhisperProcessor, WhisperForConditionalGeneration
import torch

# Load processor and model for language detection
processor = WhisperProcessor.from_pretrained("openai/whisper-small")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")

def detect_language(audio_path):
    # Load audio
    from transformers import WhisperFeatureExtractor
    feature_extractor = WhisperFeatureExtractor.from_pretrained("openai/whisper-small")
    audio = feature_extractor(audio_path, return_tensors="pt")["input_features"]
    
    # Generate language token
    with torch.no_grad():
        generated_ids = model.generate(
            audio,
            max_length=1,
            num_beams=1,
            return_dict_in_generate=True,
            output_scores=True,
        )
    
    # Get the predicted language
    language_token = generated_ids.sequences[0][0]
    language = processor.decode(language_token, skip_special_tokens=True)
    return language

def get_pipeline(language):
    if language == "en":
        model_name = "openai/whisper-base.en"
    else:
        model_name = "openai/whisper-medium"
    
    return pipeline(
        "automatic-speech-recognition",
        model=model_name,
        return_timestamps=True   
    )

def transcribe(audio_path):
    lang = detect_language(audio_path)
    pipe = get_pipeline(lang)
    result = pipe(audio_path)
    return result["text"]

def transcribe_audio(audio_path):
    lang = detect_language(audio_path)
    pipe = get_pipeline(lang)
    result = pipe(audio_path)
    return result["chunks"]
