import re
import requests
import json

from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import xml.etree.ElementTree as ET

from assignment_codes.helper import update_github_file,trigger_github_workflow

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


async def q_wikipedia_outline(question: str, file=None):
    
    base_url = "https://tds-solver-sigma.vercel.app"
    return f"{base_url}/q-wikipedia-outline"


async def q_bbc_weather_api(question: str, file=None):
    # Use regex to extract the city name.
    # This regex looks for 'weather forecast for' followed by a city name (letters and spaces)
    match = re.search(r"weather forecast for\s+([A-Za-z\s]+)", question, re.IGNORECASE)
    if not match:
        return json.dumps({"error": "City not found in the input text."})
    
    city = match.group(1).strip()
    
    # Retrieve the location ID using the BBC locator service.
    locator_params = {
        "api_key": "AGbFAKx58hyjQScCXIYrxuEwJh2W2cmv",
        "stack": "aws",
        "locale": "en",
        "filter": "international",
        "place-types": "settlement,airport,district",
        "order": "importance",
        "s": city,
        "a": "true",
        "format": "json"
    }
    locator_url = "https://locator-service.api.bbci.co.uk/locations"
    locator_response = requests.get(locator_url, params=locator_params, verify=False)
    locator_data = locator_response.json()
    
    # Extract the first matching location's ID.
    try:
        location_id = locator_data["response"]["results"]["results"][0]["id"]
    except (KeyError, IndexError):
        return json.dumps({"error": f"Location ID for city '{city}' could not be found."})
    
    # Fetch the weather forecast for the given location.
    forecast_url = f"https://weather-broker-cdn.api.bbci.co.uk/en/forecast/aggregated/{location_id}"
    forecast_response = requests.get(forecast_url, verify=False)
    forecast_data = forecast_response.json()
    
    # Build a dictionary mapping each date to its enhanced weather description.
    forecast = {
        entry["summary"]["report"]["localDate"]: entry["summary"]["report"]["enhancedWeatherDescription"]
        for entry in forecast_data.get("forecasts", [])
    }
    
    # Return the result as a JSON-formatted string.
    return forecast



async def q_nominatim_api(question: str, file=None):
    """
    Extracts variables from a templated question and returns the corresponding
    latitude value from the bounding box via the Nominatim API.
    
    The expected question format is:
    "What is the <measurement> of the bounding box of the city <city> in the country <country> on the Nominatim API?"
    
    Where <measurement> is either "minimum latitude" or "maximum latitude".
    """
    # Regular expression to extract the measurement, city, and country
    pattern = r"What is the (.+?) of the bounding box of the city (.+?) in the country (.+?) on the Nominatim API\?"
    match = re.search(pattern, question, re.IGNORECASE)
    
    if not match:
        raise ValueError("Could not parse the question. Please ensure it follows the correct format.")
    
    measurement = match.group(1).strip().lower()  # e.g., "minimum latitude"
    city = match.group(2).strip()                   # e.g., "Chongqing"
    country = match.group(3).strip()                # e.g., "China"
    
    # Initialize the geolocator with a custom user agent
    geolocator = Nominatim(user_agent="my_geocoder")
    
    # Combine city and country for the search query
    query = f"{city}, {country}"
    # Get all candidates by setting exactly_one=False
    locations = geolocator.geocode(query, exactly_one=False)
    
    if not locations:
        raise ValueError(f"Location not found for city '{city}' in country '{country}'.")
    
    # Filter candidates if possible: here we look for results that likely represent a city.
    # Some results have a 'type' or 'class' field in the raw dict.
    filtered_locations = [
        loc for loc in locations 
        if "city" in (loc.raw.get("type") or "").lower() or "city" in (loc.raw.get("class") or "").lower()
    ]
    
    # If filtering yields no result, fall back to all candidates
    if not filtered_locations:
        filtered_locations = locations
    
    # Sort the results by their "importance" field (if available), descending.
    # Not all results might have the "importance" field, so we default to 0.
    filtered_locations.sort(key=lambda loc: float(loc.raw.get("importance", 0)), reverse=True)
    
    best_candidate = filtered_locations[0]
    
    # Extract the bounding box. Expected format: [min_lat, max_lat, min_lon, max_lon]
    bounding_box = best_candidate.raw.get("boundingbox")
    if not bounding_box or len(bounding_box) < 2:
        raise ValueError("Bounding box information is incomplete or missing from the API response.")
    
    # Determine which value to return based on the measurement
    if measurement == "minimum latitude":
        result = float(bounding_box[0])
    elif measurement == "maximum latitude":
        result = float(bounding_box[1])
    else:
        raise ValueError("Measurement must be either 'minimum latitude' or 'maximum latitude'.")
    
    # return {
    #     "city": city,
    #     "country": country,
    #     "measurement": measurement,
    #     "bounding_box": bounding_box,
    #     "result": result,
    #     "osm_id": best_candidate.raw.get("osm_id")
    # }

    return result


async def q_hacker_news_search(question, file=None):
    """
    Extracts search parameters from the question and searches the Hacker News RSS feed
    for the latest post mentioning the given topic with at least the specified points.
    """
    # Regular expression to extract topic and minimum points
    pattern = r"What is the link to the latest Hacker News post mentioning (.+?) having at least (\d+) points"
    match = re.search(pattern, question, re.IGNORECASE)
    
    if not match:
        raise ValueError("Could not parse the question. Please ensure it follows the correct format.")
    
    topic = match.group(1).strip()
    min_points = match.group(2).strip()
    
    # Define the HNRSS API URL with search query and minimum points filter
    url = f"https://hnrss.org/newest?q={topic.replace(' ', '%20')}&points={min_points}"
    
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch Hacker News: {response.status_code} {response.reason}")
    
    # Parse the XML response
    root = ET.fromstring(response.text)
    
    # Extract the latest <item> mentioning the topic
    for item in root.findall(".//item"):
        title = item.find("title").text if item.find("title") is not None else ""
        link = item.find("link").text if item.find("link") is not None else ""
        
        # Ensure the topic is mentioned in the title
        if re.search(rf'\b{re.escape(topic)}\b', title, re.IGNORECASE):
            return link  # Return only the URL as required

    return "No matching post found"



async def q_find_newest_github_user(question, GITHUB_TOKEN=None):

    # Define search parameters
    # location = "Chicago"
    # min_followers = 80

    # find all users located in the city Chicago with over 80 followers.

    pattern = r"find all users located in the city (.+?) with over (\d+) followers"
    match = re.search(pattern, question, re.IGNORECASE)
    
    if not match:
        raise ValueError("Could not parse the question. Please ensure it follows the correct format.")
    
    location = match.group(1).strip()
    min_followers = match.group(2).strip()

    # GitHub API URL for searching users
    search_url = f"https://api.github.com/search/users?q=location:{location}+followers:>={min_followers}&sort=joined&order=desc"

    # Headers with authentication
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # Fetch the list of users
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        users = response.json().get("items", [])
        
        if users:
            # Get the most recently joined user's profile
            newest_user_url = users[0]['url']  # API URL for the first user in sorted results
            user_response = requests.get(newest_user_url, headers=headers)
            
            if user_response.status_code == 200:
                created_at = user_response.json().get("created_at")
                # print(f"Newest user joined on: {created_at}")  # Print account creation date
                return created_at
            else:
                print(f"Failed to fetch user details: {user_response.status_code} {user_response.reason}")
        else:
            print("No users found matching criteria.")
    else:
        print(f"Failed to fetch data: {response.status_code} {response.reason}")


async def q_scheduled_github_actions(question, GITHUB_TOKEN=None):

    email_match = re.search(r"email\s+([\w.\-+@]+)", question, re.IGNORECASE)
    email = email_match.group(1) if email_match else "default@example.com"
    print(email)
    # email = "miryala@straive.com"
    yml_file = f"""name: Daily Commit

on:
  push:
    branches:
      - main
  schedule:
    - cron: '30 18 * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  commit:
    runs-on: ubuntu-latest

    steps:
    - name: {email}
      run: |
        echo "Hello, world!"
    - name: Checkout repository
      uses: actions/checkout@v2
      with:
        token: ${{{{ secrets.GITHUB_TOKEN }}}}

    - name: Set up Git
      run: |
        git config --global user.name "GitHub Actions"
        git config --global user.email "{email}"

    - name: Create a commit
      run: |
        echo "Daily update: $(date)" >> daily_commit.txt
        git add daily_commit.txt
        git commit -m "Daily commit by GitHub Actions"
        git push
"""
    
    USERNAME = "MiryalaNarayanaReddy"
    REPO_NAME = "tds-project-scheduled-workflow"
    WORKFLOW_PATH = ".github/workflows/8.yml"
    
    await update_github_file(yml_file, WORKFLOW_PATH, USERNAME, REPO_NAME, "master", GITHUB_TOKEN)
    await trigger_github_workflow(USERNAME, REPO_NAME, "8.yml", GITHUB_TOKEN,"master")
    
    return f"https://github.com/{USERNAME}/{REPO_NAME}"
