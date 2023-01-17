## Clin ID Map

**ClinIDMap**  is a tool for mapping identifiers (ID, codes) between clinical ontologies and lexical resources.

ClinIDMap interlinks identifiers from UMLS, SMOMED-CT, ICD-10, the corresponding Wikipedia articles and WordNet synsets. It's main goal is to provide semantic interoperability across the clinical concepts from various knowledge bases. 

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

```shell script
# update Elasticsearch indexes 
# --headers list of headers in your table 
# --path path to the table 
# --index_name the name of the index in Elasticsearch which will be used for extracting codes. Hardcoded index names are given in the config.py file but you can provide your own names 
# --separator it is tabulator '\t' or |  
python elastic_index_db.py \\
--headers item itemLabel itemDescription code \\
--path database/cui2wiki.tsv \\
--index_name cui2wiki --separator '\t'
```

Update Wikidata and Wikipedia database: get all CUIs and MeSH codes which occur in Wikidata and Wikpedia  

```shell script
python update_wiki.py 
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

### Elastic commans 

curl 'localhost:9200/_cat/indices?v'


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
