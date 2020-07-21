import nltk
import pandas as pd
from random import shuffle
import re #regexes
import sys #command line arguments
import os, os.path
import numpy as np
import string
from nltk.corpus import stopwords


#text pre-processing and tagging
from IPython.display import HTML as html_print
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize


## Dictionary reading

df = pd.read_csv('./dic/Dictionary.csv', encoding = 'latin1')
df = df.fillna('N/A')
#CGM
df_cgm = df[df['Category']=='Sensor general category']
terms = df_cgm['Terms'].unique()

cgm_term = []
cgm_map = {}
cgm_corr = []

for i in terms:
    i = re.sub(r'[^\x00-\x7F]+',' ', i)
    cgm_map[' ' + str(i).lower() + ' '] = ' ' + str(i) + ' '
    cgm_term.append(' ' + str(i).lower() + ' ')
    #cgm_corr.append(df_cgm[df_cgm['Terms']==i]['Corr_term'])        
cgm_term.sort(key = len)
cgm_term.reverse()
print(cgm_term)
#FGM
df_fgm = df[df['Category']=='Flash Glucose monitoring']
terms = df_fgm['Terms'].unique()
fgm_term = []
fgm_map = {}
for i in terms:
    i = re.sub(r'[^\x00-\x7F]+',' ', i)
    fgm_map[' ' + str(i).lower() + ' '] = ' ' + str(i) + ' '
    fgm_term.append(' ' + str(i).lower() + ' ')
fgm_term.sort(key = len)
fgm_term.reverse()

#FS
df_fs = df[df['Category']=='Fingerstick']
terms = df_fs['Terms'].unique()
fs_term = []
fs_map = {}
for i in terms:
    i = re.sub(r'[^\x00-\x7F]+',' ', i)
    fs_map[' ' + str(i).lower() + ' '] = ' ' + str(i) + ' '
    fs_term.append(' ' + str(i).lower() + ' ')
fs_term.sort(key = len)
fs_term.reverse()

#Insulin-injection
df_ii = df[df['Category']=='Insulin injection']
terms = df_ii['Terms'].unique()
ii_term = []
ii_map = {}
ii_corr = []
for i in terms:
    i = re.sub(r'[^\x00-\x7F]+',' ', i)
    ii_map[' ' + str(i).lower() + ' '] = ' ' + str(i) + ' '
    ii_term.append(' ' + str(i).lower() + ' ')
    #ii_corr.append(df_ii[df_ii['Terms']==i]['Corr_term'])
ii_term.sort(key = len)
ii_term.reverse()
#Insulin-pump
df_ip = df[df['Category']=='Insulin pump']
terms = df_ip['Terms'].unique()
ip_term = []
ip_map = {}
for i in terms:
    i = re.sub(r'[^\x00-\x7F]+',' ', i)
    ip_map[' ' + str(i).lower() + ' '] = ' ' + str(i) + ' '
    ip_term.append(' ' + str(i).lower() + ' ')
ip_term.sort(key = len)
ip_term.reverse()

date_input = "" #global for date input (can be removed if we use lambdas later)
pairs = {} #global variable to count common pairs
exclude_list =  set(stopwords.words('english'))

re1='((?:[0]?[1-9]|[1][012])[-:\\/.](?:(?:[0-2]?\\d{1})|(?:[3][01]{1}))[-:\\/.](?:(?:[1]{1}\\d{1}\\d{1}\\d{1})|(?:[2]{1}\\d{3})))(?![\\d])'	# MMDDYYYY 1

date = re.compile(re1,re.IGNORECASE|re.DOTALL)

def concatenate_into_string(infile):
    total_text = ""
    for line in infile:
        line = line.replace('\n', ' ')
        total_text += line
    return total_text

def remove_forbidden_tokens(output, exclude_list):
    for item in exclude_list:
        output = re.sub(r""+re.escape(item)+r"", " ", output)
    return output


'''
The primary method. Takes input as a string and an exclusion list of strings and outputs a string.
'''
def preprocess(inputstr):
    output = inputstr.lower() #tolowercase
    output = re.sub(date, ' ', inputstr) #processes dates of the form MM/DD/YYYY
    
    output = re.sub(r'([+-]?\\d*\\.\\d+)(?![-+0-9\\.])', ' ', output) #remove special characters
    #output = re.sub('['+string.punctuation+']', ' ', output)
    #words = output.split(' ')
    #words = [str(convert2int(word)) for word in words]
    #output = ' '.join(words)
   #num = filter(str.isdigit, output)
 
    #output = output.replace(i,' ') #try without the number
    #output = remove_forbidden_tokens(output, exclude_list)
    output = re.sub(r" +", " ", output) #remove extraneous whitespace
    return output

def dateprocess(date):
    string = str(date)
    splitdate = string.split()[0].split('-')
    newformatted = splitdate[2] +'/'+ splitdate[1]+'/'+splitdate[0]
    return newformatted 



def cstr(s, color='black'):
    return "<text style=color:{}>{}</text>".format(color, s)

   
   
def UIsentence_extraction(df_relevant):
    Dt = 'pads pad leakage'
    try:
        rawnote = str(df_relevant['NOTE'])
    except:
        rawnote = ' '
    
    rawnote = rawnote.split('PLAN:')[0]       
    
    #content  = rawnote.lower();
    str1 = rawnote
    str1 = ' '+str1+' '
    sentences_cgm = []
    sentences_fgm = []
    sentences_fs = []
    sentences_ii = []
    sentences_ip = []
    str1 = re.sub(r'[^\x00-\x7f]',r' ', str1)
    re1='(\\d+)'	# Integer Number 1
    re2='(\\.)'	# Any Single Character 1
    re3='( )'	# White Space 1
    re4='((?:[a-z][a-z]+))'	# Word 1
    p = 0
    rg = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)
    str1 = re.sub(rg,r'\n', str1)
    str1 = re.sub('\s\s\s+','\n',str1)
    str1 = str1.replace('\r', '\n')
    str1 = str1.replace('#', '\n')
    paragraphs = [p for p in str1.split('\n') if p]
    #paragraphs = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', str1)
    #paragraphs = filter(None, re.split("([A-Z][^A-Z]*)", str1))
    for paragraph in paragraphs:
        temp_sentences = sent_tokenize(paragraph)
        for i in range(len(temp_sentences)):
            temp_sentences[i] = temp_sentences[i].lower()
            for term in cgm_term:
                #if term in temp_sentences[i]: ## Alternative approach: more flexible
                if re.search(r'\b' + term + r'\b', temp_sentences[i]):
                    sentences_cgm.append(temp_sentences[i])
                    p = 1
            for term in fgm_term:
                #if term in temp_sentences[i]: ## Alternative approach: more flexible
                if re.search(r'\b' + term + r'\b', temp_sentences[i]):
                    sentences_fgm.append(temp_sentences[i])
                    p = 1
            for term in fs_term:
                #if term in temp_sentences[i]: ## Alternative approach: more flexible
                if re.search(r'\b' + term + r'\b', temp_sentences[i]):
                    sentences_fs.append(temp_sentences[i])
                    p = 1
            for term in ii_term:
                #if term in temp_sentences[i]: ## Alternative approach: more flexible
                if re.search(r'\b' + term + r'\b', temp_sentences[i]):
                    sentences_ii.append(temp_sentences[i])
                    p = 1
            for term in ip_term:
                #if term in temp_sentences[i]: ## Alternative approach: more flexible
                if re.search(r'\b' + term + r'\b', temp_sentences[i]):
                    sentences_ip.append(temp_sentences[i])
                    p = 1
    
    return p, ' '.join(sentences_cgm), ' '.join(sentences_fgm), ' '.join(sentences_fs), ' '.join(sentences_ii), ' '.join(sentences_ip)
    
