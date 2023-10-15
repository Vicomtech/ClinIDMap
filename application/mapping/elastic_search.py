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

def result2list_(result_dict, field):
    ''' Get a list of valies for the given field. '''
    lst = []
    if result_dict['hits']['total']['value'] > 0:
        for hit in result_dict['hits']['hits']:
            lst.append(hit['_source'][field])
    return lst


#### QUERY MODELS
def get_umls_query(source_id, target_sab):
    '''
    source_id: UMLS ID (CUI) to search
    target_sab: ontology mapped to this ID
    '''
    q_dic = {
        "query": { 
            "bool": { 
            "must": [
                {"match_phrase": {"CUI": source_id}},
                # {"match_phrase": {"SAB": target_sab}}, 
                # {"match_phrase": {"LAT": "ENG"}}
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

