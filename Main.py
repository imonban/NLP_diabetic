import pandas as pd
import sys
from data_filtering import filtering
from combine_cohort import combine
from Classification import annotation
from Patient_level import patient_annotation

## I/O
name = input("Enter file path + file name ")

## filter sentence
l = filtering(name)

## Clean and combine
i = combine(l)

## Classification

try:
    ann_df = annotation(i)
    print('Annotated '+str(ann_df.shape[0]) + ' notes successfully')
except:
    print('Failed for encounter level annotation')
    sys.exit(0)

## compute patient level

if patient_annotation(ann_df) == 1:
    print('Annotated '+str(len(ann_df['PAT_DEID'].unique())) + ' pateints successfully')
else:
    print('Failed for patient level annotation')
