from datetime import datetime, timezone
import time
import typing
import requests
from enum import Enum
from loguru import logger

from src import env


class EmbedColor(Enum):
    GREEN = 0x69ff7e
    RED = 0xff8080


class DiscordWebhookUtils:
    @staticmethod
    def __make_request(json: typing.Any) -> None:
        if not env.get_webhook_url():
            return

        while True:
            response = requests.post(env.get_webhook_url(), json=json)
            if response.status_code == 204:
                logger.trace("Discord webhook sent successfully")
                return
            elif response.status_code == 429:
                data: dict = response.json()
                retry_after_seconds: float = data.get("retry_after", 1)
                logger.warning(f"Discord webhook rate limited. Retrying after {round(retry_after_seconds, 2)}s")
                time.sleep(retry_after_seconds)
                continue
            else:
                logger.error(f"Failed to send discord webhook: {response.status_code} - {response.text}")
                return


    @staticmethod
    def send_webhook_embed(embed_color: EmbedColor, title: str, description: str = "", content: str = "", fields: list[dict[str, str | bool]] = []) -> None:
        if not env.get_webhook_url():
            return

        embed: dict[str, typing.Any] = {
            "title": title,
            "description": description,
            "fields": fields,
            "color": embed_color.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        data = {
            "content": content,
            "embeds": [embed],
        }

        DiscordWebhookUtils.__make_request(json=data)


    @staticmethod
    def send_webhook_message(content: str) -> None:
        if not env.get_webhook_url():
            return

        data = {
            "content": content,
        }

        DiscordWebhookUtils.__make_request(json=data)
