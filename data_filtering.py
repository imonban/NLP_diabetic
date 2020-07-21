import nltk
import pandas as pd
from random import shuffle
import re #regexes
import sys #command line arguments
import os, os.path
from ML_sentence import UIsentence_extraction

#from Text_vectorization import text_vector
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle


#name = input("Enter file path + file name ")







def word_steming(sent):
    stemmer = SnowballStemmer("english")
    #print(outputstr)
    #print exclude_list         
    words = sent.split(' ')
    words = [stemmer.stem(str(word)) for word in words]
    newContent = ' '.join([word for word in words])
    return newContent

def filtering(name):

    k = 0
    l = 0
    # ## read notes -- in chunk to save memory
    for gm_chunk in pd.read_csv(name,chunksize=10000, encoding='latin1'):
        df_relevant = gm_chunk.reset_index(drop = True)
        #extract sentence from the text
        for i in (range(df_relevant.shape[0])):
            p, cgm_sentences, fgm_sentences, fs_sentences, ii_sentences, ip_sentences = UIsentence_extraction(df_relevant.iloc[i])
            if p ==1:
                PAT_DEID = []
                NOTE_DEID = []
                NOTE_DATE = []
                PAT_DEID.append(df_relevant.iloc[i]['PAT_DEID'])
                NOTE_DEID.append(df_relevant.iloc[i]['NOTE_DEID'])
                NOTE_DATE.append(df_relevant.iloc[i]['NOTE_DATE'])
                df_frame_temp = pd.DataFrame({'PAT_DEID':PAT_DEID,'NOTE_DEID':NOTE_DEID,'NOTE_DATE':NOTE_DATE,'CGM_SNIPPET':cgm_sentences, 'FGM_SNIPPET':fgm_sentences, 'FS_SNIPPET':fs_sentences, 'II_SNIPPET':ii_sentences,'IP_sentences':ip_sentences})
                print(df_frame_temp)
                if (k>0):
                    data_frame = data_frame.append(df_frame_temp, ignore_index=True)
                else:
                    data_frame = df_frame_temp
                    k= k+1
        data_frame.to_csv('./outcome/Dia_cohort/diabetic_sentence_'+str(l)+'.csv')
        l = l+1
        return(l)

