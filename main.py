import os
import pathlib
import json
from dotenv import load_dotenv

from src.ugc_posters import get_all_posters
from src.discord_bot import DiscordBot

# Loading environment variables #
if pathlib.Path("/.dockerenv").exists():
    print("Running in Docker")
    os.chdir("/app")
    load_dotenv("/app/.env")
else:
    print("Running locally")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(".env")

if __name__ == "__main__":
    discord_bot = DiscordBot()
    
    # Creates empty JSON file to compare to if this is the first check #
    if not pathlib.Path(".previous_posters.json").is_file():
        with open(".previous_posters.json", "w+") as f_out:
            json.dump({}, f_out)
    
    # Loading previous data for future comparison #
    with open(".previous_posters.json", "r") as f_in:
        previous_posters = json.load(f_in)
    
    (images, current_posters) = get_all_posters()
    
    # Comparing previous and current data; sending Discord message if differences are found #
    for movie_title, is_currently_available in current_posters.items():
        if movie_title not in previous_posters:
            discord_bot.post_message_poster(movie_title, images[movie_title], True, is_currently_available)
        elif is_currently_available != previous_posters[movie_title]:
            discord_bot.post_message_poster(movie_title, images[movie_title], False, is_currently_available)
    
    # Overwriting with current data for next check #
    with open(".previous_posters.json", "w") as f_out:
        json.dump(current_posters, f_out)