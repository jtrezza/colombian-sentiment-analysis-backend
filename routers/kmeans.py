from operator import lt
from fastapi import APIRouter, Query
import json
import json
import numpy as np
from gensim.models import Word2Vec
import pickle

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

w2v_model = Word2Vec.load("ml_models/word2vec_kmeans.model")
word_vectors = w2v_model.wv.vectors
model = pickle.load(open('ml_models/model_kmeans.sav', 'rb'))

def text_to_list(str):
    """Converts a string to a list of words"""
    return str.split()

def get_array(word):
        try:
            out = w2v_model.wv[word]
        except KeyError:
            out = []
        return out

def get_avg_vector(phrase):
    array_of_arrays = [get_array(word)for word in phrase]
    arr_filtered = [arr for arr in array_of_arrays if len(arr) > 0]
    return np.mean( np.array(arr_filtered), axis=0 )

@router.get("/evaluate")
async def evaluate_lexicon(query: str = Query(..., max_length=500)):
    t = lemmatize_tweet(clean_text(query))
    avg_v = get_avg_vector(text_to_list(t))
    try:
        prediction = model.predict(avg_v.reshape(1,-1))
    except:
        return {"tag": 'neu'}
    return {"tag": 'pos'} if prediction == 0 else {"tag": 'neg'}
