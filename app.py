from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

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
    key = a1.process_question(question)
    response = await a1.solve(key,question,file)


    if response :
        # print("Response:", response) 
        return {"answer": str(response)}
    else:
        print("No response found")
        return {"error": "No response found"}

@app.get("/")
async def root():
    return  {"message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
