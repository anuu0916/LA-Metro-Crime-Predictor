import pandas as pd
import sqlite3

data = {
    'apples' : [3, 2, 0, 1],
    'oranges' : [0, 3, 7, 2]
}

purchases = pd.DataFrame(data, index=['June', 'Robert', 'Lily', 'David'])

print(purchases.loc['June'])
con = sqlite3.connect("database.db")