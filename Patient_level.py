import pandas as pd

def patient_annotation(df):
    ## change from FS to CGM -- change from II to IP -- from CGM to FS -- from IP to II
    ids = df['PAT_DEID'].unique()
    df['DATE'] = pd.to_datetime(df['DATE'])
    Diagnosis_date1 = []
    Thera_date2 = []
    for i in ids:
        temp = df[df['PAT_DEID']==i].sort_values(by=['DATE'])
        temp = temp.reset_index(drop =True)
        ## Thera
        tempT = temp[temp['Anno_Diagnosis']!='Exclude']
        tempL = list(tempT['Anno_Diagnosis'])
        date = list(tempT['DATE'])
        if all(x=='FS' for x in tempL):
            Diagnosis_date1.append(' ')
        else:
            index = tempL.index('CGM')
            Diagnosis_date1.append(date[index])
        ## Diagnosis
        tempT = temp[temp['Anno_Thera']!='Exclude']
        tempL = list(tempT['Anno_Thera'])
        date = list(tempT['DATE'])
        if all(x=='II' for x in tempL):
            Thera_date2.append(' ')
        else:
            index = tempL.index('IP')
            Thera_date2.append(date[index])
    df_ann = pd.DataFrame({'PAT_DEID':ids, 'FS->CGM date':Diagnosis_date1, 'II->IP date':Thera_date2})
    try:
        df_ann.to_csv('./outcome/patient_level_ann.csv', encoding='latin1')
        return 1
    except:
        return 0
