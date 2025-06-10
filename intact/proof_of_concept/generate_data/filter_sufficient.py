from definitions.constants import SUFFICIENT
import pandas as pd

def find_sufficient_profiles():
    df = pd.read_csv("C:/Users/lisab/Documents/GitHub/perimeter_institute/intact/proof_of_concept/data/retention.csv")

    filtered_df = df[df['treatment'].str.strip() != '']
    filtered_df = filtered_df[filtered_df[' age  '].str.strip() != '']
    filtered_df = filtered_df[filtered_df[' marital_status'].str.strip() != '']
    filtered_df = filtered_df[filtered_df[' income '].str.strip() != '']
    filtered_df = filtered_df[filtered_df[' accidents'].str.strip() != '']
    filtered_df = filtered_df[filtered_df[' sex'].str.strip() != '']
    filtered_df = filtered_df[filtered_df[' number_of_clients'] >= SUFFICIENT]

    filtered_df.to_csv('C:/Users/lisab/Documents/GitHub/perimeter_institute/intact/proof_of_concept/data/sufficient_clients.csv', index=False)