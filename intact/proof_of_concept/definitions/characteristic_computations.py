import random
import math
import constants

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
        score += constants.RISK_SEX_MALE

    for i in range(len(constants.AGE_BOUNDS)):
        if age < constants.AGE_BOUNDS[i]:
            score += constants.AGE_RISKS[i]
            break
    else:
        score += constants.AGE_RISKS[-1]

    if marital_status == 'single':
        score += constants.RISK_MARITAL_SINGLE

    for i in range(len(constants.ACCIDENT_BOUNDS)):
        if accidents < constants.ACCIDENT_BOUNDS[i]:
            score += constants.ACCIDENT_RISKS[i]
            break
    else: 
        score += constants.ACCIDENT_RISKS[-1]

    for i in range(len(constants.INCOME_BOUNDS)):
        if income < constants.INCOME_BOUNDS[i]:
            score += constants.INCOME_RISKS[i]
            break
    else:
        score += constants.INCOME_RISKS[-1]
    return score

def compute_base_premium(score):
    '''
    Computes the base premium based on the risk score
    '''
    premium = constants.PREMIUM_LOWER_BOUND + (constants.PREMIUM_UPPER_BOUND - constants.PREMIUM_LOWER_BOUND) / (1 + math.exp(-constants.PREMIUM_K * (score - constants.PREMIUM_X0)))
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
    z = (constants.RETENTION_SEX_FEMALE_EFFECT * (x[1] == 'f') +
         constants.RETENTION_AGE_EFFECT * (x[2] - average_age) / std_dev_age +
         constants.RETENTION_MARITAL_MARRIED_EFFECT * (x[3] == 'married') +
         constants.RETENTION_ACCIDENTS_EFFECT * (x[4] - average_accidents) / std_dev_accidents +
         constants.RETENTION_INCOME_EFFECT * (x[5] - average_income) / std_dev_income +
         constants.RETENTION_PREMIUM_EFFECT * (x[7] - average_premium) / std_dev_premium +
         constants.RETENTION_TREATMENT_EFFECT * x[8])
    z += random.gauss(0, constants.RETENTION_RANDOM_STD_DEV)
    return round(sigmoid(z), 3)

def bucket_age(age):
    '''
    Buckets the age into different categories
    '''
    for i in range(len(constants.AGE_BOUNDS)):
        if age < constants.AGE_BOUNDS[i]:
            if i == 0:
                return '<' + str(constants.AGE_BOUNDS[i])
            if i < len(constants.AGE_BOUNDS) - 1:
                return str(constants.AGE_BOUNDS[i-1]) + '-' + str(constants.AGE_BOUNDS[i+1]-1)
            if i == len(constants.AGE_BOUNDS) - 1:
                return str(constants.AGE_BOUNDS[i-1]) + '+'

def bucket_accidents(acc):
    '''
    Buckets the number of accidents into different categories
    '''
    for i in range(len(constants.ACCIDENT_BOUNDS)):
        if acc < constants.ACCIDENT_BOUNDS[i]:
            return constants.ACCIDENT_CATEGORIES[i]
    return constants.ACCIDENT_CATEGORIES[-1]

def bucket_income(income):
    '''
    Buckets the income into different categories
    '''
    for i in range(len(constants.INCOME_BOUNDS)):
        if income < constants.INCOME_BOUNDS[i]:
            if i == 0:
                return '<' + str(constants.INCOME_BOUNDS[i])
            if i < len(constants.INCOME_BOUNDS) - 1:
                return str(constants.INCOME_BOUNDS[i-1]) + '-' + str(constants.INCOME_BOUNDS[i+1]-1)
            if i == len(constants.INCOME_BOUNDS) - 1:
                return str(constants.INCOME_BOUNDS[i-1]) + '+'
