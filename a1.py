import re

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
            "q-count-wednesdays": r"(?:Wednesdays?|Count\s+Wednesdays)",
            "q-extract-csv-zip": r"(?:extract\.csv|csv\s+file)",
            "q-use-json": r"(?:Sort\s+this\s+JSON\s+array)",
            "q-multi-cursor-json": r"(?:multi[-\s]?cursor).*(?:json)",
            "q-css-selectors": r"(?:CSS\s+selectors|select\s+elements\s+using\s+CSS)",
            "q-unicode-data": r"(?:unicode.*data|files\s+in\s+.*zip)",
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