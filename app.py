from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/api")
def root():
    return JSONResponse({
        "answer": "Hello, World!"
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


