
import pyterrier as pt
import pandas as pd
import os

### generate train and test file
### for train, pick user experience--job description pairs whose feedback score >= 4
### generate csv files for bm25 search
import json  
import csv  
from csv import reader
import pandas as pd

def initial():
    # skip first line i.e. read header first and then iterate over each row od csv as a list
    temp = [] # a lisr to store (job_id,user,id)
    score = {} # dictionary, key(job_id,user_id),value(score)
    #with open('data/job_user_rating.csv', 'r') as read_obj:
    with open(os.path.dirname(__file__) + '/../data/job_user_rating.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        row_id = 0
        # Check file as empty
        if header != None:
            # Iterate over each row after the header in the csv
            for row in csv_reader:
                # row variable is a list that represents a row in csv, length = 40 
                for i in range(40):
                    score[(row_id,i)] = str(0)
                    if (len(row[i]) > 0 and float(row[i]) >=0):
                        score[(row_id,i)] = row[i] 
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

    f = open(os.path.dirname(__file__) + '/../data/all_jobs.json')
    # returns JSON object as a dictionary
    data = json.load(f)
    # Iterating through the json list
    job_num = len(data)
    for i in range(job_num):
        des = data[i]["Short_Description"]
        job_dic[str(i)] = des 
    # Closing file
    f.close()    
    
    f = open(os.path.dirname(__file__) + '/../data/all_users.json')
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
    
    with open(os.path.dirname(__file__) + '/../data/job_user_train.txt', 'w') as f1:
        
        for pair in temp:
            job_d = job_dic[pair[0]]
            work_exp = user_dic[pair[1]]
    #    if (len(work_exp.split()) > max_l):
    #    max_l = len(work_exp.split())
            line = job_d +'<SPLIT>'+ work_exp
            f1.write(line)
            f1.write('\n')

    print('length of train files',len(temp))
    # print('max length of work experience in train files',max_l)

    line_num = 0
  
    with open( os.path.dirname(__file__) + '/../data/job_user_test.txt', 'w') as f2:
        for i in range(job_num):
            for j in range(user_num):
                job_d = job_dic[str(i)]
                work_exp = user_dic[str(j)]
                if work_exp is None:
                    work_exp = ''
                line = job_d +'<SPLIT>'+ work_exp
                f2.write(line)
                f2.write('\n')
                line_num += 1

    print('length of test files',line_num)   

    #generate csv files for bm25 search
    import csv  

    header = ['user_expe', 'user_id', 'job_desc', 'job_id','relevance']
 
    with open(os.path.dirname(__file__) + '/../data/job_user.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f,escapechar='\\')
        # write the header
        writer.writerow(header)
        # write the data
        for i in range(job_num):
            for j in range(user_num):
                line = []
                work_exp = user_dic[str(j)]
                if work_exp is None:
                    work_exp = ''
                line.append(work_exp)
                line.append(str(j))
                
                job_d = job_dic[str(i)]
                line.append(job_d)
                line.append(str(i))
                score_here = score[(i,j)]
                line.append(score_here)
                try:
                    writer.writerow(line)
                except:
                    print(line)
                
    df = pd.read_csv(os.path.dirname(__file__) + '/../data/job_user.csv')
    print(df.head())
    return user_dic, job_dic,score






class bm25_pk:
    user_dic = {}
    job_dic = {}
    score_dic = {}
    def __init__(self):
        self.user_dic,self.job_dic,self.score_dic = initial()
    
    def create_idx(self):
        if not pt.started():
            pt.init()

        if not os.path.exists('pd_index' + "/data.properties"):

            df = pd.read_csv('./data/all_jobs.json')
            # print(df.head())
            temp_dic = dict({'text':[],'docno':[]})
            for i in range(len(df)):
                temp_dic['docno'].append(df[i]["Job_ID"])
                temp_dic['text'].append(df[i]["Short_Description"])
            job_df = pd.DataFrame(temp_dic)
            # print(code_df)
            pd_indexer = pt.DFIndexer("pd_index",overwrite = True)
            index_ref = pd_indexer.index(job_df["text"], job_df["docno"])
        else:
            index_ref = pt.IndexRef.of('pd_index'+ "/data.properties")
        index = pt.IndexFactory.of(index_ref)
        print(index.getCollectionStatistics().toString())
        return index

 
    def bm25_search(self,user_id,index):
        '''serach()return type is dataframe
        '''
        bm25 = pt.BatchRetrieve(index, wmodel="BM25")
        return bm25.search(self.user_dic[str(user_id)])


 