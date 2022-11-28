import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

dfs = list()
for filename in os.listdir("../train/osf_labelled_data/"):
    with open(os.path.join("../train/osf_labelled_data/", filename), 'r') as f:
        data = pd.read_csv(f)
        dfs.append(data)
        
df = pd.concat(dfs, ignore_index=True)
sentiment = list(df['Sentiment'])

hist, bins = np.histogram(sentiment, bins = [0, 0.1,
                                     0.2, 0.3,
                                     0.4, 0.5,
                                     0.6, 0.7,
                                     0.8, 0.9,
                                     1])
print(hist)
fig = plt.figure(figsize =(10, 7))
plt.hist(sentiment, bins = [0, 0.1,
                            0.2, 0.3,
                            0.4, 0.5,
                            0.6, 0.7,
                            0.8, 0.9,
                            1], rwidth=0.7)
plt.title("Dataset Histogram")
plt.xlabel("Sentiment Score")
plt.show()