import requests 
from urllib.parse import quote_plus

def link_youtube(title, artist):
    query = f"{title} {artist} official music video"
    url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
    response = requests.get(url)

    if response.status_code == 200:
        video = None
        start_index = response.text.find('{"videoRenderer":{"videoId":"')
        
        if start_index != -1:
            end_index = response.text.find('"', start_index + 30)
            video = response.text[start_index + 29:end_index]
        if video:
            return f"https://www.youtube.com/watch?v={video}"
    return None