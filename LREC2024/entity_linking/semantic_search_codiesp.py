
import numpy as np
import pandas as pd
import torch
import pickle5 as pickle 
import os
import sys
from sentence_transformers import util
from faiss_utils import faiss_search
from transformer_utils import texts2vectors, cls_pooling, get_chunks, flatten, mean_pooling
from sklearn.metrics import f1_score



# DATA
df = pd.read_csv('DATA/codiesp_train.tsv', sep='\t', dtype='str').fillna('')
print(df.head())
print('Total', len(df))
print('ICD10', df.code.value_counts())
print('CUI', df.CUI.value_counts())
print('SNOMED', df.SNOMED_CT.value_counts())
# print('ICD10CM_ES', df.ICD10CM_ES.value_counts())
print('STY', df.STY.value_counts())

df_train = df[df['SNOMED_CT'] != 'NO_MAPPING']
print(df_train.head())
print(df_train)

# SNOMED 
df_snomed_ = pd.read_csv('/DATA/ezotova_data/MedProcNER/medprocner_train/medprocner_gazetteer/gazzeteer_medprocner_v1.tsv', sep='\t', dtype='str')
print('SNOMED CT',  len(df_snomed_))
df_snomed = df_snomed_
print('SNOMED CT mainterm',  len(df_snomed))

output_folder = 'SapBERT_codiesp'
if not os.path.exists(output_folder):
	os.mkdir(output_folder)

descriptions0 = df_snomed.term.str.lower().to_list()
codes = df_snomed.code.str.lower().to_list()

labels = df_train.SNOMED_CT.str.lower().to_list()

## CORPUS
output_file_corpus = os.path.join(output_folder, 'corpus_vectors.pkl')

if os.path.exists(output_file_corpus): 
    print('Corpus embeddings exist, loading')
    query_embeddings = pickle.load( open(output_file_corpus, "rb"))
else: 
    print('Calculating corpus embeddings')
    queries0 = df_train.text.str.lower().to_list()
    queries_chunks = get_chunks(queries0, 2000)
    print('Corpus queries chunks', len(queries_chunks))

    query_embeddings_chunks = []
    for i, queries in enumerate(queries_chunks): 
        print('Corpus chunk', i)
        model_output_queries, attention_mask = texts2vectors(queries)
        query_embeddings0 = cls_pooling(model_output_queries)
        query_embeddings0 = query_embeddings0.cpu().detach().numpy()
        query_embeddings_chunks.append(query_embeddings0)

    query_embeddings = flatten(query_embeddings_chunks)
    print(query_embeddings[0])
    with open(output_file_corpus, 'wb') as handle:
        pickle.dump(query_embeddings, handle, protocol=pickle.HIGHEST_PROTOCOL)

output_file_icd10 = os.path.join(output_folder, 'snomed_vectors.pkl')

if os.path.exists(output_file_icd10): 
    print('Database emdeddings exist, loading')
    descriptions_embeddings = pickle.load( open(output_file_icd10, "rb"))
else: 
    print('Calcualting database embeddings')
    descriptions_chunks = get_chunks(descriptions0, 2000)
    
    print('Database chunks', len(descriptions_chunks))

    descriptions_embeddings_chunks = []
    for i, descriptions in enumerate(descriptions_chunks):  
        print('Descriptions chunk ', i)
        model_output_descr, attention_mask = texts2vectors(descriptions)
        
        descriptions_embeddings0  = cls_pooling(model_output_descr)
        descriptions_embeddings0 = descriptions_embeddings0.cpu().detach().numpy()
        descriptions_embeddings_chunks.append(descriptions_embeddings0)

    descriptions_embeddings = flatten(descriptions_embeddings_chunks)
    with open(output_file_icd10, 'wb') as handle:
        pickle.dump(descriptions_embeddings, handle, protocol=pickle.HIGHEST_PROTOCOL)

d = 1024 # model vector demension
k = 64   # number of nearest neighbors

D, I = faiss_search(descriptions_embeddings, query_embeddings, k=k, d=d)

result = []
for inds, ds, vecs, label in zip(I, D, query_embeddings, labels): #inds in ICD-10 corpus
    top_descriptions = [descriptions0[i] for i in inds]
    top_predictions = [codes[i] for i in inds]
    result.append({'descriptions': top_descriptions, 'distancies': ds, 'predicted_labels': top_predictions, 'true': label})

ns = [1, 64, 100]
for n in ns: 
    predictions = []
    dictances = []
    top_n = []
    pred_descriptions = []
    for item in result:
        predictions.append(str(item['predicted_labels'][0]))
        dictances.append(item['distancies'][0])
        pred_descriptions.append(item['descriptions'][0])
        top = item['predicted_labels']
        if item['true'] in top[:n]:
            top_n.append(1)
        else:
            top_n.append(0)
        
    accuracy = np.array(top_n).sum()/len(top_n)
    print('P@{} Bi-Encoder : {}'.format(n, accuracy))

    f1 = f1_score(labels, predictions, average='macro')
    print('F1-score Bi-Encoder: {}'.format(f1)) 
    print()

    df_train['prediction'] = predictions
    df_train['pred_descr'] = pred_descriptions
    df_train.to_csv(os.path.join(output_folder, 'predictions.tsv'), sep='\t')

