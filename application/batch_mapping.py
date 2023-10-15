import pandas as pd 
from application.mapping.mapper import IDMapper


mapper = IDMapper()

def get_mapping(source_id, source_type, wiki):
    result_dict = mapper.map(source_id, source_type, wiki)
    return {'result': result_dict} 

codes = ["C0020740"]

print('')
mapped_cuis = []
mapped_icd10cm = []
mapped_icd10pcs = []
for code in codes: 
    mapped = get_mapping(code, 'UMLS', wiki=False)
    print()

    # print(mapped)
    # print()