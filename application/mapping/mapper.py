import time

from application.mapping.elastic_search import query_search, result2list_unique, get_query, get_umls_query
from application.mapping.mapping_logic import map_source_umls, cui2sty
from application.mapping.util import wikidata2wikipedia_urls

import application.constants as constants

def flatten(l):
    return [item for sublist in l for item in sublist]



class IDMapper: 
    def __init__(self):
        self.umls_cuis = None 
        
    def map(self, source_id, source_type, language, wiki=False): 

        start = time.time()

        match source_type: 
            case 'UMLS': 
                result = map_source_umls(source_id, language)
                cuis_list = [source_id]
            # case 'SNOMED_CT': 
            #     result = map_source_snomedct(source_id, language)
            # case 'ICD10CM': 
            #     result = map_source_icd10cm(source_id, language)
            # case 'ICD10PCS': 
            #     result = map_source_icd10pcs(source_id, language)
            case _: 
                result['status'] = '{} is irrelevant Source Taxonomy Type. Must be: UMLS, SNOMED_CT, ICD10CM or ICD10PCS'.format(self.source_type)

        # cuis_list = [source_type]
        # for i in result['UMLS_CUI']: 
        #     if i['id'] != []: 
        #         cuis_list.append(i['id'])

        if len(cuis_list) > 0: 
            self.umls_cuis = list(set([d for d in cuis_list]))
            sem_types = cui2sty(self.umls_cuis)
            print(sem_types)
            result = result | sem_types

        if wiki: 
            wikidata_items = []
            wiki_result = []
            if self.umls_cuis:
                for c in self.umls_cuis:
                    q_dic_ = get_query('cui', c)
                    wiki_result = query_search(q_dic_, constants.CUI2WIKI)
                    print('WIKI RESULT')
                    print(wiki_result)
                    wikidata_items = result2list_unique(wiki_result, 'item') # get links to the Wikidata items
                    result['wikidata_item_url'] = wikidata_items
                    
                    if len(wikidata_items) > 0: 
                        wikipedia_urls = wikidata2wikipedia_urls(wikidata_items)
                        result['wikipedia_article_url'] = wikipedia_urls
                    else:
                        q_dic = get_umls_query(c)
                        umls_mesh = query_search(q_dic, constants.UMLS)
                        mesh = result2list_unique(umls_mesh, 'CODE')
                        wikidata_items = []
                        for m in list(set(mesh)): 
                            q_dic_m = get_query("mesh", m)
                            wiki_result = query_search(q_dic_m, constants.CUI2WIKI) # config.MESH2WIKI
                            if wiki_result['hits']['total']['value'] > 0:
                                for hit in wiki_result['hits']['hits']: 
                                    if hit['_source']['item'] not in wikidata_items: 
                                        wikidata_items.append(hit['_source']['item'])
                            
                        result['wikidata_item_url'] = wikidata_items
                        wikipedia_urls = wikidata2wikipedia_urls(wikidata_items)
                        result['wikipedia_article_url'] = wikipedia_urls
            else: 
                result['wiki_status'] = 'No code provided for search in Wikidata and WordNet'

            if len(wikidata_items) == 0: 
                if len(result['ICD10CM_ES']) > 0: 
                    for c in result['ICD10CM_ES']:
                        q_dic_ = get_query('ICD10', c['id'])
                        wiki_result = query_search(q_dic_, constants.CUI2WIKI)
                        wikidata_items = result2list_unique(wiki_result, 'item') # get links to the Wikidata items
                        result['wikidata_item_url'] = wikidata_items      
                        wikipedia_urls = wikidata2wikipedia_urls(wikidata_items)
                        result['wikipedia_article_url'] = wikipedia_urls
                else: 
                    result['wiki_status'] = 'No code provided for search in Wikidata and WordNet'                      
            
            wordnet31_ids = result2list_(wiki_result, 'wordnet31_id')
            wordnet_senses = result2list_(wiki_result, 'sense')
            wns = []
            for w, s in zip(wordnet31_ids, wordnet_senses): 
                d = {}
                d['wordnet3.1_id'] = w
                d['senses'] = s
                if d not in wns: 
                    wns.append(d)
            result['wordnet'] = wns
            
        end = time.time()
        hours, rem = divmod(end-start, 3600)
        minutes, seconds = divmod(rem, 60)
        # print("Time: {:0>2}:{:0>2}:{:05.4f}".format(int(hours),int(minutes),seconds))

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

