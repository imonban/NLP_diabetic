import glob
import pandas as pd


def combine(l):
    pat_id = pd.read_csv('./data/Diabetic_cohort.csv')
    p_id = list(pat_id.PAT_DEID.unique())
    snip = []
    date = []
    ids = []

    i = 0
    for files in glob.glob('./outcome/Dia_cohort/*.csv'):
        print(files)
        i = i +1
        data_sen_filter = pd.read_csv(files)
        data_sen_filter = data_sen_filter[data_sen_filter['PAT_DEID'].isin(p_id)]
        data_sen_filter = data_sen_filter.reset_index(drop = True)
        data_sen_filter = data_sen_filter.fillna('N/A')
        for j in range(data_sen_filter.shape[0]):        
            if data_sen_filter.iloc[j]['CGM_SNIPPET']!='N/A':
                ids.append(data_sen_filter.iloc[j]['PAT_DEID'])
                snip.append(data_sen_filter.iloc[j]['CGM_SNIPPET'])
                date.append(data_sen_filter.iloc[j]['NOTE_DATE'])
            if data_sen_filter.iloc[j]['FS_SNIPPET']!='N/A':
                ids.append(data_sen_filter.iloc[j]['PAT_DEID'])
                snip.append(data_sen_filter.iloc[j]['FS_SNIPPET'])
                date.append(data_sen_filter.iloc[j]['NOTE_DATE'])
            if data_sen_filter.iloc[j]['FGM_SNIPPET']!='N/A':
                ids.append(data_sen_filter.iloc[j]['PAT_DEID'])
                snip.append(data_sen_filter.iloc[j]['FGM_SNIPPET'])
                date.append(data_sen_filter.iloc[j]['NOTE_DATE'])
            if data_sen_filter.iloc[j]['II_SNIPPET']!='N/A':
                ids.append(data_sen_filter.iloc[j]['PAT_DEID'])
                snip.append(data_sen_filter.iloc[j]['II_SNIPPET'])
                date.append(data_sen_filter.iloc[j]['NOTE_DATE'])
            if data_sen_filter.iloc[j]['IP_sentences']!='N/A':
                ids.append(data_sen_filter.iloc[j]['PAT_DEID'])
                snip.append(data_sen_filter.iloc[j]['IP_sentences'])
                date.append(data_sen_filter.iloc[j]['NOTE_DATE'])
            
    ann_df = pd.DataFrame({'PAT_DEID':ids,'SNIPPET':snip, 'DATE':date})
    ann_df.to_csv('./data/Glucose_annotated_v2.csv')
    return i
