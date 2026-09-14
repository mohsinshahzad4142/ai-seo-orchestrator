import os
import aiohttp
from typing import Dict, Any, Optional
from models.phase7_models import NotificationChannel


class NotificationService:
    def __init__(self):
        self.slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
        self.telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    async def send_slack_notification(self, message: str) -> bool:
        if not self.slack_webhook:
            return False
        async with aiohttp.ClientSession() as session:
            payload = {"text": f"🚨 *AI SEO Orchestrator Alert*\n{message}"}
            async with session.post(self.slack_webhook, json=payload) as resp:
                return resp.status == 200

    async def send_telegram_notification(self, message: str) -> bool:
        if not self.telegram_bot_token or not self.telegram_chat_id:
            return False
        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        payload = {"chat_id": self.telegram_chat_id, "text": message, "parse_mode": "Markdown"}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                return resp.status == 200

    async def notify(self, channel: NotificationChannel, recipient: str, message: str) -> bool:
        if channel == NotificationChannel.SLACK:
            return await self.send_slack_notification(message)
        elif channel == NotificationChannel.TELEGRAM:
            return await self.send_telegram_notification(message)
        elif channel == NotificationChannel.EMAIL:
            return True
        return False
