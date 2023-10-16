from __future__ import unicode_literals

from elasticsearch_dsl import Search
from application.db_processing.elastic_utils import get_elastic


def query_search(q_dic, index_name, elastic=None):
    '''
    q_dic: query dictionary in Elastic format ready to search 
    index_name: index in Elastic where to search
    '''
    if elastic is None:
        elastic = get_elastic()

    s = Search(using=elastic, index=index_name)
    s.update_from_dict(q_dic)
    search_result = s.execute()
    search_result = search_result.to_dict()
    
    return search_result

def result2list_unique(result_dict, field):
    lst = []
    if result_dict['hits']['total']['value'] > 0:
        for hit in result_dict['hits']['hits']:
            if hit['_source'][field] not in lst: 
                lst.append(hit['_source'][field])
    return lst


def result2dicts(result_dict):
    ''' Get a list of valies for the given field. '''
    lst = []
    vocabs = [ 'SCTSPA', 'ICD10CM', 'ICD10', 'ICD10PCS', 'SNOMEDCT_US'] # 
    res = {}
    if result_dict['hits']['total']['value'] > 0:
        for hit in result_dict['hits']['hits']:
            if hit['_source']['SAB'] in vocabs: 
                d = {'lang': hit['_source']['LAT'], 
                     'CUI':  hit['_source']['CUI'],
                 'vocabulary': hit['_source']['SAB'], 
                 'id': hit['_source']['CODE'], 
                 'description': hit['_source']['STR'], 
                 'wikidata': 'http://www.wikidata.org/entity/'+hit['_source']['WIKIDATA'], 
                 'mesh_wiki': hit['_source']['MESH_WIKI'],
                 'snomed_ct_wiki': hit['_source']['SNOMED_CT_WIKI'], 
                 'icd_10_wiki': hit['_source']['ICD10_WIKI'], 
                 'icd_10_cm_wiki': hit['_source']['ICD10CM_WIKI'], 
                 'icd_10_pcs_wiki': hit['_source']['ICD10PCS_WIKI'], 
                 'icbi_wiki': hit['_source']['NCBI_WIKI'], 
                 'wordnet_3_1': hit['_source']['WN31'], 
                 'wordnet_3_0': hit['_source']['WN30'], 
                 'wordnet_senses': hit['_source']['SENSE'], 
                 'snomedct2icd10': hit['_source']['SNOMEDCT2ICD10'], 
                 'icd_10_cm_spa': hit['_source']['ICD10CM_SPA'], 
                 'icd_10_pcs_spa': hit['_source']['ICD10OCS_SPA']
                 }    
                lst.append(d)
    res['UMLS'] = lst
    return res


#### QUERY MODELS
def get_umls_query(source_id, lang=None):
    '''
    source_id: UMLS ID (CUI) to search
    target_sab: ontology mapped to this ID
    '''
    if lang: 
        q_dic = {
            "size": 1000,
            "query": { 
                "bool": { 
                "must": [
                    {"match_phrase": {"CUI": source_id}}, 
                    {"match_phrase": {"LAT": lang}}
                    ]
                        }
                    }
                }
    else: 
        q_dic = {
            "size": 1000,
            "query": { 
                "bool": { 
                "must": [
                    {"match_phrase": {"CUI": source_id}}
                    ]
                        }
                    }
                }
    return q_dic


def get_umls2sab_query(source_id, target_sab):
    '''
    source_id: UMLS ID (CUI) to search
    target_sab: ontology mapped to this ID
    '''
    q_dic = {
        "query": { 
            "bool": { 
            "must": [
                {"match_phrase": {"CODE": source_id}},
                {"match_phrase": {"SAB": target_sab}}, 
                {"match_phrase": {"LAT": "ENG"}}
                ]
                    }
                }
            }
    return q_dic

def get_umls2snomed_query(source_id, target_sab):
    '''
    source_id: UMLS ID (CUI) to search
    target_sab: ontology mapped to this ID
    '''
    q_dic = {
        "query": { 
            "bool": { 
            "must": [
                {"match_phrase": {"SAB": 'SNOMEDCT_US'}},
                {"match_phrase": {"CODE": source_id}},
                {"match_phrase": {"SAB": target_sab}}, 
                {"match_phrase": {"LAT": "ENG"}}
                ]
                    }
                }
            }
    return q_dic

def get_umls2code_query(source_id):
    '''
    source_id: UMLS ID (CUI) to search
    target_sab: ontology mapped to this ID
    '''
    q_dic = {
        "query": { 
            "bool": { 
            "must": [
                {"match_phrase": {"CODE": source_id}},
                {"match_phrase": {"LAT": "ENG"}}
                ]
                    }
                }
            }
    return q_dic

def get_query(field, code): 
    q_dic = {
        "query": {
            "bool": {
                "must": [
                    {"match_phrase": {field: code}}
                ]
                }
            }
            }
    return q_dic

