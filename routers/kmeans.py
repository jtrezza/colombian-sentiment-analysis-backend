from operator import lt
from fastapi import APIRouter, HTTPException, status, Query
from fastapi.params import Depends
import json
import json
import numpy as np

from models.data_clean import DataClean, DataCleanTortoise
from vaderSentimentEs import SentimentIntensityAnalyzer
from data_wrangling import clean_text, replace_sentiment_words, lemmatize_tweet

f = open ('data/dictionary.json', "r")
sentiment_dict = json.loads(f.read())

router = APIRouter()

# Routes 

@router.get("/chart_data")
async def get_chart_data():
    f = open ('data/kmeans.json', "r")
    data = json.loads(f.read())

    return data


@router.get("/evaluate")
async def evaluate_lexicon(query: str = Query(..., max_length=500)):
    t = lemmatize_tweet(clean_text(query))
    sent_coef = [replace_sentiment_words(word, sentiment_dict) for word in t.split()]
    sentiment_rate = np.array(sent_coef).mean()

    tag = "neutral"
    if sentiment_rate < -0.25 and sentiment_rate >= -0.50:
        tag = "dissatisfied"
    if sentiment_rate < -0.5:
        tag = "very_dissatisfied"
    if sentiment_rate > 0.25 and sentiment_rate <= 0.50:
        tag = "satisfied"
    if sentiment_rate > 0.5:
        tag = "very_satisfied"

    return {"tag": tag, "rating": sentiment_rate}
