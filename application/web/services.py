import os 
from application import constants

from application.db_processing.indexer import ElasticIndexer
from application.db_processing.elastic_utils import load_table, get_elastic
from application.mapping.mapper import IDMapper


indexer = ElasticIndexer()
elastic = get_elastic()

def index_database_service(path, separator, headers, index_name): 
    df = load_table(path, separator, headers)
    message = indexer.index_in_elastic(df, index_name)
    return {'message': message}


def delete_elastic_index(index_name: str):
    message = elastic.indices.delete(index=index_name, ignore=[400, 404])
    response = {'message': message}
    print(response)
    return response

mapper = IDMapper()

def get_mapping(source_id, source_type, wiki):
    result_dict = mapper.map(source_id, source_type, wiki)
    return {'result': result_dict} 

# def update_wikipedia(): 
#     return update_wiki_database() 

# def get_wordnet_domains(): 
#     return result 
