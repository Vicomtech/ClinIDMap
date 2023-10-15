import logging
import sys
from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Depends

from clinidmap.errors import ElasticsearchIsNotAvailable, EmptyDatasetError
from clinidmap.web.models import (
    IndexResponseModel, IndexExpectModel, MappingExpectModel, MappingResponseModel
    # RetrieveResponseModel, 
    # RetrieveExpectModel, MatchExpectModel, MatchResponseModel, 
    # MatchSemanticResponseModel, MatchSemanticExpectModel
    )

from clinidmap.web.services import (
    index_database_service, delete_elastic_index, get_mapping
    # search_index, neural_extractor, 
    # exact_match_search_index, delete_elastic_index, match_semantic_search_index
    )

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


api = APIRouter(
    prefix='/clinidmap',
    tags=['Clinical ID mapping'],
    responses={
        ElasticsearchIsNotAvailable.error_code: {'description': ElasticsearchIsNotAvailable.error_name}
    }
)

## MATCH 
@api.post(
    '/map',
    response_model=MappingResponseModel,
    status_code=200, 
    responses={
         404: {"description": "Not found"}
    }
)

def get_item_mapping(item:MappingExpectModel):
    return get_mapping(item.source_id, item.source_type, item.wiki)


@api.post(
    '/{index_name}',
    response_model=IndexResponseModel,
    status_code=201,
    # dependencies=[Depends(index_does_not_exist)],
    responses={
        EmptyDatasetError.error_code: {'description': EmptyDatasetError.error_name},
        HTTPStatus.FORBIDDEN.value: {'description': 'Index Already Exists'}
    }
)
def post_index(index_name: str, item: IndexExpectModel):
    print(index_name)
    # TODO: this should probably be an ASYNC method?
    return index_database_service(item.path, item.separator, item.headers, index_name)


@api.delete(
    '/{index_name}',
    response_model=IndexResponseModel,
    status_code=201,
    # dependencies=[Depends(index_exists)],
    responses={
        EmptyDatasetError.error_code: {'description': EmptyDatasetError.error_name},
        HTTPStatus.NOT_FOUND.value: {'description': 'Index Not Found'}
    }
)

def delete_index(index_name: str):
    return delete_elastic_index(index_name)