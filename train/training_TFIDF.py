import pandas as pd
import os
import re
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


dfs = list()
for filename in os.listdir("osf_labelled_data/"):
    with open(os.path.join("osf_labelled_data", filename), 'r') as f:
        data = pd.read_csv(f)
        dfs.append(data)
        
df = pd.concat(dfs, ignore_index=True)
df = df[['Message', 'Sentiment']]

def PreProcessOneMessage(s):
    # remove unicode characters
    s = s.encode("ascii", "ignore").decode()
    # remove punctuations
    # not removing : for it's a emoji pattern we are about to handle in the loop
    # not removing _ for it relates to emoji patterns
    s = re.sub('[,.?!@#*/~`$%^&()<>\-+=;\'\"]', '', s)
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

# Preprocess training data
for index, row in df.iterrows():
    if index % 10000 == 0:
        print("Preprocession process: {}".format(index))
    df.loc[index, 'Message'] = PreProcessOneMessage(row['Message'])

# Set Threshold 0.6
for index, row in df.iterrows():
    if row['Sentiment'] > 0.6:
        df.loc[index, 'Sentiment'] = 1
    else:
        df.loc[index, 'Sentiment'] = 0

# TF_IDF
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
vectorizer.fit(df['Message'])

# Split training dataset
from sklearn.model_selection import train_test_split 
X_train, X_test, y_train, y_test = train_test_split(df['Message'], df['Sentiment'], test_size=0.2)

# Logistic regression model fit and prediction
from sklearn.linear_model import LogisticRegression
model_LR = LogisticRegression()
model_LR.fit(vectorizer.transform(X_train), y_train)

y_pred = model_LR.predict(vectorizer.transform(X_test))

# Simple evaluation
count = 0
for index, i in enumerate(y_test):
    if i != y_pred[index]:
        count = count + 1
print(count / len(y_pred))