import random
import copy
import pandas as pd

mock_pre = [random.randint(0,1) for _ in range(1000)]
mock_y = copy.deepcopy(mock_pre)

for i in range(0, len(mock_pre)):
    if random.randint(0, 7) == 1:
        mock_pre[i] = 1 - mock_pre[i]
df = pd.DataFrame(list(zip(mock_pre, mock_y)), columns=['pre', 'y'])
df.to_csv("mock_prediction.csv", index=False)