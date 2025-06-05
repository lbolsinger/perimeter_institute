import random
import math
import data_constants

def sigmoid(x):
    '''
    Computes the sigmoid function centered at (0, 0.5)
    '''
    return 1 / (1 + math.exp(-x))

def prob_married(age):
    '''
    Computes the probability of being married based on age
    '''
    z = -6 + 0.12 * age
    return sigmoid(z)

def compute_risk(sex, age, marital_status, accidents, income):
    '''
    Computes the risk score based on the input features
    '''
    score = 0

    if sex == 'm':
        score += data_constants.RISK_SEX_MALE

    for i in range(len(data_constants.AGE_BOUNDS)):
        if age < data_constants.AGE_BOUNDS[i]:
            score += data_constants.AGE_RISKS[i]
            break
    else:
        score += data_constants.AGE_RISKS[-1]

    if marital_status == 'single':
        score += data_constants.RISK_MARITAL_SINGLE

    for i in range(len(data_constants.ACCIDENT_BOUNDS)):
        if accidents < data_constants.ACCIDENT_BOUNDS[i]:
            score += data_constants.ACCIDENT_RISKS[i]
            break
    else: 
        score += data_constants.ACCIDENT_RISKS[-1]

    for i in range(len(data_constants.INCOME_BOUNDS)):
        if income < data_constants.INCOME_BOUNDS[i]:
            score += data_constants.INCOME_RISKS[i]
            break
    else:
        score += data_constants.INCOME_RISKS[-1]
    return score

def compute_base_premium(score):
    '''
    Computes the base premium based on the risk score
    '''
    premium = data_constants.PREMIUM_LOWER_BOUND + (data_constants.PREMIUM_UPPER_BOUND - data_constants.PREMIUM_LOWER_BOUND) / (1 + math.exp(-data_constants.PREMIUM_K * (score - data_constants.PREMIUM_X0)))
    return round(premium, 2)

def update_premium(premium, treatment_percent):
    '''
    Updates the premium based on the treatment percentage
    '''
    return round(premium * (1 + treatment_percent), 2)

def retention_prob(x):
    '''
    Computes the retention probability based on the input features
    '''
    z = (data_constants.RETENTION_SEX_FEMALE_EFFECT * (x[1] == 'f') +
         data_constants.RETENTION_AGE_EFFECT * (x[2] - average_age) / std_dev_age +
         data_constants.RETENTION_MARITAL_MARRIED_EFFECT * (x[3] == 'married') +
         data_constants.RETENTION_ACCIDENTS_EFFECT * (x[4] - average_accidents) / std_dev_accidents +
         data_constants.RETENTION_INCOME_EFFECT * (x[5] - average_income) / std_dev_income +
         data_constants.RETENTION_PREMIUM_EFFECT * (x[7] - average_premium) / std_dev_premium +
         data_constants.RETENTION_TREATMENT_EFFECT * x[8])
    z += random.gauss(0, data_constants.RETENTION_RANDOM_STD_DEV)
    return round(sigmoid(z), 3)

def bucket_age(age):
    '''
    Buckets the age into different categories
    '''
    for i in range(len(data_constants.AGE_BOUNDS)):
        if age < data_constants.AGE_BOUNDS[i]:
            if i == 0:
                return '<' + str(data_constants.AGE_BOUNDS[i])
            if i < len(data_constants.AGE_BOUNDS) - 1:
                return str(data_constants.AGE_BOUNDS[i-1]) + '-' + str(data_constants.AGE_BOUNDS[i+1]-1)
            if i == len(data_constants.AGE_BOUNDS) - 1:
                return str(data_constants.AGE_BOUNDS[i-1]) + '+'

def bucket_accidents(acc):
    '''
    Buckets the number of accidents into different categories
    '''
    for i in range(len(data_constants.ACCIDENT_BOUNDS)):
        if acc < data_constants.ACCIDENT_BOUNDS[i]:
            return data_constants.ACCIDENT_CATEGORIES[i]
    return data_constants.ACCIDENT_CATEGORIES[-1]

def bucket_income(income):
    '''
    Buckets the income into different categories
    '''
    for i in range(len(data_constants.INCOME_BOUNDS)):
        if income < data_constants.INCOME_BOUNDS[i]:
            if i == 0:
                return '<' + str(data_constants.INCOME_BOUNDS[i])
            if i < len(data_constants.INCOME_BOUNDS) - 1:
                return str(data_constants.INCOME_BOUNDS[i-1]) + '-' + str(data_constants.INCOME_BOUNDS[i+1]-1)
            if i == len(data_constants.INCOME_BOUNDS) - 1:
                return str(data_constants.INCOME_BOUNDS[i-1]) + '+'
