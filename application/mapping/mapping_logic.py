import pandas as pd

from application.mapping.elastic_search import query_search, get_query, get_umls_query, get_umls2sab_query, result2dicts, result2list_unique
from application.db_processing.elastic_utils import get_elastic
from application.mapping.util import lists2tuples

from application import constants


# def icd10_in_umls(umls_cuis, icd10_type): 
#     '''Search ICD-10 code in UMLS'''

#     icd10_conf = ''
#     match icd10_type: 
#         case 'ICD10PCS': 
#             icd10_conf = constants.ICD10PCS
#         case 'ICD10CM': 
#             icd10_conf = constants.ICD10CM
#         case _: 
#             print('Wrong ICD-10 type')

#     icd10_descrs_es = []
#     icd10_codes = []
    
#     for cui in umls_cuis: 
#         q_dic = get_umls_query(cui)
#         # print(q_dic)

#         icd10pcs_umls_result = query_search(q_dic, constants.UMLS)
#         # print(icd10pcs_umls_result)

#         if icd10pcs_umls_result['hits']['total']['value'] > 0:
#             for hit in icd10pcs_umls_result['hits']['hits']: 
#                 q_dic = get_query("CODE", hit['_source']['CODE'])
#                 icd10psc_es_result =  query_search(q_dic, icd10_conf)  
#                 if icd10psc_es_result['hits']['total']['value'] > 0:
#                     for hit in icd10psc_es_result['hits']['hits']: 
#                         if hit['_source']['CODE'] not in icd10_codes: 
#                             icd10_descrs_es.append(hit['_source']['ICD10DESCR_SPA'])
#                             icd10_codes.append(hit['_source']['CODE'])

#     result = lists2tuples(icd10_codes, icd10_descrs_es)
#     return result

def map_source_umls(source_id, language): 
    '''All codes related to UMLS CUI'''
    result = {} 
    result['status'] = 'OK'

    umls_cuis = [source_id]
    #get all SNOMED codes in UMLS related to this CUI
    q_dic = get_umls_query(source_id, language) 
    print('QUERY', q_dic)
    
    umls_result = query_search(q_dic, constants.UMLS_EXT)
    print('RESULT')
    # print(umls_result)
    # snomed_codes_en = result2list_(umls_result, 'CODE')
    # umls_descrs = result2list_(umls_result, 'STR')
    # dict_names = result2list_(umls_result, 'SAB')
    result = result2dicts(umls_result)
    print(result)

    icd10cm_codes  = []
    snomed_descrs_en = []
    snomed_codes_es = []
    snomed_descrs_es  = []
    # search in SNOMED-CT
    
    # for code in snomed_codes_en: 
    #     q_dic = get_query("conceptId", code)

    #     snomed_en_result = query_search(q_dic, constants.SNOMED_EN)
    #     snomed_en_result_lst = result2list_unique(snomed_en_result, 'term')
    #     if len(snomed_en_result_lst) != 0: 
    #         snomed_descrs_en.append(' '.join(snomed_en_result_lst)) 

    #     q_dic = get_query("referencedComponentId", code)
    #     snomed_map_result = query_search(q_dic, constants.SNOMED2ICD10)
    #     snomed_map_result_lst = result2list_unique(snomed_map_result, 'mapTarget')

    #     if len(snomed_map_result_lst) > 0: 
    #         for icd in snomed_map_result_lst: 
    #             icd10cm_codes.append(icd)

    #     q_dic_es = get_query("conceptId", code)
    #     snomed_es_result = query_search(q_dic_es, constants.SNOMED_ES)

    #     snomed_es_result_term = result2list_(snomed_es_result, 'term')

    #     if len(snomed_es_result_term) > 0: 
    #         for descript in snomed_es_result_term: 
    #             snomed_descrs_es .append(descript)

    #     snomed_es_result_id = result2list_(snomed_es_result, 'conceptId')
    #     if len(snomed_es_result_id) > 0: 
    #         for c in snomed_es_result_id: 
    #             snomed_codes_es.append(c)

    # icd10cm_descrs_es = []
    # for c in icd10cm_codes : 
    #     q_dic = get_query("CODE", c)
    #     icd10cm_es_result =  query_search(q_dic, constants.ICD10CM)
    #     if icd10cm_es_result['hits']['total']['value'] > 0:
    #         for hit in icd10cm_es_result['hits']['hits']: 
    #             icd10cm_descrs_es.append(hit['_source']['ICD10DESCR_SPA'])

    # d_list = []
    # for descr in umls_descrs: 
    #     d = {}
    #     d['id'] = source_id
    #     d['description'] = descr
    #     d_list.append(d)

    # result['UMLS_CUI'] = d_list

    # result['SNOMED_CT_EN'] = lists2tuples(snomed_codes_en, snomed_descrs_en)
    # result['SNOMED_CT_ES'] = lists2tuples(snomed_codes_es, snomed_descrs_es)

    # result['ICD10CM_ES'] = lists2tuples(icd10cm_codes, icd10cm_descrs_es)
    # result['ICD10PCS_ES'] =  icd10_in_umls(umls_cuis, 'ICD10PCS')
 
 
    # result['ICD10CM_EN'] = lists2tuples(icd10cm_codes, icd10cm_descrs_es)

    return result 

# def map_source_snomedct(source_id): 

#     result = {}
#     result['status'] = 'OK'
#     result['source_id'] = source_id

#     q_dic = get_query('CODE', source_id)
#     umls_result = query_search(q_dic, constants.UMLS)

#     umls_cuis = result2list_(umls_result, 'CUI')
#     umls_descrs = result2list_(umls_result, 'STR')

#     snomed_descrs_en = []
#     snomed_codes_es = []
#     snomed_descrs_es  = []
#     icd10cm_codes  = []

#     q_dic = get_query("conceptId", source_id)
#     snomed_en_result = query_search(q_dic, constants.SNOMED_EN)
#     if snomed_en_result['hits']['total']['value'] > 0:
#         for hit in snomed_en_result['hits']['hits']: 
#             snomed_descrs_en.append(hit['_source']['term'])

#     q_dic = get_query("referencedComponentId", source_id)
#     snomed_map_result = query_search(q_dic, constants.SNOMED2ICD10)
#     if snomed_map_result['hits']['total']['value'] > 0:
#         for hit in snomed_map_result['hits']['hits']: 
#             icd10cm_codes .append(hit['_source']['mapTarget'])

#     q_dic_es = get_query("conceptId", source_id)
#     snomed_es_result = query_search(q_dic_es, constants.SNOMED_ES)

#     if snomed_es_result['hits']['total']['value'] > 0:
#         for hit in snomed_es_result['hits']['hits']: 
#             snomed_descrs_es .append(hit['_source']['term'])
#             snomed_codes_es.append(hit['_source']['conceptId'])

#     icd10cm_descrs_es = []

#     for code in icd10cm_codes : 
#         q_dic = get_query("CODE", code)
#         icd10cm_es_result =  query_search(q_dic, constants.ICD10CM)
#         if icd10cm_es_result['hits']['total']['value'] > 0:
#             for hit in icd10cm_es_result['hits']['hits']: 
#                 icd10cm_descrs_es.append(hit['_source']['ICD10DESCR_SPA'])

#     result['UMLS_CUI'] = lists2tuples(umls_cuis, umls_descrs)

#     result['SNOMED_CT_EN'] = lists2tuples([source_id], snomed_descrs_en)
#     result['SNOMED_CT_ES'] = lists2tuples([source_id], snomed_descrs_es)

#     result['ICD10CM_ES'] = lists2tuples(icd10cm_codes, icd10cm_descrs_es)
#     result['ICD10PCS_ES'] = icd10_in_umls(umls_cuis, 'ICD10PCS')

#     return result

# def map_source_icd10cm(source_id): 
#     result = {}
#     result['status'] = 'OK'
#     result['source_id'] = source_id

#     result['SNOMED_CT_ES'] = []
#     result['SNOMED_CT_EN'] = []
#     result['ICD10CM_ES'] = []


#     # search in ICD-10_CM
#     q_dic = get_query("CODE", source_id) 
#     icd10cm_es_result =  query_search(q_dic, constants.ICD10CM)
#     icd10cm_descrs_es  = result2list_(icd10cm_es_result, 'ICD10DESCR_SPA')
#     # search in SNOMED-CT to ICD-10 mapping
#     q_dic = get_query("mapTarget", source_id)
#     snomed_map_result = query_search(q_dic, constants.SNOMED2ICD10)

#     umls_cuis = []
#     umls_descrs = []
#     snomed_codes_en = []
#     snomed_descrs_en = []
    
#     if snomed_map_result['hits']['total']['value'] > 0:

#         for hit in snomed_map_result['hits']['hits']: 
#             snomed_codes_en.append(hit['_source']['referencedComponentId'])
#             snomed_descrs_en.append(hit['_source']['referencedComponentName'])

    
#         snomed_codes_es = []
#         snomed_descrs_es = []
#         for snomed_id in list(set(snomed_codes_en)): 
#             q_dic_es = get_query("conceptId", snomed_id)
#             snomed_es_result = query_search(q_dic_es, constants.SNOMED_ES)
#             snomed_descrs_es = []
#             if snomed_es_result['hits']['total']['value'] > 0:
#                 for hit in snomed_es_result['hits']['hits']: 
#                     snomed_codes_es.append(hit['_source']['conceptId'])
#                     snomed_descrs_es.append(hit['_source']['term']) 

#         result['SNOMED_CT_ES'] = lists2tuples(snomed_codes_es, snomed_descrs_es)

#         for snomed_id in list(set(snomed_codes_en)): 
#             q_dic = get_umls2sab_query(snomed_id, 'SNOMED_US') 
#             umls_snomed_result = query_search(q_dic, constants.UMLS)
#             umls_cui = []
#             umls_descr = []
#             if umls_snomed_result['hits']['total']['value'] > 0:
#                 for hit in umls_snomed_result['hits']['hits']: 
#                     umls_cui.append(hit['_source']['CUI'])
#                     umls_descr.append(hit['_source']['STR'])
#             if umls_cui not in umls_cuis and umls_cui != []: 
#                 umls_cuis.append(umls_cui)
#                 umls_descrs.append(umls_descr)

#         result['ICD10CM_ES'] = lists2tuples([source_id], icd10cm_descrs_es) 

#         if len(umls_cuis) > 0: 
#             result['UMLS_CUI'] = lists2tuples(umls_cuis, umls_descrs)
#         else: 
#             result['UMLS_CUI'] = []

#     else: 
#         # search ICD-10 in UMLS
#         q_dic = get_umls2sab_query(source_id, 'ICD10CM') 
#         umls_icd_result = query_search(q_dic, constants.UMLS)

#         if umls_icd_result['hits']['total']['value'] > 0:
#             for hit in umls_icd_result['hits']['hits']: 
#                 umls_cuis.append(hit['_source']['CUI'])
#                 umls_descrs.append(hit['_source']['STR'])
                
#         if len(umls_cuis) > 0: 
#             result['UMLS_CUI'] = lists2tuples(umls_cuis, umls_descrs)
#         else: 
#             result['UMLS_CUI'] = []        
#         # result['UMLS_CUI'] = lists2tuples(umls_cuis, umls_descrs)

#         snomed_ids_umls = []
#         for c in list(set(umls_cuis)): 
#             q_dic = get_umls_query(c, 'SNOMEDCT_US') 
#             umls_snomed_result =  query_search(q_dic, constants.UMLS)
#             if umls_snomed_result['hits']['total']['value'] > 0:
#                 for hit in umls_snomed_result['hits']['hits']: 
#                     snomed_ids_umls.append(hit['_source']['CODE'])

#         snomed_codes_es = []
#         snomed_descrs_es = []
#         snomed_codes_en = []
#         snomed_descrs_en = []
#         for snomed_id in list(set(snomed_ids_umls)): 
#             q_dic_es = get_query("conceptId", snomed_id)
#             snomed_es_result = query_search(q_dic_es, constants.SNOMED_ES)
#             snomed_descrs_es = []
#             if snomed_es_result['hits']['total']['value'] > 0:
#                 for hit in snomed_es_result['hits']['hits']: 
#                     snomed_codes_es.append(hit['_source']['conceptId'])
#                     snomed_descrs_es.append(hit['_source']['term']) 
            
#             snomed_en_result = query_search(q_dic_es, constants.SNOMED_EN)
#             if snomed_en_result['hits']['total']['value'] > 0:
#                 for hit in snomed_en_result['hits']['hits']: 
#                     snomed_codes_en.append(hit['_source']['conceptId'])
#                     snomed_descrs_en.append(hit['_source']['term']) 
        
#         result['SNOMED_CT_ES'] = lists2tuples(snomed_codes_es, snomed_descrs_es)
#         result['SNOMED_CT_EN'] = lists2tuples(snomed_codes_en, snomed_descrs_en)
#         result['ICD10CM_ES'] = lists2tuples([source_id], icd10cm_descrs_es) 

#     return result

# def map_source_icd10pcs(source_id):
#     result = {}
#     result['status'] = 'OK'
#     result['source_id'] = source_id

#     q_dic = get_query("CODE", source_id)
#     icd10cm_es_result =  query_search(q_dic, constants.ICD10PCS)
#     icd10cm_descrs_es  = result2list_(icd10cm_es_result, 'ICD10DESCR_SPA')

#     result['ICD10PCS_ES'] = lists2tuples([source_id], icd10cm_descrs_es) 

#     q_dic = get_umls2sab_query(source_id, 'ICD10PCS') 
#     umls_icd_result = query_search(q_dic, constants.UMLS)

#     umls_cuis = []
#     umls_descrs = []
#     if umls_icd_result['hits']['total']['value'] > 0:
#         for hit in umls_icd_result['hits']['hits']: 
#             umls_cuis.append(hit['_source']['CUI'])
#             umls_descrs.append(hit['_source']['STR'])

#     result['UMLS_CUI'] = lists2tuples(umls_cuis, umls_descrs)

#     snomed_codes_en_umls = []
#     if len(umls_cuis) > 0: 
#         for c in umls_cuis: 
#             q_dic = get_umls_query(c, 'SNOMEDCT_US') 
#             umls_snomed_result = query_search(q_dic, constants.UMLS)
#             if umls_snomed_result['hits']['total']['value'] > 0:
#                 for hit in umls_snomed_result['hits']['hits']: 
#                     if hit['_source']['CODE'] not in snomed_codes_en_umls: 
#                         snomed_codes_en_umls.append(hit['_source']['CODE'])

                    
#     snomed_codes_en = []
#     snomed_descrs_en = []
#     snomed_codes_es = []
#     snomed_descrs_es = []
#     # if len(snomed_codes_en_umls): 
#     for code in snomed_codes_en_umls: 

#         q_dic = get_query("conceptId", code)
#         snomed_en_result = query_search(q_dic, constants.SNOMED_EN)

#         if snomed_en_result['hits']['total']['value'] > 0:
#             for hit in snomed_en_result['hits']['hits']: 
#                 if hit['_source']['conceptId'] not in snomed_codes_en: 
#                     snomed_descrs_en.append(hit['_source']['term'])
#                     snomed_codes_en.append(hit['_source']['conceptId'])

#         snomed_es_result = query_search(q_dic, constants.SNOMED_ES)

#         if snomed_es_result['hits']['total']['value'] > 0:
#             for hit in snomed_es_result['hits']['hits']: 
#                 if hit['_source']['conceptId'] not in snomed_codes_es: 
#                     snomed_descrs_es.append(hit['_source']['term'])
#                     snomed_codes_es.append(hit['_source']['conceptId'])
                
                    
#     result['SNOMED_CT_EN'] = lists2tuples(snomed_codes_en, snomed_descrs_en)
#     result['SNOMED_CT_ES'] = lists2tuples(snomed_codes_es, snomed_descrs_es)

#     # print('RESULT', result)

#     return result

def cui2sty(mapped_cuis): 

    names_groupes = ['STY', 'DEF', 'UI', 'TYPE']
    df_sem_groups = pd.read_csv(constants.PATH_SEMANTIC_GROUPS, sep='|', names=names_groupes)
    print(df_sem_groups.head())

    results = {}
    res_list = []

    for cui in mapped_cuis: 
        print(cui)
    
        q_dic = get_query('CUI', cui)
        print(q_dic)

        sty_result =  query_search(q_dic, constants.SEMANTIC_TYPES)
        print('STY')
        print(sty_result)
        tuis = result2list_unique(sty_result, 'TUI')
        defs = result2list_unique(sty_result, 'STY')

        for t, d in zip(tuis, defs): 

            df_t = df_sem_groups[df_sem_groups['UI'] == t]
            stys = df_t.STY.to_list()
            sty_defs = df_t.DEF.to_list()
            res_list.append({'cui': cui, 'semantic_group': stys[0], 'semantic_group_definition': sty_defs[0], 'semantic_type': t, 'semantic_type_definition': d})

    results['semantic'] = res_list
    print(results)
    return results
