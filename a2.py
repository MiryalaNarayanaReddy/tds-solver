import re

from assignment_codes.tds_2025_01_ga2 import q_markdown
from assignment_codes.tds_2025_01_ga2 import q_image_compression

from assignment_codes.tds_2025_01_ga2 import q_use_colab
from assignment_codes.tds_2025_01_ga2 import q_use_colab_image_library

from assignment_codes.tds_2025_01_ga2 import q_github_pages

class A2:
    def __init__(self):
        pass

    def process_question(self, question: str):
        """Map a question to its corresponding key using extended regex patterns."""
    
        patterns = {
                "q-docker-hub-image": r"(?:Docker\s+Hub.*image\s+URL|hub\.docker\.com/repository/docker/\w+/\w+/general)",
                "q-fastapi": r"(?:FastAPI\s+server\s+endpoint|http://127\.0\.0\.1:\d+/api)",
                "q-github-action": r"Create a GitHub action on one of your GitHub repositories",
                "q-github-pages": r"Publish a page using GitHub Pages that showcases your work. Ensure that your email address",
                "q-image-compression": r"Download the image below and compress it losslessly to an image that is",
                "q-llamafile": r"Download Llamafile | Run the Llama-3.2-1B-Instruct.Q6_K.llamafile model with it.",
                "q-markdown": r"(?:Write\s+documentation\s+in\s+Markdown)",
                "q-use-colab": r"(?:make sure you can access Google Colab|Run this program in Google Colab)",
                "q-use-colab-image-library": r"(?:Google\s+Colab\s+notebook.*number\s+of\s+pixels\s+with\s+lightness\s+>\s+0\.217)",
                "q-vercel-python": r"(?:Download\s+this\s+.*?\.json\s+which\s+has\s+the\s+marks\s+of\s+\d+\s+imaginary\s+students|Create\s+and\s+deploy\s+a\s+Python\s+app\s+to\s+Vercel)"
            }

        # Loop through the patterns and return the key of the first match
        for key, pattern in patterns.items():
            if re.search(pattern, question, re.IGNORECASE):
                return key
        return None
    
    async def solve(self,key,question,file=None,GITHUB_TOKEN=None):

        solver = {
            "q-markdown": q_markdown,
            "q-image-compression": q_image_compression,

            "q-github-pages": q_github_pages,

            "q-use-colab": q_use_colab,
            "q-use-colab-image-library": q_use_colab_image_library,
            
        }

        if key not in solver:
            # return "No such question"
            return key

        if key in ["q-github-pages"]:
            if key == "q-github-pages":
                return await solver[key](question, GITHUB_TOKEN)
        
        return await solver[key](question, file)

        
