import pandas as pd

flights = pd.read_csv('flights.csv')

# Which month did we have the most departure delays?
temp = flights.copy()
# temp['dep_delay'] = temp['dep_delay'].apply(lambda x: -x if x < 0 else x)
temp = temp[temp['dep_delay'] > 0]
flights_m = temp.groupby(['month']).sum()
flights_m = flights_m.sort_values(by = 'dep_delay', ascending=False)
print(flights_m['dep_delay'])


# Average arrival and departure delay per air carrier
# Average arrival delay
temp = flights.copy()
temp['arr_delay'] = temp['arr_delay'].apply(lambda x: -x if x < 0 else x)
temp_arr = temp.groupby(['carrier']).mean()
temp_arr = temp_arr.sort_values(by = 'arr_delay', ascending=False)
print(temp_arr['arr_delay'])

#Average departure delay
temp = flights.copy()
temp = temp[temp['dep_delay'] > 0]
temp_dep = temp.groupby(['carrier']).mean()
temp_dep = temp_dep.sort_values(by = 'dep_delay', ascending=False)
print(temp_dep['dep_delay'])

# Which airline has the longest departure delays?
temp = flights.copy()
temp = temp.sort_values(by = 'dep_delay', ascending=False)
print(temp[['carrier', 'dep_delay']].head())

# What are top 5 flights which have the most delay time?
temp = flights.copy()
temp = temp.groupby(['flight']).max()
temp = temp.sort_values(by = ['dep_delay', 'arr_delay'], ascending = [False, False])
print(temp.head(5))