import os 

### Names of Elastic index for each database
UMLS = 'umls' 
SNOMED2ICD10 = 'snomed2icd10'
SNOMED_ES = 'snomed_es'
SNOMED_EN = 'snomed_en'
SEMANTIC_TYPES = 'semantic_types'
ICD10PCS = 'icd10pcs'
ICD10CM = 'icd10cm'
CUI2WIKI = 'cui2wiki'
MESH2WIKI = 'mesh2wiki'
WORDNET2WIKI = 'wordnet2wiki'


### INDEX ELASTIC 

# separators to read tables  
TAB = '\t'
PIPE = '|'

# separator = '\t'
PATH_ICD10CM = os.path.join('/DATA/ezotova_data/ICD-10_CodiEsp/data/icd', 'ICD10_diagnosticos_block_2020.tsv')
HEADRES_ICD10CM = ['id', 'codigo', 'descripcion', 'block_label']

PATH_ICD10PCS = os.path.join('/DATA/ezotova_data/ICD-10_CodiEsp/data/icd', 'ICD10_procedimientos_block_2020.tsv')
HEADRES_ICD10PCS = ['id', 'codigo', 'descripcion', 'block_label']

PATH_WIKI_MESH = os.path.join('database', 'query_wikidata_mesh.tsv')
HEADRES_WIKI_MESH = ['item', 'itemLabel', 'itemDescription', 'code']

PATH_WIKI_WNET = os.path.join(
    'database', 
    'query_wikidata_identificador_de_synset_de_WordNet_3_1.tsv'
    )
HEADERS_WIKI_WNET = ['item', 'wordnet_id', 'MESH', 'CUI']

PATH_WIKI_CUI = os.path.join('database', 'query_wikidata_cui.tsv')
HEADERS_WIKI_CUI = ['item', 'itemLabel', 'itemDescription', 'code']

PATH_SNOMEDCT_EN = os.path.join('database', 'sct2_Description_Full-en_INT_20210731.txt')
HEADERS_SNOMEDCT_EN = ['id', 'effectiveTime', 'active', 'moduleId', 'conceptId', 'languageCode', 'typeId', 'term', 'caseSignificanceId']


PATH_SNOMEDCT_ES = os.path.join(
    'database', 
    'sct2_Description_SpanishExtensionFull-es_INT_20211031.txt'
    )
HEADERS_SNOMEDCT_ES = ['id', 'effectiveTime', 
	'active',  'moduleId', 'conceptId', 'languageCode', 
    'typeId', 'term', 'caseSignificanceId']

PATH_SNOMEDCT_ICD10 = os.path.join(
    'database', 
    'tls_Icd10cmHumanReadableMap_US1000124_20210901.tsv'
    )
HEADERS_SNOMEDCT_ICD10 = ['id', 'effectiveTime', 'active', 
    'moduleId', 'refsetId', 'referencedComponentId', 
    'referencedComponentName', 'mapGroup', 'mapPriority', 'mapRule', 
    'mapAdvice', 'mapTarget', 'mapTargetName', 'correlationId', 
    'mapCategoryId', 'mapCategoryName']

# separator = '|'
PATH_UMLS = os.path.join('/DATA/ezotova_data/UMLS', 'MRCONSO.RRF')
HEADERS_UMLS = ['CUI', 'LAT', 'TS', 'LUI', 'STT', 'SUI', 'ISPREF', 'AUI', 
    'SAUI', 'SCUI', 'SDUI', 'SAB', 'TTY', 'CODE', 'STR', 'SRL', 
    'SUPPRESS', 'CVF']

PATH_SEM_GROUPS = os.path.join('database', 'SemGroups.txt')
HEADERS_SEM_GROUPS = ['STY', 'DEF', 'UI', 'TYPE']

PATH_SEM_TYPES = os.path.join('database', 'MRSTY.RRF')
HEADERS_SEM_TYPES = ['CUI', 'TUI', 'STN', 'STY', 'ATUI', 'CVF']
