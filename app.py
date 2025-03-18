from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import zipfile
import pandas as pd
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
async def root(
    question: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # Read the uploaded ZIP file
        with zipfile.ZipFile(io.BytesIO(await file.read()), 'r') as zip_ref:
            # Extract the list of files
            file_names = zip_ref.namelist()
            
            # Find the CSV file inside the ZIP
            csv_file_name = next((f for f in file_names if f.endswith('.csv')), None)
            if not csv_file_name:
                return JSONResponse({"error": "No CSV file found in ZIP"}, status_code=400)
            
            # Read the CSV file into a DataFrame
            with zip_ref.open(csv_file_name) as csv_file:
                df = pd.read_csv(csv_file)

            # Ensure 'answer' column exists
            if "answer" not in df.columns:
                return JSONResponse({"error": "No 'answer' column in CSV"}, status_code=400)

            # Get the first value in the "answer" column
            answer_value = df["answer"].iloc[0]

            return JSONResponse({"answer": str(answer_value)})

    except zipfile.BadZipFile:
        return JSONResponse({"error": "Invalid ZIP file"}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


