
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

from assignment_codes.helper import update_github_file,trigger_github_workflow

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

async def q_image_compression(question, file):
    """Compress an uploaded image losslessly to WebP and return Base64 in JSON format."""
    try:
        # Read uploaded file
        image = Image.open(BytesIO(await file.read()))

        # Convert and compress to WebP (lossless)
        output_buffer = BytesIO()
        image.save(output_buffer, "WEBP", lossless=True, quality=100, method=6)

        # Check file size
        compressed_size = output_buffer.tell()
        if compressed_size > 1500:  # Adjust this size limit if needed
            return {"error": "Unable to compress image losslessly under 1,500 bytes."}

        # Encode to Base64 and format as data URI
        base64_image = base64.b64encode(output_buffer.getvalue()).decode("utf-8")
        return  f"data:image/webp;base64,{base64_image}"

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



async def q_vercel_python(question, GITHUB_TOKEN=None, file=None):
    """Update a file at the given GitHub URL with the data from the uploaded file."""
    
    REPO_OWNER = "MiryalaNarayanaReddy"
    REPO_NAME = "tds-project-scheduled-workflow"
    BRANCH = "master"
    FILE_PATH = "q-vercel-python.json"
    FILE_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{FILE_PATH}"
    
    try:
        # Read the uploaded file
        file_content = await file.read()
        file_content_str = file_content.decode("utf-8")

        # Update the file in GitHub
        result = await update_github_file(file_content_str, FILE_PATH, REPO_OWNER, REPO_NAME, BRANCH, GITHUB_TOKEN)
        
        if result is True:
            return "https://tds-project-vercel-app.vercel.app/api"
        return result  # Return error if update fails
    
    except Exception as e:
        return {"error": f"Error processing file: {e}"}


async def q_github_action(question, GITHUB_TOKEN=None):

    email_match = re.search(r"email\s+address\s+([\w.\-+@]+)", question, re.IGNORECASE)
    email = email_match.group(1) if email_match else "default@example.com"
    print(email)
    # email = "miryala@straive.com"
    yml_file = f"""name: GitHub Actions Demo

on: [push]

jobs:
  explore-github-actions:
    runs-on: ubuntu-latest
    steps:
      - name: {email}
        run: echo "Hello, world!"

      - name: Checkout Repository
        uses: actions/checkout@v4
      
      - name: Display Information
        run: |
          echo "🚀 Workflow triggered by ${{ github.event_name }}"
          echo "🐧 Running on ${{ runner.os }}"
          echo "🔎 Branch: ${{ github.ref }}, Repo: ${{ github.repository }}"
          echo "💡 Repository cloned successfully"
          echo "📂 Listing repository files:"
          ls ${{ github.workspace }}
          echo "🍏 Job status: ${{ job.status }}"
"""
    
    USERNAME = "MiryalaNarayanaReddy"
    REPO_NAME = "tds-project-gitpage"
    WORKFLOW_PATH = ".github/workflows/test.yml"
    
    await update_github_file(yml_file, WORKFLOW_PATH, USERNAME, REPO_NAME, "main", GITHUB_TOKEN)
    await trigger_github_workflow(USERNAME, REPO_NAME, "test.yml", GITHUB_TOKEN,"main")
    
    return f"https://github.com/{USERNAME}/{REPO_NAME}"


async def q_fastapi(question, GITHUB_TOKEN=None, file=None):
    """Update q-fastapi.csv in the GitHub repository and return the API URL."""
    
    REPO_OWNER = "MiryalaNarayanaReddy"
    REPO_NAME = "tds-project-scheduled-workflow"
    BRANCH = "master"
    FILE_PATH = "q-fastapi.csv"
    FILE_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{FILE_PATH}"
    
    try:
        # Read the uploaded file
        file_content = await file.read()
        file_content_str = file_content.decode("utf-8")

        # Update the file in GitHub
        result = await update_github_file(file_content_str, FILE_PATH, REPO_OWNER, REPO_NAME, BRANCH, GITHUB_TOKEN)
        
        if result is True:
            return "https://q-fastapi.vercel.app/api"
        return result  # Return error if update fails
    
    except Exception as e:
        return {"error": f"Error processing file: {e}"}



async def q_docker_hub_image(question, GITHUB_TOKEN=None):
    import re
    # Extract email from the question
    # email_match = re.search(r"email\s+([\w.\-+@]+)", question, re.IGNORECASE)

    # Add a tag named miryala.narayanareddy to the image.

    tag_name = re.search(r"Add a tag named (.*) to the image", question, re.IGNORECASE)
    if not tag_name:
        return "Could not parse the question. Please ensure it follows the correct format."
    
    tag_name = tag_name.group(1)

    print(tag_name)


    yml_file = f"""name: Build and Push Docker Image with Tag

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  build_and_push:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Create a sample Dockerfile
      run: |
        echo "FROM alpine:3.17" > Dockerfile
        echo "CMD [\\\"echo\\\", \\\"Hello from a tagged Docker image!\\\"]" >> Dockerfile

    - name: Log in to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{{{ secrets.DOCKER_USERNAME }}}}
        password: ${{{{ secrets.DOCKER_PASSWORD }}}}

    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: narayanareddy123/sample-image:{tag_name}
"""

    # Define GitHub repository details and workflow file path
    USERNAME = "MiryalaNarayanaReddy"
    REPO_NAME = "tds-project-scheduled-workflow"
    WORKFLOW_PATH = ".github/workflows/docker-push.yml"
    
    # Update the workflow file in the repository and trigger the workflow
    await update_github_file(yml_file, WORKFLOW_PATH, USERNAME, REPO_NAME, "master", GITHUB_TOKEN)
    await trigger_github_workflow(USERNAME, REPO_NAME, "docker-push.yml", GITHUB_TOKEN, "master")
    
    # Construct and return the Docker image URL.
    # The URL follows the pattern: https://hub.docker.com/repository/docker/$USER/$REPO/general
    return f"https://hub.docker.com/repository/docker/narayanareddy123/sample-image/general"
