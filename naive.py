
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

# Opening JSON file
f = open('./JobReccer/data/Boston_SE_Job listings_Indeed _Local_.json')
# returns JSON object as a dictionary
jd = json.load(f)
document = [] #list of dict
for i in range(len(jd)):
    document.append({"docno":i, "text":jd[i]["Short_Description"] })

# jobD = jd[0]["Short_Description"]

# WORD = re.compile(r"\w+")

# def get_cosine(vec1, vec2):
#     intersection = set(vec1.keys()) & set(vec2.keys())
#     numerator = sum([vec1[x] * vec2[x] for x in intersection])

#     sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
#     sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
#     denominator = math.sqrt(sum1) * math.sqrt(sum2)

#     if not denominator:
#         return 0.0
#     else:
#         return float(numerator) / denominator

# def text_to_vector(text):
#     words = WORD.findall(text)
#     return Counter(words)

# text1 = data
# text2 = jobD

# vector1 = text_to_vector(text1)
# vector2 = text_to_vector(text2)

# cosine = get_cosine(vector1, vector2)

# print("Cosine:", cosine)


if not pt.started():
    pt.init()


iter_indexer = pt.IterDictIndexer("./index", meta={'docno': 20, 'text': 4096})
index_ref = iter_indexer.index(document)
index = pt.IndexFactory.of(index_ref)

bm25 = pt.BatchRetrieve(index, wmodel="BM25")
bm25.search(query_input)
# indexref4 = pt.IterDictIndexer("./index", meta={'docno': 20, 'text': 4096}).index(iter_file("'./JobReccer/data/Boston_SE_Job listings_Indeed _Local_.json'"))