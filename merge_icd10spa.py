import pandas as pd 
import os 


def drop_y(df):
    # list comprehension of the cols that end with '_y'
    to_drop = [x for x in df if x.endswith('_y')]
    df.drop(to_drop, axis=1, inplace=True)

def rename_x(df):
    for col in df:
        if col.endswith('_x'):
            df.rename(columns={col:col.rstrip('_x')}, inplace=True)


df = pd.read_csv('database_/UMLS_WIKI_ICD10_17102023.txt', sep='|', dtype='str').fillna('')

print(df.head())

# df_cie10d = pd.read_csv('database_/CIE10DIAGNOSTICOS_2022.tsv', sep='\t', dtype='str')
# df_cie10d = df_cie10d.rename(columns={'ICD10CM_SPA': 'SNOMEDCT2ICD10_SPA'})
# # df_cie10d['SAB'] = 'ICD10CM'
# df_merge_cie10d = df.merge(df_cie10d, left_on=['SNOMEDCT2ICD10'], right_on=['CODE'], how='left').fillna('')
# print('Merge CIE10CM SPA ', len(df_merge_cie10d))
# drop_y(df_merge_cie10d)
# rename_x(df_merge_cie10d)
# df_merge_cie10d = df_merge_cie10d.rename(columns={'ICD10ENG': 'SNOMEDCT2ICD10_ENG'})
# print(df_merge_cie10d.head())

# check1 = df_merge_cie10d[df_merge_cie10d['SNOMEDCT2ICD10'] != '']
# print('SNOMEDCT2ICD10', len(check1))
# check2 = df_merge_cie10d[df_merge_cie10d['SNOMEDCT2ICD10_SPA'] != '']
# print('SNOMEDCT2ICD10_SPA', len(check2))

# check3 = df_merge_cie10d[(df_merge_cie10d['SNOMEDCT2ICD10_SPA'] == '') & (df_merge_cie10d['SNOMEDCT2ICD10'] != '')]

# check3.to_csv('snomed_prueba.tsv', sep='\t', index=False)
# # df_cie10p = pd.read_csv('database_/CIE10PROCEDIMIENTOS_2022.tsv', sep='\t', dtype='str')
# # df_cie10p['SAB'] = 'ICD10PCS'
# # df_merge_cie10p = df_merge_cie10d.merge(df_cie10p, on=['CODE', 'SAB'], how='left').fillna('')
# # print('Merge CIE10PCS SPA', len(df_merge_cie10p))

df = df.rename(columns={'ICD10OCS_SPA': 'ICD10PCS_SPA'})

df_merge_cie10d = df[["CUI", "LAT", "TS", "LUI", "STT", "SUI", "ISPREF", "AUI", 
    "SAUI", "SCUI", "SDUI", "SAB", "TTY", "CODE", "STR", "SRL", 
    "SUPPRESS", "CVF", "ICD10CM_SPA", "ICD10PCS_SPA", "SNOMEDCT2ICD10", "SNOMEDCT2ICD10_ENG", "SNOMEDCT2ICD10_SPA",
    "WIKIDATA", "MESH_WIKI", "SNOMED_CT_WIKI", "ICD10_WIKI", "ICD10CM_WIKI", "ICD10PCS_WIKI", "NCBI_WIKI", "WN31", "WN30", "WN_SENSE"
    ]]

# df_merge_cie10d.to_csv('database_/UMLS_WIKI_ICD10_17102023.txt', sep='|', index=False)

df_select = df_merge_cie10d[(df_merge_cie10d['WN31'] != '') & (df_merge_cie10d['SNOMEDCT2ICD10'] != '')]
df_select.to_csv('LREC2024/samples/example_01.tsv', sep='|')

df_select2 = df_merge_cie10d[(df_merge_cie10d['WN31'] != '') & (df_merge_cie10d['ICD10CM_SPA'] != '')]
df_select2.to_csv('LREC2024/samples/example_02.tsv', sep='|')

df_sty = pd.read_csv('/DATA/ezotova_data/UMLS/2023/MRSTY.RRF', sep='|', dtype='str', names=["CUI", "TUI", "STN", "SEMTYPE", "ATUI", "CVF", "_"])

df_sty = df_sty[['CUI', 'TUI', 'SEMTYPE']]
print(df_sty.head())

df_merge_cie10d_sty = df_merge_cie10d.merge(df_sty, on=['CUI'], how='left').fillna('')

df_groups = pd.read_csv('database/SemGroups.txt', sep='|', dtype='str', names=['SEMGROUP', 'DEF', 'TUI', 'GROUPTYPE'])
print(df_groups.head())
df_merge_cie10d_sty_g = df_merge_cie10d_sty.merge(df_groups, on=['TUI'], how='left').fillna('')

df_merge_cie10d_sty_g = df_merge_cie10d_sty_g[["CUI", "LAT", "TS", "LUI", "STT", "SUI", "ISPREF", "AUI", 
    "SAUI", "SCUI", "SDUI", "SAB", "TTY", "CODE", "STR", "SRL", 
    "SUPPRESS", "CVF", "ICD10CM_SPA", "ICD10PCS_SPA", "SNOMEDCT2ICD10", "SNOMEDCT2ICD10_ENG", "SNOMEDCT2ICD10_SPA",
    "WIKIDATA", "MESH_WIKI", "SNOMED_CT_WIKI", "ICD10_WIKI", "ICD10CM_WIKI", "ICD10PCS_WIKI", "NCBI_WIKI", "WN31", "WN30", "WN_SENSE", 
    "TUI", "SEMTYPE", "SEMGROUP", "DEF"
    ]]
df_merge_cie10d_sty_g.to_csv('database_/UMLS_WIKI_ICD10_STY_18102023.txt', sep='|', index=False)
print(df_merge_cie10d_sty_g.head())
df_merge_cie10d_sty_g_sample = df_merge_cie10d_sty_g[:1000]

df_merge_cie10d_sty_g_sample.to_csv('LREC2024/samples/example_03.tsv', sep='|', index=False, )
column_names = df_merge_cie10d_sty_g.columns.tolist()
print(column_names)
print(len(column_names))
print(len(df_merge_cie10d_sty_g))