import cv2
import torch
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
AUDIO_EXTS = {".wav", ".mp3"}

MODEL_PATH = "models/RealESRGAN_x4plus.pth"

def enhance_image(input_path, output_path, resolution="1080p", strength=1.0):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # ✅ CREATE THE MODEL (THIS WAS MISSING)
    model = RRDBNet(
        num_in_ch=3,
        num_out_ch=3,
        num_feat=64,
        num_block=23,
        num_grow_ch=32,
        scale=4,
    )

    upsampler = RealESRGANer(
        scale=4,
        model_path=MODEL_PATH,
        model=model,           # ✅ PASS REAL MODEL
        tile=0,
        tile_pad=10,
        pre_pad=0,
        half=(device == "cuda"),
        device=device,
    )

    img = cv2.imread(input_path, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid image")

    output, _ = upsampler.enhance(img, outscale=4)

    # Resize to requested resolution
    if resolution == "720p":
        output = cv2.resize(output, (1280, 720))
    elif resolution == "1080p":
        output = cv2.resize(output, (1920, 1080))
    elif resolution == "4k":
        output = cv2.resize(output, (3840, 2160))

    cv2.imwrite(output_path, output, [cv2.IMWRITE_JPEG_QUALITY, 95])
    return output_path
