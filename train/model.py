import numpy as np
import pandas as pd
import sys
import os 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

#assign profane class based on score 
def calculateClass(score):
  return 1 if score > 0.66 else 0 

#vectorize sentence with BoW
from collections import OrderedDict
files = os.listdir("./osf_labelled_data")
df = pd.DataFrame()

#pick first 30 csv
#this requires about 30G RAM, so be cautious about # of csv we want to use for training
for i in range(30):
  data = pd.read_csv("/content/drive/MyDrive/NLP/project/labelled/osf_labelled_data/" + files[i], sep=',')
  df = pd.concat([df, data])

uniqueWords = OrderedDict()
index = 0
for msg, score in zip(df["Message"], df["Sentiment"]):
  for word in msg.split(" "):
    if word not in uniqueWords:
      uniqueWords[word] = index
      index += 1

#preparing features and labels from raw data
features = []
labels = []
for msg, score in zip(df["Message"], df["Sentiment"]):
  feature = np.array(np.zeros(len(uniqueWords)))
  for word in msg.split(" "):
    feature[uniqueWords[word]] += 1
  features.append(feature)
  labels.append(calculateClass(score))

#split test train
x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=0)

logModel = LogisticRegression(max_iter=1000)
logModel.fit(x_train, y_train)
y_pred = logModel.predict(x_test)

print(classification_report(y_test, y_pred))
