from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import zipfile
import io

app = FastAPI()

# allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api")
async def api_root(
    question: str = Form(...), 
    file: Optional[UploadFile] = File(None)
):
    print("Question:", question)
    if file:
        content = await file.read()
        with zipfile.ZipFile(io.BytesIO(content)) as z:
            file_list = z.namelist()
            print("Files in the zip:", file_list)
    return {"message": "success"}


@app.get("/")
async def root():
    return  {"message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
