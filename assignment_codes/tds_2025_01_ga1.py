import requests
import json
import re
import httpx
import numpy as np
from datetime import datetime, timedelta

import os
import zipfile
import csv
import shutil

import hashlib

# Constants
TEMP_PATH = "/tmp"
CSV_FILENAME = "extract.csv"

async def q_vs_code_version(question=None,file=None):
    # code -s
    return "Version:          Code 1.96.4 (cd4ee3b1c348a13bafd8f9ad8060705f6d4b9cba, 2025-01-16T00:16:19.038Z)\nOS Version:       Windows_NT x64 10.0.26100\nCPUs:             AMD Ryzen 5 PRO 7530U with Radeon Graphics      (12 x 1996)\nMemory (System):  14.80GB (6.68GB free)\nVM:               0%\nScreen Reader:    no\nProcess Argv:     --crash-reporter-id 7cb1abbc-0806-4071-90df-891b75f5c994\nGPU Status:       2d_canvas:                              enabled\n                  canvas_oop_rasterization:               enabled_on\n                  direct_rendering_display_compositor:    disabled_off_ok\n                  gpu_compositing:                        enabled\n                  multiple_raster_threads:                enabled_on\n                  opengl:                                 enabled_on\n                  rasterization:                          enabled\n                  raw_draw:                               disabled_off_ok\n                  skia_graphite:                          disabled_off\n                  video_decode:                           enabled\n                  video_encode:                           enabled\n                  vulkan:                                 disabled_off\n                  webgl:                                  enabled\n                  webgl2:                                 enabled\n                  webgpu:                                 enabled\n                  webnn:                                  disabled_off\n\nCPU %   Mem MB     PID  Process\n    0      136   13604  code main\n    0      115    4712  shared-process\n    0      222   10512  window [1] (.gitlab-ci.yml - lexis-nexis-product-recommender - Visual Studio Code)\n    0      114   12484  ptyHost\n    0       15    8660       conpty-agent\n    0       99   13544       C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -noexit -command \"try { . \\\"c:\\Users\\e430271.SPI-GLOBAL\\AppData\\Local\\Programs\\Microsoft VS Code\\resources\\app\\out\\vs\\workbench\\contrib\\terminal\\common\\scripts\\shellIntegration.ps1\\\" } catch {}\"\n    0       13   18112         C:\\WINDOWS\\system32\\cmd.exe /c \"\"C:\\Users\\e430271.SPI-GLOBAL\\AppData\\Local\\Programs\\Microsoft VS Code\\bin\\code.cmd\" -s\"\n    0      116    5588           electron-nodejs (cli.js )\n    0      144   15200             \"C:\\Users\\e430271.SPI-GLOBAL\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe\" -s\n    1      102    5112               gpu-process\n    0      100   15512               utility-network-service\n    0       95   20192               crashpad-handler\n    0      105   13136  fileWatcher [1]\n    0       44   20240     crashpad-handler\n    0       61   20676     utility-network-service\n    0      145   21460     gpu-process\n    0      467   23144  extensionHost [1]\n\nWorkspace Stats:\n|  Window (.gitlab-ci.yml - lexis-nexis-product-recommender - Visual Studio Code)\n|    Folder (lexis-nexis-product-recommender): 6 files\n|      File types: yml(1) json(1) py(1) html(1) md(1)\n|      Conf files:"


async def q_uv_http_get(question,file=None):

    #  extract only email from question
    email = re.search(r"email\s*set\s*to\s*([\w\.\@\-\+]+)", question, re.IGNORECASE).group(1)

    res = requests.get(f"https://httpbin.org/get?email={email}")
    ans = res.json()

    ans = json.dumps(ans)
    return ans

async def q_npx_prettier(question, file):
    if file:
        # Read the file content
        file_content = await file.read()

        # Prepare the files parameter for the request
        files = {
            "file": (file.filename, file_content, file.content_type)
        }

        # Define the external API URL
        external_api_url = "https://npx-prettier.vercel.app/upload"
        # external_api_url = "http://127.0.0.1:3000/upload"

        # Forward the file to the external API
        async with httpx.AsyncClient() as client:
            response = await client.post(external_api_url, files=files)

        # Return the response from the external API
            res = response.json()
            return res["sha256"]
    else:
        return {"error": "No file provided"}

async def q_use_google_sheets(question, file=None):
    # Extract numbers from SEQUENCE function
    sequence_match = re.search(r"SEQUENCE\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", question, re.IGNORECASE)
    constraint_match = re.search(r"ARRAY_CONSTRAIN\s*\(\s*SEQUENCE\s*\(.*?\)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", question, re.IGNORECASE)
    
    if sequence_match and constraint_match:
        rows, cols, start, step = map(int, sequence_match.groups())
        constraint_rows, constraint_cols = map(int, constraint_match.groups())
        
        # Generate the sequence matrix
        sequence_matrix = np.arange(start, start + rows * cols * step, step, dtype=int).reshape(rows, cols)
        
        # Apply ARRAY_CONSTRAIN constraints
        constrained_matrix = sequence_matrix[:constraint_rows, :constraint_cols]
        
        # Compute SUM and ensure it's a Python int
        result = int(np.sum(constrained_matrix))
        return result
    else:
        return "Could not parse formula."


async def q_use_excel(question, file=None):
    # Extract numbers from SORTBY and TAKE functions
    sortby_match = re.search(r"SORTBY\s*\(\s*\{([\d\s,]+)\}\s*,\s*\{([\d\s,]+)\}\s*\)", question, re.IGNORECASE)
    take_match = re.search(r"TAKE\s*\(\s*SORTBY\s*\(.*?\)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", question, re.IGNORECASE)
    
    if sortby_match and take_match:
        values = list(map(int, sortby_match.group(1).split(',')))
        sort_keys = list(map(int, sortby_match.group(2).split(',')))
        take_rows, take_cols = map(int, take_match.groups())
        
        # Sort values based on sort_keys
        sorted_indices = np.argsort(sort_keys)
        sorted_values = np.array(values)[sorted_indices]
        
        # Apply TAKE constraints
        taken_values = sorted_values[:take_cols]  # Assuming a 1D array
        
        # Compute SUM and ensure it's a Python int
        result = int(np.sum(taken_values))
        return result
    else:
        return "Could not parse formula."


async def count_week_days(question,file=None):
    # Extract day and date range from question
    day_match = re.search(r"How many (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)s are there in the date range (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})", question, re.IGNORECASE)
    
    if not day_match:
        return "Could not parse question."
    
    day, start_date, end_date = day_match.groups()
    
    week_day_map = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,  
        "Sunday": 6
    }
    
    if day not in week_day_map:
        return f"Invalid day: {day}"
    
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    count = sum(1 for i in range((end_date - start_date).days + 1)
                if (start_date + timedelta(days=i)).weekday() == week_day_map[day])
    
    return count



async def q_extract_csv_zip(question,file):
    """Process ZIP file received in FastAPI request."""
    try:
        # Ensure temp directory exists
        os.makedirs(TEMP_PATH, exist_ok=True)
        
        # Save uploaded file
        zip_path = os.path.join(TEMP_PATH, "q-extract-csv-zip.zip")
        with open(zip_path, "wb") as buffer:
            buffer.write(await file.read())

        # Extract ZIP contents
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(TEMP_PATH)

        # Check if extract.csv exists
        csv_path = os.path.join(TEMP_PATH, CSV_FILENAME)
        if not os.path.exists(csv_path):
            return {"error": f"{CSV_FILENAME} not found in ZIP."}

        # Read CSV and extract answer column
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "answer" in row:
                    answer = row["answer"]
                    break
            else:
                return {"error": "Column 'answer' not found in CSV."}

        # Cleanup temp directory
        shutil.rmtree(TEMP_PATH, ignore_errors=True)

        return answer

    except Exception as e:
        return {"error": f"Error processing file: {e}"}
    


async def q_multi_cursor_json(question, file):
    """Process TXT file, convert to JSON, and compute SHA-256 hash."""
    try:
        # Ensure temp directory exists
        os.makedirs(TEMP_PATH, exist_ok=True)

        # Save uploaded file
        txt_path = os.path.join(TEMP_PATH, "uploaded.txt")
        with open(txt_path, "wb") as buffer:
            buffer.write(await file.read())

        # Read file and convert to JSON
        json_data = {}
        with open(txt_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    json_data[key.strip()] = value.strip()

        # Convert JSON object to string
        json_string = json.dumps(json_data, separators=(',', ':'))

        # Compute SHA-256 hash
        hash_value = hashlib.sha256(json_string.encode()).hexdigest()

        # Cleanup temp directory
        shutil.rmtree(TEMP_PATH, ignore_errors=True)

        return hash_value

    except Exception as e:
        return {"error": f"Error processing file: {e}"}


def extract_json_from_text(text):
    """Extracts the JSON array from a given text using regex."""
    match = re.search(r'\[\s*\{.*?\}\s*\]', text, re.DOTALL)
    if not match:
        raise ValueError("JSON array not found in the text")
    return match.group().replace(" ", "").replace("\n", "")

async def q_use_json(question, file=None):
    """Sorts a JSON array of objects by age and name, and returns compact JSON without spaces or newlines."""
    try:
        json_text = extract_json_from_text(question)
        json_array = json.loads(json_text)
        sorted_array = sorted(json_array, key=lambda x: (x["age"], x["name"]))
        return json.dumps(sorted_array, separators=(',', ':'))
    except Exception as e:
        return f"Error:{e}"
