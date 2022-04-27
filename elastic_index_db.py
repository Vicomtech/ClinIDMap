from __future__ import unicode_literals, division, print_function

from elasticsearch import helpers
from elastic_utils import get_elastic, check_elastic_index_names, doc_generator, get_header_names

import os
import logging

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

settings= {
    'index': {
        'number_of_replicas': 0
        }
    }

def index_database(headers, path, index_name, separator, settings=settings): 
    names_dict = get_header_names(headers)
    print(names_dict)
            
    df = pd.read_csv(path, sep=separator, dtype='str', header=None)
    df = df.fillna('None')
    df = df.rename(columns=names_dict)
    print(df.head())

    elastic = get_elastic()

    index_names = check_elastic_index_names(elastic=elastic)
    print('Index names', index_names)

    if index_name in index_names:
            elastic.indices.delete(index=index_name, ignore=[400, 404])

    elastic.indices.create(
        index=index_name, 
        ignore=400, 
        body=settings
        )

    success, failed = 0, 0
    errors = []
    try:
        for ok, response in helpers.parallel_bulk(
                client=elastic,
                actions=doc_generator(df, index_name, headers),
                chunk_size=1000,
                thread_count=8,
                queue_size=600,
                request_timeout=30
        ):
            if not ok:
                errors.append(response)
                failed += 1
            else:
                success += 1
    except Exception as e:
        logger.warning("Exit parallel bulking with exception: %s." % str(e))
    logger.info("Indexing finished, %s success, %s errors, %s failed.", str(success), str(len(errors)), str(failed))


if __name__ == "__main__":
    separator = '\t'
    path = os.path.join('/DATA/ezotova_data/ICD-10_CodiEsp/data/icd', 'ICD10_diagnosticos_block_2020.tsv')
    headers = ['id', 'codigo', 'descripcion', 'block_label']
    index_name = 'icd10cm'

    # separator = '|'
    # path = os.path.join('database', 'SemGroups.txt')
    # headers = ['STY', 'DEF', 'UI', 'TYPE']
    # index_name = 'cui2semgroup'

    # separator = '\t'
    # path = os.path.join('database', 'query_wikidata_mesh.tsv')
    # headers = ['item', 'itemLabel', 'itemDescription', 'code']
    # index_name = 'mesh2wiki'

    # separator = '\t'
    # path = os.path.join('database', 'query_wikidata_identificador_de_synset_de_WordNet_3_1.tsv')
    # headers = ['item', 'wordnet_id', 'MESH', 'CUI']
    # index_name = 'wordnet2wiki'

    # separator = '\t'
    # path = os.path.join('database', 'sct2_Description_Full-en_INT_20210731.txt')
    # headers = ['id', 'effectiveTime', 'active', 'moduleId', 'conceptId', 'languageCode', 'typeId', 'term', 'caseSignificanceId']
    # index_name = 'snomed_en'

    # separator = '\t'
    # path = os.path.join('database', 'query_wikidata_cui.tsv')
    # headers = ['item', 'itemLabel', 'itemDescription', 'code']
    # index_name = 'cui2wiki'

    # separator = '\t'
    # path = os.path.join('/DATA/ezotova_data/ICD-10_CodiEsp/data/icd', 'ICD10_procedimientos_block_2020.tsv')
    # headers = ['id', 'codigo', 'descripcion', 'block_label']
    # index_name = 'icd10pcs'

    # separator = '|'
    # path = os.path.join('database', 'MRSTY.RRF')
    # headers = ['CUI', 'TUI', 'STN', 'STY', 'ATUI', 'CVF']
    # index_name = 'semantic_types'

    # separator = '\t'
    # path = os.path.join('database', 'sct2_Description_SpanishExtensionFull-es_INT_20211031.txt')
    # headers = ['id', 'effectiveTime', 
    # 	'active',  'moduleId', 'conceptId', 'languageCode', 
    #     'typeId', 'term', 'caseSignificanceId']
    # index_name = 'snomed_es'

    # separator = '\t'
    # path = os.path.join('database', 'tls_Icd10cmHumanReadableMap_US1000124_20210901.tsv')
    # headers = ['id', 'effectiveTime', 'active', 
    #     'moduleId', 'refsetId', 'referencedComponentId', 
    #     'referencedComponentName', 'mapGroup', 'mapPriority', 'mapRule', 
    #     'mapAdvice', 'mapTarget', 'mapTargetName', 'correlationId', 
    #     'mapCategoryId', 'mapCategoryName']
    # index_name = 'snomed2icd10'

    # separator = '|'
    # path = os.path.join('/DATA/ezotova_data/UMLS', 'MRCONSO.RRF')
    # headers = ['CUI', 'LAT', 'TS', 'LUI', 'STT', 'SUI', 'ISPREF', 'AUI', 
    #     'SAUI', 'SCUI', 'SDUI', 'SAB', 'TTY', 'CODE', 'STR', 'SRL', 
    #     'SUPPRESS', 'CVF']
    # index_name = 'umls'

    index_database(headers, path, index_name, separator)