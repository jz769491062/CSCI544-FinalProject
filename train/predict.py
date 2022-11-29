from sklearn.linear_model import LogisticRegression
import json
import pickle
import numpy as np
import pandas as pd
import re
import nltk
import contractions
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stopWords = stopwords.words('english')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
### A list of dirty words
dirtyWordFile = pd.read_csv('../CommonCode/scratch/profanity_words.csv', error_bad_lines='skip')
workaroundDirtyWords = dirtyWordFile['text'].values.tolist()
canonicalDirtyWords = dirtyWordFile['canonical_form_1'].values.tolist()
# a dictionary that maps workaround dirty words to canonical forms, later substitute these words
dirtyDict = {}
dirtyDict = {workaroundDirtyWords[i]: canonicalDirtyWords[i] for i in range(len(workaroundDirtyWords))}

def PreProcessOneMessage(s):
    # to lower cases
    s = re.sub('[A-Z]', '[a-z]', s)
    # remove numerical characters
    s = re.sub('[0-9]', '', s)
    # remove unicode characters
    s = s.encode("ascii", "ignore").decode()
    # remove punctuations
    # not removing : for it's a emoji pattern we are about to handle in the loop
    # not removing _ for it relates to emoji patterns
    s = re.sub('[,.?!@#*/~`$%^&()<>-+=;\'\"]', '', s)
    slist = s.split()
    newstr = ""
    for i in slist:
        # order of if matters
        # substitute workaround profane words with canonical forms
        if i in dirtyDict:
            i = dirtyDict[i]
        # remove emoji words in format of ":smiling_face_with_smiling_eyes:"
        if i[0] != ':':
            newstr += i
            newstr += " "
    # remove contractions
    newstr = contractions.fix(newstr)

    #remove stop words
    retOneSentence = ""
    # tokenize
    wordTokens = word_tokenize(newstr)
    for w in wordTokens:
        if w not in stopWords:
            # only keep non-stopword words
            retOneSentence += w + " "
    # remove tail space
    tempStr = retOneSentence[:-1]
    # lemmatization
    resultMessage = lemmatizer.lemmatize(tempStr)
    return resultMessage

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
