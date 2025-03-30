
import re
import json
import requests
import hashlib

import os
import base64
from io import BytesIO
from PIL import Image

import colorsys
import numpy as np

from assignment_codes.helper import update_github_file

async def q_markdown(question, file=None):
    return """# Analysis of Number of Steps walked

## Description

**Introduction**: 

This is an analysis of the number of steps you walked each day for a week, comparing over time and with friends. 

***code:*** 

in a single line `sum(steps)`

To calculate sum

```
sum = 0
for x in steps:
    sum+=x
print(sum)

```

## steps 


1. Collect some friends and ask them to do the following
    - note down steps walked everyday
    - list them in an array after a week
2. after the end of the week get all the data 
    - calculate sum 
    - do analysis
    

## collected Data

| Name | Total no of steps |
|------|-------------------|
| ravi | 12023             |
|charan| 20039|
|rahul| 30443|
|govind| 43531|

## Analysis


link to anaysis website is [here](https://mystepsanalysis.com)
image of line chart
![Line chart]("https://mystepsanalysis.com/images/line-chart.jpg")


> Walking everyday is good for health


"""


async def q_image_compression(question,file):
    """Compress an uploaded image losslessly to WebP and return Base64 in JSON."""

    try:
        # Read uploaded file
        image = Image.open(BytesIO(await file.read()))

        # Convert and compress to WebP (lossless)
        output_buffer = BytesIO()
        image.save(output_buffer, "WEBP", lossless=True, quality=100, method=6)

        # Check file size
        compressed_size = output_buffer.tell()
        if compressed_size > 1500:
            return {"error": "Unable to compress image losslessly under 1,500 bytes."}

        # Encode to Base64
        base64_image = base64.b64encode(output_buffer.getvalue()).decode("utf-8")

        return base64_image
    
    
    except Exception as e:
        return {"error": f"Error processing file: {e}"}


async def q_use_colab(question, file=None):
    # Extract only the email from the question
    # Run this program on Google Colab, allowing all required access to your email ID: miryala.narayanareddy@straive.com 

    match = re.search(r"email\sID:\s*([\w.\@\-\+]+)", question, re.IGNORECASE)
    if not match:
        return json.dumps({"error": "No email found in the question."})

    email = match.group(1)

    # Compute a hash fragment
    token_expiry_year = 2025  # Example token expiry year
    hash_fragment = hashlib.sha256(f"{email} {token_expiry_year}".encode()).hexdigest()[-5:]

    return hash_fragment


async def q_use_colab_image_library(question, file):
    """Analyze the lightness of an uploaded image and count pixels above a threshold."""
    
    try:
        # Read uploaded file
        image = Image.open(BytesIO(await file.read()))
        
        # Convert image to RGB array
        rgb = np.array(image) / 255.0

        # Compute lightness using HLS color space
        lightness = np.apply_along_axis(lambda x: colorsys.rgb_to_hls(*x[:3])[1], 2, rgb)
        light_pixels = np.sum(lightness > 0.217)

        return int(light_pixels)

    except Exception as e:
        return {"error": f"Error processing file: {e}"}
    
async def q_github_pages(question, GITHUB_TOKEN=None):
    match = re.search(r"Ensure that your email address (.*?) is in the page's HTML", question, re.IGNORECASE)
    email = match.group(1) if match else None

    if not email:
        raise ValueError("Email not found in the question.")

    html_code = f"""
    <html>
    <head>
        <title>Test A2</title>
    </head>
    <body>
        <h1>A2 Task deploy through GitHub Pages</h1>
        <div>
            <!--email_off-->{email}<!--/email_off-->
        </div>
    </body>
    </html>
    """

    # print(email)
    # print(GITHUB_TOKEN)

    FILE_PATH = "index.html"
    REPO_NAME = "tds-project-gitpage"
    BRANCH = "main"
    REPO_OWNER = "MiryalaNarayanaReddy"

    result = await update_github_file(html_code, FILE_PATH, REPO_OWNER, REPO_NAME, BRANCH, GITHUB_TOKEN)

    if result is True:
        return f"https://{REPO_OWNER}.github.io/{REPO_NAME}/"
    return result  # Return error if not successful