import json 
import re 
import requests

import base64
import os


async def q_llm_sentiment_analysis(question, file=None):
    return "import httpx\nimport json\n\n# Define API endpoint and headers\nurl = \"https://api.openai.com/v1/chat/completions\"\nheaders = {\n    \"Content-Type\": \"application/json\",\n    \"Authorization\": \"Bearer MY_DUMMY_API_KEY\"\n}\n\n# Define request payload\npayload = {\n    \"model\": \"gpt-4o-mini\",\n    \"messages\": [\n        {\n            \"role\": \"system\",\n            \"content\": \"You are an expert at analyzing sentiment. Classify the given text as GOOD, BAD, or NEUTRAL.\"\n        },\n        {\n            \"role\": \"user\",\n            \"content\": \"1NhNEU MqYTv eZfRSVkm4mOqnX   pjAneE69  3d6bOmGcr6\"\n        }\n    ]\n}\n\n# Make the API request\nresponse = httpx.post(url, json=payload, headers=headers)\n\n# Raise an error if the request fails\nresponse.raise_for_status()\n\n# Parse and print the response\nprint(response.json())\n"

async def q_get_llm_to_say_yes(question, file=None):
    return " def IntegrateChunks():     x=  {         \"name\": \"llms_ay_yes\",         \"description\": \"Generate a yes or no answer based on the LLMs\",         \"parameters\": {             \"type\": \"object\",             \"properties\": {                 \"question\": {                     \"type\": \"string\",                     \"description\": \"The question to ask the LLMs\"                 }             },             \"required\": [\"question\"],             \"additionalProperties\": False         },         \"response\": {             \"type\": \"object\",             \"properties\": {                 \"answer\": {                     \"type\": \"string\",                     \"description\": \"The answer to the question\"                     }                     },                     \"required\": [\"answer\"],                     \"additionalProperties\": False                 }     }      s = \"Yq-llms-ay-yes\"     t = \"LLMs: Yes or No\"     y =  {\"name\": 's', \"description\": t, \"parameters\": x, \"response\": x}      return  s[0] + t[7] + y[\"name\"]; what does the above funciton reutrn "

async def q_embedding_similarity(question, file=None):
    return "import numpy as np\n\ndef most_similar(embeddings):\n    # Your code here\n    d = 0  # Initialize with a large value\n\n    keys = list(embeddings.keys())\n\n    phrase1 = \"\"\n    phrase2 = \"\"\n\n    for i in range(0, len(keys)):\n        for j in range(i + 1, len(keys)):\n            a = embeddings[keys[i]]\n            b = embeddings[keys[j]]\n            # Cosine similarity formula\n            dist = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))\n\n            # Update the smallest distance\n            if dist > d:\n                d = dist\n                phrase1 = keys[i]\n                phrase2 = keys[j]\n    return (phrase1, phrase2)\n"

async def q_llm_embeddings(question, file=None):
    print(question)
    # Extract all transaction messages from the input text
    pattern = r"Dear user, please verify your transaction code \d+ sent to (?:[\w.\-]+\s*)+@(?:[\w.\-]+\s*)+\.\w+"

    matches = re.findall(pattern, question)

    payload = {
        "model": "text-embedding-3-small",
        "input": matches
    }
    
    return json.dumps(payload, indent=4)

async def q_generate_addresses_with_llms(question, file=None):
    reference_schema = {
        "street": "string",
        "city": "string",
        "state": "string",
        "zip": "number",
        "apartment": "string",
        "county": "string",
        "country": "string",
        "latitude": "number",
        "longitude": "number"
    }

    # Extract required fields from the input text
    pattern = r"\b(\w+)\s*\(\s*(string|number)\s*\)"
    matches = re.findall(pattern, question)

    # Ensure extracted fields exist in reference schema
    extracted_properties = {
        key: {"type": value} for key, value in matches if key in reference_schema and reference_schema[key] == value
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Respond in JSON"},
            {"role": "user", "content": "Generate 10 random addresses in the US"}
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "math_response",  # Corrected name
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "addresses": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": extracted_properties,
                                "required": list(extracted_properties.keys()),
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["addresses"],
                    "additionalProperties": False
                }
            }
        }
    }
    
    return json.dumps(payload, indent=2)  # Ensure direct JSON output


async def q_token_cost(question, LLM_TOKEN=None):
    # "List only the valid English words from these: eede, nVxt, dUu, dLGDietCB, gNhZf1rp, 2UD, slvTrzZ, RVub8q0C7, 6d0t, S4dr, Ea63pC8, 4AxYPKwDR, VDeNXdkR, ZP9Uo"
    pattern = r"user message\s*:\s*(.*?)(?=\s*\.\.\.)"
    match = re.search(pattern, question, re.DOTALL)

    text_content=""

    if match:
        text_content = match.group(1)
    
    response = requests.post(
        "https://llmfoundry.straive.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {LLM_TOKEN}:tds-solver"},
        json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": text_content}]}
    )

    r = response.json()

    # prompt tokens 
    prompt_tokens = r["usage"]["prompt_tokens"]

    return prompt_tokens


def encode_image(image_path):
    """Encodes an image as Base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def q_llm_vision(question, file=None):
    temp_file_path = "/tmp/uploaded_image"

    # Save the uploaded file content to the /tmp folder
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(await file.read())

    # Encode the saved image as Base64
    base64_image = encode_image(temp_file_path)

    # Determine content type based on filename or extension
    content_type = getattr(file, "content_type", "image/png")  # Default to 'image/png'
    if content_type== None:
        content_type = "image/png"
    # Construct the data URL for the image
    data_url = f"data:{content_type};base64,{base64_image}"

    # Construct the JSON body with the correct structure
    json_body = f"""{{
  "model": "gpt-4o-mini",
  "messages": [
    {{
      "role": "user",
      "content": [
        {{"type": "text", "text": "Extract text from this image"}},
        {{
          "type": "image_url",
          "image_url": {{ "url": "{data_url}" }}
        }}
      ]
    }}
  ]
}}
"""
    
    """
    # Set up the headers with content type and authorization
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LLM_TOKEN}"
    }

    # Make a synchronous POST request to the API using requests
    response = requests.post(
        url="https://llmfoundry.straive.com/openai/v1/chat/completions",
        json=json_body,
        headers=headers,
        verify=False  # Disable SSL verification (not recommended for production)
    )

    # Raise an exception for non-200 responses
    response.raise_for_status()

 
    # Return the API's GPT response as JSON
    return response.json()
    """
   # Clean up: remove the temporary file after use
    os.remove(temp_file_path)
 
    return json_body
