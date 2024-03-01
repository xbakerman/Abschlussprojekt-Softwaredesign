from duckduckgo_search import DDGS

def get_album_cover(title, interpret):    
    keywords = f"{title}{interpret} Albumcover"

    #Albumcover in DuckDuckGo suchen
    with DDGS() as ddgs:
        ddgs_images_gen = ddgs.images(
            keywords,
            region="wt-wt",
            safesearch="off",
            size=None,
            color=None,
            type_image=None,
            layout=None,
            license_image=None,
            max_results=1, 
        )
        
        for result in ddgs_images_gen:
            return result['image']
        
        return None