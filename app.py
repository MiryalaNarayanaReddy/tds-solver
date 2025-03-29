from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import zipfile
import io
import re
import requests

from process import process_question

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from a1 import A1

@app.post("/api")
async def api_root(
    question: str = Form(...), 
    file: Optional[UploadFile] = File(None)
):
    print("Question:", question)
    
    # Process the question
    # response = process_question(question)
    a1 = A1()
    response = a1.process_question(question)

    if response :
        print("Response:", response) 
        return {"answer": response}
    else:
        print("No response found")
        return {"error": "No response found"}

    # Handle file upload if provided
    if file:
        content = await file.read()
        with zipfile.ZipFile(io.BytesIO(content)) as z:
            file_list = z.namelist()
            print("Files in the zip:", file_list)

    return {"answer": response}

@app.get("/")
async def root():
    return  {"message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
