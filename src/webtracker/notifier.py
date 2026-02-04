"""
#Module for sending notifications to Discord via webhook
"""

import requests

from typing import Optional

#Sends messages to a Discord channel via webhook.

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
        except requests.RequestException as e:
            print(f"Notifier error: {e}")

#TEST

#if __name__ == "__main__":

    #WEBHOOK_URL = "https://discord.com/api/webhooks/1466515978497036380/F8JwMrt75R1uCE5iXbsx74PW9lVYFu6pNlh7AAtdR7JEYGQKERdbAC4T3DmTRRe8fs6g"
    
    #notifier = DiscordNotifier(WEBHOOK_URL)
    #notifier.send("Test message from McYfee")