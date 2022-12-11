
import spacy
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import math
import re
from collections import Counter
import json
import pyterrier as pt

import os
os.environ["JAVA_HOME"] = "C:\\Program Files\\Java\\jdk-19"

with open('./resume/resume_output/result.txt', 'r') as file:
    data = file.read().replace('\n', '')
# print(type(data))

query_input = [data]
nlp = spacy.load("en_core_web_sm")

# # Opening JSON file
# f = open('./data/Boston_SE_Job listings_Indeed _Local_.json')
# # returns JSON object as a dictionary
# jobs = json.load(f)


if not pt.started():
    pt.init()

file = pt.io.find_files("./data/Boston_SE_Job listings_Indeed _Local_.json")
file_indexer = pt.FilesIndexer("./index")
indexref = file_indexer.index(file)
index = pt.IndexFactory.of(indexref)

# # iter_indexer = pt.IterDictIndexer(".\\index")
# index_ref = iter_indexer.index(jobs)
# index = pt.IndexFactory.of(index_ref)

# bm25 = pt.BatchRetrieve(index, wmodel="BM25")
# indexref4 = pt.IterDictIndexer("./index", meta={'docno': 20, 'text': 4096}).index(iter_file("'./JobReccer/data/Boston_SE_Job listings_Indeed _Local_.json'"))