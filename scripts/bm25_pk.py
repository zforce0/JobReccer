from train_search_prep import initial
import pyterrier as pt
import pandas as pd
import os

class bm25_pk:
    user_dic = {}
    job_dic = {}
    score_dic = {}
    def __init__(self):
        self.user_dic,self.job_dic,self.score_dic = initial()
    
    def create_idx(self):
        if not pt.started():
            pt.init()

        if not os.path.exists('./pd_index' + "/data.properties"):

            df = pd.read_csv('../data/all_jobs.json')
            # print(df.head())
            temp_dic = dict({'text':[],'docno':[]})
            for i in range(len(df)):
                temp_dic['docno'].append(df[i]["Job_ID"])
                temp_dic['text'].append(df[i]["Short_Description"])
            job_df = pd.DataFrame(temp_dic)
            # print(code_df)
            pd_indexer = pt.DFIndexer("./pd_index",overwrite = True)
            index_ref = pd_indexer.index(job_df["text"], job_df["docno"])
        else:
            index_ref = pt.IndexRef.of('./pd_index'+ "/data.properties")
        index = pt.IndexFactory.of(index_ref)
        print(index.getCollectionStatistics().toString())
        return index


    def bm25_search(self,user_id,index):
        bm25 = pt.BatchRetrieve(index, wmodel="BM25")
        return bm25.search(self.user_dic[str(user_id)])


 