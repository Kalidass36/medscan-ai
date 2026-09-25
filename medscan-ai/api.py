from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from .pipeline import process_image

app = FastAPI(title="MedScan-AI")


@app.post("/process")
async def process_upload(file: UploadFile = File(...)):
    content = await file.read()
    result = process_image(content)
    return JSONResponse(result)
