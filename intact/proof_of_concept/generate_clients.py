import random
import math
import statistics as stat
import csv
import numpy as np
import constants
import characteristic_computations as comp

random.seed(42)
clients = []

treatment_dict = {}

for year in constants.YEARS:
    for _ in range(constants.N_PER_YEAR):
        sex = random.choice(constants.SEXES)
        age = random.randint(constants.MIN_AGE, constants.MAX_AGE)
        if random.random() < comp.prob_married(age):
            marital_status = 'married'
        else:
            marital_status = 'single'
        accidents = round(random.gauss(stat.mean(constants.ACCIDENT_RANGE), constants.ACCIDENT_SDE))
        income = round(random.gauss(stat.mean(constants.INCOME_RANGE), constants.INCOME_SDE))

        features_key = (
            sex,
            comp.bucket_age(age),
            marital_status,
            comp.bucket_accidents(accidents),
            comp.bucket_income(income)
        )
        key = (year, features_key)

        if key not in treatment_dict:
            treatment_dict[key] = random.choice(constants.TREATMENTS)

        treatment = treatment_dict[key]
        risk = comp.compute_risk(sex, age, marital_status, accidents, income)
        premium = comp.compute_base_premium(risk)
        new_premium = comp.update_premium(premium, treatment)

        clients.append([
            year, sex, age, marital_status, accidents, income,
            risk, premium, treatment,new_premium, 0, False
        ])

average_age = stat.mean([client[2] for client in clients])
std_dev_age = stat.stdev([client[2] for client in clients])

average_income = stat.mean([client[5] for client in clients])
std_dev_income = stat.stdev([client[5] for client in clients])

average_accidents = stat.mean([client[4] for client in clients])
std_dev_accidents = stat.stdev([client[4] for client in clients])

average_premium = stat.mean([client[7] for client in clients])
std_dev_premium = stat.stdev([client[7] for client in clients])

for client in clients:
    client[10] = comp.retention_prob(client)
    client[11] = random.random() < client[10]

with open("clients.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        "year", "sex", "age", "marital_status", "accidents", "income",
        "score", "premium", "treatment", "adjusted_premium", "retention_prob",
        "retained"
    ])
    writer.writerows(clients)
