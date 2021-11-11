#!pip install spacy==3.0.0


import pandas as pd
import random
import operator
import spacy
from spacy.pipeline.textcat_multilabel import DEFAULT_MULTI_TEXTCAT_MODEL
from spacy.training import Example
from spacy.util import minibatch, compounding
from Data_annotation import train_dataformatting


def label_list(input_file):
  
  # Meta data of the input file
  meta_Data=input_file.info()

  #exploded input file based on category_ids for getting unique values for label adding in TextCategorizer
  explode_category=(input_file.set_index("text")["category_ids"]
     .str.split(',')
     .explode()
     .rename("category_ids")
     .reset_index())
  Categories=list(explode_category["category_ids"].unique())
  
  return Categories

def data_splitting(input_file):
  # splitting train_test data
  dataset_size=len(input_file)/10
  #print(int(dataset_size*2))
  train_data=input_file[:int(dataset_size*3)]
  test_data=input_file[:-int(dataset_size*2)]
  return train_data, test_data


# function to preprocess-remove stop words from the input text
def remove_Stopwords(text):
    doc=nlp(text)
    stoprm_text=" ".join([str(token) for token in doc if token.is_stop==False])
    return stoprm_text

train_data,test_data=data_splitting(input_file)

# formatted train data
Formatted_traindata=train_dataformatting(train_data)

# creating blank spacy model
nlp = spacy.blank("en")

# model configuration
config = {"threshold": 0.5,"model": DEFAULT_MULTI_TEXTCAT_MODEL}
textcat = nlp.add_pipe("textcat_multilabel", config=config)


# adding labels into modelling-label
for label in Categories:
   textcat.add_label(label)
    
    
    
# training initiation
train_examples = [Example.from_dict(nlp.make_doc(text), label) for text,label in Formatted_traindata]
textcat.initialize(lambda: train_examples, nlp=nlp)


def model_training(formatted_data, out_path,epochs=5):
  # model training 
  #epochs=3  # training iteration
  with nlp.select_pipes(enable="textcat_multilabel"):
      optimizer =nlp.resume_training() # resuming initiated model
      batches = minibatch(Formatted_traindata, size=compounding(4., 32., 1.001))
      for i in range(epochs):
        losses = {}
        for batch in batches:
            for text, label in batch:
                text=remove_Stopwords(text)
                print(text,label)
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, label)
                nlp.update([example], sgd=optimizer, drop=0.2,losses=losses)
   nlp.to_disk(out_path)
   #return out_path
    

model_training(Formatted_traindata,out_path,epochs=5)
