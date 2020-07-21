import pandas as pd
import glob

i = 0
for files in glob.glob('./outcome/Dia_cohort/*.csv'):
    try:
        print(files)
        data_sen_filter = pd.read_csv(files)
        data_sen_filter = data_sen_filter.fillna('N/A')
        data_sen_filter = data_sen_filter[~(data_sen_filter['II_SNIPPET'].str.contains('mdi') & ~(data_sen_filter['II_SNIPPET'].str.contains('glucose')|data_sen_filter['II_SNIPPET'].str.contains('insulin')))]
        data_sen_filter = data_sen_filter[~(data_sen_filter['CGM_SNIPPET'].str.contains('medtronic') & ~(data_sen_filter['CGM_SNIPPET'].str.contains('pump')|data_sen_filter['CGM_SNIPPET'].str.contains('glucose')|data_sen_filter['CGM_SNIPPET'].str.contains('insulin')))]
        data_sen_filter.to_csv(files)
    except:
        print('Not able to process'+files)
    
