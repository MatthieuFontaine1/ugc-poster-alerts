import requests
from bs4 import BeautifulSoup

from src.exceptions import RequestFailedException

def get_all_posters():
    """Get info on all posters displayed on the UGC Fidelity Program
    
    Returns:
        dict: Dictionary containing the pictures of all posters
        dict: Dictionary containing the availability of all posters
    """
    req = requests.get("https://fidelite.ugc.fr", timeout = 10)
    
    if req.status_code != 200:
        raise RequestFailedException(f"Request failed with status code {req.status_code}")

    soup = BeautifulSoup(req.text, "html.parser")
    
    images = {}
    availabilities = {}
    for item in soup.find_all("div", {"class":"catalog-list-item"}):
        tag_img = item.findChild("img", recursive = True)
        
        if "affiche" in tag_img["alt"]:
            movie_name = tag_img["alt"].split("film ")[1]
            movie_pic = tag_img["src"]
            
            button_sold_out = item.findChild("a", {"class":"disabled"}, recursive = True)
            is_poster_available = (button_sold_out == None)
            
            images[movie_name] = movie_pic
            availabilities[movie_name] = is_poster_available
    
    return (images, availabilities)