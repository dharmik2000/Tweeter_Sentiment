#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tweepy
import json
import pandas as pd


# In[3]:


# Step 1: Twitter API credentials (replace these with your actual keys)
consumer_key = 'xbc9jL5u3bkhQitwR3jgMT8VP'
consumer_secret = 'dJKXwSkygjHXdjdnx8FQaLZQsIAeYScaym5U6zoELDCp5yM3bD'
access_token = '1847149597900132352-7w9QCnbXvfFziGd7FYZrHNLVVrAwQp'
access_token_secret = 'y7foAgPoBhEyyvuYAwLYnrNvjMLA7aVoGg30N8cpmyOz5'


# In[4]:


# Step 2: Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)


# In[5]:


# Step 3: Function to scrape tweets
def scrape_tweets(hashtag, count=100):
    tweets = tweepy.Cursor(api.search_tweets, q=hashtag, lang="en").items(count)
    tweet_list = [[tweet.created_at, tweet.user.screen_name, tweet.text] for tweet in tweets]
    df = pd.DataFrame(tweet_list, columns=['Timestamp', 'Username', 'Tweet'])
    return df


# In[ ]:


# Step 4: Example usage - scrape 100 tweets with #example
df = scrape_tweets("#example", 100)


# In[ ]:


# Step 5: Save the tweets to a CSV file
df.to_csv('tweets.csv', index=False)
print("Tweets saved to tweets.csv")


# Sentiment Analysis Using VADER

# In[ ]:


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd


# In[ ]:


# Step 1: Load the scraped tweets
df = pd.read_csv('tweets.csv')


# In[ ]:


# Step 2: Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()


# In[ ]:


# Step 3: Function to analyze sentiment
def analyze_sentiment(text):
    sentiment_dict = analyzer.polarity_scores(text)
    if sentiment_dict['compound'] >= 0.05:
        return 'Positive'
    elif sentiment_dict['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'


# In[ ]:


# Step 4: Apply sentiment analysis on each tweet
df['Sentiment'] = df['Tweet'].apply(analyze_sentiment)


# In[ ]:


# Step 5: Save the results with sentiment labels
df.to_csv('tweets_with_sentiment.csv', index=False)
print("Tweets with sentiment saved to tweets_with_sentiment.csv")


#  MySQL Database Integration

# In[ ]:


import mysql.connector
import pandas as pd


# In[ ]:


# Step 1: Connect to MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_password',
    database='your_database'
)


# In[ ]:


cursor = conn.cursor()


# In[ ]:


# Step 2: Create a table for storing tweets and sentiment
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        username VARCHAR(255),
        tweet TEXT,
        sentiment VARCHAR(50)
    )
''')


# In[ ]:


# Step 3: Load the tweet data
df = pd.read_csv('tweets_with_sentiment.csv')


# In[ ]:


# Step 4: Insert tweet data into the database
for _, row in df.iterrows():
    cursor.execute('''
        INSERT INTO tweets (timestamp, username, tweet, sentiment)
        VALUES (%s, %s, %s, %s)
    ''', (row['Timestamp'], row['Username'], row['Tweet'], row['Sentiment']))


# In[ ]:


# Step 5: Commit and close the connection
conn.commit()
cursor.close()
conn.close()
print("Data inserted into MySQL database")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




