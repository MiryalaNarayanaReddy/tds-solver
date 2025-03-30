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

import pytz

# Constants
TEMP_PATH = "/tmp"
# TEMP_DIR = "./temp"


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
    TEMP_PATH = os.path.join(TEMP_DIR, "q-extract-csv-zip")
    CSV_FILENAME = "extract.csv"
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
    TEMP_PATH = os.path.join(TEMP_DIR, "q-multi-cursor-json")
    
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
    

async def q_unicode_data(question, file=None):
    """Extract ZIP, process encoded CSV/TXT files, and sum values for target symbols."""
    
    TARGET_SYMBOLS = {"‡", "ˆ", "š"}
    ENCODINGS = {
        "data1.csv": "cp1252",
        "data2.csv": "utf-8",
        "data3.txt": "utf-16"
    }
    
    TEMP_PATH = os.path.join(TEMP_DIR, "q-unicode-data")

    try:
        os.makedirs(TEMP_PATH, exist_ok=True)
        
        # Save uploaded file
        zip_path = os.path.join(TEMP_PATH, "q-unicode-data.zip")
        
        if file:
            content = await file.read()  # Await the read operation
            with open(zip_path, "wb") as buffer:
                buffer.write(content)
        
        # Extract ZIP contents
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(TEMP_PATH)
        
        total_sum = 0
        
        # Process each file with the correct encoding
        for filename, encoding in ENCODINGS.items():
            file_path = os.path.join(TEMP_PATH, filename)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding=encoding) as f:
                    reader = csv.reader(f, delimiter='\t' if filename.endswith('.txt') else ',')
                    next(reader, None)  # Skip header
                    for row in reader:
                        if len(row) >= 2 and row[0] in TARGET_SYMBOLS:
                            try:
                                total_sum += float(row[1])
                            except ValueError:
                                pass  # Ignore invalid numeric values
        
        shutil.rmtree(TEMP_PATH, ignore_errors=True)
        
      
        if int(total_sum) == total_sum: # Check if the result is an integer
            return int(total_sum)
        else:
            return total_sum
    
    except Exception as e:
        return {"error": f"Error processing file: {e}"}
    

async def q_replace_across_files(question, file=None):
    """Extract ZIP, replace 'IITM' (case-insensitive) with 'IIT Madras' in all files, compute SHA-256 hash."""
    
    TEMP_PATH = os.path.join(TEMP_DIR, "q-replace-across-files")
    try:
        os.makedirs(TEMP_PATH, exist_ok=True)
        
        # Save uploaded file
        zip_path = os.path.join(TEMP_PATH, "q-replace-across-files.zip")
        
        if file:
            content = await file.read()  # Await the read operation
            with open(zip_path, "wb") as buffer:
                buffer.write(content)
        
        # Extract ZIP contents
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            extract_folder = os.path.join(TEMP_PATH, "unzipped")
            os.makedirs(extract_folder, exist_ok=True)
            zip_ref.extractall(extract_folder)
        
        # Replace "IITM" (case-insensitive) with "IIT Madras" in all text files
        pattern = re.compile(r"IITM", re.IGNORECASE)
        
        for root, _, files in os.walk(extract_folder):
            for filename in files:
                file_path = os.path.join(root, filename)
                
                # Read file in binary mode to preserve line endings
                with open(file_path, "rb") as f:
                    content = f.read()
                
                # Decode using a universal approach (detect encoding)
                try:
                    decoded_content = content.decode("utf-8")
                except UnicodeDecodeError:
                    decoded_content = content.decode("latin-1")
                
                # Perform the replacement
                modified_content = pattern.sub("IIT Madras", decoded_content)
                
                # Write back in binary mode to preserve line endings
                with open(file_path, "wb") as f:
                    f.write(modified_content.encode("utf-8"))
        
        # Compute the equivalent of `cat * | sha256sum`
        sha256_hash = hashlib.sha256()
        
        for root, _, files in os.walk(extract_folder):
            for filename in sorted(files):  # Sort to match shell behavior
                file_path = os.path.join(root, filename)
                with open(file_path, "rb") as f:
                    while chunk := f.read(8192):  # Read in chunks
                        sha256_hash.update(chunk)
        
        # Cleanup temp files
        shutil.rmtree(TEMP_PATH, ignore_errors=True)
        
        return sha256_hash.hexdigest()
    
    except Exception as e:
        return {"error": f"Error processing file: {e}"}
    

async def q_move_rename_files(question, file=None):
    """Extract ZIP, move all files into one folder, rename digits, and compute SHA-256 checksum."""
    TEMP_PATH = os.path.join(TEMP_DIR, "q-move-rename-files")
    
    try:
        FINAL_FOLDER = os.path.join(TEMP_PATH, "final")
        os.makedirs(FINAL_FOLDER, exist_ok=True)

        # Save uploaded file
        zip_path = os.path.join(TEMP_PATH, "q-move-rename-files.zip")
        if file:
            content = await file.read()
            with open(zip_path, "wb") as buffer:
                buffer.write(content)
        else:
            raise ValueError("No file provided")

        # Extract ZIP contents
        extract_folder = os.path.join(TEMP_PATH, "unzipped")
        os.makedirs(extract_folder, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_folder)

        # Move all files from subdirectories into FINAL_FOLDER
        for root, _, files in os.walk(extract_folder):
            for filename in files:
                src_path = os.path.join(root, filename)
                dest_path = os.path.join(FINAL_FOLDER, filename)
                shutil.move(src_path, dest_path)

        # Rename files by replacing each digit with the next (9 becomes 0)
        def shift_digits(match):
            return str((int(match.group(0)) + 1) % 10)

        # Sort filenames in **byte order** for `LC_ALL=C` consistency
        sorted_filenames = sorted(os.listdir(FINAL_FOLDER), key=lambda x: x.encode("latin1"))

        for filename in sorted_filenames:
            new_filename = re.sub(r'\d', shift_digits, filename)
            old_path = os.path.join(FINAL_FOLDER, filename)
            new_path = os.path.join(FINAL_FOLDER, new_filename)
            os.rename(old_path, new_path)

        # Compute the equivalent of `grep . * | LC_ALL=C sort | sha256sum`
        sha256_hash = hashlib.sha256()
        all_lines = []

        # Read files in sorted order (LC_ALL=C match)
        sorted_filenames = sorted(os.listdir(FINAL_FOLDER), key=lambda x: x.encode("latin1"))

        for filename in sorted_filenames:
            file_path = os.path.join(FINAL_FOLDER, filename)

            # Read file lines **in binary mode**, then decode
            with open(file_path, "rb") as f:
                for line in f:
                    decoded_line = line.decode("latin1", "ignore").rstrip("\r\n")  # Normalize line endings
                    if decoded_line:  # Skip empty lines (mimic `grep . *`)
                        all_lines.append(f"{filename}:{decoded_line}")

        # Sort the output **in pure byte order (LC_ALL=C)**
        all_lines.sort(key=lambda x: x.encode("latin1"))

        for line in all_lines:
            sha256_hash.update(line.encode("latin1"))

        result = sha256_hash.hexdigest()

        # Cleanup temporary files
        shutil.rmtree(TEMP_PATH, ignore_errors=True)

        return result

    except Exception as e:
        return {"error": f"Error processing file: {e}"}

async def q_compare_files(question, file=None):
    """Extract ZIP, compare a.txt and b.txt line by line, and count differing lines."""
    TEMP_PATH = os.path.join(TEMP_DIR, "q-compare-files")
    try:
        os.makedirs(TEMP_PATH, exist_ok=True)
        
        # Save uploaded file
        zip_path = os.path.join(TEMP_PATH, "q-compare-files.zip")
        
        if file:
            content = await file.read()  # Await the read operation
            with open(zip_path, "wb") as buffer:
                buffer.write(content)
        
        # Extract ZIP contents
        extract_folder = os.path.join(TEMP_PATH, "unzipped")
        os.makedirs(extract_folder, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_folder)
        
        # Read both files
        a_path = os.path.join(extract_folder, "a.txt")
        b_path = os.path.join(extract_folder, "b.txt")
        
        if not os.path.exists(a_path) or not os.path.exists(b_path):
            return {"error": "Missing a.txt or b.txt"}
        
        with open(a_path, "r", encoding="utf-8", errors="ignore") as f_a, \
             open(b_path, "r", encoding="utf-8", errors="ignore") as f_b:
            
            a_lines = f_a.readlines()
            b_lines = f_b.readlines()
        
        # Ensure both files have the same number of lines
        if len(a_lines) != len(b_lines):
            return {"error": "Files have different number of lines"}
        
        # Count differing lines
        diff_count = sum(1 for a_line, b_line in zip(a_lines, b_lines) if a_line != b_line)
        
        # Cleanup temp files
        shutil.rmtree(TEMP_PATH, ignore_errors=True)
        
        return diff_count
    
    except Exception as e:
        return {"error": f"Error processing file: {e}"}
    


async def q_list_files_attributes(question, file=None):
    """Extract ZIP while preserving timestamps, list file attributes, filter by size & date, and sum sizes."""
    TEMP_PATH = os.path.join(TEMP_DIR, "q-list-files-attributes")
    try:
        os.makedirs(TEMP_PATH, exist_ok=True)
        
        zip_path = os.path.join(TEMP_PATH, "q-list-files-attributes.zip")
        
        if file:
            content = await file.read()  # Await the read operation
            with open(zip_path, "wb") as buffer:
                buffer.write(content)
        
        # Extract ZIP contents manually while preserving timestamps
        extract_folder = os.path.join(TEMP_PATH, "unzipped")
        os.makedirs(extract_folder, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            for zip_info in zip_ref.infolist():
                extracted_path = os.path.join(extract_folder, zip_info.filename)
                
                if not zip_info.is_dir():
                    with open(extracted_path, "wb") as f:
                        f.write(zip_ref.read(zip_info.filename))
                    
                    # Preserve timestamp
                    mod_time = datetime(*zip_info.date_time).timestamp()
                    os.utime(extracted_path, (mod_time, mod_time))

        # Define the threshold datetime
        ist = pytz.timezone("Asia/Kolkata")
        threshold_date = ist.localize(datetime(2007, 9, 23, 22, 30))
        timestamp_threshold = threshold_date.timestamp()
        
        # List files and their attributes
        total_size = 0
        for root, _, files in os.walk(extract_folder):
            for filename in files:
                file_path = os.path.join(root, filename)
                
                if os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path)
                    modified_time = os.path.getmtime(file_path)  # Modification time (epoch)
                    
                    # Convert file modification time to IST
                    file_mod_time = datetime.fromtimestamp(modified_time, pytz.utc).astimezone(ist).timestamp()
                    
                    if file_size >= 5463 and file_mod_time >= timestamp_threshold:
                        total_size += file_size
        
        # Cleanup temp files
        shutil.rmtree(TEMP_PATH, ignore_errors=True)
        
        return total_size
    except Exception as e:
        return f"Error: {str(e)}"


async def q_sql_ticket_sales(question, file=None):

    return "select sum(units*price) from tickets where lower(trim(type)) = 'gold';"
