import os
import praw
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sys

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

load_dotenv()

reddit_client_id = os.environ.get('REDDIT_CLIENT_ID')
reddit_client_secret = os.environ.get('REDDIT_CLIENT_SECRET')
reddit_user_agent = os.environ.get('REDDIT_USER_AGENT')

if not all([reddit_client_id, reddit_client_secret, reddit_user_agent]):
    raise ValueError("One or more required environment variables are missing.")

# Initialize Reddit instance
reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent=reddit_user_agent,
)

def analyze_sentiment(comment_text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(comment_text)['compound']

    if sentiment_score >= 0.05:
        return 'positive'
    elif sentiment_score <= -0.05:
        return 'negative'
    else:
        return 'neutral'

def main():
    
    post_id = '1baaigq'
    submission = reddit.submission(id=post_id)

    for comment in submission.comments.list():
        if hasattr(comment, 'body'):
            sentiment = analyze_sentiment(comment.body)
            print(f"Comment: {comment.body}\nSentiment: {sentiment}\n{'='*30}")

if __name__ == "__main__":
    main()
