# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/
from distutils.command.config import config
import os 
import tqdm
import sys
import requests 
import json
from functools import reduce
import pandas as pd 
from SPARQLWrapper import SPARQLWrapper, JSON

from application.constants import DATABASE
from application.wiki_wordnet.wn_mapping import wn_sense_mapping

# ?itemLabel ?itemDescription 

endpoint_url = "https://query.wikidata.org/sparql"

# query_cui = """PREFIX bd: <http://www.bigdata.com/rdf#> 
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
# PREFIX schema: <http://schema.org/> 
# PREFIX wd: <http://www.wikidata.org/entity/> 
# PREFIX wikibase: <http://wikiba.se/ontology#> 

# SELECT ?item ?UMLS_CUI WHERE {
#   ?item wdt:P2892 ?UMLS_CUI.
#   SERVICE wikibase:label {
#     bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
# }"""

query_cui = """
PREFIX bd: <http://www.bigdata.com/rdf#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX schema: <http://schema.org/> 
PREFIX wd: <http://www.wikidata.org/entity/> 
PREFIX wikibase: <http://wikiba.se/ontology#> 

SELECT ?item ?UMLS_CUI WHERE {   
  ?item wdt:P2892 ?UMLS_CUI.
  SERVICE wikibase:label { 
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". 
    }  
}
"""
# ?itemLabel ?itemDescription
query_mesh = """PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>
PREFIX mesh: <http://id.nlm.nih.gov/mesh/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wikibase: <http://wikiba.se/ontology#>

SELECT ?item ?mesh WHERE {  
  ?item wdt:P486 ?mesh.
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
"""

query_snomed = """PREFIX bd: <http://www.bigdata.com/rdf#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX schema: <http://schema.org/> 
PREFIX wd: <http://www.wikidata.org/entity/> 
PREFIX wikibase: <http://wikiba.se/ontology#> 

SELECT ?item ?Snomed_CT WHERE {
  ?item wdt:P5806 ?Snomed_CT.
  SERVICE wikibase:label { 
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}

"""

# identificador_MeSH
# query_wordnet0 = """PREFIX bd: <http://www.bigdata.com/rdf#>
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# PREFIX schema: <http://schema.org/>
# PREFIX wd: <http://www.wikidata.org/entity/>
# PREFIX wikibase: <http://wikiba.se/ontology#>

# SELECT ?item ?identificador_de_synset_de_WordNet_3_1 ?UMLS_CUI ?mesh ?icd10 ?Snomed_CT WHERE {
#   SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
#   OPTIONAL { ?item wdt:P8814 ?identificador_de_synset_de_WordNet_3_1. }
#   OPTIONAL { ?item wdt:P2892 ?UMLS_CUI. }
#   OPTIONAL { ?item wdt:P486 ?mesh. }
#   OPTIONAL { ?item wdt:P494 ?icd10. }
#   OPTIONAL { ?item wdt:P5806 ?Snomed_CT. }
# }
# """
query_wordnet0 = """PREFIX bd: <http://www.bigdata.com/rdf#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX schema: <http://schema.org/> 
PREFIX wd: <http://www.wikidata.org/entity/> 
PREFIX wikibase: <http://wikiba.se/ontology#> 

SELECT ?item ?identificador_de_synset_de_WordNet_3_1 WHERE {   
  ?item wdt:P8814 ?identificador_de_synset_de_WordNet_3_1.
  SERVICE wikibase:label { 
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }   

}"""

query_icd10 = """ 
PREFIX bd: <http://www.bigdata.com/rdf#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX schema: <http://schema.org/> 
PREFIX wd: <http://www.wikidata.org/entity/> 
PREFIX wikibase: <http://wikiba.se/ontology#> 

SELECT ?item ?icd10 ?icd10cm ?icd10pcs WHERE {   
  ?item wdt:P494 ?icd10.
  SERVICE wikibase:label { 
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }  
} 
"""

query_icd10cm = """ 
PREFIX bd: <http://www.bigdata.com/rdf#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX schema: <http://schema.org/> 
PREFIX wd: <http://www.wikidata.org/entity/> 
PREFIX wikibase: <http://wikiba.se/ontology#> 

SELECT ?item ?icd10cm WHERE {   
  ?item wdt:P4229 ?icd10cm.
  SERVICE wikibase:label { 
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }  
} 
"""

query_icd10pcs = """ 
PREFIX bd: <http://www.bigdata.com/rdf#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX schema: <http://schema.org/> 
PREFIX wd: <http://www.wikidata.org/entity/> 
PREFIX wikibase: <http://wikiba.se/ontology#> 

SELECT ?item ?icd10pcs WHERE {   
  ?item wdt:P1690 ?icd10pcs.
  SERVICE wikibase:label { 
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }  
} 
"""

query_ncbi = """ 
PREFIX bd: <http://www.bigdata.com/rdf#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX schema: <http://schema.org/> 
PREFIX wd: <http://www.wikidata.org/entity/> 
PREFIX wikibase: <http://wikiba.se/ontology#> 

SELECT ?item ?ncbi WHERE {   
  ?item wdt:P685 ?ncbi.
  SERVICE wikibase:label { 
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }  
} 
"""

output_folder = DATABASE
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def drop_y(df):
    # list comprehension of the cols that end with '_y'
    to_drop = [x for x in df if x.endswith('_y')]
    df.drop(to_drop, axis=1, inplace=True)

def rename_x(df):
    for col in df:
        if col.endswith('_x'):
            df.rename(columns={col:col.rstrip('_x')}, inplace=True)


def get_results(query, endpoint_url=endpoint_url):
    r = requests.get(endpoint_url, params={'format': 'json', 'query': query})
    json_str = r.text
    f = open("sparql1001.txt", "w")
    f.write(json_str)
    f.close()
    result = json.loads(json_str, strict=False)

    return result

def results2csv(results, code_type):
    items = []
    itemLabels = [] 
    itemDescriptions = []
    codes = []

    for result in results["results"]["bindings"]:
        items.append(result['item']['value'])
        codes.append(result[code_type]['value'])

    df = pd.DataFrame({'item': items,  code_type: codes}) # 'itemDescription': itemDescriptions, 'itemLabel': itemLabels,
    print('{} {} codes are in Wikidata'.format(len(df), code_type))
    df.to_csv(os.path.join(output_folder, code_type+'2wiki.tsv'), sep='\t', index=False)
    return df

def wordnet_results2csv(results, filename):
    items = []
    codes = []
    for result in results["results"]["bindings"]:
        items.append(result['item']['value'])
        codes.append(result['identificador_de_synset_de_WordNet_3_1']['value'])

    df = pd.DataFrame({'item': items,  'wordnet31_id': codes}) # 'itemLabel': itemlabels, 'mesh': meshs, 'cui': cuis, 'ICD10': icds, 'SNOMEDCT': snomeds
    print('{} {} codes are in Wikidata'.format(len(df), 'identificador_de_synset_de_WordNet_3_1'))
    df.to_csv(os.path.join(output_folder, filename), sep='\t', index=False)

    return df


def update_wiki_database(): 
    print('Starting Wikidata update')
    results_cui = get_results(query_cui)
    results_mesh = get_results(query_mesh)
    results_snomed = get_results(query_snomed)
    results_wordnet = get_results(query_wordnet0)
    results_icd10 = get_results(query_icd10)
    results_icd10cm = get_results(query_icd10cm)
    results_icd10pcs = get_results(query_icd10pcs)
    results_ncbi = get_results(query_ncbi)
    # print(results_ncbi)

    df_cui = results2csv(results_cui, code_type='UMLS_CUI')
    cuis = len(list(set(df_cui.UMLS_CUI.to_list())))
    print('Unique CUIs in Wikidata', cuis)
    items = len(list(set(df_cui.item.to_list())))
    print('Unique items in Wikidata', items)
    df_cui.to_csv('cuis_wikidata.tsv', sep='\t', index=False)

    df_mesh = results2csv(results_mesh, code_type='mesh')
    print('Mesh len', len(df_mesh))
    df_snomed = results2csv(results_snomed, code_type='Snomed_CT')
    print('SNOMED CT', len(df_snomed))
    print(df_snomed.head())

    df_icd10 = results2csv(results_icd10, code_type='icd10')
    print('ICD-10', len(df_icd10))
    print(df_icd10.head())

    df_icd10cm = results2csv(results_icd10cm, code_type='icd10cm')
    print('ICD-10-CM', len(df_icd10cm))

    df_icd10pcs = results2csv(results_icd10pcs, code_type='icd10pcs')
    print('ICD-10-PCS', len(df_icd10pcs))

    df_ncbi = results2csv(results_ncbi, code_type='ncbi')
    print('NCBI', len(df_ncbi))

    filename = 'query_wikidata_identificador_de_synset_de_WordNet_3_1.tsv'
    df_wn = wordnet_results2csv(results_wordnet, filename)
    print('WORDNET IDs', len(df_wn))

    dfs = [df_cui, df_mesh, df_snomed, df_icd10, df_icd10cm, df_icd10pcs, df_ncbi, df_wn]

    df_merdge = reduce(lambda  left,right: pd.merge(left,right,on='item', how='outer').fillna(''), dfs)
    print(df_merdge.head(10))
    print(len(df_merdge))

    wn31_ids = df_merdge.wordnet31_id.to_list()

    wn30_ids = []
    wn31_senses = []
    for wn31_id in tqdm.tqdm(wn31_ids): 
        wn30_id = ''
        sense31 = ''
        if wn31_id != '': 
            wn30_id = wn_sense_mapping(wn31_id)[0]
            sense31 = wn_sense_mapping(wn31_id)[1]
        wn30_ids.append(wn30_id)
        wn31_senses.append(sense31)

    df_merdge['wordnet30_id'] = wn30_ids
    df_merdge['sense'] = wn31_senses

    df_merdge.to_csv(os.path.join(DATABASE, 'final_cui2mesh2icd102wn.tsv'), sep='\t', index=False)


if __name__ == "__main__":
    update_wiki_database()
