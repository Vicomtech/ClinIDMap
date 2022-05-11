import os
from xmlrpc.client import boolean
from xxlimited import Str
import json
import time
import argparse

import config

# from search_term import search 

from elastic_search import query_search, result2list_, result2list_unique, get_query, get_umls_query, get_umls2sab_query
from elastic_utils import get_elastic

from util import wikidata2wikipedia_urls

start = time.time()

class ClinIDMapper: 
    def __init__(self, source_type, source_id, wiki, elastic=None):
        self.wiki = wiki
        self.umls = 'umls' 
        self.snomed2icd10 = config.SNOMED2ICD10
        self.snomed_es = config.SNOMED_ES
        self.snomed_en = config.SNOMED_EN
        self.icd10pcs = config.ICD10PCS
        self.icd10cm = config.ICD10CM
        self.cui2wiki = config.CUI2WIKI
        self.mesh2wiki = config.MESH2WIKI
        # TODO
        # self.wordnet2wiki = config.WORDNET2WIKI
        # semantic_types = config.SEMANTIC_TYPES
        self.umls_cuis = None 
        self.elastic = elastic
        self.result = {}
        self.source_type = source_type
        self.source_id = source_id
        
    def map(self): 
        if self.elastic is None: 
            self.elastic = get_elastic()

        self.result['source_type'] = self.source_type
        self.result['source_id'] = self.source_id

        if self.source_type == 'UMLS': 
            self.result['status'] = 'OK'
            self.umls_cuis = [self.source_id]
            #get all SNOMED codes in UMLS related to this CUI
            q_dic = get_umls_query(self.source_id, 'SNOMEDCT_US') 
            umls_result = query_search(q_dic, self.umls)
            snomed_codes_en = result2list_unique(umls_result, 'CODE')
            umls_descrs = result2list_unique(umls_result, 'STR')

            icd10cm_codes  = []
            snomed_descrs_en = []
            snomed_codes_es = []
            snomed_descrs_es  = []
            # search in SNOMED ontology
            for code in snomed_codes_en: 
                q_dic = get_query("conceptId", code)
                snomed_en_result = query_search(q_dic, self.snomed_en)
                snomed_en_result_lst = result2list_unique(snomed_en_result, 'term')
                if len(snomed_en_result_lst) != 0: 
                    snomed_descrs_en.append(' '.join(snomed_en_result_lst)) 

                q_dic = get_query("referencedComponentId", code)
                snomed_map_result = query_search(q_dic, self.snomed2icd10)
                snomed_map_result_lst = result2list_unique(snomed_map_result, 'mapTarget')

                if len(snomed_map_result_lst) != 0: 
                    for icd in snomed_map_result_lst: 
                        icd10cm_codes .append(icd)

                q_dic_es = get_query("conceptId", code)
                snomed_es_result = query_search(q_dic_es, self.snomed_es)

                snomed_es_result_term = result2list_(snomed_es_result, 'term')
                if len(snomed_es_result_term) != 0: 
                    for descript in snomed_es_result_term: 
                        snomed_descrs_es .append(descript)

                snomed_es_result_id = result2list_(snomed_es_result, 'conceptId')
                if len(snomed_es_result_id) != 0: 
                    for c in snomed_es_result_id: 
                        snomed_codes_es.append(c)

            icd10pcs_descrs_es = []
            icd10pcs_codes = []
            icd10cm_descrs_es = []

            print('PCS RESULT')
            for cui in self.umls_cuis: 
                q_dic = get_umls_query(cui, 'ICD10PCS')
                icd10pcs_umls_result = query_search(q_dic, self.umls)
                if icd10pcs_umls_result['hits']['total']['value'] > 0:
                    for hit in icd10pcs_umls_result['hits']['hits']: 
                        q_dic = get_query("codigo", hit['_source']['CODE'])
                        icd10psc_es_result =  query_search(q_dic, self.icd10pcs)  
                        if icd10psc_es_result['hits']['total']['value'] > 0:
                            for hit in icd10psc_es_result['hits']['hits']: 
                                if hit['_source']['codigo'] not in icd10pcs_codes: 
                                    icd10pcs_descrs_es.append(hit['_source']['descripcion'])
                                    icd10pcs_codes.append(hit['_source']['codigo'])
            for c in icd10cm_codes : 
                q_dic = get_query("codigo", c)
                icd10cm_es_result =  query_search(q_dic, self.icd10cm)
                if icd10cm_es_result['hits']['total']['value'] > 0:
                    for hit in icd10cm_es_result['hits']['hits']: 
                        icd10cm_descrs_es.append(hit['_source']['descripcion'])

            self.result['UMLS_CUI'] = {'ids': self.umls_cuis, 'descriptions': umls_descrs}
            self.result['SNOMED_CT_EN'] = {'ids': snomed_codes_en, 'descriptions': snomed_descrs_en}
            self.result['SNOMED_CT_ES'] = {'ids': snomed_codes_es, 'descriptions': snomed_descrs_es }
            self.result['ICD10CM_ES'] ={'ids': icd10cm_codes, 'descriptions': icd10cm_descrs_es}
            self.result['ICD10PCS_ES'] ={'ids': icd10pcs_codes, 'descriptions': icd10pcs_descrs_es}
            self.result['ICD10PCS_ES'] = {'ids': icd10pcs_codes, 'descriptions': icd10pcs_descrs_es}

        elif self.source_type == 'SNOMED_CT': 
            self.result['status'] = 'OK'
            q_dic = get_query('CODE', self.source_id)
            umls_result = query_search(q_dic, self.umls)
            self.umls_cuis = result2list_(umls_result, 'CUI')
            umls_descrs = result2list_(umls_result, 'STR')

            snomed_descrs_en = []
            snomed_codes_es = []
            snomed_descrs_es  = []
            icd10cm_codes  = []

            q_dic = get_query("conceptId", self.source_id)
            snomed_en_result = query_search(q_dic, self.snomed_en)
            if snomed_en_result['hits']['total']['value'] > 0:
                for hit in snomed_en_result['hits']['hits']: 
                    snomed_descrs_en.append(hit['_source']['term'])

            q_dic = get_query("referencedComponentId", self.source_id)
            snomed_map_result = query_search(q_dic, self.snomed2icd10)
            if snomed_map_result['hits']['total']['value'] > 0:
                for hit in snomed_map_result['hits']['hits']: 
                    icd10cm_codes .append(hit['_source']['mapTarget'])

            q_dic_es = get_query("conceptId", self.source_id)
            snomed_es_result = query_search(q_dic_es, self.snomed_es)

            if snomed_es_result['hits']['total']['value'] > 0:
                for hit in snomed_es_result['hits']['hits']: 
                    snomed_descrs_es .append(hit['_source']['term'])
                    snomed_codes_es.append(hit['_source']['conceptId'])

            icd10pcs_descrs_es = []
            icd10pcs_codes = []
            icd10cm_descrs_es = []

            print('PCS RESULT')
            for cui in self.umls_cuis: 
                q_dic = get_umls_query(cui, 'ICD10PCS')
                icd10pcs_umls_result = query_search(q_dic, self.umls)
                if icd10pcs_umls_result['hits']['total']['value'] > 0:
                    for hit in icd10pcs_umls_result['hits']['hits']: 
                        q_dic = get_query("codigo", hit['_source']['CODE'])
                        icd10psc_es_result =  query_search(q_dic, self.icd10pcs)  
                        if icd10psc_es_result['hits']['total']['value'] > 0:
                            for hit in icd10psc_es_result['hits']['hits']: 
                                if hit['_source']['codigo'] not in icd10pcs_codes: 
                                    icd10pcs_descrs_es.append(hit['_source']['descripcion'])
                                    icd10pcs_codes.append(hit['_source']['codigo'])

            for code in icd10cm_codes : 
                q_dic = get_query("codigo", code)
                icd10cm_es_result =  query_search(q_dic, self.icd10cm)
                if icd10cm_es_result['hits']['total']['value'] > 0:
                    for hit in icd10cm_es_result['hits']['hits']: 
                        icd10cm_descrs_es.append(hit['_source']['descripcion'])

            self.result['UMLS_CUI'] = {'ids': self.umls_cuis, 'descriptions': umls_descrs}
            self.result['SNOMED_CT_EN'] = {'ids': [self.source_id], 'descriptions': snomed_descrs_en} 
            self.result['SNOMED_CT_ES'] = {'ids': [self.source_id], 'descriptions': snomed_descrs_es}
            self.result['ICD10CM_ES'] = {'ids': icd10cm_codes, 'descriptions': icd10cm_descrs_es}
            self.result['ICD10PCS_ES'] = {'ids': icd10pcs_codes, 'descriptions': icd10pcs_descrs_es}

        elif self.source_type == 'ICD10CM': 
            self.result['status'] = 'OK'

            q_dic = get_query("codigo", self.source_id)
            icd10cm_es_result =  query_search(q_dic, self.icd10cm)
            icd10cm_descrs_es  = result2list_(icd10cm_es_result, 'descripcion')

            self.result['ICD10CM_ES'] = {'ids': [self.source_id], 'descriptions': icd10cm_descrs_es} 

            q_dic = get_query("mapTarget", self.source_id)
            snomed_map_result = query_search(q_dic, self.snomed2icd10)

            if snomed_map_result['hits']['total']['value'] > 0:
                self.umls_cuis = []
                umls_descrs = []
                snomed_codes_en = []
                snomed_descrs_en = []
                for hit in snomed_map_result['hits']['hits']: 
                    snomed_codes_en.append(hit['_source']['referencedComponentId'])
                    snomed_descrs_en.append(hit['_source']['referencedComponentName'])

                self.result['SNOMED_CT_EN'] = {'ids': snomed_codes_en, 'descriptions': snomed_descrs_en}

                snomed_codes_es = []
                snomed_descrs_es = []
                for snomed_id in list(set(snomed_codes_en)): 
                    q_dic_es = get_query("conceptId", snomed_id)
                    snomed_es_result = query_search(q_dic_es, self.snomed_es)
                    snomed_descrs_es = []
                    if snomed_es_result['hits']['total']['value'] > 0:
                        for hit in snomed_es_result['hits']['hits']: 
                            snomed_codes_es.append(hit['_source']['conceptId'])
                            snomed_descrs_es.append(hit['_source']['term']) 

                self.result['SNOMED_CT_ES'] = {'ids': snomed_codes_es, 'descriptions': snomed_descrs_es}

                for snomed_id in list(set(snomed_codes_en)): 
                    q_dic = get_umls2sab_query(snomed_id, 'SNOMED_US') 
                    umls_snomed_result = query_search(q_dic, self.umls)
                    umls_cui = []
                    umls_descr = []
                    if umls_snomed_result['hits']['total']['value'] > 0:
                        for hit in umls_snomed_result['hits']['hits']: 
                            umls_cui.append(hit['_source']['CUI'])
                            umls_descr.append(hit['_source']['STR'])

                    self.umls_cuis.append(umls_cui)
                    umls_descrs.append(umls_descr)

                self.result['UMLS_CUI'] = {'ids': self.umls_cuis, 'descriptions': umls_descrs}

            else: 
                self.umls_cuis = []
                umls_descrs = []
                q_dic = get_umls2sab_query(self.source_id, 'ICD10CM') 
                umls_icd_result = query_search(q_dic, self.umls)

                if umls_icd_result['hits']['total']['value'] > 0:
                    for hit in umls_icd_result['hits']['hits']: 
                        self.umls_cuis.append(hit['_source']['CUI'])
                        umls_descrs.append(hit['_source']['STR'])

                self.result['UMLS_CUI'] = {'ids': self.umls_cuis, 'descriptions': umls_descrs}

                snomed_ids_umls = []
                for c in list(set(self.umls_cuis)): 
                    q_dic = get_umls_query(c, 'SNOMEDCT_US') 
                    umls_snomed_result =  query_search(q_dic, self.umls)
                    if umls_snomed_result['hits']['total']['value'] > 0:
                        for hit in umls_snomed_result['hits']['hits']: 
                            snomed_ids_umls.append(hit['_source']['CODE'])

                snomed_codes_es = []
                snomed_descrs_es = []
                snomed_codes_en = []
                snomed_descrs_en = []
                for snomed_id in list(set(snomed_ids_umls)): 
                    q_dic_es = get_query("conceptId", snomed_id)
                    snomed_es_result = query_search(q_dic_es, self.snomed_es)
                    snomed_descrs_es = []
                    if snomed_es_result['hits']['total']['value'] > 0:
                        for hit in snomed_es_result['hits']['hits']: 
                            snomed_codes_es.append(hit['_source']['conceptId'])
                            snomed_descrs_es.append(hit['_source']['term']) 
                    
                    snomed_en_result = query_search(q_dic_es, self.snomed_en)
                    if snomed_en_result['hits']['total']['value'] > 0:
                        for hit in snomed_en_result['hits']['hits']: 
                            snomed_codes_en.append(hit['_source']['conceptId'])
                            snomed_descrs_en.append(hit['_source']['term']) 
                
                self.result['SNOMEDCT_ES'] = {'ids': snomed_codes_es, 'descriptions': snomed_descrs_es}
                self.result['SNOMEDCT_EN'] = {'ids': snomed_codes_en, 'descriptions': snomed_descrs_en}

        elif self.source_type == 'ICD10PCS':
            self.result['status'] = 'OK'

            q_dic = get_query("codigo", self.source_id)
            icd10cm_es_result =  query_search(q_dic, self.icd10pcs)
            icd10cm_descrs_es  = result2list_(icd10cm_es_result, 'descripcion')

            self.result['ICD10PCS_ES'] = {'ids': [self.source_id], 'descriptions': icd10cm_descrs_es} 

            q_dic = get_umls2sab_query(self.source_id, 'ICD10PCS') 
            umls_icd_result = query_search(q_dic, self.umls)
            self.umls_cuis = []
            umls_descrs = []
            if umls_icd_result['hits']['total']['value'] > 0:
                for hit in umls_icd_result['hits']['hits']: 
                    self.umls_cuis.append(hit['_source']['CUI'])
                    umls_descrs.append(hit['_source']['STR'])

            self.result['UMLS_CUI'] = {'ids': self.umls_cuis, 'descriptions': umls_descrs}

            snomed_codes_en_umls = []
            for c in self.umls_cuis: 
                q_dic = get_umls_query(c, 'SNOMEDCT_US') 
                umls_snomed_result = query_search(q_dic, self.umls)
                if umls_snomed_result['hits']['total']['value'] > 0:
                    for hit in umls_snomed_result['hits']['hits']: 
                        if hit['_source']['CODE'] not in snomed_codes_en_umls: 
                            snomed_codes_en_umls.append(hit['_source']['CODE'])
                            
            snomed_codes_en = []
            snomed_descrs_en = []
            snomed_codes_es = []
            snomed_descrs_es = []
            for code in snomed_codes_en_umls: 
                q_dic = get_query("conceptId", code)
                snomed_en_result = query_search(q_dic, self.snomed_en)
                if snomed_en_result['hits']['total']['value'] > 0:
                    for hit in snomed_en_result['hits']['hits']: 
                        if hit['_source']['conceptId'] not in snomed_codes_en: 
                            snomed_descrs_en.append(hit['_source']['term'])
                            snomed_codes_en.append(hit['_source']['conceptId'])

                snomed_es_result = query_search(q_dic, self.snomed_es)
                if snomed_es_result['hits']['total']['value'] > 0:
                    for hit in snomed_es_result['hits']['hits']: 
                        if hit['_source']['conceptId'] not in snomed_codes_es: 
                            snomed_descrs_es.append(hit['_source']['term'])
                            snomed_codes_es.append(hit['_source']['conceptId'])
                            
            self.result['SNOMEDCT_EN'] = {'ids':snomed_codes_en, 'descriptions': snomed_descrs_en}
            self.result['SNOMEDCT_ES'] = {'ids':snomed_codes_es, 'descriptions': snomed_descrs_es}

        else: 
            self.result['status'] = '{} is irrelevant Source Taxonomy Type. Must be: UMLS, SNOMED_CT, ICD10CM or ICD10PCS'.format(source_type)

        if self.wiki: 
            if self.umls_cuis:
                for c in list(set(self.umls_cuis)):
                    q_dic_ = get_query('code', c)
                    wiki_result = query_search(q_dic_, 'cui2wiki')
                    wikidata_items = result2list_(wiki_result, 'item')
                    self.result['wikidata_item_url'] = wikidata_items
                    
                    if len(wikidata_items) > 0: 
                        wikipedia_urls = wikidata2wikipedia_urls(wikidata_items)
                        self.result['wikipedia_article_url'] = wikipedia_urls
                    else:
                        q_dic = get_umls_query(c, 'MSH')
                        umls_mesh = query_search(q_dic, self.umls)
                        mesh = result2list_(umls_mesh, 'CODE')
                        wikidata_items = []
                        for m in list(set(mesh)): 
                            q_dic_m = get_query("code", m)
                            wiki_result_m = query_search(q_dic_m, self.mesh2wiki)
                            if wiki_result_m['hits']['total']['value'] > 0:
                                for hit in wiki_result_m['hits']['hits']: 
                                    if hit['_source']['item'] not in wikidata_items: 
                                        wikidata_items.append(hit['_source']['item'])
                            
                        self.result['wikidata_item_url'] = wikidata_items
                        wikipedia_urls = wikidata2wikipedia_urls(wikidata_items)
                        self.result['wikipedia_article_url'] = wikipedia_urls
            else: 
                self.result['wiki_status'] = 'Provide valid Taxonomy Type or CUI for search in Wikidata'

        return self.result

end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("Time: {:0>2}:{:0>2}:{:05.4f}".format(int(hours),int(minutes),seconds))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clinical IDs mapping')

    parser.add_argument('source_type', type=str, help='Type of taxonomy to map with')
    parser.add_argument('source_id', type=str, help='ID from the taxonomy to map')
    parser.add_argument('--wiki', action='store_true')
    parser.add_argument('--no-wiki', action='store_false')
    parser.set_defaults(feature=True)

    args = parser.parse_args()

    # source_id = 'C0020587' #C0026845 # 'C0011860' #C0026845 # ICD-10-PCS C0020587 C0020587
    # source_type = 'UMLS'
    # source_type = 'UMLS' # 'C0011860' # ICD10CM # SNOMED # WORD # ICD10PCS
    # source_id = 'C0011860' # UMLS C3277232 C0001175 # C0024808 # C0678449 # C1533734 #286992006
    # source_id = '2006300612' # SNOMEDCT # 19997007 # 20016009 # 20063006
    # source_id = 'H35.35' # H35.352   # ICD10CM

    # source_id = 'C0020587' #C0026845 # 'C0011860' #C0026845 # ICD-10-PCS C0020587 C0020587
    # source_type = 'UMLS'

    # source_id = '19997007' # '20016009' 44054006 # ICD-10-PCS 19997007 70503004 151644003  183409005 151646001
    # source_type = 'SNOMED_CT'

    # source_id = 'A03.1' 
    # source_id = 'H35.35'
    # source_type = 'ICD10CM'

    # source_id = 'GZFZZZZ'
    # source_type = 'ICD10PCS'
    # print('Source type to map:', source_type)

    mapper = ClinIDMapper(args.source_type, args.source_id, args.wiki)
    result_dict = mapper.map()

    for k, v in result_dict.items(): 
        print(k)
        print(v)

    with open(args.source_type+'_'+args.source_id+'.json', 'w', encoding='utf-8') as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=4)




