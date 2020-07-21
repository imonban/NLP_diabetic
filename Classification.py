
# coding: utf-8

from keras.preprocessing.text import Tokenizer
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from nltk.corpus import stopwords
import re
from random import shuffle



# In[ ]:


def remove_number(snip):
    output = re.sub(r'\d+', ' ', snip)
    return output


# In[ ]:


#compute the word map based on common-term dictionary
GeneralwordMap = {}
Gterms = []
with open('./dic/clever_base_terminologyv2.txt', 'r') as termFile:
    for line in termFile:
        words = line.split('|')
        if len(words) == 3:
            GeneralwordMap[' ' + words[1].lstrip(' ').rstrip(' ') + ' '] = ' ' + words[2].replace('\n', '') + ' '
            Gterms.append(' ' + words[1].lstrip(' ').rstrip(' ') + ' ')
Gterms = sorted(Gterms, key=len, reverse=True)
def G_mapping(snip):
    snip = snip.lower()
    for term in Gterms:
        snip = snip.replace(term, GeneralwordMap[term])
    return snip


# In[ ]:

def annotation(i):
    pat_id = pd.read_csv('./data/Diabetic_cohort.csv')
    ann_df= pd.read_csv('./data/Glucose_annotated_v2.csv')
    
    ann_df.drop_duplicates(subset=['PAT_DEID','SNIPPET','DATE'], keep='first', inplace=True)
    ann_df['Snippet'] = ann_df['SNIPPET'].apply(remove_number)
    #ann_df['Snippet'] = ann_df['Snippet'].apply(D_mapping)
    ann_df['Snippet'] = ann_df['Snippet'].apply(G_mapping)

    with open('./model/vectorizer.pkl', 'rb') as fin:
        t = pickle.load(fin)
    with open('./model/dia_class.pkl', 'rb') as fin:
        clf_dia = pickle.load(fin)
    with open('./model/thera_class.pkl', 'rb') as fin:
        clf_thera = pickle.load(fin)
    docs_test = list(ann_df['Snippet'])
    encoded_docs_test = t.transform(docs_test)
    random_pred = clf_thera.predict(encoded_docs_test)
    anno_thera = []

    for i in range(len(random_pred)):
        if random_pred[i]==2:
            anno_thera.append('IP') 
        if random_pred[i]==0:
            anno_thera.append('Exclude') 
        if random_pred[i]==1:
            anno_thera.append('II') 
    ann_df['Anno_Thera'] = anno_thera


    # ## Diagnostic
    random_pred = clf_dia.predict(encoded_docs_test)
    anno_dia = []

    for i in range(len(random_pred)):
        if random_pred[i]==2:
            anno_dia.append('FS') 
        if random_pred[i]==0:
            anno_dia.append('CGM') 
        if random_pred[i]==1:
            anno_dia.append('Exclude') 

    ann_df['Anno_Diagnosis'] = anno_dia


    # ## Save annotated data


    ann_df.to_csv('./outcome/annotated_encounter.csv', encoding='latin1')
    return ann_df

