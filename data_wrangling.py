from re import sub
from unidecode import unidecode
import nltk
import spacy

from nltk.corpus import stopwords
nltk.download('stopwords')

#initializing stopwords and spacy
stop_words = stopwords.words("spanish")
nlp = spacy.load("es_core_news_sm")

def replace_sentiment_words(word, sentiment_dict):
    '''
    replacing each word with its associated sentiment score from sentiment dict
    '''
    try:
        out = sentiment_dict[word]
    except KeyError:
        out = 0
    return out

def lemmatize_tweet(tweet):
    '''
    Lemmatizes and removes stop words from tweet
    '''
    tokens = nlp(tweet)
    tweet = " ".join([token.lemma_ for token in tokens])
    tweet = " ".join([word for word in tweet.split() if word not in stop_words])

    return tweet

#Cleaning the dataset
def clean_text(text: str) -> str:
    ''' Code adapted from https://github.com/rafaljanwojcik/Unsupervised-Sentiment-Analysis/blob/master/preprocessing_and_embeddings/Preprocessing_and_Embeddings.ipynb'''
    # Remove Spanish accents
    text = unidecode(text)
    text = str(text)
    text = text.lower()

    # Remove usernames
    text = sub('@[A-Za-z0-9_]+',' ',text)
    # Remove URLs
    text = sub('http://\S+|https://\S+', '', text)
    # Remove special characters
    text = sub(r"[^A-Za-z0-9^!?\/\\+]", " ", text)
    # Replace + sign by "mas" word
    text = sub(r"\+", " mas ", text)
    # Considering exclamation a separate word
    text = sub(r"!", " ! ", text)
    # Considering question mark a separate word
    text = sub(r"\?", " ? ", text)
    # Considering colon a separate word
    text = sub(r":", " : ", text)

    text = text.split()
    text = " ".join(text)

    return text
