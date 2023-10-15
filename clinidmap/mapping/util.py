import requests
from requests import utils


def lists2tuples(list1, list2): 
    result = []
    for i, j in zip(list1, list2): 
        d = {}
        d['id'] = str(i)
        d['description'] = str(j)
        result.append(d)
    return result
    
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


def wikidata2wikipedia_urls(wikidata_items):
    wikipedia_urls = []
    for item in wikidata_items: 
        wiki_id = item.split('/')[-1]
        wikipedia_url = get_wikipedia_url_from_wikidata_id(wiki_id, debug=False)
        wikipedia_urls.append(wikipedia_url)
    return wikipedia_urls


def remove_duplicates(lst): 
    lst_uniq = []
    for i in lst: 
        if i not in lst_uniq:
            lst_uniq.append(i) 
    return lst_uniq
