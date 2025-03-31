import re

from  assignment_codes.tds_2025_01_ga5 import q_clean_up_excel_sales_data
from assignment_codes.tds_2025_01_ga5 import q_clean_up_student_marks
from assignment_codes.tds_2025_01_ga5 import q_apache_log_requests

class A5:
    def __init__(self):
        pass

    def process_question(self, question: str):
        """Map a question to its corresponding key using extended regex patterns."""
    
        patterns = {
            "q-apache-log-downloads": r"(?:total\s+number\s+of\s+bytes\s+that\s+this\s+IP\s+address\s+downloaded|how\s+many\s+bytes\s+did\s+the\s+top\s+IP\s+address\s+download\?)",
            "q-apache-log-requests": r"What is the number of successful GET requests for pages under",
            "q-clean-up-excel-sales-data": r"(?:clean\s+this\s+Excel\s+data\s+and\s+calculate\s+the\s+total\s+margin|transactions\s+before\s+Tue\s+Aug\s+15\s+2023\s+10:22:08\s+GMT\+0530\s+for\s+Alpha\s+sold\s+in\s+UK)",
            "q-clean-up-sales-data": r"(?:units\s+of\s+Sausages\s+were\s+sold\s+in\s+Shenzhen|transactions\s+with\s+at\s+least\s+23\s+units\?)",
            "q-clean-up-student-marks": r"(?:adherence\s+to\s+regulatory\s+requirements\s+by\s+maintaining\s+precise\s+student\s+records|How\s+many\s+unique\s+students\s+are\s+there\s+in\s+the\s+file\?)",
            "q-duckdb-social-media-interactions": r"(?:DuckDB\s+SQL\s+query\s+to\s+find\s+all\s+post\s+IDs\s+after\s+2024-12-24T18:30:10.418Z|at\s+least\s+1\s+comment\s+with\s+2\s+useful\s+stars)",
            "q-extract-nested-json-keys": r"(?:data-driven\s+insights\s+that\s+support\s+strategic\s+planning|How\s+many\s+times\s+does\s+IZ\s+appear\s+as\s+a\s+key\?)",
            "q-image-jigsaw": r"(?:Upload\s+the\s+reconstructed\s+image|moving\s+the\s+pieces\s+from\s+the\s+scrambled\s+position\s+to\s+the\s+original\s+position)",
            "q-parse-partial-json": r"(?:provided\s+JSON\s+data\s+contains\s+100\s+rows|total\s+sales\s+value\?)",
            "q-transcribe-youtube": r"(?:text\s+of\s+the\s+transcript\s+of\s+this\s+Mystery\s+Story\s+Audiobook|between\s+288.4\s+and\s+383.4\s+seconds)"
        }

        # Loop through the patterns and return the key of the first match
        for key, pattern in patterns.items():
            if re.search(pattern, question, re.IGNORECASE):
                return key
        return None
    
    async def solve(self,key,question,file=None,GITHUB_TOKEN=None):

        solver = {
            "q-clean-up-excel-sales-data": q_clean_up_excel_sales_data,
            "q-clean-up-student-marks": q_clean_up_student_marks,
            # "q-apache-log-requests": q_apache_log_requests,
        }

        if key not in solver:
            # return "No such question"
            return key

        # if key in ["q-github-pages"]:
        #     if key == "q-github-pages":
        #         return await solver[key](question, GITHUB_TOKEN)
    
        return await solver[key](question, file)

        
