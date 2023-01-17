import pandas as pd 
import os


def files2dicts(path):
    names = ['identifier', 'pos', '0', '1', '2', 'num_descendants', 'gloss', 'max_levels', 'level_top', 'mark']
    result = []
    for _, dirnames, files in os.walk(path):
        for folder in dirnames:
            if 'WN' in folder:
                for _, _, files in os.walk(os.path.join(path, folder)): 
                    for file in files: 
                        if 'synset' in file: 
                            df = pd.read_csv(os.path.join(path, folder, file), sep='\t', names=names)
                            df['gloss'] = df['gloss'].fillna('')
                            lang_dict = {}
                            lang_dict[file.split('-')[0].split('_')[1]] = dict(zip(df['identifier'].to_list(), df['gloss'].to_list()))
                            result.append(lang_dict)
    return result


mcr_dir = '/DATA/ezotova_data/ClinIDMap/MCR30_2016'

dictionaries = files2dicts(mcr_dir)

code = '05478139'

results = []
d = {}
for dictionary in dictionaries: 
    for key, value in dictionary.items(): 
        for k, v in value.items(): 
            if code in k: 
                d[key] = v

print(d)
