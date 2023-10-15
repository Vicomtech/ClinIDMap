import pandas as pd 
import os
import tqdm
from clinidmap.constants import DATABASE
# pd.options.display.float_format = '{:,.4f}'.format

df_wikidata = pd.read_csv(os.path.join(DATABASE, 'final_cui2mesh2icd102wn.tsv'), sep='\t', dtype='str')
df_wikidata = df_wikidata
df_domains = pd.read_csv('/DATA/ezotova_data/_ClinIDMap/_wn30_domains.tsv', sep='\t', dtype='str')
df_domains['coeff'] = df_domains['coeff'].astype(float).map('{:,.6f}'.format)
df_wn_dom_sorted = df_domains.sort_values('coeff', ascending=False)
wn30_list = df_wikidata.wordnet30_id.to_list()

domains = []
coeffs = []
for wn in tqdm.tqdm(wn30_list):
    df_wn_dom = df_wn_dom_sorted[df_wn_dom_sorted['id'] == wn]
    # df_wn_dom['coeff'] = df_wn_dom['coeff'].astype(float).map('{:,.6f}'.format)
    if len(df_wn_dom) > 0: 
        # df_wn_dom_sorted = df_wn_dom.sort_values('coeff', ascending=False)
        domain = df_wn_dom.domain.to_list()[0]
        coeff = df_wn_dom.coeff.to_list()[0]
    else: 
        domain = 'no_domain'
        coeff = 'no_coeff'
    domains.append(domain)
    coeffs.append(coeff)

df_wikidata['domain'] = domains
df_wikidata['coeff'] = coeffs

df_wikidata.to_csv(os.path.join(DATABASE, 'final_cui2mesh2icd102wn_domains.tsv'), sep='\t', index=False)