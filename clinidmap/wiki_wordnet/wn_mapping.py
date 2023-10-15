import pandas as pd 
import os 
from clinidmap.constants import DATABASE


wn30_dir = '/DATA/ezotova_data/_ClinIDMap/wordnet30'
wn31_dir = '/DATA/ezotova_data/_ClinIDMap/wordnet31'

index_sense30 = os.path.join(wn30_dir, 'index.sense')
index_sense31 = os.path.join(wn31_dir, 'index.sense')

colnames = ['sense_key', 'synset_offset', 'sense_number', 'tag_cnt']

df_index_sense30 = pd.read_csv(index_sense30, sep=' ', names=colnames, header=None, dtype='str')
print('Senses WN 3.0', len(df_index_sense30))

df_index_sense31     = pd.read_csv(index_sense31, sep=' ', names=colnames, header=None, dtype='str')
print('Senses WN 3.1', len(df_index_sense31))


def wn_sense_mapping(wn_id):

    id_ = str(wn_id.split('-')[0])
    df_wn31_id = df_index_sense31[df_index_sense31['synset_offset'] == id_]
    sense_keys31 = df_wn31_id.sense_key.to_list()
    wn_ids30 = []
    senses = []
    for sense in sense_keys31: 
        df_wn30_id = df_index_sense30[df_index_sense30['sense_key'] == sense]
        if len(df_wn30_id) > 0: 
            wn30_id = df_wn30_id.synset_offset.to_list()[0]+'-'+str(wn_id.split('-')[1])
            senses.append(sense) 
            wn_ids30.append(wn30_id)
        else: 
            wn30_id = 'nomapping'
            wn_ids30.append(wn30_id)
            senses.append('nosense')

    return [' '.join(list(set(wn_ids30))).strip(), ' '.join(list(set(senses))).strip()]


# wn31_id = '00774891-n'
# res = wn_sense_mapping(wn31_id, df_index_sense30, df_index_sense31)

# df_wikidata_wn = pd.read_csv(
#     os.path.join(DATABASE, 'query_wikidata_identificador_de_synset_de_WordNet_3_1.tsv'), 
#     sep='\t', dtype='str'
#     ) # got from Wikipedia query (wiki.update_wiki)

# wn31_ids = df_wikidata_wn.wordnet_id.to_list()

# wn30_ids = []
# wn31_senses = []
# for wn31_id in tqdm.tqdm(wn31_ids): 
#     wn30_id = wn_sense_mapping(wn31_id, df_index_sense30, df_index_sense31)[0]
#     sense31 = wn_sense_mapping(wn31_id, df_index_sense30, df_index_sense31)[1]
#     wn30_ids.append(wn30_id)
#     wn31_senses.append(sense31)

# df_wikidata_wn['wordnet30_id'] = wn30_ids
# df_wikidata_wn['sense'] = wn31_senses

# df_wikidata_wn.to_csv(os.path.join(DATABASE, 'query_wikidata_identificador_de_synset_de_WordNet_3_1_wn_3_0.tsv'), sep='\t', index=False)