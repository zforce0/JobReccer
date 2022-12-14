import json  
from csv import reader
import pandas as pd
import numpy as np
import math
import io

rating_file = '../data/job_user_rating.csv'
jobs_file = '../data/all_jobs.json'
users_file = '../data/all_users.json'
train_file = '../data/job_user_train.txt'
test_file = '../data/job_user_test.txt'
validation_file = '../data/job_user_validation.txt'

with open(jobs_file, "r+") as infile:
    jobs = json.load(infile) #Read json file into buffer

try:
    rating_df = pd.read_csv(rating_file, header=0)
    print("Loading past rating records...")
    number_of_jobs, number_of_users = rating_df.shape
except OSError as err:
    print("OS Error:", err)
    print(f"No file named", rating_file)
    raise 

with open(jobs_file, 'r') as jobs:
    job_obj = json.load(jobs)
# print(len(job_obj))
res = list(filter(lambda x:x["Job_ID"]=="31", job_obj))[0]
# print(f'jid 31 is:', res)
# print(f'desc of jid 31 is:', res['Short_Description'])
# print(type(res))

with open(users_file, 'r') as users:
    user_obj = json.load(users)

# print(user_obj)
ures = list(filter(lambda x:x["User_ID"]=="12", user_obj))[0]
# print(f'user exp: ', ures['experience'])

valid_rating_lookup_table = {}
for uid, rating_srs in rating_df.iteritems():
    counter = 0
    for jid, rating in rating_srs.iteritems():
        if not math.isnan(rating):
            valid_rating_lookup_table[(uid,str(jid))] = rating
            counter += 1
#     print(f'uid: ', uid, 'has', counter, 'ratings \n')
# print(valid_rating_lookup_table)
print(len(valid_rating_lookup_table))

# Prepare dataframe for output
row_list = []
for (row,((uid,jid), rating)) in enumerate(valid_rating_lookup_table.items()):
    rel_score = rating
    user = list(filter(lambda x:x["User_ID"]==uid, user_obj))[0]
    job = list(filter(lambda x:x["Job_ID"]==jid, job_obj))[0]
    job_url = job['Job_Detail_Link']
    job_title = job['Job_Title']
    query_exp = user['experience']
    job_desc = job['Short_Description']
    row_list.append([rel_score,job_url,job_title,query_exp,job_desc])
df_output = pd.DataFrame(row_list)
df_output.columns = ['rel_score', 'job_url', 'job_title', 'query_exp', 'job_desc']
print(df_output.head(5))
print(len(df_output))

# Split the valid data into training and testing sets and write output files
df_train = df_output.sample(frac = 0.7)
df_test = df_output.drop(df_train.index).sample(frac = 0.5)
df_validation = df_output.drop(df_train.index).drop(df_test.index)
print(f'number of training samples: ', len(df_train))
print(f'number of testing samples: ', len(df_test))
print(f'number of validation samples: ', len(df_validation))

train_line_num = 0
with io.open(train_file, mode='w', encoding='utf-8') as file_output:
    for i in range(len(df_train)):
        line = ''.join(str(df_train.iloc[i][0]) + '<SPLIT>' + \
            str(df_train.iloc[i][1]) + '<SPLIT>' + \
            str(df_train.iloc[i][2]) + '<SPLIT>' + \
            str(df_train.iloc[i][3]) + '<SPLIT>' + \
            str(df_train.iloc[i][4]))
        file_output.write(line)
        file_output.write('\n')
        train_line_num += 1
print(f'train line number is: ', train_line_num)

test_line_num = 0
with io.open(test_file, mode='w', encoding='utf-8') as file_output:
    line = ''
    for i in range(len(df_test)):
        line = str(df_test.iloc[i][0]) + '<SPLIT>' + \
            str(df_test.iloc[i][1]) + '<SPLIT>' + \
            str(df_test.iloc[i][2]) + '<SPLIT>' + \
            str(df_test.iloc[i][3]) + '<SPLIT>' + \
            str(df_test.iloc[i][4])
        file_output.write(line)
        file_output.write('\n')
        test_line_num += 1

print(f'testline number is: ', test_line_num)

validation_line_num = 0
with io.open(validation_file, mode='w', encoding='utf-8') as file_output:
    line = ''
    for i in range(len(df_test)):
        line = str(df_test.iloc[i][0]) + '<SPLIT>' + \
            str(df_test.iloc[i][1]) + '<SPLIT>' + \
            str(df_test.iloc[i][2]) + '<SPLIT>' + \
            str(df_test.iloc[i][3]) + '<SPLIT>' + \
            str(df_test.iloc[i][4])
        file_output.write(line)
        file_output.write('\n')
        validation_line_num += 1

print(f'validation number is: ', validation_line_num)