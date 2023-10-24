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
    vocabs = ['SCTSPA', 'ICD10CM', 'ICD10', 'ICD10PCS', 'SNOMEDCT_US', 'MSH'] # 
    res = {}
    if result_dict['hits']['total']['value'] > 0:
        for hit in result_dict['hits']['hits']:
            if hit['_source']['SAB'] in vocabs:   
                lst.append(hit['_source'])
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
            "size": 100,
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
            "size": 100,
            "query": { 
                "bool": { 
                "must": [
                    {"match_phrase": {"CUI": source_id}}
                    ]
                        }
                    }
                }
    return q_dic


def get_sab_query(source_id, target_sab, lang=None):
    if lang:
        q_dic = {
            "size": 100,
            "query": { 
                "bool": { 
                "must": [
                    {"match_phrase": {"CODE": source_id}},
                    {"match_phrase": {"SAB": target_sab}}, 
                    {"match_phrase": {"LAT": lang}}
                    ]
                        }
                    }
                }
    else: 
        q_dic = {
            "query": { 
                "bool": { 
                "must": [
                    {"match_phrase": {"CODE": source_id}},
                    {"match_phrase": {"SAB": target_sab}}
                    ]
                        }
                    }
                }      
    return q_dic
