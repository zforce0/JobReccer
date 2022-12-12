import random, json, time, csv
import numpy as np
import pandas as pd
from os.path import exists



all_jobs_file = "../data/all_jobs.json"
with open(all_jobs_file, "r+") as infile:
    jobs = json.load(infile) #Read json file into buffer

number_of_jobs = len(jobs)
number_of_users = 40

def sanitised_input(prompt, type_=None, min_=None, max_=None, range_=None):
    if min_ is not None and max_ is not None and max_ < min_:
        raise ValueError("min_ must be less than or equal to max_.")
    while True:
        ui = input(prompt)
        if type_ is not None:
            try:
                ui = type_(ui)
            except ValueError:
                print("Input type must be {0}.".format(type_.__name__))
                continue
        if max_ is not None and ui > max_:
            print("Input must be less than or equal to {0}.".format(max_))
        elif min_ is not None and ui < min_:
            print("Input must be greater than or equal to {0}.".format(min_))
        elif range_ is not None and ui not in range_:
            if isinstance(range_, range):
                template = "Input must be between {0.start} and {0.stop}."
                print(template.format(range_))
            else:
                template = "Input must be {0}."
                if len(range_) == 1:
                    print(template.format(*range_))
                else:
                    expected = " or ".join((
                        ", ".join(str(x) for x in range_[:-1]),
                        str(range_[-1])
                    ))
                    print(template.format(expected))
        else:
            return ui
# Define headers for job_user_rating.csv
# columns are User_ID, rows are Job_ID
rating_file = "../data/job_user_rating.csv"

print("Starting rating program...")
time.sleep(0.3)
print("You will be impersonating 20 different users to rate how desirable the job recommendated to you.")
time.sleep(0.5)
print("Initiating...")
time.sleep(0.3)

if exists(rating_file):
    df = pd.read_csv("../data/job_user_rating.csv", header=0)
    print("Loading past rating record...")
else:
    print("##############################\n")
    print("Past rating file not found, creating one...")
    df = pd.DataFrame(np.nan, index=range(number_of_jobs), columns=range(number_of_users))
    df.to_csv("../data/job_user_rating.csv", index=True)

for u in range(number_of_users):
    uid = sanitised_input("Please enter your user id. (for test user, in [0,39]", int, 0, number_of_users-1)
    print("Thank you!")
    print("Directing you to rating system... \n")
    time.sleep(0.3)
    for _ in range(3):
        #randomly choose(recommend) one job for rating
        job = random.choice(jobs)
        jid = int(job["Job_ID"])
        print(job)
        rating = sanitised_input("Please rate your favorness of this job in integer between 1 (least favorable) to 5 (most favorable). \n" + "Enter your rating: ", int, 1, 5)
        
        #update rating
        df.iat[jid, uid] = rating

        print("----------------------------------\n")
    print("User_ID " + str(uid) + ", Thank you for your rating! \n ****************************************\n")
    df.to_csv("../data/job_user_rating.csv", index=False)

