from operator import lt
from fastapi import APIRouter, status, Query
import json
import pickle

from models.data_clean import DataClean, DataCleanTortoise
from vaderSentimentEs import SentimentIntensityAnalyzer
from data_wrangling import clean_text

router = APIRouter()

# Routes 

@router.get("/chart_data")
async def get_chart_data():
    f = open ('data/svm.json', "r")
    data = json.loads(f.read())

    return data

vectorizer = pickle.load(open('ml_models/vectorizer_svm.sav', 'rb'))
model = pickle.load(open('ml_models/model_svm.sav', 'rb'))

def classify(text):
    vectors = vectorizer.transform([text])
    return model.predict(vectors)[0]

@router.get("/evaluate")
async def evaluate_lexicon(query: str = Query(..., max_length=500)) -> DataClean:
    sentence: str = clean_text(query)
    tag = classify(sentence)

    return {"tag": tag}
