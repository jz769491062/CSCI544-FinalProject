import sys
import pandas as pd
import numpy as np
get_ipython().system('{sys.executable} -m pip install contractions')
import contractions
import re
import nltk
import sklearn
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
nltk.download('omw-1.4')
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

### Usage: ipython .\preproctemp.py

# Real csv name in dataset: 0a633aa33731985aa52985e79bb12f38b95b9404_0.csv
# drop invalid and empty rows
df = pd.read_csv('tempdata.csv', on_bad_lines='skip')
df = df.dropna()

df_messages = df['Message']
# df_messages = df[df['Message'].map(lambda x: x.isascii())]
# print(df.info()) 

### A list of swearing words
#TODO: Do we use predefined profane words to start labeling some sentences in advance?
# Or just keep it in the training and testing stage instead?
dirtyWordFile = pd.read_csv('profanity_en.csv', on_bad_lines='skip')
workaroundDirtyWords = dirtyWordFile['text'].values.tolist()
canonicalDirtyWords = dirtyWordFile['canonical_form_1'].values.tolist()
# a dictionary that maps workaround dirty words to canonical forms, later substitute these words
dirtyDict = {}
dirtyDict = {workaroundDirtyWords[i]: canonicalDirtyWords[i] for i in range(len(workaroundDirtyWords))}
# TODO: handle dirty words with spaces? like "s h i t"

# average length of reviews before cleaning
means = [df_messages.apply(len).mean()]
msgLengthBeforeCleaning = sum(means) / len(means)

### Data Cleaning
# TODO: how to handle non-English messages? For now ignore them.

def MyClean(myDf):
    # to lower cases, keep alphabets only, remove extra whitespaces
    myDf = myDf.replace('[^a-zA-Z]', '')
    myDf = myDf.replace(' +', ' ')
    myProcStr = myDf.str.lower()
    ret = []
    for s in myProcStr:
        # remove unicode characters
        s = s.encode("ascii", "ignore").decode()
        # remove numeric characters
        s = re.sub('[0-9]', '', s)
        slist = s.split()
        newstr = ""
        for i in slist:
            # order of if matters
            # substitute workaround profane words with canonical forms
            if i in dirtyDict:
                #print("before " + i)
                i = dirtyDict[i]
                #print("after " + i)
            # remove emoji words in format of ":smiling_face_with_smiling_eyes:"
            if i[0] != ':':
                newstr += i
                newstr += " "
        # remove contractions
        newstr = contractions.fix(newstr)
        ret.append(newstr)
    return ret

cleanedMessages = MyClean(df_messages)

tmp = [len(e) for e in cleanedMessages]
# average length of reviews after cleaning(and before preprocessing)
msgLengthAfterCleaning = float(sum(tmp)) / len(tmp)
print("Message Length After Cleaning: " + str(msgLengthBeforeCleaning) + "," + str(msgLengthAfterCleaning))

### Remove Stop Words, Perform Lemmatization
stopWords = stopwords.words('english')

def RemoveStopWords(ss):
    ret = []
    for s in ss:
        retOneSentence = []
        # tokenize
        wordTokens = word_tokenize(s)
        for w in wordTokens:
            if w not in stopWords:
                # only keep non-stopword words
                retOneSentence.append(w)
        ret.append(retOneSentence)
    return ret

cleanedMessages = RemoveStopWords(cleanedMessages)

### perform lemmatization  
lemmatizer = WordNetLemmatizer()
# tmp and tmpCnt used for calculating char length of lemmatized reviews
tmp = []
# stemming and lemmatization of words
def LemmWords(sss):
    ret = []
    for ss in sss:
        retOneSentence = []
        tmpCnt = 0
        for s in ss:
            tempStr = lemmatizer.lemmatize(s)
            tmpCnt += len(tempStr)
            retOneSentence.append(tempStr)
        tmp.append(tmpCnt)
        ret.append(retOneSentence)
    return ret

cleanedMessages = LemmWords(cleanedMessages)

msgLengthAfterPreproc = float(sum(tmp)) / len(tmp)
# reviews after cleaning == reviews before preprocessing
# TODO: word size reduced by ~40% after lemmatization, may be too much?
print("Message Length After Lemmatization: " + str(msgLengthAfterCleaning) + "," + str(msgLengthAfterPreproc))

#print(cleanedMessages)