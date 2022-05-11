from __future__ import unicode_literals, division, print_function
from distutils.command.config import config
from elasticsearch import helpers
from elastic_utils import get_elastic, check_elastic_index_names, doc_generator, get_header_names
import argparse 
import logging
import pandas as pd

import config

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

settings= {
    "index": {
        "number_of_replicas": 0
        }
    }

def index_database(path, index_name, separator, headers=None, settings=settings): 
    names_dict = {}
    if headers: 
        df = pd.read_csv(path, sep=separator, dtype='str', header=None)
        names_dict = get_header_names(headers)
        df = df.rename(columns=names_dict)
    else: 
        df = pd.read_csv(path, sep=separator, dtype='str')
            
    df = df.fillna('None')
    print(df.head())

    elastic = get_elastic()

    index_names = check_elastic_index_names(elastic=elastic)

    if index_name in index_names:
        elastic.indices.delete(index=index_name, ignore=[400, 404])

    elastic.indices.create(
        index=index_name,
        ignore=400, 
        body=settings
        )

    print('INDEX AFTER CREATE')
    print(check_elastic_index_names(elastic=elastic))

    success, failed = 0, 0
    errors = []
    try:
        for ok, response in helpers.parallel_bulk(
                client=elastic,
                actions=doc_generator(df, index_name),
                chunk_size=1000,
                thread_count=8,
                queue_size=600,
                request_timeout=30
        ):
            print(ok, response)
            if not ok:
                errors.append(response)
                failed += 1
            else:
                success += 1
    except Exception as e:
        logger.warning("Exit parallel bulking with exception: %s." % str(e))
    logger.info("Indexing finished, %s success, %s errors, %s failed.", str(success), str(len(errors)), str(failed))


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Index Elastic Database')
    # parser.add_argument('--headers', nargs='+', type=str,  help='A list of headers names in the table')
    # parser.add_argument('--path', type=str, default=None, help='A path to the table')
    # parser.add_argument(
    #     '--index_name', 
    #     type=str, 
    #     help='Index name in Elastic, will be used for search. All the names are given en the config.py file. You can add, delete or edit your own index names'
    #     )
    # parser.add_argument('--separator', type=str, help='Separator | or tab, depending on the table to process')
    # args = parser.parse_args()
    # print(args)
    # path, index_name, separator
    # index_database(args.path, args.index_name, args.separator)
    # path, index_name, separator, headers=None
    index_database(config.PATH_SEM_TYPES, config.SEMANTIC_TYPES, config.PIPE, config.HEADERS_SEM_TYPES) 