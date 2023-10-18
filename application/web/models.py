from pathlib import Path
from typing import Dict, List, Optional, Any

from pydantic import BaseModel, validator, Field


class IndexExpectModel(BaseModel):
    path: Path = Field(..., description=f'Path to the file whose content will be indexed. Shoud be a textual table')
    headers: Optional[List[str]] = Field(None, description=f'List of columns in the table to be used for database indexing, if there is no header in the file.')

    __annotations__ = {
        'path': Path,
        'headers': Optional[List[str]]
        }

    @validator('path')
    def data_path_validation(cls, value: Path):
        if not value.exists():
            raise ValueError(f'File "{value}" does not exist.')
        if not value.is_file():
            raise ValueError(f'"{value}" is a directory.')
        return value


class IndexResponseModel(BaseModel): 
    message: Dict[str, Any]

    __annotations__ = {
        'message': Dict[str, Any]
    }


class MappingExpectModel(BaseModel):
    source_id: str = Field(..., description=f'Item ID in the ontology')
    source_type: str = Field(..., description=f'Ontology type')
    language: str = Field(..., description=f'Language of UMLS, three letters notation, for example ENG, SPA')
    wiki: Optional[bool] = Field(..., description=f'If we need to get Wikipedia items')
    
    __annotations__ = {
        'source_id': str, 
        'source_type': str, 
        'language': str,
        'wiki': bool        
    }

    class Config: 
        schema_extra = {
            'example': {
                'source_id': 'C0001344', # C0025519 (metabolism)
                'source_type': 'UMLS', 
                'language': 'ENG', 
                'wiki': False
            }
        }


class MappingResponseModel(BaseModel): 
    result: Dict[str, Any]

    __annotations__ = {
        'result': Dict[str, Any] 
    }

    