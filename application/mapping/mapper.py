import time

from application.mapping.mapping_logic import map_source_umls, map_source_sab
from application.mapping.util import wikidata2wikipedia_urls

import application.constants as constants


class IDMapper: 
    def __init__(self):
        self.cuis_list = []
    
    def map_timer(self, start, end):
        hours, rem = divmod(end-start, 3600)
        minutes, seconds = divmod(rem, 60)
        print("Time: {:0>2}:{:0>2}:{:05.4f}".format(int(hours),int(minutes),seconds))
        return "{:0>2}:{:0>2}:{:05.4f}".format(int(hours),int(minutes),seconds)

    def map(self, source_id, source_type, language, wiki=False): 

        start = time.time()
        match source_type:
            case 'UMLS': 
                result = map_source_umls(source_id, language)
                self.cuis_list = [source_id]
            case 'SNOMED_CT': 
                sab = 'SNOMEDCT_US'
                if language == 'SPA':
                    sab = 'SCTSPA'
                result = map_source_sab(source_id, sab, language)
                self.cuis_list = [d['CUI'] for d in result['UMLS']]
            case 'ICD10CM':
                sab = 'ICD10CM'
                result = map_source_sab(source_id, sab, language)
                self.cuis_list = [d['CUI'] for d in result['UMLS']]
            case 'ICD10PCS':
                sab = 'ICD10PCS'
                result = map_source_sab(source_id, sab, language)
                self.cuis_list = [d['CUI'] for d in result['UMLS']]
            case _: 
                result['status'] = '{} is irrelevant Source Taxonomy Type. Must be: UMLS, SNOMED_CT, ICD10CM or ICD10PCS'.format(self.source_type)

        if wiki: 
            wikidata_items = [d['WIKIDATA'] for d in result['UMLS']]
            urls = {}
            for item, cui in zip(wikidata_items, self.cuis_list): 
                wikipedia_urls = wikidata2wikipedia_urls(item)
                urls[cui] = wikipedia_urls   

        result['wikipedia_article_url'] = urls         
        end = time.time()

        result['time'] = self.map_timer(start, end)

        return result



# if __name__ == "__main__":
#     # parser = argparse.ArgumentParser(description='Medical IDs mapping')

#     # parser.add_argument('source_type', type=str, help='Type of taxonomy to map with. Must be: UMLS, SNOMED_CT, ICD10CM or ICD10PCS')
#     # parser.add_argument('source_id', type=str, help='ID from the taxonomy to map')
#     # parser.add_argument('--wiki', action='store_true')
#     # parser.add_argument('--no-wiki', action='store_false')
#     # parser.set_defaults(wiki=True)

#     # args = parser.parse_args()

#     # source_id = 'C0020587' #C0026845 # 'C0011860' #C0026845 # ICD-10-PCS C0020587 C0020587
#     # source_type = 'UMLS'
#     # source_type = 'UMLS' # 'C0011860' # ICD10CM # SNOMED # WORD # ICD10PCS
#     # source_id = 'C0011860' # UMLS C3277232 C0001175 # C0024808 # C0678449 # C1533734 #286992006
#     # source_id = '2006300612' # SNOMEDCT # 19997007 # 20016009 # 20063006
#     # source_id = 'H35.35' # H35.352   # ICD10CM

#     # source_id = 'C0026845' #C0026845 # 'C0011860' #C0026845 # ICD-10-PCS C0020587 C0020587
#     # source_type = 'UMLS'

#     source_id = '19997007' # '20016009' 44054006 # ICD-10-PCS 19997007 70503004 151644003  183409005 151646001
#     source_type = 'SNOMED_CT'

#     # source_id = 'A03.1' 
#     # source_id = 'H35.35'
#     # source_type = 'ICD10CM'

#     # source_id = 'GZFZZZZ'
#     # source_type = 'ICD10PCS'
#     # print('Source type to map:', source_type)

