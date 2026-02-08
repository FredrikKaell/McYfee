"""
#Module for sending notifications to Discord via webhook
"""

import requests
from typing import Optional
from webtracker.utils.logger import AppLogger

logger = AppLogger().get_logger()
class DiscordNotifier:
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, message: str, username: Optional[str] = "McYfee Bot"):

        payload = {
            "username": username,
            "content": message
        }

        try:
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info(f"Notifier sent message: {message}")
        except requests.RequestException as e:
            logger.error(f"Notifier error: {e}")

#TEST

#if __name__ == "__main__":

    #WEBHOOK_URL = "https://discord.com/api/webhooks/1466515978497036380/F8JwMrt75R1uCE5iXbsx74PW9lVYFu6pNlh7AAtdR7JEYGQKERdbAC4T3DmTRRe8fs6g"
    
    #notifier = DiscordNotifier(WEBHOOK_URL)
    #Test INFO-logg
    #notifier.send("Test message from McYfee again")
    #Test ERROR-logg
    #notifier_fail = DiscordNotifier("https://discord.com/api/Webhooks/wrong_url")
    #notifier_fail.send("Detta ska trigga error log")