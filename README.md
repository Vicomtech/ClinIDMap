## ClinIDMap

**ClinIDMap**  is a tool for mapping identifiers (ID, codes) between clinical ontologies and lexical resources.

ClinIDMap interlinks identifiers from UMLS, SMOMED-CT, ICD-10, the corresponding Wikipedia articles and WordNet synsets. It's main goal is to provide semantic interoperability across the clinical concepts from various knowledge bases. 


uvicorn clinidmap.web.main:create_app --host 0.0.0.0 --port 5858 --reload


### CLI 

To update the Wikidata codes

```shell script
python -m clinidmap.wiki.update_wiki
```

### Application 

The API has three methods

1) clinidmap/{index_name} Post Index - method for database indexing 

Input format contains the source ID we want to map, the type of the taxonomy and the flag if we need to get the infromation about this ID from Wikipedia and WordNet. 

The source type must me UMLS, SNOMED_CT, ICD10CM or ICD10PCS. 

```shell script
{
  "source_id": "C0020587",
  "source_type": "UMLS",
  "wiki": false
}
```

2) clinidmap/{index_name} Delete Index - method for index deleting 

```shell script
{
  "path": "string",
  "headers": [
    "string"
  ],
  "separator": "string"
}
```

3) clinidmap/map Get Item Mapping - the main method for code mapping



### Requirements and Installation 

1. Before starting, the following databases should be downloaded. We do not provide the databases (ontologies and taxonomies), as they depend on the licences and cannot be publicly distributed. We share only CUI and MESH that occur in Wikipedia and Wikidata in database folder.  

UMLS Metathesaurus https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html

SNOMED-CT 2 ICD-10 Map https://www.nlm.nih.gov/research/umls/mapping_projects/snomedct_to_icd10cm.html

SNOMED-CT International Edition https://www.nlm.nih.gov/healthit/snomedct/international.html 

SNOMED_CT Spanish Edition https://snomed-ct.sanidad.gob.es/snomed-ct/descarga/listadoDocumentos.do

ICD-10 CM and PCS International https://www.cms.gov/medicare/icd-10/2022-icd-10-cm https://www.cms.gov/medicare/icd-10/2022-icd-10-pcs

ICD-10 CM and PCS Spanish Version https://www.sanidad.gob.es/fr/estadEstudios/estadisticas/normalizacion/home.htm

2. These databases will be uploaded and indexed in Elasticseach, which should be installed on your device. Here, we install Elasticsearch as a Docker application.  

Start Docker application:

```shell script
docker-compose up
```

Stop and delete Docker application: 

```shell script
docker-compose down
```

When the Elasticsearch API is up, we should update databases in Elasticsearch index 

We pass all the CSV tables to the API. To process them correctly, the following arguments should be provided. 
Tables must be \t or | separated 

The list of index names is hardcoded in config.py, you can provide your own names.

Update Wikidata and Wikipedia database: get all CUIs and MeSH codes which occur in Wikidata and Wikpedia  

```shell script
python -m clinidmap.wiki_wordnet.update_wiki
```

### Configuration 


### CLI use 

Principal use 

```shell script
# get all Wikidata and Wikipedia items related to the code
python mapping.py <taxonomy type> <taxonomy id> --wiki 

# skip Wikidata and Wikipedia 
python mapping.py <taxonomy type> <taxonomy id> --no-wiki 
```

### Elastic commands 

curl 'localhost:9200/_cat/indices?v'

curl -XDELETE 'http://localhost:9500/umls'



### Citing 
```
@inproceedings{zotova2022lrec,
  title={ClinIDMap: Clinical IDs Mapping for Data Interoperability},
  author={Zotova, Elena and Cuadros, Montse and Rigau, German},
  booktitle = {{LREC} 2022, 13th International Conference on  Language Resources (LRs) and Evaluation for Language Technologies (LT)},
  pages     = {3661--3669},
  year      = {2022}
}
```
###

to try 

% UMLS
C0011860 - diabetes tipo 2
C0025519 - metabolsm 

% SNOMED_CT
19997007 - hipnosis

% ICD10CM
H35.35 - Cystoid macular degeneration



