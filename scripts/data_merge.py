import json

files=["../data/Atlanta_DS_Job listings_Indeed _Local_.json",
"../data/Chicago_DS_Job listings_Indeed _Local_.json",
"../data/New-York_DS_Job listings_Indeed _Local_.json",
"../data/Seattle_DS_Job listings_Indeed _Local_.json",
"../data/Boston_SE_Job listings_Indeed _Local_.json",
"../data/New-York_SE_Job listings_Indeed _Local_.json",
"../data/San-Jose_SE_Job listings_Indeed _Local_.json",
"../data/Santa-Clara_SE_Job listings_Indeed _Local_.json"]

def merge_JsonFiles(filename):
    result = list()
    for f1 in filename:
        with open(f1, 'r') as infile:
            result.extend(json.load(infile))

    with open('../data/all_jobs.json', 'w') as output_file:
        json.dump(result, output_file)

from os.path import exists

all_jobs_file = "../data/all_jobs.json"
merge_exists = exists(all_jobs_file)

if merge_exists:
    with open(all_jobs_file, "r+") as infile:
        jobs = json.load(infile) #Read json file into buffer
    if "Job_ID" not in jobs[0] or jobs[0]["Job_ID"] !=0:
        infile.close()
        writeFile = open(all_jobs_file, "w+")
        for id,job in enumerate(jobs):
            assign_ID = {"Job_ID": str(id)}
            job.update(assign_ID)
        writeFile.write(json.dumps(jobs))
        writeFile.close()
else:
    merge_JsonFiles(files)

