from retention_analysis import calculate_conditional_retention_probability, count_clients_in_bucket
import constants
import csv

treatments = [None] + constants.TREATMENTS
sexes = [None] + constants.SEX_VALUES
age_groups = [None, 0]
for bound in constants.AGE_BOUNDS:
    age_groups.append(bound)
marital_groups = [None] + constants.MARITAL_STATUS_VALUES
income_groups = [None, 0]
for bound in constants.INCOME_BOUNDS:
    income_groups.append(bound)
accident_groups = [None, 0]
for bound in constants.ACCIDENT_BOUNDS:
    accident_groups.append(bound)

outcomes = []
for treatment in treatments:
    for sex in sexes:
        for age in age_groups:
            for marital_status in marital_groups:
                for income in income_groups:
                    for accidents in accident_groups:
                        retention = calculate_conditional_retention_probability(df, treatment=treatment, sex=sex, age=age, marital_status=marital_status, income=income, accidents=accidents)
                        num = count_clients_in_bucket(df, treatment=treatment, sex=sex, age=age, marital_status=marital_status, income=income, accidents=accidents)
                        outcomes.append([treatment, sex, age, marital_status, income, accidents, retention, num])
