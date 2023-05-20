# LA-Metro-Crime-Predictor
### The Safety Prediction using LA metro crime statistics

---

## Description
![image](https://user-images.githubusercontent.com/56395764/230440107-dbfaf305-c44e-4c30-b438-b6ddbf452426.png)

### Why is this meaningful?
Provide Metro users with predictive information on the probability of crime based on crime data.

### What to solve?
It helps citizens make boarding decisions for safe use of Metro.

### Dataset
- Crime Data from 2020 to Present
https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8

- Crime Data from 2010 to 2019
https://data.lacity.org/Public-Safety/Crime-Data-from-2010-to-2019/63jg-8b9z

- Ratio of Metro Riders' Age, Ethnicity, Gender, etc.
https://thesource.metro.net/2020/06/26/metro-programs-that-work-toward-racial-justice/

- LA Metro Ridership
https://isotp.metro.net/MetroRidership/

According to la City Hall data, the time, location, gender of the victim, age of the victim, race, severity of the crime, etc.

### Method used 
Assuming that each probability is independent, the likelihood of exposure to a crime was calculated as a conditional probability

---

## Algorithm - Conditional Probability
P(A) = Probability that metro passengers meet the conditions entered (assume each independent event) 

```python
ratio_total_time * ratio_line[line] * ratio_race[race] * ratio_sex[gender]
```

P(B) =Probability of Metro riders being criminally harmed
```python
(total_crime_num / year_gap) / total_ridership
```

### What we need to figure out : P(B|A)
The probability that a passenger will be subjected to criminal damage if the conditions entered are met

### What we know : P(A|B)
The probability that the victim meets the conditions entered in the event of a crime
```python
crime_count / total_crime_num
```

### Algorithm
**P(A|B)**
= P(AnB) / P(B)  
-> P(A|B)*P(B)   
= P(AnB)  
= `(crime_count / total_crime_num) * ((total_crime_num / year_gap) / total_ridership)`  
= `(crime_count / year_gap) / total_ridership`  

**P(B|A)**  
= P(AnB)/P()
= `(crime_count / year_gap / total_ridership) / (ratio_total_time * ratio_line[line] * ratio_race[race] * ratio_sex[gender])`


### Variables
|Name|Description|
|------|---|
|ratio_total_time|Probability that the passenger is on the metro at that time|
|ratio_race[race]|Probability that the occupant is of the race|
|ratio_line[line]|The probability that the occupant is on that route|
|ratio_sex[gender]|Probability that the occupant is of that gender|
|total_crime_num|The number of crimes committed in Metro from 2010 to now|
|total_ridership|Total number of passengers per year in 2021|
|year_gap|2022 - 2010 + 1: Number of years data collected|
|crime_count|Number of metro crimes that meet the conditions entered|

---

## Team
|Name|Role|
|------|---|
|Youjin Ahn|Leader, Algorithm Design|
|Sinyeong Bak|Filtering Datasets|
|Chanil Park|Data Analysis|
|Jeonggon Lee|Data Analysis|
