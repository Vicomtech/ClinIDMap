from typing import Set


class ElasticsearchIsNotAvailable(Exception):
    error_code = 599
    error_name = 'Elasticsearch Service Is Not Available'

    def __init__(self, e):
        super().__init__(e)


class EmptyDatasetError(Exception):
    error_code = 202  # Not an actual error :-)
    error_name = 'No Content To Index'

    def __init__(self):
        super(EmptyDatasetError, self).__init__('No content left to index after filtering null values.')


class InvalidFileError(Exception):
    error_code = 422
    error_name = 'Unprocessable Entity'

    def __init__(self, message: str):
        super(InvalidFileError, self).__init__(message)


class IllegalColumnsFound(InvalidFileError):

    def __init__(self, invalid_columns: Set[str]):
        message = f'The input file contains reserved column names: {invalid_columns}; please replace them and try again.'
        super(IllegalColumnsFound, self).__init__(message)


class ColumnsNotFound(InvalidFileError):

    def __init__(self, invalid_columns: Set[str]):
        message = f'The specified columns {invalid_columns} were not found in the input file'
        super(ColumnsNotFound, self).__init__(message)


class SheetsNotFound(InvalidFileError):

    def __init__(self):
        message = f'The specified sheets were not found in the input file'
        super(SheetsNotFound, self).__init__(message)


class WrongExtensionException(InvalidFileError):

    def __init__(self, extention):
        message = f'{extention} is incorrect file extension. Should be XLSX, TSV or CSV'
        super(WrongExtensionException, self).__init__(message)
