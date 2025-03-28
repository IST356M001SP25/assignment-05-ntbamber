import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here

def load_data(): #Load survey, states, and COL data
    survey_data = pd.read_csv('cache/survey.csv')
    states_data = pd.read_csv('cache/states.csv')

    # Load all COL files
    cols = []
    for year in survey_data['year'].dropna().unique():
        col = pd.read_csv(f'cache/col_{int(year)}.csv')
        cols.append(col)
    col_data = pd.concat(cols, ignore_index=True)
    return survey_data, states_data, col_data


def transform_data(survey_data, states_data, col_data):
    """Clean and merge datasets to produce an adjusted salary dataset."""
    # Clean the country column
    survey_data['_country'] = survey_data['What country do you work in?'].apply(pl.clean_country_usa)

    # Merge with state abbreviations
    survey_states_combined = survey_data.merge(
        states_data,
        left_on="If you're in the U.S., what state do you work in?",
        right_on='State',
        how='inner'
    )

    # Create full city string
    survey_states_combined['_full_city'] = (
        survey_states_combined['What city do you work in?'] + ', ' +
        survey_states_combined['Abbreviation'] + ', ' +
        survey_states_combined['_country']
    )

    # Merge with COL data
    combined = survey_states_combined.merge(
        col_data,
        left_on=['year', '_full_city'],
        right_on=['year', 'City'],
        how='inner'
    )

    # Clean and adjust salary
    salary_col = (
        "What is your annual salary? (You'll indicate the currency in a later question. "
        "If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"
    )

    combined["_annual_salary_cleaned"] = combined[salary_col].apply(pl.clean_currency)

    combined['_annual_salary_adjusted'] = combined.apply(
        lambda row: row["_annual_salary_cleaned"] * (100 / row['Cost of Living Index']),
        axis=1
    ).round(2)

    return combined


def save_reports(combined):
    """Save the transformed dataset and pivot table reports."""
    # Save full combined dataset
    combined.to_csv('cache/survey_dataset.csv', index=False)

    # Report 1: by location and age
    report_age = combined.pivot_table(
        index='_full_city',
        columns='How old are you?',
        values='_annual_salary_adjusted',
        aggfunc='mean'
    ).round(2)
    report_age.to_csv('cache/annual_salary_adjusted_by_location_and_age.csv')

    # Report 2: by location and education
    report_edu = combined.pivot_table(
        index='_full_city',
        columns='What is your highest level of education completed?',
        values='_annual_salary_adjusted',
        aggfunc='mean'
    ).round(2)
    report_edu.to_csv('cache/annual_salary_adjusted_by_location_and_education.csv')

    return report_age, report_edu


survey_data, states_data, col_data = load_data()
combined = transform_data(survey_data, states_data, col_data)
report_age, report_edu = save_reports(combined)
st.write("✅ Transformation complete.")
st.write(report_edu)