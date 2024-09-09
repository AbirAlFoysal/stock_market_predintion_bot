import pandas  as pd

# Load the dataset
model = "ACI"
dataset = pd.read_csv(f'./DB_csv/unadjusted_amarstock/{model}.csv')

print(dataset.head())
print(len(dataset))