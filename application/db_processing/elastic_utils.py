from __future__ import unicode_literals

import csv
import pandas as pd

from application.config import settings

from elasticsearch import Elasticsearch


class ElasticsearchIsNotAvailable(Exception):
    error_code = 599
    error_name = 'Elasticsearch Service Is Not Available'

    def __init__(self, e):
        super().__init__(e)


def get_header_names(headers_list): 
    names_dict = {}
    for i in range(len(headers_list)): 
        names_dict[i] = headers_list[i]
    return names_dict
    
def filterKeys(document, headers):
    return {key: document[key] for key in headers}

def detect_delimiter(path):

    with open(path, 'r') as f:
        sample = f.read(1024)
        dialect = csv.Sniffer().sniff(sample)
        delimiter = dialect.delimiter
        return delimiter

def load_table(path, headers=None): 
    names_dict = {}
    separator = detect_delimiter(path)
    if headers: 
        df = pd.read_csv(path, sep=separator, dtype='str', header=None)
        names_dict = get_header_names(headers)
        df = df.rename(columns=names_dict)
        print(df.head())
    else: 
        df = pd.read_csv(path, sep=separator, dtype='str')
    df = df.fillna('')
    
    print('{} documents are prepared to index'.format(len(df)))
    return df

def doc_generator(df, index_name):
    headers = list(df.columns)
    df_iter = df.iterrows()
    for index, document in df_iter:
        yield {
                "_index": index_name,
                "_id" : f"{index}",
                "_source": filterKeys(document, headers),
                
            }
    raise StopIteration

def check_elastic_mappings(index_name, elastic=None):

    if elastic is None:
        elastic = get_elastic()
    try:
        mapping = elastic.indices.get_mapping(index_name)
        for k, v in mapping.items(): 
            print(k)
            print(v)
        return mapping
    except Exception as e: 
        print(str(e))

def check_elastic_index_names(elastic=None):

    if elastic is None:
        elastic = get_elastic()

    index_names = []
    try:
        for elem in elastic.cat.indices(format="json"):
            index_names.append(elem['index'])
        return index_names
    except Exception as e:
        raise ElasticsearchIsNotAvailable(e)

def get_elastic():
    return Elasticsearch(
        [{'host': settings.host_es, 'port': settings.port_es, 'scheme': 'http'}], 
        timeout=30, 
        max_retries=1, 
        retry_on_timeout=False
        )


