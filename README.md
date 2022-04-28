## Clin ID Map

**ClinIDMap**  is a tool for mapping identifiers (ID, codes) between clinical ontologies and lexical resources.

ClinIDMap interlinks identifiers from UMLS, SMOMED-CT, ICD-10 and the corresponding Wikipedia articles for concepts
from the UMLS Metathesaurus. It's main goal is to provide semantic interoperability across the clinical concepts from various
knowledge bases. 

### Requiremants and Installation 



### CLI use 

```shell script
# get all Wikidata and Wikipedia items related to the code
python mapping_elastic.py <taxonomy type> <taxonomy id> --wiki 
# skip Wikidata and Wikipedia 
python mapping_elastic.py <taxonomy type> <taxonomy id> --no-wiki 
```