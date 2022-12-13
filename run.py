import random, json, time, csv
import numpy as np
import pandas as pd
from os.path import exists
from utils.ui import *

all_jobs_file = "./data/all_jobs.json"
# columns are User_ID, rows are Job_ID
rating_file = "./data/job_user_rating.csv"

with open(all_jobs_file, "r+") as infile:
    jobs = json.load(infile) #Read json file into buffer

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
time.sleep(0.3)
run_flag = True
while run_flag ==True:
    #Recommend jobs for the user
    job = random.choice(jobs)

    jid = int(job["Job_ID"])

    #Job display interface 
    print(json.dumps(job, indent=4))
    rating = sanitised_input("How do you like this job from 1 (least favorable) to 5 (most favorable)? Enter 0 to exit. \n" + "Enter your rating: ", int, 0, 5)

    if rating == 0:
        run_flag = False
    else: 
        #update rating
        df.iat[jid, uid] = rating
    df.to_csv(rating_file, index=False)
    print("-------------------------------\n Looking for another matching job for you ...\n ------------------------------\n")

print("User_ID " + str(uid) + ", Thank you for using JobReccer! \n ****************************************\n")

