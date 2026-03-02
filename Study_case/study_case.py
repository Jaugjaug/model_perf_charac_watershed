import pandas as pd
import simindex
from ete3 import Tree
import numpy as np

##Important as ete3 hasn't be updated to recent python release 
import builtins
# Save the original open function
original_open = builtins.open
# Redefine open to strip 'U' from the mode string
def patched_open(*args, **kwargs):
    if 'mode' in kwargs:
        kwargs['mode'] = kwargs['mode'].replace('U', '')
    elif len(args) > 1:
        args = list(args)
        args[1] = args[1].replace('U', '')
    return original_open(*args, **kwargs)
builtins.open = patched_open


##Main code
tree_type=['model','watershed']

##Read csv file containing process in modele and in studied watershed (or watershed(s) around) 
    ##(ID comparaison;modele or watershed;name/ID modele or watershed;list process)
df = pd.read_csv('study_case.csv')

Final_result = []
##Trees building
for try_nb in df['ID_try'].unique():
    ##Trees building
    for type_tree_unique in tree_type: 
        df_tempo = df.loc[(df['ID_try'] == try_nb) & (df['tree_type'] == type_tree_unique)].copy()
        t=simindex.Tree_building(df_tempo)
        t.write(format=1, outfile="output/Tree/Tree_nb_"+str(try_nb)+"_"+type_tree_unique+".nw",features=["weight","name"]) 

    ##Evaluation similarity index
    t_model = Tree("output/Tree/Tree_nb_"+str(try_nb)+"_model.nw",format=1)
    t_wts = Tree("output/Tree/Tree_nb_"+str(try_nb)+"_watershed.nw",format=1)
    sim_index = simindex.similarity_index(t_model,t_wts)

    ##Output:txt file with info: modele name, how many watershed, watershed name, similarity index 
    filtered_comments = df[(df['ID_try'] == try_nb) & (df['Comment'].notna()) & (df['Comment'].astype(str) != "")]
    if not filtered_comments.empty:
        filtered_comments = "-".join(filtered_comments['Comment'].astype(str))
    else:
        filtered_comments = ""
    Final_result.append({'Try_nb':try_nb,
                                 'Model':df.loc[(df['ID_try'] == try_nb) & (df['tree_type'] == 'model'),'ID_type'].values[0],
                                 'Watershed':df.loc[(df['ID_try'] == try_nb) & (df['tree_type'] == 'watershed'),'ID_type'].values[0], 
                                 'sim_index':sim_index,
                                 'Comment':filtered_comments})
Final_result=pd.DataFrame(Final_result)
Final_result.to_csv('output/Similarity_index.csv', index=False, sep=";")
