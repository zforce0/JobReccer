# generate train and test file
# for train, pick user experience--job description pairs whose feedback score >= 4
import json  
from csv import reader
# skip first line i.e. read header first and then iterate over each row od csv as a list
temp = [] # a lisr to store (job_id,user,id)
with open('data/job_user_rating.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    header = next(csv_reader)
    row_id = 0
    # Check file as empty
    if header != None:
        # Iterate over each row after the header in the csv
        for row in csv_reader:
            # row variable is a list that represents a row in csv, length = 40 
            for i in range(40):
                if (len(row[i]) > 0 and float(row[i]) >=4.0):
                    user_id = i
                    job_id = row_id
                    temp.append((str(job_id),str(user_id)))        
            row_id = row_id + 1
            
#build dict of (user_id, experience), (job_id , job description)
user_dic = {} 
user_num = 0
job_dic = {}
job_num = 0
 # Opening JSON file
f = open('data/all_jobs.json')
# returns JSON object as a dictionary
data = json.load(f)
# Iterating through the json list
job_num = len(data)
for i in range(job_num):
    des = data[i]["Short_Description"]
    job_dic[str(i)] = des 
# Closing file
f.close()    
    
f = open('data/all_users.json')
data = json.load(f)
user_num = len(data)
for i in range(user_num):
    exper = data[i]["experience"]
    if exper is None:
        user_dic[str(i)] = None
        continue
    exper = ' '.join(exper)
    if (len(exper.split()) > 200):
        exper = ' '.join(exper.split()[:200])
    user_dic[str(i)] = exper 
f.close()            

max_l = 0 
with open('data/job_user_rating_train.txt', 'w') as f:
    for pair in temp:
        job_d = job_dic[pair[0]]
        work_exp = user_dic[pair[1]]
#         if (len(work_exp.split()) > max_l):
#             max_l = len(work_exp.split())
        line = job_d +'<SPLIT>'+ work_exp
        f.write(line)
        f.write('\n')
print('length of train files',len(temp))
# print('max length of work experience in train files',max_l)

line_num = 0
with open('data/job_user_rating_test.txt', 'w') as f:
    for i in range(job_num):
        for j in range(user_num):
            job_d = job_dic[str(i)]
            work_exp = user_dic[str(j)]
            if work_exp is None:
                work_exp = ''
            line = job_d +'<SPLIT>'+ work_exp
            f.write(line)
            f.write('\n')
            line_num += 1
print('length of test files',line_num)   
