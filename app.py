from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os 

import requests
import lxml.html # install lxml using pip install lxml

from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

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
from a2 import A2
from a3 import A3
from a4 import A4
from a5 import A5

assignments = {
    "a1": A1(),
    "a2": A2(),
    "a3": A3(),
    "a4": A4(),
    "a5": A5(),
}

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub token with repo access


async def process_request(question: str, file: Optional[UploadFile] = File(None)):
    
    for assignment in assignments.values():

        key = assignment.process_question(question)

        if key:
            answer = await assignment.solve(key, question, file, GITHUB_TOKEN)
            return answer
        else: 
            continue
    
    return "No such question"


@app.post("/api")
async def api_root(
    question: str = Form(...), 
    file: Optional[UploadFile] = File(None)
):
    answer = await process_request(question, file)

    if answer:
        if isinstance(answer, int) or isinstance(answer, float):
            return {"answer": str(answer)}
        else:
            return {"answer": answer}
    else:
        print("No response found")
        return {"error": "No response found"}

@app.get("/")
async def root():
    return  {"message": "API is running"}


@app.get("/q-wikipedia-outline")
async def root(country: str):
    # get wikipedia page
    WIKI_URL = f"https://en.wikipedia.org/wiki/{country}"
    # response = httpx.get(WIKI_URL)

    response = requests.get(WIKI_URL,verify=False)

    # extract h1 to h6 tags
    tree = lxml.html.fromstring(response.content)
    h_tags = tree.xpath("//h1|//h2|//h3|//h4|//h5|//h6")

    # create markdown list 
    # h1: #, h2: ##, h3: ###, h4: ####, h5: #####, h6: ######
    # markdown_list = "\n".join([f"{i.tag}: {i.text}" for i in h_tags])
    # return {"message": markdown_list}

    # create markdown outline
    '''
    # <h1 text>
    ## <h2 text>
    ### <h3 text>
    # <h1 text> 
    '''

    markdown_outline = "" 
    for i in h_tags:
        if i.tag == "h1":
            markdown_outline += f"# {i.text}\n"
        elif i.tag == "h2":
            markdown_outline += f"## {i.text}\n"
        elif i.tag == "h3":
            markdown_outline += f"### {i.text}\n"
        elif i.tag == "h4":
            markdown_outline += f"#### {i.text}\n"
        elif i.tag == "h5":
            markdown_outline += f"##### {i.text}\n"
        elif i.tag == "h6":
            markdown_outline += f"###### {i.text}\n"
        
    return markdown_outline


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
