import re

from assignment_codes.tds_2025_01_ga4 import q_google_sheets_importhtml
from assignment_codes.tds_2025_01_ga4 import q_scrape_imdb_movies
from assignment_codes.tds_2025_01_ga4 import q_wikipedia_outline
from assignment_codes.tds_2025_01_ga4 import q_bbc_weather_api
from assignment_codes.tds_2025_01_ga4 import q_nominatim_api
from assignment_codes.tds_2025_01_ga4 import q_hacker_news_search   
from assignment_codes.tds_2025_01_ga4 import q_find_newest_github_user
from assignment_codes.tds_2025_01_ga4 import q_scheduled_github_actions

class A4:
    def __init__(self):
        pass

    def process_question(self, question: str):
        """Map a question to its corresponding key using extended regex patterns."""
    
        patterns = {
            "q-google-sheets-importhtml": r"(?:total\s+number\s+of\s+ducks\s+across\s+players)",
            "q-bbc-weather-api": r"(?:JSON\s+weather\s+forecast\s+description|Kuwait\s+City)",
            "q-extract-tables-from-pdf": r"(?:total\s+English\s+marks\s+of\s+students|scored\s+48\s+or\s+more\s+marks\s+in\s+Biology)",
            "q-find-newest-github-user": r"(?:newest\s+user\s+joined\s+GitHub|ISO\s+8601\s+date\s+format)",
            "q-hacker-news-search": r"(?:latest\s+Hacker\s+News\s+post\s+mentioning\s+Hacker\s+Culture|at\s+least\s+82\s+points)",
            "q-nominatim-api": r"(?:minimum\s+latitude\s+of\s+the\s+bounding\s+box|city\s+Chongqing\s+in\s+the\s+country\s+China)",
            "q-pdf-to-markdown": r"(?:markdown\s+content\s+of\s+the\s+PDF|formatted\s+with\s+prettier@3\.4\.2)",
            "q-scheduled-github-actions": r"(?:Trigger\s+the\s+workflow\s+and\s+wait\s+for\s+it\s+to\s+complete|repository\s+URL\s+format:\s+https://github\.com/USER/REPO)",
            "q-scrape-imdb-movies": r"(?:StreamFlix's\s+data\s+analytics\s+team\s+requires\s+an\s+automated\s+solution|Extract\s+Data:\s+Retrieve\s+movie\s+information\s+from\s+IMDb)",
            "q-wikipedia-outline": r"(?:GlobalEdu\s+Platforms\s+seeks\s+to\s+integrate\s+comprehensive\s+country\s+information|fetch\s+the\s+corresponding\s+Wikipedia\s+page\s+for\s+that\s+country)",
        }


        # Loop through the patterns and return the key of the first match
        for key, pattern in patterns.items():
            if re.search(pattern, question, re.IGNORECASE):
                return key
        return None
    
    async def solve(self,key,question,file=None,GITHUB_TOKEN=None):

        solver = {
            "q-google-sheets-importhtml": q_google_sheets_importhtml,
            "q-scrape-imdb-movies": q_scrape_imdb_movies,
            "q-wikipedia-outline": q_wikipedia_outline,
            "q-bbc-weather-api": q_bbc_weather_api,
            "q-nominatim-api": q_nominatim_api,
            "q-hacker-news-search": q_hacker_news_search,
            "q-find-newest-github-user": q_find_newest_github_user,
            "q-scheduled-github-actions": q_scheduled_github_actions,
           
        }

        if key not in solver:
            # return "No such question"
            return key


        if key in ["q-find-newest-github-user","q-scheduled-github-actions"]:
                return await solver[key](question, GITHUB_TOKEN)
    
        return await solver[key](question, file)
