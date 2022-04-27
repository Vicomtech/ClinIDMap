import requests
from requests import utils


def get_wikipedia_url_from_wikidata_id(wikidata_id, debug=False):
    url = (
        'https://www.wikidata.org/w/api.php'
        '?action=wbgetentities'
        '&props=sitelinks/urls'
        f'&ids={wikidata_id}'
        '&format=json')
    json_response = requests.get(url).json()
    if debug: 
        print(wikidata_id)
        print()
        print(url) 
        print(json_response) 

    entities = json_response.get('entities')  
    if entities:
        entity = entities.get(wikidata_id)
        if entity:
            sitelinks = entity.get('sitelinks')
            if sitelinks:
                wiki_urls = {}
                for key, sitelink in sitelinks.items():
                    wiki_url = sitelink.get('url')
                    if wiki_url:
                        wiki_urls[key] = requests.utils.unquote(wiki_url)
                return wiki_urls
            else: 
                return('There is no Wikipedia article for {} item'.format(wikidata_id))
    return None


def get_icd_10_es_descr(icd_code_list, df_icd_es): 
    icd_10_descr_es_lst = []
    for code in icd_code_list: 
        # SPANISH ICD-10
        icd_10_es = df_icd_es.loc[df_icd_es['codigo'] == code]
        icd_10_es_descr = icd_10_es.descripcion.to_list()
        icd_10_descr_es_lst.append(''.join(icd_10_es_descr))   

    return icd_10_descr_es_lst


def remove_O(dps): 
    # removes O label from string
    new_dps = []
    for lst in dps: 
        # print(i)
        # i = i.split()
        if len(lst) > 1 and 'O' in lst:
            lst_new = [x for x in lst if x != 'O']
            i = list(set(lst_new))
            # print(i)
            if len(i) == 0: 
                new_dps.append('O')
            else: 
                new_dps.append(''.join(i))
        else: 
            lst = list(set(lst))
            new_dps.append(''.join(lst))
    return new_dps

def remove_duplicates(lst): 
    lst_uniq = []
    for i in lst: 
        if i not in lst_uniq:
            lst_uniq.append(i) 
    return lst_uniq

def wikidata2wikipedia_urls(wikidata_items):
    wikipedia_urls = []
    for item in wikidata_items: 
        wiki_id = item.split('/')[-1]
        wikipedia_url = get_wikipedia_url_from_wikidata_id(wiki_id, debug=False)
        wikipedia_urls.append(wikipedia_url)
    return wikipedia_urls