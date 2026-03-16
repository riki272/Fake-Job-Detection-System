import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = pickle.load(open(os.path.join(BASE_DIR,"model.pkl"),"rb"))
vectorizer = pickle.load(open(os.path.join(BASE_DIR,"vectorizer.pkl"),"rb"))

def predict_job(text):

    vec = vectorizer.transform([text])

    prediction = model.predict(vec)[0]
    probability = model.predict_proba(vec).max()

    if prediction == 1:
        result = "Fake Job"
    else:
        result = "Real Job"

    return result, probability