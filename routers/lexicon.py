from operator import lt
from fastapi import APIRouter, status, Query
import json

from models.data_clean import DataClean, DataCleanTortoise
from vaderSentimentEs import SentimentIntensityAnalyzer
from data_wrangling import clean_text

router = APIRouter()

# Routes 

@router.get("/chart_data")
async def get_chart_data():
    f = open ('data/lexicon.json', "r")
    data = json.loads(f.read())

    return data


@router.get("/evaluate")
async def evaluate_lexicon(query: str = Query(..., max_length=500)) -> DataClean:
    analyzer = SentimentIntensityAnalyzer()
    sentence: str = clean_text(query)
    result = analyzer.polarity_scores(sentence)
    tag = "neutral"
    if result['compound'] < -0.25 and result['compound'] >= -0.50:
        tag = "dissatisfied"
    if result['compound'] < -0.5:
        tag = "very_dissatisfied"
    if result['compound'] > 0.25 and result['compound'] <= 0.50:
        tag = "satisfied"
    if result['compound'] > 0.5:
        tag = "very_satisfied"

    return {"tag": tag, "rating": result["compound"]}
