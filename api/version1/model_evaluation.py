import pandas as pd
from Training import data_splitting
import spacy

#Read input file
input_file= pd.read_csv("/content/drive/MyDrive/Doc_classification/train_test_article_data.csv")


train_data,test_data=data_splitting(input_file)

# input for model prediction
testdata=test_data.text[11000]
print(testdata)

#load model
nlp = spacy.load("model_path")

# prediction
doc2 = nlp(testdata)
article_Categories=doc2.cats

#sorted article label based on probability
sorted_d = dict( sorted(article_Categories.items(), key=operator.itemgetter(1),reverse=True))
#print(sorted(article_Categories, reverse=True)) 

# predicton output
print (testdata)
for k,v in sorted(article_Categories.items(), key=operator.itemgetter(1),reverse=True)[:10]:
  print (k,":",v)
