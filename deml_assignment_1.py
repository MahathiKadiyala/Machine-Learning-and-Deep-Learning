# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 13:34:42 2026

@author: mahat
"""
#Question 1
import pandas as pd

# Load the CSV file
df = pd.read_csv(r"C:\Users\mahat\Downloads\public-covid-19-cases-canada.csv")

# Display the first 5 rows
print(df)

# Number of rows and columns
print(df.shape)

# Column names
print(df.columns)

# Data types
print(df.dtypes)

# First 10 rows
print(df.head(10))

#Dataset information
print("\nDataset Information:")
df.info()

print(df.describe(include='all'))

#Unique Values in Each Column
for col in df.columns:
    print("\n---------------------------")
    print("Column:", col)
    print("Unique Values:", df[col].nunique())
    print(df[col].unique())
    
    
#Missing (Null) Values
print("Missing Values in Each Column:")
print(df.isnull().sum())


#Frequency of Values
for col in df.columns:
    print("\n======================")
    print("Column:", col)
    print(df[col].value_counts(dropna=False))
    
    
#Range of Values
for col in df.columns:
    print(f"\n{col}")
    print("Minimum :", df[col].min())
    print("Maximum :", df[col].max())
    
#Useless or Less Useful Values

for col in df.columns:
    print("\n", col)
    print(df[col].value_counts(dropna=False))
    
#Data Pre-processing 
#Check Missing Values
print(df.isnull().sum())

import numpy as np

# Replace useless values with NaN
df.replace(['NULL', 'Null', 'null',
            'Not Reported',
            'Not Report',
            'Unknown',
            '',
            ' '], np.nan, inplace=True)

df = df.dropna(subset=['age'])

#Fill Missing Values in Other Columns
df.fillna({
    'sex': 'Unknown',
    'province': 'Unknown',
    'health_region': 'Unknown',
    'country': 'Unknown',
    'has_travel_history': 'Unknown',
    'locally_acquired': 'Unknown',
    'case_source': 'Unknown'
}, inplace=True)


#Reformat age groups 
def clean_age(age):

    age = str(age).strip()

    if age in ['<18', '<20', '0-19']:
        return '0-19'

    elif age in ['20-29']:
        return '20-29'

    elif age in ['30-39']:
        return '30-39'

    elif age in ['40-49']:
        return '40-49'

    elif age in ['50-59']:
        return '50-59'

    elif age in ['60-69']:
        return '60-69'

    elif age in ['70-79']:
        return '70-79'

    elif age in ['80-89']:
        return '80-89'

    elif age in ['90+', '90-99']:
        return '90-99'

    else:
        return np.nan

df['age'] = df['age'].apply(clean_age)

# Remove invalid age groups
df = df.dropna(subset=['age'])

#verification
print(df['age'].value_counts())

#Total Number of Infected Persons for Each Age Group 
age_count = df['age'].value_counts().sort_index()
print(age_count)

#Cleaned Dataset 
df.to_csv('cleaned_covid19_canada.csv', index=False)
print("Cleaned dataset saved successfully.")

#Question 2(b)(i)

#Total number of male and female infectors for each month

# Convert date to datetime
df["date_report"] = pd.to_datetime(df["date_report"])

# Create month column
df["month"] = df["date_report"].dt.month_name()

# Male and Female cases for each month
gender_month = pd.crosstab(df["month"], df["sex"])

print("Male and Female infectors for each month")
print(gender_month)
print(df.columns.tolist())
    
#Question 2(b)(ii)
#Sort age groups by number of female infectors
female_age = (
    df[df["sex"] == "Female"]
    .groupby("age")
    .size()
    .sort_values(ascending=False)
)

print("\nFemale infectors by age group")
print(female_age)

#Question 2(b)(iii)
#Top TWO months (No travel history & age > 50)
older = ["50-59", "60-69", "70-79", "80-89", "90-99"]

top_months = (
    df[
        (df["has_travel_history"] == "No") &
        (df["age"].isin(older))
    ]
    .groupby("month")
    .size()
    .sort_values(ascending=False)
    .head(2)
)

print("\nTop 2 months (Age > 50 and No Travel History)")
print(top_months)

#Question 3(a)

print("\nQuestion 3(a)(i)")
print(gender_month)

print("\nQuestion 3(a)(ii)")
print(female_age)

print("\nQuestion 3(a)(iii)")
print(top_months)

#Question 3(b)(i)
#Function to find the top 3 provinces for each month
def top_three_provinces(data):

    months = sorted(data["month"].unique())

    for month in months:

        print("\nMonth:", month)

        top = (
            data[data["month"] == month]
            .groupby("province")
            .size()
            .sort_values(ascending=False)
            .head(3)
        )

        print(top)

top_three_provinces(df)

#Question 3(b)(ii)
#Graph: Total COVID-19 cases by province

import matplotlib.pyplot as plt

province_cases = df.groupby("province").size()

province_cases.plot(kind="bar", figsize=(12,6))

plt.title("Total COVID-19 Cases by Province")
plt.xlabel("Province")
plt.ylabel("Number of Cases")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

#Question 3(b)(iii)
#Graph: Age distribution by gender in the province with the highest cases
highest_province = df.groupby("province").size().idxmax()

province_df = df[df["province"] == highest_province]

table = pd.crosstab(province_df["age"], province_df["sex"])

table.plot(kind="bar", figsize=(10,6))

plt.title("Age Distribution by Gender - " + highest_province)
plt.xlabel("Age Group")
plt.ylabel("Number of Cases")

plt.tight_layout()
plt.show()

#Question 3(c)(i)
#Function to compute weekday and update report_week
from datetime import datetime

def get_day(date):

    return datetime.strptime(str(date), "%Y-%m-%d").strftime("%A")

df["report_week"] = df["date_report"].astype(str).apply(get_day)

print(df[["date_report", "report_week"]].head())

#Question 3(c)(ii)
#Top THREE weekdays with the most COVID-19 cases
top_days = (
    df.groupby("report_week")
    .size()
    .sort_values(ascending=False)
    .head(3)
)

print("\nTop 3 Days")
print(top_days)

#Question 3(c)(iii)
#Graph: Number of COVID-19 cases per gender for each month
gender_month_graph = pd.crosstab(df["month"], df["sex"])

gender_month_graph.plot(kind="bar", figsize=(12,6))

plt.title("COVID-19 Cases per Gender for Each Month")
plt.xlabel("Month")
plt.ylabel("Number of Cases")

plt.tight_layout()
plt.show()