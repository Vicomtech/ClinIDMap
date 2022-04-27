########################################################################
# Copyright (c) 2021 Vicomtech (http://www.vicomtech.org)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#    - Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#    - Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
########################################################################
from __future__ import unicode_literals

import json
from elastic_utils import get_elastic

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)

def query_search(q_dic, index_name, n_search=1000, elastic=None):
    '''
    q_dic: query dictionary in Elastic format ready to search 
    index_name: index in Elastic where to search
    '''
    if elastic is None:
        elastic = get_elastic()
    body = json.dumps(q_dic, ensure_ascii=False)
    search_result = elastic.search(index=index_name, body=body, size=n_search, from_=0)

    return search_result

def result2list_unique(result_dict, field):
    lst = []
    if result_dict['hits']['total']['value'] > 0:
        for hit in result_dict['hits']['hits']:
            if hit['_source'][field] not in lst: 
                lst.append(hit['_source'][field])
    return lst

def result2list_(result_dict, field):
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
                {"match": {"CUI": source_id}},
                {"match": {"SAB": target_sab}}, 
                {"match": {"LAT": "ENG"}}
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
                {"match": {"CODE": source_id}},
                {"match": {"SAB": target_sab}}, 
                {"match": {"LAT": "ENG"}}
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
                {"match": {"SAB": 'SNOMEDCT_US'}},
                {"match": {"CODE": source_id}},
                {"match": {"SAB": target_sab}}, 
                {"match": {"LAT": "ENG"}}
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
                {"match": {"CODE": source_id}},
                {"match": {"LAT": "ENG"}}
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
                    {"match": {field: code}}
                ]
                }
            }
            }
    return q_dic

def query_and_search(field, code, index): 
    result_list = []
    q_dic = get_query(field, code)
    result = query_search(q_dic, index)
    if result['hits']['total']['value'] > 0:
        for hit in result['hits']['hits']: 
            result_list.append(hit['_source']['term'])

    return result_list
