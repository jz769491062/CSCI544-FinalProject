from sklearn.linear_model import LogisticRegression
import json
import pickle
import numpy as np

#input: A string of sentence to evaluate its level of profanity
#output: a numerical value between 0 and 1 inclusive representing the confidence of profanity
def predict(sentence):

    #load vocab set
    uniqueWords = dict()
    with open("vocab.txt", "r") as f:
        uniqueWords = json.loads(f.read())
    
    #load trained model
    logModel = pickle.load(open("model.pkl", "rb"))

    features = []
    feature = np.array(np.zeros(len(uniqueWords)))
    for w in sentence.split(" "):
        if w in uniqueWords:
            feature[uniqueWords[w]] += 1
    features.append(feature)
    
    result = logModel.predict_proba(features)
    return result[0][1]
