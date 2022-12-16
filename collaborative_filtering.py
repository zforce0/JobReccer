import pandas as pd
import numpy as np
import math
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics.pairwise import cosine_similarity

file_path = "./data/job_user_rating.csv"
df = pd.read_csv(file_path, header=0)


def job_job_collab_filter(uid, df, k=3):
    """
    input
    uid: user id. type int; df,dataframe of rating file type dataframe; k:how many similar items to pick
    *****************************
    output
    return an array of all jobs rating in job_id incresing order(existing + predicted) for the given user
    type pandas.core.series.Series(usage similar to list)
    """
    global_mean = sum(df.sum(skipna=True))/df.size
    uid_ratings = df.iloc[:,uid]
    uid_baseline = uid_ratings.mean(skipna=True) - global_mean
    df_row_diff = df.sub(df.mean(axis=1), axis=0)
    cos_sim = cosine_similarity(df_row_diff.fillna(0))
    # print(f'uid base is: ', uid_baseline)
    for jid, rating in enumerate(uid_ratings):
        if math.isnan(rating): #no existing user rating, use cf
            # print(f'jid is: ', jid)
            temp_ratings_uid = uid_ratings.fillna(0)
            # prep k largest for cos_sim
            largest_k_indicies = np.argpartition(cos_sim[:,jid],-k)[-k:]
            k_nearest_sims = cos_sim[:,jid]
            for i in range(len(cos_sim[:,jid])):
                if i not in largest_k_indicies:
                    k_nearest_sims[i] = 0
            # print(f'k_nearest sims: ', k_nearest_sims)
            # print(f'dot prod with cos_sim: ', temp_ratings_uid.dot(k_nearest_sims))
            # print(f'sum of sims: ', sum(cos_sim[:,jid]))
            # print(f'normalizeed dot prod with cos_sim is: ', temp_ratings_uid.dot(k_nearest_sims)/sum(k_nearest_sims))
            # print(f'predicted rating is: ', temp_ratings_uid.dot(k_nearest_sims)/sum(k_nearest_sims) + cos_sim[:,jid].mean() + uid_baseline)

            uid_ratings[jid] = temp_ratings_uid.dot(k_nearest_sims)/sum(k_nearest_sims)\
                + uid_baseline + cos_sim[:,jid].mean()
        else:
            pass
    return uid_ratings