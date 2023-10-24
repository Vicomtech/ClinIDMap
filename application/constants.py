import os 


DATABASE = "database"

### Names of Elastic index for each database
# UMLS = "umls" 
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

HEADRES_ICD10CM = ["CODE", "ICD10DESCR_SPA"]
HEADRES_ICD10PCS = ["CODE", "ICD10DESCR_SPA"]

PATH_WIKI_MESH = os.path.join(DATABASE, "query_wikidata_mesh.tsv")
HEADRES_WIKI_MESH = ["item", "itemLabel", "itemDescription", "code"]

PATH_WIKI_WNET = os.path.join(
    DATABASE, 
    "query_wikidata_identificador_de_synset_de_WordNet_3_1.tsv"
    )
HEADERS_WIKI_WNET = ["item", "wordnet_id", "MESH", "CUI"]

HEADERS_SNOMEDCT_EN = ["id", "effectiveTime", "active", "moduleId", "conceptId", "languageCode", "typeId", "term", "caseSignificanceId"]

HEADERS_SNOMEDCT_ES = ["id", "effectiveTime", "active", "moduleId", "conceptId", "languageCode",  "typeId", "term", "caseSignificanceId"]

HEADERS_SNOMEDCT_ICD10 = ["id", "effectiveTime", "active", 
    "moduleId", "refsetId", "referencedComponentId", 
    "referencedComponentName", "mapGroup", "mapPriority", "mapRule", 
    "mapAdvice", "mapTarget", "mapTargetName", "correlationId", 
    "mapCategoryId", "mapCategoryName"]


HEADERS_UMLS = ["CUI", "LAT", "TS", "LUI", "STT", "SUI", "ISPREF", "AUI", 
    "SAUI", "SCUI", "SDUI", "SAB", "TTY", "CODE", "STR", "SRL", 
    "SUPPRESS", "CVF", "_"]

HEADERS_UMLS_EXT = ["CUI", "LAT", "TS", "LUI", "STT", "SUI", "ISPREF", "AUI", 
    "SAUI", "SCUI", "SDUI", "SAB", "TTY", "CODE", "STR", "SRL", 
    "SUPPRESS", "CVF", "WIKIDATA", "MESH_WIKI", "SNOMED_CT_WIKI", "ICD10_WIKI", 
    "ICD10CM_WIKI", "ICD10PCS_WIKI", "NCBI_WIKI", "WN31", "WN30", "WN_SENSE", 
    "SNOMEDCT2ICD10", "ICD10ENG", "ICD10CM_SPA", "ICD10OCS_SPA"]


PATH_SEMANTIC_GROUPS  = os.path.join("database/SemGroups.txt")
HEADERS_SEMANTIC_GROUPS = ["STY", "DEF", "UI", "TYPE"]

PATH_SEMANTIC_TYPES = os.path.join("/DATA/ezotova_data/UMLS/2023", "MRSTY.RRF")
HEADERS_SEMANTIC_TYPES = ["CUI", "TUI", "STN", "STY", "ATUI", "CVF"]
