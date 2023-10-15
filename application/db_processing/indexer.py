from __future__ import unicode_literals, division, print_function

from elasticsearch import helpers
from application.db_processing.elastic_utils import get_elastic, check_elastic_index_names, doc_generator
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ElasticIndexer():
    def __init__(self):
        self.settings =  {"index": {"number_of_replicas": 0}}
        self.elastic = get_elastic()

    def index_in_elastic(self, df, index_name): 

        index_names = check_elastic_index_names(elastic=self.elastic)

        if index_name in index_names:
            self.elastic.indices.delete(index=index_name, ignore=[400, 404])

        self.elastic.indices.create(
            index=index_name,
            ignore=400
            )

        print('INDEX AFTER CREATE')
        print(check_elastic_index_names(elastic=self.elastic))

        success, failed = 0, 0
        errors = []
        try:
            for ok, response in helpers.parallel_bulk(
                    client=self.elastic,
                    actions=doc_generator(df, index_name),
                    chunk_size=1000,
                    thread_count=8,
                    queue_size=600,
                    request_timeout=30):  
                if not ok:
                    errors.append(response)
                    failed += 1
                else:
                    success += 1
        except Exception as e:
            logger.warning("Exit parallel bulking with exception: %s." % str(e))

        message = {"result": "Indexing finished, {} documents indexed with success, {} errors, {} failed.".format(str(success), str(len(errors)), str(failed))}
        logger.info(message)
    
        return message 

