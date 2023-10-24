import requests

    
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

def wikidata2wikipedia_urls(item):
    wikipedia_urls = []
    wiki_id = item.strip()
    wikipedia_urls = get_wikipedia_url_from_wikidata_id(wiki_id, debug=False)
    return wikipedia_urls

