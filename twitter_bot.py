import os
import tweepy
import logging
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Supabase configuration (optional, remove if not used)
# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Twitter API credentials
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# Authenticate with the Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

def log_to_supabase(action, status):  # (optional, remove if not used)
    # Supabase logging functionality (modify if needed)
    # data = {
    #     "timestamp": datetime.now().isoformat(),
    #     "action": action,
    #     "status": status
    # }
    # supabase.table("bot_logs").insert(data).execute()
    pass  # Placeholder for Supabase logging

def create_tweet(content):
    try:
        # Check tweet length (280 characters for text-only tweets)
        if len(content) <= 280:
            api.update_status(content)
            logging.info(f"Tweeted: {content}")
            log_to_supabase("create_tweet", f"Success: {content}")  # (optional)
        else:
            logging.error(f"Tweet content exceeds 280 characters.")
    except tweepy.TweepError as e:
        logging.error(f"Error creating tweet: {e.reason}")
        log_to_supabase("create_tweet", f"Error: {e.reason}")  # (optional)

def create_tweet_with_media(content, media_path):  # Add this function for media tweets
    try:
        # Check tweet length (261 characters for tweets with media)
        if len(content) <= 261:
            media = api.media_upload(media_path)
            api.update_status(status=content, media_ids=[media.media_id])
            logging.info(f"Tweeted with media: {content}")
            log_to_supabase("create_tweet_with_media", f"Success: {content}")  # (optional)
        else:
            logging.error(f"Tweet content with media exceeds 261 characters.")
    except tweepy.TweepError as e:
        logging.error(f"Error creating tweet with media: {e.reason}")
        log_to_supabase("create_tweet_with_media", f"Error: {e.reason}")  # (optional)

# Like and follow functions remain the same (optional)

def scheduled_tasks():
    create_tweet("Hello world! This is a bot tweet.")
    # like_tweets("#examplehashtag", 5)  # (optional)
    # follow_users("#examplehashtag", 5)  # (optional)

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(scheduled_tasks, 'interval', hours=1)

    try:
        logging.info("Starting bot...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")
