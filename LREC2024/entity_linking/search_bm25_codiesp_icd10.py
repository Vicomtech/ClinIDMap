import warnings
warnings.simplefilter(action='ignore', category=Warning)

import numpy as np
import pandas as pd
pd.reset_option('all')
import torch
import pickle5 as pickle 
import os
import sys
from faiss_utils import faiss_search
from transformer_utils import texts2vectors, cls_pooling, get_chunks, flatten, mean_pooling
from sklearn.metrics import f1_score
import tqdm

from rank_bm25 import BM25Okapi

def argsort(seq, reverse):
    # http://stackoverflow.com/questions/3071415/efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    return sorted(range(len(seq)), key=seq.__getitem__, reverse =reverse)


# environment
gpu_ids = ["4"]
os.environ['CUDA_VISIBLE_DEVICES'] = ','.join(gpu_ids)


# DATA
# DATA
df = pd.read_csv('/DATA/train_cui_mapped_.tsv', sep='\t', dtype='str').fillna('')
df_dev  = pd.read_csv('/DATA/dev_cui_mapped_.tsv', sep='\t', dtype='str').fillna('')

df_train = pd.concat([df, df_dev], axis=0)

print(df_train.head())
print('Total', len(df_train))


icd_codes_dir = '/DATA/ICD-10_CodiEsp/data/icd'
df_icd_d = pd.read_csv(os.path.join(icd_codes_dir, 'ICD10_diagnosticos_block_2020.tsv'), sep='\t', dtype='str')
df_icd_p = pd.read_csv(os.path.join(icd_codes_dir, 'ICD10_procedimientos_block_2020.tsv'), sep='\t', dtype='str')
df_snomed = pd.concat([df_icd_d, df_icd_p], ignore_index=True)
print(len(df_snomed))


output_folder = 'SapBERT_UMLS_BM25_ICD10_Codiesp'
if not os.path.exists(output_folder):
	os.mkdir(output_folder)

descriptions0 = df_snomed.descripcion.str.lower().to_list()
codes = df_snomed.codigo.str.lower().to_list()

labels = df_train.code.str.lower().to_list()
queries = df_train.text.str.lower().to_list()

tokenized_corpus = [doc.split(" ") for doc in descriptions0]
bm25 = BM25Okapi(tokenized_corpus)

result = []
for query, label in tqdm.tqdm(zip(queries, labels)): 
    tokenized_query = query.split()
    doc_scores = bm25.get_scores(tokenized_query)
    top_similar = argsort(doc_scores, True)
    top_predictions = []
    top_descriptions = []
    for i in range(100): 
        top_predictions.append(codes[top_similar[i]])
        top_descriptions.append(descriptions0[top_similar[i]])
    result.append({'descriptions': top_descriptions, 'predicted_labels': top_predictions, 'true': label})

print('Reranking started')
ns = [1]
for n in ns: 
    predictions = []
    dictances = []
    top_n = []
    pred_descriptions = []
    for item in result:
        predictions.append(str(item['predicted_labels'][0]))
        # dictances.append(item['distancies'][0])
        pred_descriptions.append(item['descriptions'][0])
        top = item['predicted_labels']
        if item['true'] in top[:n]:
            top_n.append(1)
        else:
            top_n.append(0)
        
    accuracy = np.array(top_n).sum()/len(top_n)
    print('P@{} BM25: \t\t {}'.format(n, accuracy))

    f1 = f1_score(labels, predictions, average='macro')
    print('F1-score macro BM25: \t {}'.format(f1)) 


    df_train['prediction'] = predictions
    df_train['pred_descr'] = pred_descriptions

    df_train.to_csv(os.path.join(output_folder, 'predictions_'+str(n)+'bm25.tsv'), sep='\t', index=False)
    print('========================')
