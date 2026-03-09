import pickle
import re

model = pickle.load(open("model.pkl","rb"))
vectorizer = pickle.load(open("vectorizer.pkl","rb"))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]',' ',text)
    return text

def predict_job(text):

    cleaned = clean_text(text)

    vector = vectorizer.transform([cleaned])

    prediction = model.predict(vector)[0]

    probability = model.predict_proba(vector)[0][1]

    if prediction == 1:
        result = "Fake Job"
    else:
        result = "Real Job"

    return result, probability


def detect_suspicious_words(text):

    keywords = [
        "quick money",
        "earn fast",
        "no experience",
        "work from home",
        "instant hiring",
        "easy money"
    ]

    found = []

    for word in keywords:
        if word in text.lower():
            found.append(word)

    return found
