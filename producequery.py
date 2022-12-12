import re


with open('./resume/resume_output/SDE1.txt') as f:
    lines = f.readlines()
year = list()
query = dict()
for line in lines:
    degree1 = re.search('^Bachelor', line)
    degree2 = re.search('^Master', line)
    degree3 = re.search('^Phd', line)
    uni = re.search('^University', line)
    if (uni != None):
        year = [int(s) for s in re.findall(r'\b\d+\b', line)]
    if (degree1 != None):
        query["degree"] = line
    if (degree2 != None):
        query["degree"] = line
    if (degree3 != None):
        query["degree"] = line

    language = re.search('^Language', line)
    if (language != None):
        query["technique"] = line
query["year"] = year[0]

print(query)
