# import PyPDF2
import os

# #create file object variable
# #opening method will be rb
# pdffileobj = open('./resume/SDE1.pdf','rb')
# #create reader variable that will read the pdffileobj
# pdfreader = PyPDF2.PdfFileReader(pdffileobj)
# #This will store the number of pages of this pdf file
# pageobj = pdfreader.getPage(0)
# #(x+1) because python indentation starts with 0.
# #create text variable which will store all text datafrom pdf file
# text=pageobj.extractText()
# #save the extracted data from pdf to a txt file
# #we will use file handling here
# #dont forget to put r before you put the file path
# #go to the file location copy the path by right clicking on the file
# #click properties and copy the location path and paste it here.
# #put "\\your_txtfilename"
# file1=open(r".resume/resume_output/result.txt","a")
# file1.writelines(text)


# # assign directory
# directory = 'resume'
# # iterate over files in
# # that directory

# for filename in os.listdir(directory):
#     if not filename.endswith(".pdf"):
#         continue
#     f = os.path.join(directory, filename)
#     # checking if it is a file
#     if os.path.isfile(f):
#         #print(f)
#         pdffileobj = open(f,'rb')
#         pdfreader = PyPDF2.PdfFileReader(pdffileobj)
#         pageobj = pdfreader.getPage(0)
#         text = pageobj.extractText()
#         prefix = filename.split(".")[0]
#         path = 'resume/resume_output/%s.txt' % prefix
#         file1 = open(path,"a")
#         file1.writelines(text)

import nltk
# nltk.download('omw-1.4')
# nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import json

# lemmatizer = WordNetLemmatizer()
# porter = PorterStemmer()
# print("rocks :", lemmatizer.lemmatize("Apples"))
# print("corpora :", lemmatizer.lemmatize("corpora"))
# print(porter.stem("Cats"))

from pyresparser import ResumeParser

directory = 'resume'
temp = [] # list to store all user info
cnt = 0
# iterate over files in that directory
for filename in os.listdir(directory):
    if not filename.endswith(".pdf"):
        continue
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        #print(f)
        data = ResumeParser(f).get_extracted_data()
        data['User_ID'] = str(cnt)
        cnt += 1
        temp.append(data)

out_file = open('data/all_users.json', "w")
json.dump(temp, out_file, indent = 6)
out_file.close()
        
        