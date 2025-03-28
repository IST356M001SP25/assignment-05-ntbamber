import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl


#TODO Write your extraction code here

# Constants
cache_dir = "cache"
survey_url = "https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv"
states_url = "https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv"


# 1️⃣ Extract states with codes
def extract_states():
    states_df = pd.read_csv(states_url)
    states_df.to_csv('cache/states.csv', index=False)
    print("Saved: states.csv")

# 2️⃣ Extract survey data and add year
def extract_survey():
    survey_df = pd.read_csv(survey_url)
    survey_df["year"] = survey_df["Timestamp"].apply(pl.extract_year_mdy)
    survey_df.to_csv('cache/survey.csv', index=False)
    print("Saved: survey.csv")
    return survey_df["year"].dropna().unique()

# 3️⃣ Extract cost of living data per year
def extract_col_data(years):
    for year in years:
        col_year_df = pd.read_html(f"https://www.numbeo.com/cost-of-living/rankings.jsp?title={year}&displayColumn=0")[1]
        col_year_df["year"] = year
        col_year_df.to_csv(f'cache/col_{year}.csv', index=False)
        print(f"Saved: col_{year}.csv")

# 🚀 Run everything
def main():
    extract_states()
    unique_years = extract_survey()
    extract_col_data(unique_years)

if __name__ == "__main__":
    main()