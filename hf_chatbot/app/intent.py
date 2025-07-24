import joblib
import os
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import nltk



# Download necessary NLTK data
# nltk.download('punkt')
# nltk.download("punkt_tab")
# nltk.download('wordnet')
# nltk.download('stopwords')
# nltk.download('omw-1.4')

from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")
emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=False)


INTENT_MODEL_PATH = "app/models/intent_model.pkl"
VECTORIZER_PATH = "app/models/vectorizer.pkl"

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

sample_intents = {
    "greeting": ["hello", "hi", "hey", "good morning", "good evening"],
    "weather": ["what's the weather", "weather forecast", "is it raining"],
    "time": ["what time is it", "tell me the time", "current time"],
    "date": ["what's the date", "today's date", "which day is today"],
    "Greeting": ["hi","bye", "see you", "goodbye"],
    "AI": [
    "AI",
    "What is AI?",
    "Tell me about supervised learning",
    "What is unsupervised learning?",
    "Explain RAG",
    "How does fine tuning work?",
    "Can you explain fine tuning?"
]
}

def preprocess(text):
    # Lowercase and tokenize
    tokens = word_tokenize(text.lower())

    # Remove punctuation, stopwords, and lemmatize
    cleaned_tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
        if word not in string.punctuation and word not in stop_words
    ]

    return " ".join(cleaned_tokens)

def train_intent_classifier():
    if not os.path.exists("app/models"):
        os.makedirs("app/models")

    texts = []
    labels = []

    for intent, phrases in sample_intents.items():
        for phrase in phrases:
            texts.append(preprocess(phrase))
            labels.append(intent)

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts)

    clf = LogisticRegression()
    clf.fit(X, labels)

    joblib.dump(clf, INTENT_MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print(f"✅ Intent classifier trained with {len(labels)} samples. Accuracy: {clf.score(X, labels):.2f}")

def detect_intent(text):
    if not os.path.exists(INTENT_MODEL_PATH):
        train_intent_classifier()

    clf = joblib.load(INTENT_MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    processed_text = preprocess(text)
    X = vectorizer.transform([processed_text])
    return clf.predict(X)[0]

def analyze_user_input(user_input):
    try:
        sentiment_result = sentiment_pipeline(user_input)
        sentiment = sentiment_result[0]['label'] if sentiment_result else "unknown"
    except Exception as e:
        sentiment = "unknown"
        print(f"Sentiment analysis error: {e}")
        
    try:
        emotion_result = emotion_pipeline(user_input)
        if isinstance(emotion_result, list) and len(emotion_result) > 0 and 'label' in emotion_result[0]:
            emotion = emotion_result[0]['label']
        else:
            emotion = "unknown"
    except Exception as e:
        emotion = "unknown"
        print(f"Emotion detection error: {e}")
        
    return sentiment.lower(), emotion.lower()