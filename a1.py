import re
from assignment_codes.tds_2025_01_ga1 import q_vs_code_version
from assignment_codes.tds_2025_01_ga1 import q_uv_http_get
from assignment_codes.tds_2025_01_ga1 import q_npx_prettier
from assignment_codes.tds_2025_01_ga1 import q_use_google_sheets
from assignment_codes.tds_2025_01_ga1 import q_use_excel

from assignment_codes.tds_2025_01_ga1 import count_week_days
from assignment_codes.tds_2025_01_ga1 import q_extract_csv_zip

from assignment_codes.tds_2025_01_ga1 import q_use_json
from assignment_codes.tds_2025_01_ga1 import q_multi_cursor_json
from assignment_codes.tds_2025_01_ga1 import q_unicode_data
from assignment_codes.tds_2025_01_ga1 import q_replace_across_files

from assignment_codes.tds_2025_01_ga1 import q_move_rename_files
from assignment_codes.tds_2025_01_ga1 import q_compare_files

from assignment_codes.tds_2025_01_ga1 import q_list_files_attributes
from assignment_codes.tds_2025_01_ga1 import q_sql_ticket_sales


class A1:
    def __init__(self):
        pass

    def process_question(self, question: str):
        """Map a question to its corresponding key using extended regex patterns."""
        patterns = {
    
            "q-vs-code-version": r"(?:code\s*-s|Visual\s+Studio\s+Code\s)",
            "q-uv-http-get": r"email\s*set\s*to\s*([\w\.\@\-\+]+)",
            "q-npx-prettier": r"(?:npx\s+.*prettier)",
            "q-use-google-sheets": r"(?:Google\s+Sheets|SUM\s*\(ARRAY_CONSTRAIN)",
            "q-use-excel": r"(?:Type\s+this\s+formula\s+into\s+Excel)",
            "q-use-devtools": r"(?:hidden\s+input|secret\s+value)",
            "q-count-wednesdays": r"How many (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)s are there in the date range (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})",
            "q-extract-csv-zip": r"(?:q-extract-csv-zip.*\.zip|extract\.csv\s+file)",
            "q-use-json": r"(?:Sort\s+this\s+JSON\s+array)",
            "q-multi-cursor-json": r"(?:multi[-\s]?cursor).*(?:json)",
            "q-css-selectors": r"(?:CSS\s+selectors|select\s+elements\s+using\s+CSS)",
           "q-unicode-data": r"(?:q-unicode-data.*\.zip|unicode.*files\s+with\s+different\s+encodings)",
            "q-use-github": r"(?:GitHub|commit\s+email\.json)",
            "q-replace-across-files": r"(?:replace\s+all\s+\"IITM\"|IITM\s+with\s+\"IIT Madras\")",
            "q-list-files-attributes": r"(?:ls\s+.*\s+list\s+all\s+files)",
            "q-move-rename-files": r"(?:move|rename).*(?:files)",
            "q-compare-files": r"(?:q-compare-files|compare\s+files)",
            "q-sql-ticket-sales": r"(?:tickets\s+table|SQL\s+query)",
        }
        # Loop through the patterns and return the key of the first match
        for key, pattern in patterns.items():
            if re.search(pattern, question, re.IGNORECASE):
                return key
        return None
    
    async def solve(self,key,question,file=None):

        solver = {
            "q-vs-code-version": q_vs_code_version,
            "q-uv-http-get": q_uv_http_get,
            "q-npx-prettier": q_npx_prettier,
            "q-use-google-sheets": q_use_google_sheets,
            "q-use-excel": q_use_excel,

            "q-count-wednesdays": count_week_days,
            "q-extract-csv-zip": q_extract_csv_zip,

            "q-use-json": q_use_json,

            "q-multi-cursor-json": q_multi_cursor_json,
            "q-unicode-data": q_unicode_data,

            "q-replace-across-files": q_replace_across_files,

            "q-move-rename-files": q_move_rename_files,
            "q-compare-files": q_compare_files, 
            "q-list-files-attributes": q_list_files_attributes,
            "q-sql-ticket-sales": q_sql_ticket_sales,

        }

        if key not in solver:
            return "No such question"
        
        print(key)
        
        return await solver[key](question,file)

        
