import pandas as pd 
from clinidmap.mapping.mapper import ClinIDMapper


mapper = ClinIDMapper()

def get_mapping(source_id, source_type, wiki):
    result_dict = mapper.map(source_id, source_type, wiki)
    return {'result': result_dict} 

# df = pd.read_csv('/DATA/ezotova_data/ClinIDMap/corpus/MedMentions/MedMentions_type.tsv', sep='\t', dtype='str')
# df = df[20:30]
# print(df.head())
# codes = df.code.to_list()

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