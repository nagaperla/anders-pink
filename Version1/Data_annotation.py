
#import the packages
import pandas as pd
import random
import operator



# Formatting training data before training
def train_dataformatting(train_data):
    train_formatted_tup=[]
    for index,row in train_data.iterrows():
        text=row["text"]
        labels=row["category_ids"].split(',')
        label_score=row["category_scores"].split(',')
        label_dic={}
        for label in range(len(labels)):
            label_dic[labels[label]]=label_score[label]
        train_formatted_tup.append((text,{"cats":label_dic}))
    return train_formatted_tup
