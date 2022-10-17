import pandas as pd 
import os
import tqdm
# pd.options.display.float_format = '{:,.4f}'.format

df_wikidata = pd.read_csv(os.path.join('database', 'query_wikidata_identificador_de_synset_de_WordNet_3_1_wn_3_0.tsv'), sep='\t', dtype='str')

df_wikidata = df_wikidata

df_domains = pd.read_csv('_wn30_domains.tsv', sep='\t', dtype='str')

# print(df_wikidata.head())
# print(df_domains.head())

wn30_list = df_wikidata.wordnet30_id.to_list()

domains = []
coeffs = []
for wn in tqdm.tqdm(wn30_list):
    df_wn_dom = df_domains[df_domains['id'] == wn]
    df_wn_dom['coeff'] = df_wn_dom['coeff'].astype(float).map('{:,.6f}'.format)
    if len(df_wn_dom) > 0: 
        df_wn_dom_sorted = df_wn_dom.sort_values('coeff', ascending=False)
        domain = df_wn_dom_sorted.domain.to_list()[0]
        coeff = df_wn_dom_sorted.coeff.to_list()[0]
    else: 
        domain = 'no_domain'
        coeff = 'no_coeff'
    domains.append(domain)
    coeffs.append(coeff)

df_wikidata['domain'] = domains
df_wikidata['coeff'] = coeffs

df_wikidata.to_csv(os.path.join('database', 'query_wikidata_identificador_de_synset_de_WordNet_3_1_wn_3_0_domains.tsv'), sep='\t', index=False)