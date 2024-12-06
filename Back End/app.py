from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from collections import Counter
import re
import plotly.express as px
import json
import pickle


app = Flask(__name__)

# Load Data and Model
data = pd.read_csv("C:/Users/Dell/OneDrive/Desktop/sem 3/NLP/ass-4/Sentiment_Data.csv", encoding='ISO-8859-1', nrows=10000)

model = load_model('C:/Users/Dell/OneDrive/Desktop/sem 3/deploymnet/Final Presentation/lstm_model.h5')
with open('C:/Users/Dell/OneDrive/Desktop/sem 3/deploymnet/Final Presentation/tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

# Preprocess Tweets
def clean_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = re.sub(r'\@\w+', '', text)
    text = re.sub(r'[^A-Za-z0-9\s#]', '', text)
    text = text.lower()
    return text

data['processed_text'] = data['Tweet'].apply(clean_text)

# Sentiment Analysis Function
def analyze_sentiment(filtered_tweets):
    if filtered_tweets.empty:
        return {}, "No tweets found for this hashtag."
    
    sequences = tokenizer.texts_to_sequences(filtered_tweets['processed_text'])
    padded_sequences = pad_sequences(sequences, maxlen=100, padding='post')
    predictions = model.predict(padded_sequences)
    sentiment_classes = np.argmax(predictions, axis=1)

    sentiment_mapping = {0: "Negative", 1: "Neutral", 2: "Positive"}
    risk_mapping = {"Negative": "High Risk", "Neutral": "Medium Risk", "Positive": "Low Risk"}
    sentiments = pd.Series(sentiment_classes).map(sentiment_mapping)
    risks = sentiments.map(risk_mapping).value_counts(normalize=True) * 100
    dominant_risk = risks.idxmax()
    return risks.to_dict(), dominant_risk

# Generate Hashtag Frequencies for Plotly
def generate_hashtag_wordcloud_data(filtered_tweets):
    hashtags = Counter(filtered_tweets['Tweet'].str.findall(r"#\w+").sum())
    hashtag_df = pd.DataFrame(hashtags.most_common(20), columns=["Hashtag", "Frequency"])
    return hashtag_df

@app.route("/", methods=["GET", "POST"])
def index():
    hashtag = request.form.get("hashtag")
    sentiment_summary = {}
    market_trend = None
    hashtag_wordcloud = None
    filtered_tweets = None

    if hashtag:
        filtered_tweets = data[data['Tweet'].str.contains(hashtag, case=False, na=False)]
        if not filtered_tweets.empty:
            sentiment_summary, market_trend = analyze_sentiment(filtered_tweets)
            hashtag_wordcloud = generate_hashtag_wordcloud_data(filtered_tweets)
    
    return render_template(
        "index.html",
        hashtag=hashtag,
        sentiment_summary=sentiment_summary,
        market_trend=market_trend,
        hashtag_wordcloud=hashtag_wordcloud.to_dict() if hashtag_wordcloud is not None else None,
        tweets=filtered_tweets['Tweet'].tolist() if filtered_tweets is not None else None
    )

if __name__ == "__main__":
    app.run(debug=True)
