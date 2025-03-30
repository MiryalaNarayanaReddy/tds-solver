from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os 

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
from a2 import A2

assignments = {
    "a1": A1(),
    "a2": A2()
}

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub token with repo access


async def process_request(question: str, file: Optional[UploadFile] = File(None)):
    
    for assignment in assignments.values():

        key = assignment.process_question(question)

        if key:
            answer = await assignment.solve(key, question, file, GITHUB_TOKEN)
            return answer
        else: 
            continue
    
    return "No such question"


@app.post("/api")
async def api_root(
    question: str = Form(...), 
    file: Optional[UploadFile] = File(None)
):
    # print("Question:", question)

    # a1 = A1()
    # key = a1.process_question(question)
    # response = await a1.solve(key,question,file)


    answer = await process_request(question, file)

    if answer:
        return {"answer": str(answer)}
    else:
        print("No response found")
        return {"error": "No response found"}

@app.get("/")
async def root():
    return  {"message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
