import requests 
import re
from urllib.parse import quote_plus

def link_youtube(title, artist):
    query = f"{title} {artist} official music video"
    url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
    response = requests.get(url)

    if response.status_code == 200:
        match = re.search(r'{"videoRenderer":{"videoId":"([^"]+)"', response.text)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/watch?v={video_id}"
    return None