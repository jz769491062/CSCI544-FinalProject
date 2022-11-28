import sys
import os
import glob
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

### Usage: ipython .\preprocess.py

### A list of dirty words
dirtyWordFile = pd.read_csv('./scratch/profanity_words.csv', on_bad_lines='skip')
workaroundDirtyWords = dirtyWordFile['text'].values.tolist()
canonicalDirtyWords = dirtyWordFile['canonical_form_1'].values.tolist()
# a dictionary that maps workaround dirty words to canonical forms, later substitute these words
dirtyDict = {}
dirtyDict = {workaroundDirtyWords[i]: canonicalDirtyWords[i] for i in range(len(workaroundDirtyWords))}

### Data Cleaning
def MyClean(myDf):
    # borrowed from Haocong's create_dataset.py
    myDf = myDf.str.replace('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', regex=True)
    myDf = myDf.str.replace('biblethump', ' ')
    myDf = myDf.str.replace('feelsstrongman', ' ')
    # myDf = myDf.str.replace('[^a-zA-Z0-9\']', ' ', regex=True)
    myDf = myDf.str.replace('\?+', '?', regex=True)
    myDf = myDf.str.replace('<3', '', regex=True)
    myDf = myDf.str.replace('\s+', ' ', regex=True)
    myProcStr = myDf.str.lower()
    ret = []
    for s in myProcStr:
        # remove unicode characters
        s = s.encode("ascii", "ignore").decode()
        # remove numeric characters. May hurt profanity detection so not removing for now
        s = re.sub('[0-9]', '', s)
        # remove punctuations
        # not removing : for it's a emoji pattern we are about to handle in the loop
        # not removing _ for it relates to emoji patterns
        s = re.sub('[@#*,.?!/~`$%^&()-+=;\'\"]', '', s)
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
        ret.append(newstr)
    return ret

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

### perform lemmatization  
lemmatizer = WordNetLemmatizer()
# stemming and lemmatization of words
def LemmWords(sss):
    ret = []
    for ss in sss:
        retOneSentence = []
        for s in ss:
            tempStr = WordNetLemmatizer().lemmatize(s)
            retOneSentence.append(tempStr)
        ret.append(retOneSentence)
    return ret

def PreProcessOneFile(fileStr, columnStr):
    df = pd.read_csv(fileStr, on_bad_lines='skip')
    df = df.dropna()
    df_messages = df[columnStr]
    cleanedMessages = MyClean(df_messages)
    cleanedMessages = RemoveStopWords(cleanedMessages)
    cleanedMessages = LemmWords(cleanedMessages)
    outFileName = "preprocoutput.txt"
    outFile = open(outFileName, "w", encoding='UTF-8')
    outFile.write("")
    outFile.close()
    outFile = open(outFileName, "a", encoding='UTF-8')
    for line in cleanedMessages:
        tempstr = ""
        for wordIdx in range(len(line)):
            tempstr += line[wordIdx]
            if wordIdx != (len(line) - 1):
                tempstr += " "
        tempstr += "\n"
        if tempstr != "\n":
            outFile.write(tempstr)
    outFile.close()

# PreProcessOneFile('./scratch/kaggle_data.csv', 'message')
#     For now it outputs to 'preprocoutput.txt' in the same directory. No return values. Input is file name with directory, and the column name that corresponds to the chat messages in csv file.
# PreProcessOneMessage('thank you bro :smiling_face_with_smiling_eyes: :smiling_face_with_smiling_eyes: ')
#     Returns preprocessed string. In training and testing you can import PreProcessOneMessage and call it.

# TODO: change file name and column name here as needed
PreProcessOneFile('./scratch/kaggle_data.csv', 'message')

# function for training/testing code to call
def PreProcessOneMessage(s):
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