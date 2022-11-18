import json
ATL_DS=open("../data/Atlanta_DS_Job listings_Indeed _Local_.json")
CHI_DS=open("../data/Chicago_DS_Job listings_Indeed _Local_.json")
NYC_DS=open("../data/New-York_DS_Job listings_Indeed _Local_.json")
SEA_DS=open("../data/Seattle_DS_Job listings_Indeed _Local_.json")

BOS_SE=open("../data/Boston_SE_Job listings_Indeed _Local_.json")
NYC_SE=open("../data/New-York_SE_Job listings_Indeed _Local_.json")
SJ_SE=open("../data/San-Jose_SE_Job listings_Indeed _Local_.json")
SC_SE=open("../data/Santa-Clara_SE_Job listings_Indeed _Local_.json")

all_jobs = open("../data/all_jobs.json")

data_ATL_DS = json.load(ATL_DS)
data_CHI_DS = json.load(CHI_DS)
data_NYC_DS = json.load(NYC_DS)
data_SEA_DS = json.load(SEA_DS)

data_BOS_SE = json.load(BOS_SE)
data_NYC_SE = json.load(NYC_SE)
data_SJ_SE = json.load(SJ_SE)
data_SC_SE = json.load(SC_SE)

data_all_jobs = json.load(all_jobs)

print(f'numeber of jobs in data_ATL_DS: ', len(data_ATL_DS), "\n")
print(f'numeber of jobs in data_CHI_DS: ', len(data_CHI_DS), "\n")
print(f'numeber of jobs in data_NYC_DS: ', len(data_NYC_DS), "\n")
print(f'numeber of jobs in data_SEA_DS: ', len(data_SEA_DS), "\n")

print(f'numeber of jobs in data_BOS_SE: ', len(data_BOS_SE), "\n")
print(f'numeber of jobs in data_NYC_SE: ', len(data_NYC_SE), "\n")
print(f'numeber of jobs in data_SJ_SE: ', len(data_SJ_SE), "\n")
print(f'numeber of jobs in data_SC_SE: ', len(data_SC_SE), "\n")

print(f'Number of all jobs: ',len(data_all_jobs))
