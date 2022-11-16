import sys
import pandas as pd

# Real csv name in dataset: 0a633aa33731985aa52985e79bb12f38b95b9404_0.csv
df = pd.read_csv('tempdata.csv')

print(df.info()) 
# print(df) 