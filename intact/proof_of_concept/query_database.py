import csv

with open('poc2/retention.csv', 'r') as csv_file :
    csv_reader = csv.DictReader(csv_file)
    
    
    def list_with_features (treatment, sex, age, marital_status, income, accidents) :
        bucket_list = []

        for line in csv_reader :
            flag = 1
            if treatment is not None and line["treatment"] != treatment :
                flag = 0
            
            if sex is not None and line["sex"] != sex :
                flag = 0

            if age is not None and line["age"] != age :
                flag = 0

            if marital_status is not None and line["marital_status"] != marital_status :
                flag = 0

            if income is not None and line["income"] != income :
                flag = 0
            
            if accidents is not None and line["accidents"] != accidents:
                flag = 0

            if flag == 1 :
                bucket_list.append(line)
        
        return bucket_list 
    
    def find_optimal (list_of_buckets, value, optimum, num_clients_filter) :
        optimum_so_far = list_of_buckets[0]

        for item in list_of_buckets :
            if int(item['number_of_clients']) > num_clients_filter :
                if optimum == 'MAX' and float(item[value]) > float(optimum_so_far[value]):
                    optimum_so_far = item 
                if optimum == 'MIN' and item[value] < optimum_so_far[value] :
                    optimum_so_far = item 
        
        return optimum_so_far    

# example query
#   new_list = list_with_features(treatment = None, sex = None, age = None, marital_status = None, income = None, accidents = None)

#  highest_retention = find_optimal(list_of_buckets=new_list, value='retention', optimum='MAX', num_clients_filter = 10)
#   print(highest_retention)
    
