# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

from distutils.command.config import config
import os 
import sys
import pandas as pd 
from SPARQLWrapper import SPARQLWrapper, JSON

from config import DATABASE

endpoint_url = "https://query.wikidata.org/sparql"

query_cui = """PREFIX bd: <http://www.bigdata.com/rdf#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX schema: <http://schema.org/> 
PREFIX wd: <http://www.wikidata.org/entity/> 
PREFIX wikibase: <http://wikiba.se/ontology#> 

SELECT ?item ?itemLabel ?itemDescription ?cui WHERE {   
  ?item wdt:P2892 ?cui.
  SERVICE wikibase:label { 
    bd:serviceParam wikibase:language "en". }   
}"""

query_mesh = """PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wikibase: <http://wikiba.se/ontology#>

SELECT ?item ?itemLabel ?itemDescription ?mesh WHERE {  
  ?item wdt:P486 ?mesh.
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "en,es". }  

}"""

query_wordnet = """PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wikibase: <http://wikiba.se/ontology#>

SELECT * WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
  OPTIONAL { ?item wdt:P8814 ?identificador_de_synset_de_WordNet_3_1. }
  OPTIONAL { ?item wdt:P2892 ?UMLS_CUI. }
  OPTIONAL { ?item wdt:P486 ?identificador_MeSH. }
}
"""

output_folder = DATABASE
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def get_results(query, endpoint_url=endpoint_url):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def results2csv(results, code_type):
    items = []
    itemLabels = [] 
    itemDescriptions = []
    codes = []

    for result in results["results"]["bindings"]:
        items.append(result['item']['value'])
        if 'itemLabel' in result: 
            itemLabels.append(result['itemLabel']['value'])
        else: 
            itemLabels.append('no item label')
        if 'itemDescription' in result: 
            itemDescriptions.append(result['itemDescription']['value'])
        else: 
            itemDescriptions.append('no description')
        codes.append(result[code_type]['value'])

    df = pd.DataFrame({'item': items, 'itemLabel': itemLabels, 'itemDescription': itemDescriptions, code_type: codes})
    print('{} {} codes are in Wikidata'.format(len(df), code_type))
    df.to_csv(os.path.join(output_folder, code_type+'2wiki.tsv'), sep='\t', index=False)

def wordnet_results2csv(results):
    items = []
    codes = []
    meshs = []
    cuis = []
    for result in results["results"]["bindings"]:
        items.append(result['item']['value'])
        codes.append(result['identificador_de_synset_de_WordNet_3_1']['value'])
        if 'identificador_MeSH' in result: 
            meshs.append(result['identificador_MeSH']['value'])
        else: 
            meshs.append('')
        if 'UMLS_CUI' in result: 
            cuis.append(result['UMLS_CUI']['value'])
        else: 
            cuis.append('')

    df = pd.DataFrame({'item': items, 'wordnet_id': codes, 'MESH': meshs, 'CUI': cuis })
    print('{} {} codes are in Wikidata'.format(len(df), 'identificador_de_synset_de_WordNet_3_1'))
    df.to_csv(os.path.join(output_folder, 'query_wikidata_identificador_de_synset_de_WordNet_3_1.tsv'), sep='\t', index=False)

print('Starting CUI query')
results_cui = get_results(query_cui)

print('Starting MESH query')
results_mesh = get_results(query_mesh)

print('Starting Wordnet query')
results_wordnet = get_results(query_wordnet)

##
code_type = 'cui'
results2csv(results_cui, code_type)

code_type = 'mesh'
results2csv(results_mesh, code_type)

wordnet_results2csv(results_wordnet)