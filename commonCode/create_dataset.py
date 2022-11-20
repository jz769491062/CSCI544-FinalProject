import pandas as pd
import numpy as np
pd.set_option('display.max_rows', None)

df = pd.read_csv("scratch/kaggle_data.csv")
df_pro = pd.read_csv("scratch/profanity_words.csv")

df = df[['message']]
df['message'] = df['message'].str.lower()
df['message'] = df['message'].str.replace('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', regex=True)
df['message'] = df['message'].str.replace('biblethump', ' ')
df['message'] = df['message'].str.replace('feelsstrongman', ' ')
# df['message'] = df['message'].str.replace('[^a-zA-Z0-9\']', ' ', regex=True)
df['message'] = df['message'].str.replace('\?+', '?', regex=True)
df['message'] = df['message'].str.replace('<3', '', regex=True)
df['message'] = df['message'].str.replace('\s+', ' ', regex=True)



delete_rows = []
for index, row in df.iterrows():
    if pd.isnull(row['message']):
        delete_rows.append(index)
    elif len(row['message']) == 0 or row['message'] == ' ':
        delete_rows.append(index)
df.drop(labels=delete_rows, axis=0, inplace=True)
df.drop_duplicates(['message'], inplace=True)
df.reset_index(drop=True, inplace=True)

# df.to_csv('Dataset_Clean.csv')

drop_rows = [12, 15, 37, 44, 59, 78, 85, 123, 129, 145, 146, 155, 175, 181, 183, 185, 191, 201, 203, 221, 230, 
            240, 241, 247, 293, 316, 325, 335, 341, 453, 471, 473, 489, 496, 501, 655, 707, 745, 805, 806, 821, 
            912, 946, 1004, 1070, 1080, 1216, 1224, 1313, 1388, 1592, 1695, 1704, 1787, 1798, 1830, 1925, 1952, 
            1971, 1992, 2108, 2117, 2119, 2131, 2140, 2146, 2155, 2178, 2290, 2355, 2405, 2743, 3026, 3040, 3105, 
            4036]    
for i in range(4128, 4459):
    drop_rows.append(i)
df.drop(drop_rows, inplace=True)

for index, row in df.iterrows():
    df.at[index, 'profanity'] = 0

dict_pro = {}
for index, row in df_pro.iterrows():
    dict_pro[row['text']] = row['severity_rating']
    if row['canonical_form_1'] not in dict_pro:
        dict_pro[row['canonical_form_1']] = row['severity_rating']
    else:
        dict_pro[row['canonical_form_1']] = min(dict_pro[row['canonical_form_1']], row['severity_rating'])
    if row['canonical_form_2'] not in dict_pro:
        dict_pro[row['canonical_form_2']] = row['severity_rating']
    else:
        dict_pro[row['canonical_form_2']] = min(dict_pro[row['canonical_form_2']], row['severity_rating'])
    if row['canonical_form_3'] not in dict_pro:
        dict_pro[row['canonical_form_3']] = row['severity_rating']
    else:
        dict_pro[row['canonical_form_3']] = min(dict_pro[row['canonical_form_3']], row['severity_rating'])
del dict_pro[np.nan]


for key in dict_pro:
    df = df.append({"message": key, "profanity": dict_pro[key]}, ignore_index = True)

df.to_csv('../data/tagged_dataset.csv')