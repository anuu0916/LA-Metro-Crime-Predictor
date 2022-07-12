import pandas as pd

flights = pd.read_csv('flights.csv')

print(flights.groupby(['year']).mean())
