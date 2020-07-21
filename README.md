# Natural language processing for extracting Insulin pump and CGM info from clinical text



Our annotation code takes a csv file with raw note data as input with mandatory fields (case- sensitive) :
1. 'PAT_DEID' - de-indentified patient id for tracking the status of same patient
2. 'NOTE_DEID' - de-indentified note id 
3. 'NOTE' - raw free-text notes, preferably in ASCII coding  
4. 'NOTE_DATE' - date formatted

Genrates a csv file with note level annotations and patient level annotation. 

## Dependencies needed

1. Python 3
2. NLTK
3. Pandas
4. sklearn
5. pickle

## Execution (Very simple running!! Trust me)

1. Run the Main.py from terminal as: python Main.py
2. Once it prompts: "Enter file path + file name ", provide the file location. Notes should be saved in a single csv. Find example in ./data/
3. And that's it!! It will save the outcome in './outcome/' 

### Enjoy!! 
### BTW don't waste you time. If something does not work, please reach imon.banerjee@emory.edu 
"# NLP_diabetic" 
