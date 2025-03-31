
import re
import requests
from bs4 import BeautifulSoup
import json


async def q_google_sheets_importhtml(question: str, file=None):
    # Extract the page number using regex
    match = re.search(r'page number (\d+)', question, re.IGNORECASE)
    if not match:
        raise ValueError("Page number not found in the question")
    
    page_number = match.group(1)
    url = f"https://stats.espncricinfo.com/stats/engine/stats/index.html?class=2;page={page_number};template=results;type=batting"
    
    # Set headers to mimic a real browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Fetch the page content
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    total_ducks = 0
    for table in soup.find_all('table'):
        rows = table.find_all('tr')
        if len(rows) >= 50:  # Assume this is the main data table
            headers = [th.text.strip() for th in table.find_all('thead')[0].find_all('th')]
            
            # Find the column index for "0" (Ducks)
            try:
                ducks_index = headers.index("0")
            except ValueError:
                continue
            
            for row in table.find_all('tbody')[0].find_all('tr'):
                cells = [td.text.strip() for td in row.find_all('td')]
                if len(cells) > ducks_index:
                    try:
                        total_ducks += int(cells[ducks_index])
                    except ValueError:
                        pass
    
    return total_ducks


async def q_scrape_imdb_movies(question: str, file=None):
     
    min_rating, max_rating = 6,8
    match = re.search(r'rating between (\d+) and (\d+)', question)
    if match:
        # int(match.group(1)), int(match.group(2))
        min_rating = int(match.group(1))
        max_rating = int(match.group(2))

    url = f"https://www.imdb.com/search/title/?user_rating={min_rating},{max_rating}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    movies = []
    for item in soup.select(".ipc-metadata-list-summary-item")[:25]:
        id_tag = item.select_one(".ipc-lockup-overlay")
        title_tag = item.select_one(".ipc-title")
        year_tag = item.select_one(".dli-title-metadata-item")
        rating_tag = item.select_one(".ipc-rating-star--rating")
        
        id_match = id_tag["href"].split("/title/")[1].split("/")[0] if id_tag and "href" in id_tag.attrs else None
        
        movies.append({
            "id": id_match,
            "title": title_tag.text if title_tag else None,
            "year": year_tag.text if year_tag else None,
            "rating": rating_tag.text if rating_tag else None
        })
    
    return json.dumps(movies, indent=4)


