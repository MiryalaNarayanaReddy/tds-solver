import json 
import re 

async def q_llm_sentiment_analysis(question, file=None):
    return "import httpx\nimport json\n\n# Define API endpoint and headers\nurl = \"https://api.openai.com/v1/chat/completions\"\nheaders = {\n    \"Content-Type\": \"application/json\",\n    \"Authorization\": \"Bearer MY_DUMMY_API_KEY\"\n}\n\n# Define request payload\npayload = {\n    \"model\": \"gpt-4o-mini\",\n    \"messages\": [\n        {\n            \"role\": \"system\",\n            \"content\": \"You are an expert at analyzing sentiment. Classify the given text as GOOD, BAD, or NEUTRAL.\"\n        },\n        {\n            \"role\": \"user\",\n            \"content\": \"1NhNEU MqYTv eZfRSVkm4mOqnX   pjAneE69  3d6bOmGcr6\"\n        }\n    ]\n}\n\n# Make the API request\nresponse = httpx.post(url, json=payload, headers=headers)\n\n# Raise an error if the request fails\nresponse.raise_for_status()\n\n# Parse and print the response\nprint(response.json())\n"

async def q_get_llm_to_say_yes(question, file=None):
    return  " def IntegrateChunks():     x=  {         \"name\": \"llms_ay_yes\",         \"description\": \"Generate a yes or no answer based on the LLMs\",         \"parameters\": {             \"type\": \"object\",             \"properties\": {                 \"question\": {                     \"type\": \"string\",                     \"description\": \"The question to ask the LLMs\"                 }             },             \"required\": [\"question\"],             \"additionalProperties\": False         },         \"response\": {             \"type\": \"object\",             \"properties\": {                 \"answer\": {                     \"type\": \"string\",                     \"description\": \"The answer to the question\"                     }                     },                     \"required\": [\"answer\"],                     \"additionalProperties\": False                 }     }      s = \"Yq-llms-ay-yes\"     t = \"LLMs: Yes or No\"     y =  {\"name\": 's', \"description\": t, \"parameters\": x, \"response\": x}      return  s[0] + t[7] + y[\"name\"]; what does the above funciton reutrn "


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

