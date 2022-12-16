import random, json, time, csv
import numpy as np
import pandas as pd
from os.path import exists
from utils.ui import *
# from fileName import className
from scripts.bm25_module import bm25_pk
from collaborative_filtering import job_job_collab_filter
import sys
import numpy as np
import math

def rerank(bm25_result, cf_result, bm25_top = 20, cf_top = 5):
    """
    Combine bm25 search score and item-item collaborative filter score to calculate a new score.
    Pick top 20 search result in bm25 and top10 results in CF. Unify bm25 score to 5-scaleand then compute 
    fixed weight  score. If either side score is not valid, we let it equal to 0 and weight on the side equal to one
    ***********************************************
    input
    bm25_result, bm25 search results, type: dataframe.
    cf_result, similarly, type: list
    bm25_top, bm25 parameter, type int 
    cf_top, cf parameter, type int 
    ***********************************************
    output
    sorted decreading dictionary (key doc_id int, val new score float) 
    """
    bm25_score_dic, new_score = {}, {}
    max_sc = job_df["score"][0]   # bm25 search result length equal to 1000
    min_sc = job_df["score"][999]
    for i in range(len(bm25_result)) :
        id = int(bm25_result["docid"][i])
        sc = float(bm25_result["score"][i])
        try:
            sc = 5 * (sc - min_sc) / (max_sc - min_sc)
        except:
            sc = 0
        bm25_score_dic[id] = sc


    for i in range(bm25_top):
        id = int(bm25_result["docid"][i])
        bm25_valid = not(bm25_score_dic[id] == 0 or math.isnan(bm25_score_dic[id]))
        cf_valid = not(cf_result[id] == 0 or math.isnan(cf_result[id]))
        if  not bm25_valid and not cf_valid:
            score = 0
        elif not bm25_valid:
            score = cf_result[id]
        elif not cf_valid:
            score = bm25_score_dic[id]
        else: 
            score = 0.7 * bm25_score_dic[id] + 0.3 * cf_result[id]
        new_score[id] = score
    print('new score stage 1',new_score)

    # if valid_count < cf_top, directly return 
    valid_count= sum(math.isnan(x) for x in cf_result)
    print('valid CF score',valid_count)
    if (valid_count < cf_top):
        new_score = dict(sorted(new_score.items(), key=lambda item: item[1],reverse=True))
        return new_score

    top_idx = sorted(range(len(cf_result)), key=lambda i: cf_result[i])[-cf_top:]
    for i in range(cf_top):
        id = top_idx[i]
        try:
            b_sc = bm25_score_dic[id]
        except:
            b_sc = 0
        bm25_valid = not(b_sc == 0 or math.isnan(b_sc))
        cf_valid = not(cf_result[id] == 0 or math.isnan(cf_result[id]))
        if  not bm25_valid and not cf_valid:
            score = 0
        elif  not bm25_valid:
            score = cf_result[id]
        elif  not cf_valid:
            score = bm25_score_dic[id]
        else: 
            score = 0.7 * b_sc + 0.3 * cf_result[id]
        new_score[id] = score

    print('new score stage 2',new_score)
    # sort before return 
    new_score =dict(sorted(new_score.items(), key=lambda item: item[1],reverse=True))
    return new_score



all_jobs_file = "./data/all_jobs.json"
# columns are User_ID, rows are Job_ID
rating_file = "./data/job_user_rating.csv"

with open(all_jobs_file, "r+") as infile:
    jobs = json.load(infile) #Read json file into buffer
    job_dic = {} # key:jb_id val: json object of that job
    for i in range(len(jobs)):
        job_dic[i] = jobs[i]

try:
    df = pd.read_csv(rating_file, header=0)
    print("Loading past rating record...")
    number_of_jobs, number_of_users = df.shape
except OSError as err:
    print("OS Error:", err)
    print(f"No file named", rating_file)
    raise 

uid = sanitised_input("Please enter your user id. ", int, 0, number_of_users-1)
print("Thank you!")
print("Finding best jobs for you... \n")
# start CF to calculate score(the entire column)
file_path = "./data/job_user_rating.csv"
df_ = pd.read_csv(file_path, header=0)
cf_result_ = job_job_collab_filter(uid=uid, df=df_ )

run_flag = True
bm25_here = bm25_pk()
idx = bm25_here.create_idx()
#find jobs to recommend to the user
job_df = bm25_here.bm25_search(uid,idx)
ans = rerank(bm25_result= job_df,cf_result= cf_result_ )
job_id = []         # list to store retrieved id 
for k, v in ans.items():
    job_id.append(k)
round = 0
cnt = 0 
while run_flag == True:
    # select 5 results each round from  top to bottom
    # this number is determined by parameters of fnunction rerank, max(bm25_top,cf_top) /5 = 4 here
    # 4 -1 = 3
    if round  > 3:
        break
    # select top 5 results
    job_ls = [job_dic[job_id[round * 5 + i]] for i in range(5)]
    page_refresh = False
    while not page_refresh:
        #Job display interface 
        for i in range(5):
            print(json.dumps(job_ls[i], indent=4))
        pick = sanitised_input("Which job would like to check  (1 to 5).Enter 0 to refreash a new page.Enter 6 to quit running. \n" + "Enter your pick: ", int, 0, 6)
        if pick == 6:
            run_flag = False
            break
        if pick == 0:
            page_refresh = True
            round += 1
            break
        rating = sanitised_input("How do you like this job from 1 (least favorable) to 5 (most favorable)?  \n" + "Enter your rating: ", int, 1, 5)
        if rating == 0:
            page_refresh = True
        else:
            #update rating
            df.iat[job_id[pick -1], uid] = rating
        df.to_csv(rating_file, index = False)
    
    

    print("-------------------------------\n Looking for another matching job for you ...\n ------------------------------\n")

print("User_ID " + str(uid) + ", Thank you for using JobReccer! \n ****************************************\n")


