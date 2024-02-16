import os
import pathlib
import json
#from dotenv import load_dotenv

from src.ugc_posters import get_all_posters
from src.discord_bot import DiscordBot

if not pathlib.Path(".previous_posters.json").exists():
    with open(".previous_posters.json", "w") as f_out:
        json.dump({}, f_out)

##### METTRE CHECK DOCKER ICI

if __name__ == "__main__":
    discord_bot = DiscordBot()
    
    with open(".previous_posters.json", "r") as f_in:
        previous_posters = json.load(f_in)
    
    (images, current_posters) = get_all_posters()
    
    for movie_title in current_posters:
        if movie_title not in previous_posters.keys():
            discord_bot.post_message_poster(movie_title, images[movie_title], True, current_posters[movie_title])
        elif current_posters[movie_title] != previous_posters[movie_title]:
            discord_bot.post_message_poster(movie_title, images[movie_title], False, current_posters[movie_title])
    
    with open(".previous_posters.json", "w") as f_out:
        json.dump(current_posters, f_out)