import pandas as pd

path = './data/count/run-368547.csv'
data = pd.read_csv(path, index_col=False)
print(data)

print(data.denominator.sum())
print(data.numerator.sum())

