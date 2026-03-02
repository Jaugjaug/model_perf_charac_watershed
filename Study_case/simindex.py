from ete3 import Tree


def Tree_building(df):
    t = Tree()
    for index, row in df.iterrows():
        list_pheno = row['Processes'].split(',')
        for phenom_flux in list_pheno:
            tempo = t
            phenom = phenom_flux.split('.')
            for nb,elt in enumerate(phenom):
                node=phenom[nb]
                check_test = True
                if len(tempo.get_children())==0:
                    tempo = tempo.add_child(name=node)
                    tempo.add_features(weight=0)
                    tempo.add_features(to_update=1)
                else:
                    check_test = False
                for child in tempo.get_children():
                    if child.name==node:
                        check_test = True
                if check_test == True:
                    for child in tempo.get_children():
                        if child.name==node:
                            tempo = child
                            tempo.to_update=1
                else:                        
                    tempo = tempo.add_child(name=node)
                    tempo.add_features(weight=0)
                    tempo.add_features(to_update=1)
        for node in t.iter_descendants("postorder"): 
            if node.to_update==1:
                node.weight=node.weight+1
                node.to_update=0
    return t

def similarity_index(tree_mod,tree_wts):
    account_tot=0
    account_mod=0
    for n in tree_wts.traverse("postorder"):
        tempo=n.get_ancestors()
        nodemod = tree_mod.search_nodes(name=n.name)
        if n.name!="":
            account_tot+=int(n.weight)
            if len(nodemod)!=0:
                for check_name in nodemod:
                    check_name_summary = check_name.get_ancestors()
                    check = True
                    if len(check_name_summary)==len(tempo):
                        for line,tempo_name in enumerate(tempo):
                            if tempo_name.name!=check_name_summary[line].name:
                                check=False
                    else:
                        check=False
                    if check:
                        account_mod+=int(n.weight)
    sim_index = account_mod / account_tot 
    return sim_index
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        