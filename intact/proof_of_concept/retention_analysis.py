from definitions.characteristic_computations import bucket_age, bucket_income, bucket_accidents
import pandas as pd
from definitions.constants import SUFFICIENT

def calculate_conditional_retention_probability(df, sex=None, age=None, marital_status=None, income=None, accidents=None, treatment=None):
    filtered_df = df.copy()

    if sex is not None:
        filtered_df = filtered_df[filtered_df['sex'] == sex]
    if age is not None:
        filtered_df = filtered_df[filtered_df['age'].apply(bucket_age) == bucket_age(age)]
    if marital_status is not None:
        filtered_df = filtered_df[filtered_df['marital_status'] == marital_status]
    if income is not None:
        filtered_df = filtered_df[filtered_df['income'].apply(bucket_income) == bucket_income(income)]
    if accidents is not None:
        filtered_df = filtered_df[filtered_df['accidents'].apply(bucket_accidents) == bucket_accidents(accidents)]
    if treatment is not None:
        filtered_df = filtered_df[filtered_df['treatment'] == treatment]

    if filtered_df.empty:
        return float('nan')
    else:
        return filtered_df['retained'].mean()

def count_clients_in_bucket(df, sex=None, age=None, marital_status=None, income=None, accidents=None, treatment=None):
    filtered_df = df.copy()
    if sex is not None:
        filtered_df = filtered_df[filtered_df['sex'] == sex]
    if age is not None:
        filtered_df = filtered_df[filtered_df['age'].apply(bucket_age) == bucket_age(age)]
    if marital_status is not None:
        filtered_df = filtered_df[filtered_df['marital_status'] == marital_status]
    if income is not None:
        filtered_df = filtered_df[filtered_df['income'].apply(bucket_income) == bucket_income(income)]
    if accidents is not None:
        filtered_df = filtered_df[filtered_df['accidents'].apply(bucket_accidents) == bucket_accidents(accidents)]
    if treatment is not None:
        filtered_df = filtered_df[filtered_df['treatment'] == treatment]

    return len(filtered_df)

def retention_given_characteristic_combinations(df, treatment, sex, age, marital_status, income, accidents):

    input_values = {
        'treatment': treatment,
        'sex': sex,
        'age': bucket_age(age),
        'marital_status': marital_status,
        'income': bucket_income(income),
        'accidents': bucket_accidents(accidents)
    }

    filter_columns = ['treatment', 'sex', 'age', 'marital_status', 'income', 'accidents']

    combination_filters = []
    for treatment_val in ([input_values['treatment'], None]):
        for sex_val in ([input_values['sex'], None]):
            for age_val in ([input_values['age'], None]):
                for marital_status_val in ([input_values['marital_status'], None]):
                    for income_val in ([input_values['income'], None]):
                        for accidents_val in ([input_values['accidents'], None]):
                            combination_filters.append({
                                'treatment': treatment_val,
                                'sex': sex_val,
                                'age': age_val,
                                'marital_status': marital_status_val,
                                'income': income_val,
                                'accidents': accidents_val
                            })

    filtered_rows = pd.DataFrame()
    for criteria in combination_filters:
        current_filter = df.copy()
        for col in filter_columns:
            value = criteria[col]
            if value is not None:
                current_filter = current_filter[current_filter[col] == value]
            else:
                current_filter = current_filter[current_filter[col].isna()]

        filtered_rows = pd.concat([filtered_rows, current_filter])

    filtered_rows = filtered_rows.drop_duplicates().reset_index(drop=True)

    return filtered_rows

def filter_insufficient(df, treatment, sex, age, marital_status, income, accidents):
    result = retention_given_characteristic_combinations(df, treatment, sex, age, marital_status, income, accidents)
    for row in result.itertuples():
        if row.number_of_clients < SUFFICIENT:
            result = result.drop(row.Index)
    return result

def estimate_retention(df, treatment, sex, age, marital_status, income, accidents):
    result = filter_insufficient(df, treatment, sex, age, marital_status, income, accidents)
    vars = []
    for row in result.itertuples():
        row_vars = []
        if not pd.isna(row.treatment):
            row_vars.append('treatment')
        if not pd.isna(row.sex):
            row_vars.append('sex')
        if not pd.isna(row.age):
            row_vars.append('age')
        if not pd.isna(row.marital_status):
            row_vars.append('marital_status')
        if not pd.isna(row.income):
            row_vars.append('income')
        if not pd.isna(row.accidents):
            row_vars.append('accidents')

        dominated = False
        i = 0
        while not dominated and i < len(vars):
            if set(row_vars) <= set(vars[i]):
                result = result.drop(row.Index)
                dominated = True
            i += 1
        if not dominated:
            vars.append(row_vars)
            
    return result
