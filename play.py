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
data = ResumeParser('resume/data11_.pdf').get_extracted_data()
# print(data)
print(json.dumps(data, indent = 6))