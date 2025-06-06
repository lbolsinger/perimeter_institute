import csv
import pandas as pd

def list_with_features (df, treatment, sex, age, marital_status, income, accidents) :
    bucket_list = []

    for row in df.intertuples(index=False):
        flag = 1
        if treatment is not None and row.treatment != treatment :
            flag = 0
        
        if sex is not None and row.sex != sex :
            flag = 0

        if age is not None and row.age != age :
            flag = 0

        if marital_status is not None and row.marital_status != marital_status :
            flag = 0

        if income is not None and row.income != income :
            flag = 0
        
        if accidents is not None and row.accidents != accidents:
            flag = 0

        if flag == 1 :
            bucket_list.append(row._asdict())
    
    return bucket_list 

def find_optimal (list_of_buckets, value, optimum, num_clients_filter) :
    if not list_of_buckets:
        return None
        
    optimum_so_far = list_of_buckets[0]

    for item in list_of_buckets :
        if 'number_of_clients' in item and item['number_of_clients'] is not None and \
           'retention' in item and item['retention'] is not None and \
           int(item['number_of_clients']) > num_clients_filter :
            if optimum == 'MAX' :
                try:
                    if float(item[value]) > float(optimum_so_far[value]):
                        optimum_so_far = item
                except ValueError:
                    continue 
            if optimum == 'MIN' :
                try:
                    if float(item[value]) < float(optimum_so_far[value]):
                        optimum_so_far = item
                except ValueError:
                    continue 
                    
    return optimum_so_far   
