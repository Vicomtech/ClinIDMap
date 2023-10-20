from transformers import AutoTokenizer, AutoModel, AutoConfig
import torch
import os 
import gc


device = "cuda:0" if torch.cuda.is_available() else "cpu"
print('DEVICE', device)
## MODEL
model_name = 'cambridgeltl/SapBERT-UMLS-2020AB-all-lang-from-XLMR-large' 

def texts2vectors(text_list, model_name=model_name): 
    config = AutoConfig.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name, config=config).to(device)
    #Tokenize sentences
    encoded_input = tokenizer.batch_encode_plus(
        text_list, 
        padding=True, 
        truncation=True, 
        max_length=64, 
        return_tensors='pt').to(device)
    
    with torch.no_grad():
        model_output = model(**encoded_input)

    del model
    gc.collect()
    torch.cuda.empty_cache()
    return model_output, encoded_input['attention_mask']


#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask

def cls_pooling(model_output):
    return model_output[0][:,0]

def get_chunks(ids, n): 
    return [ids[i:i+n] for i in range(0,len(ids),n)]

def flatten(chunks): 
    return [item for sublist in chunks for item in sublist]