# Weakly supervised natural language processing for assessing patient-centered outcome (UI/BD) following prostate cancer treatment
We call it weakly supervised since we extract urinary incontinence (UI) status from a range of clinical notes without considering manually engineered classification rules or large-scale manual annotations. For learning, the method exploits two sources of pre-existing medical knowledge: (1) domain-specific dictionaries that have been previously developed for implementing a rule-based information extraction system; and (2) publicly available CLEVER terminology that represents a vocabulary of terms that often present within clinical narratives. 


Our UI annotation code takes a csv file with raw note data as input with mandatory fields (case- sensitive) :
1. 'PAT_DEID' - de-indentified patient id for tracking the status of same patient
2. 'NOTE_DEID' - de-indentified note id 
3. 'NOTE' - raw free-text notes, preferably in ASCII coding  
4. 'NOTE_DATE' - date formatted

Genrates a csv file with note level annotations for Urinary Incontinence. 

## Dependencies needed

1. Python 3
2. NLTK
3. Pandas
4. sklearn
5. pickle

## Execution (Very simple running!! Trust me)

1. Run the Main.py from terminal as: python Main.py
2. Once it prompts: "Enter file path + file name ", provide the file location. Notes should be saved in a single csv. Find example in ./data/
3. And that's it!! It will save the outcome in './outcome/' named as 'Note_level_outcome.csv'

### Enjoy!! 
### BTW don't waste you time. If something does not work, please reach imonb@stanford.edu 
"# NLP_diabetic" 
