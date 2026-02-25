from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
import shutil
import os

from app.services.audio_extractor import extract_audio
from app.services.transcriber import transcribe_audio
from app.services.subtitle_generator import generate_srt


router = APIRouter()

ALLOWED_EXTENSIONS = {"mp4", "mkv", "avi", "mov"}


# ⭐ BACKGROUND WORKER
def process_video(video_path, audio_path, srt_path):

    try:
        print(f"🔥 Processing started for: {video_path}")

        extract_audio(video_path, audio_path)

        chunks = transcribe_audio(audio_path)

        generate_srt(chunks, srt_path)

        print(f"✅ VIDEO PROCESSING COMPLETE!: {video_path}")

    except Exception as e:
        print(f"❌ ERROR processing {video_path}: {str(e)}")



# ⭐ UPLOAD ROUTE
@router.post("/upload")
def upload_video(background_tasks: BackgroundTasks,
                 file: UploadFile = File(...)):

    # ✅ Validate filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid file."
        )

    # ✅ Validate extension
    extension = file.filename.split(".")[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a video."
        )

    # ⭐ sanitize filename (VERY IMPORTANT)
    safe_filename = os.path.basename(file.filename)

    # create folders
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("audio", exist_ok=True)
    os.makedirs("subtitles", exist_ok=True)

    video_path = f"uploads/{safe_filename}"

    # save video safely
    try:
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(e)}"
        )

    # prepare paths
    base_name = safe_filename.rsplit(".", 1)[0]

    audio_path = f"audio/{base_name}.wav"
    srt_path = f"subtitles/{base_name}.srt"

    # ⭐ BACKGROUND TASK
    background_tasks.add_task(
        process_video,
        video_path,
        audio_path,
        srt_path
    )

    return {
        "message": "Upload successful 🚀 Processing started in background.",
        "subtitle_file": f"{base_name}.srt",
        "download_url": f"/download/{base_name}.srt"
    }



# ⭐ DOWNLOAD ROUTE
@router.get("/download/{filename}")
def download_subtitle(filename: str):

    safe_filename = os.path.basename(filename)

    file_path = f"subtitles/{safe_filename}"

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="File not found or still processing."
        )

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=safe_filename
    )
