import pandas as pd
import re
import io
from dateutil import parser

import os
import shutil
import tempfile
import gzip

TEMP_DIR = "/tmp"

### q-clean-up-excel-sales-data

COUNTRY_MAPPING = {
    "USA": "US", "U.S.A": "US", "United States": "US",
    "UAE": "AE", "U.A.E": "AE", "United Arab Emirates": "AE",
    "UK": "GB", "U.K": "GB", "United Kingdom": "GB",
    "Ind": "IN", "IND": "IN", "India": "IN",
    "BRA": "BR", "Bra": "BR", "Brazil": "BR",
    "Fra": "FR", "FRA": "FR", "France": "FR"
}

def extract_variables(question: str):
    pattern = r"What is the total margin for transactions before (.*?) for (.*?) sold in (.*?) \(which may be spelt in different ways\)\?"
    match = re.search(pattern, question)
    if match:
        date_str = match.group(1)
        product = match.group(2).strip()
        country = match.group(3).strip()
        return date_str, product, country
    return None, None, None

def clean_data(df: pd.DataFrame):
    # Trim whitespace from all string columns
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    
    # Standardize country names
    df["Country"] = df["Country"].replace(COUNTRY_MAPPING)
    
    # Clean and convert dates
    def clean_date(date_str):
        if isinstance(date_str, str):
            # Remove random whitespace and parenthetical content
            date_str = re.sub(r'\s*\(.*?\)', '', date_str)
            date_str = re.sub(r'\s+', ' ', date_str).strip()
        try:
            return parser.parse(date_str, ignoretz=True, dayfirst=False)
        except:
            return pd.NaT
    
    df["Date"] = df["Date"].apply(clean_date)
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    
    # Extract product name
    df["Product"] = df["Product/Code"].str.split('/').str[0].str.strip()
    
    # Clean numeric columns
    df["Sales"] = df["Sales"].str.replace("USD", "", regex=False).str.strip().astype(float)
    df["Cost"] = (
        df["Cost"].str.replace("USD", "", regex=False)
        .str.strip()
        .replace("", pd.NA)
        .astype(float)
    )
    df["Cost"].fillna(df["Sales"] * 0.5, inplace=True)
    
    return df

async def q_clean_up_excel_sales_data(question, file=None):
    # Extract parameters from question
    date_str, product_filter, country_filter = extract_variables(question)
    if None in (date_str, product_filter, country_filter):
        return {"error": "Could not parse question parameters"}
    
    # Clean and parse filter date
    cleaned_date_str = re.sub(r'\s*\(.*?\)', '', date_str)
    filter_date = parser.parse(cleaned_date_str, ignoretz=True)
    filter_date = pd.to_datetime(filter_date)
    
    # Standardize country code
    country_code = COUNTRY_MAPPING.get(country_filter, country_filter)
    
    # Process Excel file
    contents = await file.read()
    df = pd.read_excel(io.BytesIO(contents))
    df = clean_data(df)
    
    # Filter data
    mask = (
        (df["Date"] <= filter_date) &
        (df["Product"] == product_filter) &
        (df["Country"] == country_code)
    )
    filtered = df[mask].copy()
    
    # Calculate margin
    total_sales = filtered["Sales"].sum()
    total_cost = filtered["Cost"].sum()
    
    if total_sales == 0:
        return 0.0
    
    margin = (total_sales - total_cost) / total_sales
    # return round(margin, 4)
    return int(margin * 10000) / 10000
    

##### q-clean-up-student-marks 

import re

def extract_student_ids(file_content: str):
    """
    Extracts unique student IDs from the provided text content.
    The student ID is assumed to be exactly 10 alphanumeric characters
    located after a hyphen (-) and immediately before the "Marks" keyword,
    which may be prefixed by optional colons and whitespace.
    """
    unique_ids = set()  # Using a set to automatically handle duplicates
    
    # Regex pattern explanation:
    # - The hyphen (-) followed by any whitespace.
    # - Then exactly 10 alphanumeric characters (the student ID).
    # - A positive lookahead (?=...) asserts that what follows is optional whitespace,
    #   optional colons (0 to 2), more optional whitespace, and then "Marks".
    pattern = r'-\s*([A-Za-z0-9]{10})(?=\s*[:]{0,2}\s*Marks)'
    
    for line in file_content.splitlines():
        match = re.search(pattern, line)
        if match:
            student_id = match.group(1).strip()  # Extract and clean the ID
            unique_ids.add(student_id)  # Add to the set
    
    return unique_ids

async def q_clean_up_student_marks(question, file=None):
    try:
        # Read the content of the uploaded file
        contents = await file.read()
        file_content = contents.decode("utf-8")  # Decode bytes to string
        
        # Extract unique student IDs
        unique_ids = extract_student_ids(file_content)
        
        # Count unique students
        unique_student_count = len(unique_ids)
        
        return unique_student_count
    
    except Exception as e:
        return {"error": f"Error processing file: {e}"}


# Mapping for month abbreviations to numeric representation
MONTH_MAP = {
    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
    "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
    "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
}

async def q_apache_log_requests(question, file=None):

    TEMP_DIR = tempfile.gettempdir()
    TEMP_PATH = os.path.join(TEMP_DIR, "q-apache-log-requests")
    
    try:
        os.makedirs(TEMP_PATH, exist_ok=True)
        
        # Save the uploaded file to a temporary .gz file
        gz_path = os.path.join(TEMP_PATH, "q-apache-log-requests.gz")
        if file:
            content = await file.read()  # Await the read operation
            with open(gz_path, "wb") as f:
                f.write(content)
        else:
            return {"error": "No file provided"}
        
        # Decompress the .gz file into a plain text log file
        log_file_path = os.path.join(TEMP_PATH, "log.txt")
        with gzip.open(gz_path, "rb") as gz_file, open(log_file_path, "wb") as out_file:
            shutil.copyfileobj(gz_file, out_file)
        
        # q_pattern =  r"What is the number of successful GET requests for pages under\s*/?\s*([^/\s]+)\s*/?\s*from\s*(\d+)\s*:\s*00\s*until before\s*(\d+)\s*:\s*00\s*on\s*([A-Za-z]+)s\?"
        # q_match = re.search(q_pattern, question)

        # Simple regex pattern
        q_pattern = r"What is the number of successful GET requests for pages under /([^/]+)/ from (\d+) until before (\d+):00 on (\w+)s"

        # Match the pattern
        q_match = re.search(q_pattern, question)

        req_path = None
        start_hour = None
        end_hour = None
        weekday = None

        if q_match:
            req_path = q_match.group(1)       # Extracts "malayalam"
            start_hour = int(q_match.group(2))  # Extracts 0
            end_hour = int(q_match.group(3))    # Extracts 6
            weekday = q_match.group(4)         # Extracts "Wednesday"

            print(req_path, start_hour, end_hour, weekday)
        else:
            print("No match found")
      
        # log_pattern = re.compile(
        #     r'(?P<ip>[\d\.]+)\s+-\s+-\s+\['
        #     r'(?P<day>\d{2})/(?P<mon>[A-Za-z]{3})/(?P<year>\d{4}):'
        #     r'(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2}).*?\]\s+"'
        #     r'(?P<method>GET)\s+'
        #     r'(?P<path>/' + re.escape(req_path) + r'/[^"]*)"'
        #     r'\s+(?P<status>[2]\d{2})\s+'
        # )
        
        # count = 0
        # with open(log_file_path, "r", encoding="utf-8", errors="ignore") as log_file:
        #     for line in log_file:
        #         match = log_pattern.search(line)
        #         if match:
        #             hour = int(match.group("hour"))
        #             if start_hour <= hour < end_hour:
        #                 # Construct the date string from the log fields
        #                 day = match.group("day")
        #                 mon_abbr = match.group("mon")
        #                 year = match.group("year")
        #                 month = MONTH_MAP.get(mon_abbr, "01")
        #                 date_str = f"{day}/{month}/{year} {match.group('hour')}:{match.group('minute')}:{match.group('second')}"
        #                 try:
        #                     dt = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
        #                 except Exception:
        #                     continue
        #                 # Check if the log entry falls on the specified weekday.
        #                 if dt.strftime("%A") == weekday:
        #                     count += 1
        
        # # Cleanup temporary files
        # shutil.rmtree(TEMP_PATH, ignore_errors=True)
        # return {"result": count}
    
    except Exception as e:
        # shutil.rmtree(TEMP_PATH, ignore_errors=True)
        return {"error": f"Error processing file: {e}"}



