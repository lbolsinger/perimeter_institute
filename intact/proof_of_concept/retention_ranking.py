import csv

with open('retention.csv', 'r') as csv_file :
    csv_reader = csv.DictReader(csv_file)

    csv_reader.fieldnames = [field.strip().lower() for field in csv_reader.fieldnames]

    lines = []
    for row in csv_reader:
        normalized_row = {k.strip().lower(): v.strip() for k, v in row.items()}
        lines.append(normalized_row)
    
    #mother profile: 0.1, f, 50-80, married, 80k+, low
    TREATMENTS = ['0.2']
    SEXES = ['m']
    AGES = ['20-39']
    MARITAL_STATUSES = ['single']
    INCOMES = ['50k-80k']
    ACCIDENTS = ['high']

    treatments = [''] + TREATMENTS
    sexes = [''] + SEXES
    ages = [''] + AGES
    marital_statuses = [''] + MARITAL_STATUSES
    incomes = [''] + INCOMES
    accidents = [''] + ACCIDENTS

    list_of_profiles = []
    list_of_dicts = []
    
    
    count = 0
    probability = 0

    def dict_of_non_nones (profile) :
        list_of_characteristics = []
        list_of_nones = []
        nones = 0
        for key in profile.keys() :
            if profile[key] == '' :
                nones += 1
                list_of_nones.append(key)
            else :
                list_of_characteristics.append(key)
        new_dict = {'chars': list_of_characteristics, 'nones': nones}
        return new_dict



    for treatment in treatments :
        for sex in sexes :
            for age in ages :
                for marital_status in marital_statuses :
                    for income in incomes :
                        for accident in accidents :
                            profile = {'treatment': treatment, 'sex': sex,'age': age,'marital_status': marital_status, 'income': income,'accidents': accident}
                            list_of_profiles.append(profile)


    for profile in list_of_profiles :
        for line in lines :
            if profile['treatment'] == line['treatment'] and profile['age'] == line['age'].strip() and profile['sex'] == line['sex'].strip() and profile['marital_status'] == line['marital_status'].strip() and profile['income'] == line['income'].strip() and profile['accidents'] == line['accidents'].strip() :
                my_dict = dict_of_non_nones(profile)
                my_dict['retention'] = float(line['retention'])
                my_dict['clients'] = int(line['number_of_clients'])
                list_of_dicts.append(my_dict)

        
    for line in lines :
        if '0.2' == line['treatment'] and '20-39' == line['age'].strip() and 'm' == line['sex'].strip() and 'single' == line['marital_status'].strip() and '50k-80k' == line['income'].strip() and 'high' == line['accidents'].strip() :
            mother_retention = float(line['retention'])
            mother_count = float(line['number_of_clients'])
            break

    for dict in list_of_dicts :
        dict['retention_dif'] = abs(mother_retention - dict['retention'])
        
    
    list_of_dicts = [dict for dict in list_of_dicts if dict['nones'] != 0]

    sorted_data = sorted(list_of_dicts, key=lambda x: x['retention_dif'], reverse=False)

    ranking_dict_list = [{'char': 'treatment', 'total_retention': 0, 'retention_count': 0, 'average_retention': 0}, 
                         {'char': 'sex', 'total_retention': 0, 'retention_count': 0, 'average_retention': 0},
                         {'char': 'age', 'total_retention': 0, 'retention_count': 0, 'average_retention': 0},
                         {'char': 'marital_status', 'total_retention': 0, 'retention_count': 0, 'average_retention': 0},
                         {'char': 'income', 'total_retention': 0, 'retention_count': 0, 'average_retention': 0},
                         {'char': 'accidents', 'total_retention': 0, 'retention_count': 0, 'average_retention': 0}
                        ]
    
    sliced_list_of_dicts = sorted_data[:20]
    
    for dict in sliced_list_of_dicts : 
        for ranking_dict in ranking_dict_list :
            if ranking_dict['char'] not in dict['chars'] :
                ranking_dict['total_retention'] += dict['retention_dif']
                ranking_dict['retention_count'] += 1
    
    for ranking_dict in ranking_dict_list :
        ranking_dict['average_retention'] = ranking_dict['total_retention']/ranking_dict['retention_count']
    
    ranked_data = sorted(ranking_dict_list, key=lambda x: x['average_retention'], reverse = False)



with open('filtered_retention.csv', 'w', newline='') as csv_file :
    fieldnames = ['chars', 'nones', 'retention', 'retention_dif', 'clients']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(sorted_data)  

with open('characteristic_ranking.csv', 'w', newline='') as csv_file :
    fieldnames = ['char', 'total_retention', 'retention_count', 'average_retention']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(ranked_data) 


    
