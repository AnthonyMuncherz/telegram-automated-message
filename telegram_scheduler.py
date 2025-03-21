#!/usr/bin/env python3
import os
import time
import logging
import schedule
from telethon.sync import TelegramClient
from telethon.errors import FloodWaitError, RPCError
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Telegram API credentials
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')
RECIPIENT = os.getenv('RECIPIENT')  # Username, phone number, or chat ID
MESSAGE = os.getenv('MESSAGE', 'This is an automated message sent every 12 hours.')

# Check required environment variables
if not API_ID or not API_HASH:
    logger.error("API_ID and API_HASH are required! Get them from https://my.telegram.org")
    exit(1)

if not PHONE_NUMBER:
    logger.error("PHONE_NUMBER is required to authenticate your account!")
    exit(1)

if not RECIPIENT:
    logger.error("RECIPIENT is required! This can be a username, phone number, or chat ID.")
    exit(1)

# Create a Telegram client session file path
SESSION_FILE = "telegram_session"

def send_message():
    """Send a message to the specified recipient using your personal Telegram account."""
    try:
        client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
        client.connect()
        
        # If not authorized, prompt for authorization code
        if not client.is_user_authorized():
            logger.info("First time setup: sending authorization code to your phone number...")
            client.send_code_request(PHONE_NUMBER)
            logger.info("Please check your Telegram app for the authorization code and enter it in the console.")
            client.sign_in(PHONE_NUMBER, input('Enter the code: '))
        
        # Send the message
        entity = RECIPIENT
        sent_message = client.send_message(entity, MESSAGE)
        
        logger.info(f"Message sent successfully to {RECIPIENT}")
        
        client.disconnect()
        return True
        
    except FloodWaitError as e:
        # Handle flood wait error - Telegram API limitation
        wait_time = e.seconds
        logger.error(f"Flood wait error: Need to wait {wait_time} seconds before sending another message.")
        time.sleep(wait_time)  # Wait the required time before retrying
        return False
        
    except RPCError as e:
        logger.error(f"Telegram RPC error: {e}")
        return False
        
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        return False

def main():
    logger.info("Telegram scheduler started using personal account")
    
    # Schedule the message to be sent every 12 hours
    schedule.every(12).hours.do(send_message)
    
    # Send a message immediately on startup
    logger.info("Sending initial message...")
    send_message()
    
    # Keep the script running and check for scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main() 