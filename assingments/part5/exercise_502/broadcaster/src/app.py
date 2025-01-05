import nats
import requests
import os
import json
import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# Environment variables
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", None)
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", None)
NATS_ENDPOINT = os.environ.get("NATS_ENDPOINT", "nats://my-nats:4222")
FORWARD_TO_EXTERNAL_SERVICE = os.environ.get(
    "FORWARD_TO_EXTERNAL_SERVICE", False)

# Telegram sendMessage URL
TELEGRAM_API_URL = (
    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
)


async def process_message(msg):
    """
    Process incoming messages from NATS and send them to Telegram.
    """
    try:
        # Decode and parse the message
        data = json.loads(msg.data.decode())

        # Format the message text
        message_text = (
            f"Todo {data['description']}\n"
            f"Done: {data['done']}"
        )

        # Prepare the payload for Telegram
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message_text
        }

        # Log messages
        logger.info(payload)

        if FORWARD_TO_EXTERNAL_SERVICE:
            # Send the message to Telegram
            response = requests.post(TELEGRAM_API_URL, json=payload)

            if response.status_code == 200:
                print("Message sent successfully to Telegram!")
            else:
                print(f"Failed to send message to Telegram: {response.text}")

    except Exception as e:
        print(f"Error processing message: {e}")


async def main():
    """
    Main function to connect to NATS and subscribe to the topic.
    """
    try:
        # Connect to NATS
        client = await nats.connect(NATS_ENDPOINT)
        print("Connected to NATS.")

        # Subscribe to the topic
        await client.subscribe("todos.status", cb=process_message)
        print("Subscribed to 'todos.status'.")

    except Exception as e:
        print(f"Error connecting to NATS: {e}")

if __name__ == "__main__":
    asyncio.run(main())
