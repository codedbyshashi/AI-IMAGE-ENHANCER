import uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool

from processing import enhance_image, IMAGE_EXTS

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
ORIG_DIR = UPLOAD_DIR / "original"
PROC_DIR = UPLOAD_DIR / "processed"

for d in (ORIG_DIR, PROC_DIR):
    d.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="MediaNoiseFixer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.get("/", response_class=HTMLResponse)
def index():
    return (BASE_DIR / "static" / "index.html").read_text(encoding="utf-8")


@app.post("/api/process-image")
async def process_image(
    file: UploadFile = File(...),
    resolution: str = Form("1080p"),
    strength: float = Form(1.0),
):
    ext = Path(file.filename).suffix.lower()
    if ext not in IMAGE_EXTS:
        raise HTTPException(400, "Unsupported image type")

    uid = uuid.uuid4().hex
    orig_path = ORIG_DIR / f"{uid}{ext}"
    proc_path = PROC_DIR / f"{uid}_proc.jpg"

    orig_path.write_bytes(await file.read())

    try:
        # IMPORTANT: run heavy task in threadpool
        await run_in_threadpool(
            enhance_image,
            str(orig_path),
            str(proc_path),
            resolution,
            strength,
        )
    except Exception as e:
        raise HTTPException(500, f"Image processing failed: {e}")

    return {
        "status": "ok",
        "original_url": f"/uploads/original/{orig_path.name}",
        "processed_url": f"/uploads/processed/{proc_path.name}",
    }
