
import faiss 
import numpy as np 
import time


def faiss_search(sentence_embeddings, query_embeddings, k=5, d=1024): 
    nb = len(list(sentence_embeddings)) 
    nq = len(list(query_embeddings))
    print('Database vecs', nb)
    print('Queries vecs', nq)			# queries

    xb = np.zeros((nb, d), dtype=object).astype('float32') # database vectors
    for i, vecs in enumerate(sentence_embeddings): 
        xb[i] = vecs

    xq = np.zeros((nq, d)).astype('float32') # query vectors
    for i, vecs in enumerate(query_embeddings):
        xq[i] = vecs

    # make faiss available
    # index = faiss.IndexFlatL2(d)   # build the index 
    index = faiss.IndexFlatIP(d)
    print('Index is trained', index.is_trained)
    
    faiss.normalize_L2(xb)
    index.add(xb)    # add vectors to the index
                  
    start_time = time.time()                       
    D, I = index.search(xq, k)    # actual search. D - distance,
    print("FAISS search --- done in %s seconds ---" % (time.time() - start_time))
    return D, I

