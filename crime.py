import pandas as pd
import matplotlib.pyplot as plt

''' Define Constant '''
# the number of total estimated ridership (2021)
total_ridership = 47866883

# the total number of crimes on metro rail (2010~2022)
total_crime_num = 8058

# year gap of the dataset
year_gap = 2022 - 2010 + 1

# the ratio of ridership by line
ratio_line = {
    "BLUE|METRO CENTER" : 0.19,
    "RED|METRO CENTER|UNION|PURPLE" : 0.45,
    "GREEN" : 0.09,
    "GOLD|UNION" : 0.1,
    "EXPO|METRO CENTER" : 0.17,
}

# the ratio of ridership by race
ratio_race = {
    "Hispanic" : 0.44,
    "Black" : 0.18,
    "White" : 0.21,
    "Asian" : 0.10,
    "Islander" : 0.01,
    "Native" : 0.01,
    "Other" : 0.06,
}

ratio_sex = {
    "M" : 0.53,
    "F" : 0.46
}

# the ratio of ridership per hour
ratio_time = [
    0.0047, 0.0024, 0.0009, 0, 0.0009, 0.019, 0.0569, 0.0853,
    0.0948, 0.0569, 0.0427, 0.0427, 0.0474, 0.0522, 0.0569, 0.0759, 
    0.1043, 0.109, 0.0522, 0.0285, 0.0237, 0.019, 0.0142, 0.0095
]

''' Read CSV file '''
crime = pd.read_csv('metro_rail_crimes_predict.csv')


''' Input information of time, line, race and sex '''
# Input boarding time
print("Enter your metro boarding time. (hr range: 0 ~ 23)")
print("ex) if you board 11am to 1pm, enter \"11-13\"")
time = input("input : ")

time = list(map(int, time.split('-')))

if time[0] < 0 or time[0] > 23 or time[1] < 0 or time[0] > 23:
    print("You entered an incorrect value.")
    exit()

print("Enter the line you want to board.")
print("1. Red, Purple")
print("2. Expo")
print("3. Blue")
print("4. Gold")
print("5. Green")
line = int(input("input : "))

if line == 1:
    line = "RED|METRO CENTER|UNION|PURPLE"
elif line == 2:
    line = "EXPO|METRO CENTER"
elif line == 3:
    line = "BLUE|METRO CENTER"
elif line == 4:
    line = "GOLD|UNION"
elif line == 5:
    line = "GREEN"
else:
    print("You entered an incorrect value.")
    exit()


print("\nEnter the race of the passenger.")
print("1. Asian (Chinese, Korean, Japanese, Filipino, Cambodian, Vietnamese, Laoian, Asian Indian and Other Asian)")
print("2. Black")
print("3. White")
print("4. Hispanic/Latin/Mexican")
print("5. Islander (Guamanian, Pacific Islander, Samoan, Hawaiian)")
print("6. American Indian/Alaskan Native")
print("7. Other")
race = int(input("input : "))


if race == 1:
    race = "Asian"
elif race == 2:
    race = "Black"
elif race == 3:
    race = "White"
elif race == 4:
    race = "Hispanic"
elif race == 5:
    race = "Islander"
elif race == 6:
    race = "Native"
elif race == 7:
    race = "Other"
else:
    print("You entered an incorrect value.")
    exit()


print("\nEnter the passenger's gender.")
print("1. Female\n2. Male")
gender = int(input("input : "))


if gender == 1:
    gender = "F"
elif gender == 2:
    gender = "M"
else:
    print("You entered an incorrect value.")
    exit()


''' Predict the probability of a crime '''

# Expands boarding time by one hour 
# for comprehensive and fluid crime probability calculations
time_arr = []
start = time[0]
end = time[1]

if start == end:
    if start + 1 < 23:
        time_arr = [start-1, start, start+1]
    else:
        time_arr = [start-1, start, start+1-24]
elif start < end:
    for i in range(start-1, end+2):
        if i < 0:
            time_arr.append(24+i)
        elif i > 23:
            time_arr.append(i-24)
        else:
            time_arr.append(i)
else:
    for i in range(start-1, end+24+2):
        if i < 0:
            time_arr.append(24+i)
        elif i > 23:
            time_arr.append(i-24)
        else:
            time_arr.append(i)


# Total ridership ratio by time_arr
ratio_total_time = 0
# print(time_arr)
for t in time_arr:
    ratio_total_time += ratio_time[t]

# Find the number of crimes
cr = crime.copy()
cr = cr[cr['Premis Desc'].str.contains(line)]
cr = cr[cr["Race"] == race]
cr = cr[cr["Hour"].isin(time_arr)]
cr = cr[cr["Vict Sex"] == gender]

crime_count = cr["DR_NO"].count()

# Carculate the probability
ratio_crime = (crime_count / year_gap) / total_ridership
result = ratio_crime / (ratio_total_time * ratio_line[line] * ratio_race[race] * ratio_sex[gender])


if line == "RED|METRO CENTER|UNION|PURPLE":
    line = "RED|PURPLE"
elif line == "EXPO|METRO CENTER":
    line = "EXPO"
elif line == "BLUE|METRO CENTER":
    line = "BLUE"
elif line == "GOLD|UNION":
    line = "GOLD"

if gender == "F":
    gender = "female"
elif gender == "M":
    gender = "male"
    
''' Output '''
print("\n-----------PREDICT RESULT-----------")
print("You're a %s %s and riding %s line at %s:00-%s:00"%(race, gender, line, time[0], time[1]) )
print("the probability of a crime : {:.4f} ‱".format(result * 10000))

print("If a crime occurs, it may be :", end=" ")
crm_cd_avg = cr["Crm Cd"].mean()
# print(crm_cd_avg)
if crm_cd_avg < 110+170:
    print("a very violent crime")
elif 110+170 <= crm_cd_avg < 110+170*2:
    print("a violent crime")
elif 110+170*2 <= crm_cd_avg < 110+170*3:
    print("a misdemeanor")
else:
    print("a minor offense")
    
top = cr[["Crm Cd"]].sort_values('Crm Cd').head(3)
top3 = []
for i in range(3):
    top3.append(top.iloc[i,0])

crm_cd = {
    110 : "CRIMINAL HOMICIDE",
    113 : "MANSLAUGHTER, NEGLIGENT",
    121 : "RAPE, FORCIBLE",
    122 : "RAPE, ATTEMPTED",
    210 : "ROBBERY",
    220 : "ATTEMPTED ROBBERY",
    230 : "ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT",
    231 : "ASSAULT WITH DEADLY WEAPON ON POLICE OFFICER",
    236 : "INTIMATE PARTNER - AGGRAVATED ASSAULT",
    237 : "CHILD NEGLECT (SEE 300 W.I.C.)",
    250 : "SHOTS FIRED AT MOVING VEHICLE, TRAIN OR AIRCRAFT",
    310 : "BURGLARY",
    330 : "BURGLARY FROM VEHICLE",
    331 : "THEFT FROM MOTOR VEHICLE - GRAND ($950.01 AND OVER)",
    341 : "THEFT-GRAND ($950.01 & OVER)EXCPT,GUNS,FOWL,LIVESTK,PROD",
    350 : "THEFT, PERSON",
    351 : "PURSE SNATCHING",
    352 : "PICKPOCKET",
    353 : "DRUNK ROLL",
    354 : "THEFT OF IDENTITY",
    410: "BURGLARY FROM VEHICLE, ATTEMPTED",
    420 : "THEFT FROM MOTOR VEHICLE - PETTY ($950 & UNDER)",
    433 : "DRIVING WITHOUT OWNER CONSENT",
    434 : "FALSE IMPRISONMENT",
    437 : "RESISTING ARREST",
    440 : "THEFT PLAIN - PETTY ($950 & UNDER)"    
}


print("\nThe worst three cases was:")
print("1. %s"%(crm_cd[top3[0]]) ) 
print("2. %s"%(crm_cd[top3[1]]) )
print("3. %s"%(crm_cd[top3[2]]) )