# pylint: disable=missing-module-docstring
import os
import time

from discord_webhook import DiscordWebhook, DiscordEmbed

class DiscordBot:
    """A class to interact with the Discord bot"""

    def __init__(self):
        webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
        self.webhook = DiscordWebhook(url=webhook_url)

    def post_message(self, title, description, img_url, movie_id):
        """Post a message in the channel with the webhook """
        self.webhook.rate_limit_retry = True

        embed = DiscordEmbed(
            title=title,
            color="32a852",
            timestamp=int(time.time()),
            fields=[
                {
                    "name": "Theaters",
                    "value": description,
                    "inline": False,
                }
            ],
            url=f"https://www.ugc.fr/film.html?id={movie_id}",
            author={
                "name": "UGC Bot",
                "icon_url": "https://ugcdistribution.fr/wp-content/themes/bbxdesert/images/logo-ugc.png",
                "url": "https://www.ugc.fr",
            },
        )
        embed.set_image(url=img_url)
        self.webhook.add_embed(embed)

        self.webhook.execute(remove_embeds=True)

    def post_message_poster(self, movie_title: str, img_url: str, is_new: bool, is_available: bool):
        """Post a status update for a given poster in the channel"""
        self.webhook.rate_limit_retry = True
        
        match (is_new, is_available):
            case (True, True):
                end_desc = "est maintenant disponible!"
                color = "0de023"
            case (False, True):
                end_desc = "est de nouveau en stock!"
                color = "11a4ed"
            case (True, False):
                end_desc = "est listé dans le catalogue cadeaux mais n'est pas encore disponible."
                color = "ed8611"
            case (False, False):
                end_desc = "n'est plus disponible à l'achat."
                color = "e02d2d"
        
        embed = DiscordEmbed(
            title="UPDATE POSTER",
            color=color,
            timestamp=int(time.time()),
            fields= [{
                "name": "",
                "value": f"Le poster du film {movie_title} {end_desc}",
                "inline": False
            }],
            author={
                "name": "UGC Fidélité",
                "icon_url": "https://fidelite.ugc.fr/assets/img/logo-fidelite.png",
                "url": "https://fidelite.ugc.fr"
            }
        )
        embed.set_image(url = img_url)
        
        self.webhook.add_embed(embed)
        self.webhook.execute(remove_embeds=True)