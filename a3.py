import re

from assignment_codes.tds_2025_01_ga3 import q_llm_sentiment_analysis

from assignment_codes.tds_2025_01_ga3 import q_llm_embeddings

from assignment_codes.tds_2025_01_ga3 import q_get_llm_to_say_yes

class A3:
    def __init__(self):
        pass

    def process_question(self, question: str):
        """Map a question to its corresponding key using extended regex patterns."""
    
        patterns = {
            "q-embedding-similarity": r"(?:text\s+embeddings\s+to\s+capture\s+the\s+semantic\s+meaning|calculate\s+the\s+cosine\s+similarity\s+between\s+each\s+pair)",
            "q-function-calling": r"(?:TechNova\s+Corp.*?digital\s+assistant|FastAPI\s+application.*?/execute\?q=)",
            "q-generate-addresses-with-llms": r"(?:RapidRoute\s+Solutions.*?language\s+model.*?standardized\s+U\.S\.\s+addresses|Generate\s+10\s+random\s+addresses\s+in\s+the\s+US)",
            "q-get-llm-to-say-yes": r"(?:SecurePrompt\s+Technologies.*?LLM.*?never\s+say\s+Yes|Write\s+a\s+prompt\s+that\s+will\s+get\s+the\s+LLM\s+to\s+say\s+Yes)",
            "q-llm-embeddings": r"(?:SecurePay\s+.*?detect\s+and\s+prevent\s+fraudulent\s+activities|convert\s+it\s+into\s+a\s+meaningful\s+embedding)",
            "q-llm-sentiment-analysis": r"(?:DataSentinel\s+Inc.*?NLP\s+solutions|analyze\s+the\s+sentiment\s+of\s+this\s+.*?text\s+into\s+GOOD,\s+BAD\s+or\s+NEUTRAL)",
            "q-llm-vision": r"(?:Acme\s+Global\s+Solutions.*?automated\s+document\s+processing|Extract\s+text\s+from\s+this\s+image)",
            "q-token-cost": r"(?:LexiSolve\s+Inc.*?token\s+usage|how\s+many\s+input\s+tokens\s+does\s+it\s+use\s+up\?)",
            "q-vector-databases": r"(?:InfoCore\s+Solutions.*?semantic\s+search|text\s+embeddings\s+to\s+capture\s+the\s+contextual\s+meaning)",
        }

        # Loop through the patterns and return the key of the first match
        for key, pattern in patterns.items():
            if re.search(pattern, question, re.IGNORECASE):
                return key
        return None
    
    async def solve(self,key,question,file=None,GITHUB_TOKEN=None):

        solver = {
            "q-llm-sentiment-analysis": q_llm_sentiment_analysis,

            "q-llm-embeddings": q_llm_embeddings,

            "q-get-llm-to-say-yes": q_get_llm_to_say_yes,

        }

        if key not in solver:
            # return "No such question"
            return key

        # if key in ["q-github-pages"]:
        #     if key == "q-github-pages":
        #         return await solver[key](question, GITHUB_TOKEN)
    
        return await solver[key](question, file)

        
