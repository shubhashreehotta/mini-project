from typing import List
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from PIL import Image
import numpy as np
import io

app = FastAPI()


class PredictionResponse(BaseModel):
    """This defines what the API will send back as a response."""
    user_id: int
    confidence_score: float


# Dummy result (will be replaced by real model later)
response_data = PredictionResponse(user_id=123456789, confidence_score=0.95)


def preprocess_image(file: UploadFile) -> np.ndarray:
    """
    Prepare the uploaded image before sending it to the model.
    Steps:
    - Open the image
    - Resize to 224x224
    - Convert to array
    - Scale values between 0 and 1
    """
    image = Image.open(io.BytesIO(file.file.read())).convert("RGB")
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    return img_array


def user_id_prediction(frames: List[UploadFile]):
    """
    Process the uploaded frames and run prediction.
    For now, this just returns a dummy result.
    """
    processed_frames = [preprocess_image(f) for f in frames]

    # Later: call the real model here with processed_frames
    response_data.user_id = 123456789
    response_data.confidence_score = 0.95


@app.get("/attendance/recognise", response_model=PredictionResponse)
async def get_attendance_recognise():
    """Get the latest prediction result."""
    return response_data


@app.post("/attendance/recognise")
async def post_attendance_model(frames: List[UploadFile] = File(...)):
    """Upload images, preprocess them, and run prediction."""
    user_id_prediction(frames)
    return {"status": "success", "message": "Frames received and processed"}
