import os
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from typing import List

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="File Transfer API",
        version="1.0.0",
        description="API for uploading and downloading zip files",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = FastAPI(
    title="File Transfer API",
    description="API for uploading and downloading zip files",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.openapi = custom_openapi

if os.path.exists("/app"):
    UPLOAD_DIRECTORY = "/app/uploads"
else:
    UPLOAD_DIRECTORY = os.path.join(os.getcwd(), "uploads")

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def serve_html():
    with open("index.html", "r") as f:
        return f.read()

@app.get("/download/{filename}", response_class=FileResponse, summary="Download a zip file")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        media_type='application/zip',
        filename=filename
    )

@app.get("/list-files", response_model=List[str], summary="List available zip files")
async def list_files():
    return [f for f in os.listdir(UPLOAD_DIRECTORY) if f.endswith('.zip')]

@app.post("/upload", summary="Upload a zip file")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Only .zip files are allowed")

    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {"filename": unique_filename, "status": "uploaded successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
