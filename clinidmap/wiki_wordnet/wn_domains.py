import pandas as pd 
import os
from os import walk
from clinidmap.constants import DATABASE


df_wikidata_wn = pd.read_csv(os.path.join(DATABASE, 'query_wikidata_identificador_de_synset_de_WordNet_3_1_wn_3_0.tsv'), sep='\t', dtype='str')

domains_dir = 'xwnd-30g'

filenames_all = []
for (dirpath, dirnames, filenames) in walk(domains_dir):
    filenames_all.extend(filenames)
    break

print(len(filenames_all))
print(filenames_all[0])

colnames = ['id', 'coeff']
dfs = []
for file in sorted(filenames_all):
    print(file) 
    df = pd.read_csv(os.path.join(domains_dir, file), sep='\t', dtype='str', names=colnames)
    df = df.fillna('')
    df['domain'] = file.split('.')[0]
    dfs.append(df)

print(len(dfs))
df_domains = pd.concat(dfs, ignore_index=True)

print(len(df_domains))
print(df_domains.head(10))

df_domains.to_csv(os.path.join(DATABASE, 'wn30_domains.tsv'), sep='\t', index=False)