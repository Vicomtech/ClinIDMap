import os 


DATABASE = "database"

### Names of Elastic index for each database
UMLS = "umls" 
UMLS_EXT = "umls_ext"
SNOMED2ICD10 = "snomed2icd10"
SNOMED_ES = "snomed_es"
SNOMED_EN = "snomed_en"
SEMANTIC_TYPES = "semtypes"
SEMANTIC_GROUPS = "semgroups"
ICD10PCS = "icd10pcs"
ICD10CM = "icd10cm"
CUI2WIKI = "cui2wiki"
MESH2WIKI = "mesh2wiki"
WORDNET2WIKI = "wordnet2wiki"


### ELASTIC INDEXING 
# separators to read tables  
TAB = "\t"
PIPE = "|"

# separator = "\t"
# PATH_ICD10CM = os.path.join("/DATA/ezotova_data/ICD-10_CodiEsp/data/icd", "ICD10_diagnosticos_block_2020.tsv")
# HEADRES_ICD10CM = ["id", "codigo", "descripcion", "block_label"]
PATH_ICD10CM = os.path.join("/DATA/ezotova_data/ClinIDMap/database", "CIE10DIAGNOSTICOS_2022.tsv")
HEADRES_ICD10CM = ["CODE", "ICD10DESCR_SPA"]

# PATH_ICD10PCS = os.path.join("/DATA/ezotova_data/ICD-10_CodiEsp/data/icd", "ICD10_procedimientos_block_2020.tsv")
PATH_ICD10PCS = os.path.join("/DATA/ezotova_data/ClinIDMap/database", "CIE10PROCEDIMIENTOS_2022.tsv")
# HEADRES_ICD10PCS = ["id", "codigo", "descripcion", "block_label"]
HEADRES_ICD10PCS = ["CODE", "ICD10DESCR_SPA"]

PATH_WIKI_MESH = os.path.join(DATABASE, "query_wikidata_mesh.tsv")
HEADRES_WIKI_MESH = ["item", "itemLabel", "itemDescription", "code"]

PATH_WIKI_WNET = os.path.join(
    DATABASE, 
    "query_wikidata_identificador_de_synset_de_WordNet_3_1.tsv"
    )
HEADERS_WIKI_WNET = ["item", "wordnet_id", "MESH", "CUI"]

PATH_WIKI_CUI = os.path.join(DATABASE, "query_wikidata_cui.tsv")
HEADERS_WIKI_CUI = ["item", "itemLabel", "itemDescription", "code"]

PATH_SNOMEDCT_EN = os.path.join("/DATA/ezotova_data/ClinIDMap/database", "sct2_Description_Full-en_INT_20231001.txt")
HEADERS_SNOMEDCT_EN = ["id", "effectiveTime", "active", "moduleId", "conceptId", "languageCode", "typeId", "term", "caseSignificanceId"]

PATH_SNOMEDCT_ES = os.path.join(
    "/DATA/ezotova_data/ClinIDMap/database", 
    "sct2_Description_SpanishExtensionFull-es_INT_20230930.txt"
    )
HEADERS_SNOMEDCT_ES = ["id", "effectiveTime", "active", "moduleId", "conceptId", "languageCode",  "typeId", "term", "caseSignificanceId"]

PATH_SNOMEDCT_ICD10 = os.path.join(
    "/DATA/ezotova_data/MAPPING/database", 
    "tls_Icd10cmHumanReadableMap_US1000124_20210901.tsv"
    )
HEADERS_SNOMEDCT_ICD10 = ["id", "effectiveTime", "active", 
    "moduleId", "refsetId", "referencedComponentId", 
    "referencedComponentName", "mapGroup", "mapPriority", "mapRule", 
    "mapAdvice", "mapTarget", "mapTargetName", "correlationId", 
    "mapCategoryId", "mapCategoryName"]

# separator = "|"
PATH_UMLS = os.path.join("/DATA/ezotova_data/UMLS/2023", "MRCONSO.RRF")
HEADERS_UMLS = ["CUI", "LAT", "TS", "LUI", "STT", "SUI", "ISPREF", "AUI", 
    "SAUI", "SCUI", "SDUI", "SAB", "TTY", "CODE", "STR", "SRL", 
    "SUPPRESS", "CVF", "_"]

PATH_UMLS_EXT =  os.path.join("/DATA/ezotova_data/Clinidmap/database", "UMLS_CIE10_WIKI.tsv")
HEADERS_UMLS_EXT = ["CUI", "LAT", "TS", "LUI", "STT", "SUI", "ISPREF", "AUI", 
    "SAUI", "SCUI", "SDUI", "SAB", "TTY", "CODE", "STR", "SRL", 
    "SUPPRESS", "CVF", "WIKIDATA", "MESH_WIKI", "SNOMED_CT_WIKI", "ICD10_WIKI", 
    "ICD10CM_WIKI", "ICD10PCS_WIKI", "NCBI_WIKI", "WN31", "WN30", "SENSE", 
    "SNOMEDCT2ICD10", "ICD10ENG", "ICD10CM_SPA", "ICD10OCS_SPA"]


PATH_SEMANTIC_GROUPS  = os.path.join("/DATA/ezotova_data/MAPPING/database", "SemGroups.txt")
HEADERS_SEMANTIC_GROUPS = ["STY", "DEF", "UI", "TYPE"]

PATH_SEMANTIC_TYPES = os.path.join("/DATA/ezotova_data/UMLS/2023", "MRSTY.RRF")
HEADERS_SEMANTIC_TYPES = ["CUI", "TUI", "STN", "STY", "ATUI", "CVF"]
