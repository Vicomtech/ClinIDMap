import pandas as pd 
import os 

df = pd.read_csv('database/UMLS_CIE10_WIKI.tsv', sep='|', dtype='str').fillna('')

print(df.head())

df_select = df[(df['WN31'] != '') & (df['SNOMEDCT2ICD10'] != '')]

df_select.to_csv('exampple_for_paper_snomed.tsv', sep='|')

df_select2 = df[(df['WN31'] != '') & (df['ICD10CM_SPA'] != '')]
df_select2.to_csv('exampple_for_paper_icd.tsv', sep='|')