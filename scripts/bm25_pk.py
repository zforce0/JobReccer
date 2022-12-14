from train_search_prep import initial
import pyterrier as pt
import pandas as pd
import os

class bm25_search:
    def __init__(self):
        self.user_dic,self.job_dic,self.score_dic = initial()
    
    def create_idx():
        df = pd.read_csv('data/job_user.csv')
        print(df.head())
        if not pt.started():
            pt.init()
            

        temp_dic = dict({'text':[],'docno':[]})
        job_dic[str(i)] = des 
        for i in range(len(job_dic)):
            temp_dic['docno'].append(str(i))
            temp_dic['text'].append(job_dic[str(i)])

        job_df = pd.DataFrame(temp_dic)
        # print(code_df)
        pd_indexer = pt.DFIndexer("./pd_index",overwrite = True)
        index_ref = pd_indexer.index(job_df["text"], job_df["docno"])
        index = pt.IndexFactory.of(index_ref)
        print(index.getCollectionStatistics().toString())


    def bm25_search(user_id,):

 