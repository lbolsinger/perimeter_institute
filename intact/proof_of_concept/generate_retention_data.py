from retention_analysis import calculate_conditional_retention_probability, count_clients_in_bucket
import constants

TREATMENTS = [None, -0.1, 0, 0.1, 0.2]
SEX = [None, "f", "m"]
AGE = [None, 0, 20, 40, 60] # instances from each bucket based on premium buckets
MARITAL_STATUS = [None, "married", "single"]
INCOME = [None, 0, 20000, 50000, 80000]
ACCIDENTS = [None, 0, 1, 5]

outcomes = []
for treatment in TREATMENTS:
    for sex in SEX:
        for age in AGE:
            for marital_status in MARITAL_STATUS:
                for income in INCOME:
                    for accidents in ACCIDENTS:
                        retention = calculate_conditional_retention_probability(df, treatment=treatment, sex=sex, age=age, marital_status=marital_status, income=income, accidents=accidents)
                        num = count_clients_in_bucket(df, treatment=treatment, sex=sex, age=age, marital_status=marital_status, income=income, accidents=accidents)
                        outcomes.append([treatment, sex, age, marital_status, income, accidents, retention, num])
