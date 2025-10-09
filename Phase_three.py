import pandas as pd
from ete3 import Tree
import sys

def Tree_creation(input_directory,input_directory2,path_result,category):
    list_pheno=["Store_Phenom","Flux_Phenom"] #
    if category == 'WTS':
        name_data="Flux_Knoben_WTS.csv" 
        prov_watershed_name="Knoben_WTS"  ##Name to add for extracting all unique name of watershed which will create a tree
        name_BV_column='BV_Knoben'  #Name of the column where the name of watershed/model appears
    elif category == 'model':
        name_data="Flux_Knoben_models.csv"  
        prov_watershed_name="Knoben_mod"   ##Name to add for extracting all unique name of watershed which will create a tree
        name_BV_column='Model_Knoben'   #Name of the column where the name of watershed/model appears
    
    ##Import excel file with tree components per watershed
    content = pd.read_csv(input_directory2+name_data,sep=";")
    convertname=pd.read_csv(input_directory+"Conversion_name_process.txt",sep=";")
    
    ##Determinating unicity watershed in .csv file:
    unicity = content[name_BV_column].unique()
    BV_list=pd.DataFrame(unicity)
    BV_list.to_csv(path_result+prov_watershed_name+".csv", index=False, header=False)
    
    amount_wts_per_wts_knoben=pd.DataFrame(columns=['WTS_Knoben','Amount_WTS_HPD'])
    ##Extracting individual watershed's assets
    check_unit=0
    for watershed_nb in unicity:
        check_unit=check_unit+1
        watershed_nb=str(watershed_nb)
        t = Tree()
        amount_wts=0
        for row in range(len(content)):
            Wat_ID = str(content[name_BV_column][row])
            if Wat_ID == watershed_nb:
                amount_wts=amount_wts+1
                for phenom_flux in list_pheno:
                    if str(content[phenom_flux][row])!='nan':
                        phenom_recap = content[phenom_flux][row].split(', ')
                        for line_recap in phenom_recap:
                            line_recap=line_recap.replace(" ", "")
                            index_conv=convertname[convertname['Abbrev']==line_recap].index
                            if not index_conv.empty:
                                line_recap = ' '.join(convertname['Full_name'][index_conv])
                            else:
                                sys.exit(str(check_unit)+'/'+str(len(unicity))+'-'+str(row)+'/'+str(len(content))+'-'+line_recap)
                            tempo = t
                            phenom = line_recap.split('.')
                            for node in phenom:
                                check_test = True
                                if len(tempo.get_children())==0:
                                    tempo = tempo.add_child(name=node, dist=1.0)
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
            
        print(t.get_ascii())
        t.write(format=1, outfile=path_result+str(watershed_nb)+".nw",features=["weight","dist"])
        amount_wts_per_wts_knoben.loc[len(amount_wts_per_wts_knoben)] = [watershed_nb, amount_wts]
    amount_wts_per_wts_knoben.to_csv(path_result+'amount_wts_per_wts_knoben.csv', index=False)

    ##Pour lire les BV enregistres
    for watershed_nb in unicity:
        t = Tree(path_result+str(watershed_nb)+".nw",format=1)
        print(t.get_ascii())
    
    
    ##Exemple pour illustration
    if category =='WTS':
        list_wts=[unicity[6]] #6:BV1123000
    else:
        list_wts=[unicity[6],unicity[36]] #6:GR4J, 36:HBV
    list_wts=unicity #For vizualising each tree
    for watershed_nb in list_wts:  
        t = Tree(path_result+str(watershed_nb)+".nw",format=1)

        from ete3 import TreeStyle, TextFace
        def layout(node):
            name_face = TextFace(node.name,fsize=14)  # Style the text  fsize=10
            node.add_face(name_face, column=0, position="branch-top")  # Attach name to the top of the branch
              
        ts = TreeStyle()
        ts.show_leaf_name = False  # Show leaf names
        ts.show_scale = False  # Disable scale bar
        ts.show_branch_support = False  # Show internal node names
        ts.layout_fn = layout  # Apply the custom layout function
        ts.force_topology = True
        ts.scale = 300  # Increase this value to make branches appear longer
        
        # Show tree
        #t.show(tree_style=ts)
        t.render(path_result+"Graph_tree_"+str(watershed_nb)+".svg", tree_style=ts,dpi=300, units='mm', w=100)  

def Tree_comparison(input_directory,input_d_tree,path_result):
    name_data=["Knoben_WTS.csv","Knoben_mod.csv","Caracteristic_Models.csv"]
    
    unicity_BV=pd.read_csv(input_directory+name_data[0],header=None,names=['Watershed'])
    unicity_model=pd.read_csv(input_directory+name_data[1],header=None,names=['Watershed'])
    caract_model=pd.read_csv(input_directory+name_data[2],delimiter=";")
    
    ##test pour comparer les arbres
    WTS_list=[]
    model_list=[]
    param_model=[]
    score=[]
    score_tot=[]
    sim_index=[]
    for nb_wts in range(len(unicity_BV)):
        for nb_mod in range(len(unicity_model)):
            print(str(nb_wts)+"/"+str(len(unicity_BV))+"-"+str(nb_mod)+"/"+str(len(unicity_model)))
            testref=Tree(input_d_tree+str(unicity_BV['Watershed'][nb_wts])+".nw",format=1)
            testmod=Tree(input_d_tree+str(unicity_model['Watershed'][nb_mod])+".nw",format=1)
            WTS_list.append(unicity_BV['Watershed'][nb_wts])
            model_list.append(unicity_model['Watershed'][nb_mod])
            param_model.append(caract_model.loc[caract_model['Model']==unicity_model['Watershed'][nb_mod],'Nb_parameter'].item())
            
            account_tot=0
            account_mod=0
            for n in testref.traverse("postorder"):
                print(n)
                tempo=n.get_ancestors()
                nodemod = testmod.search_nodes(name=n.name)
                print(n.name)
                if n.name!="":
                    account_tot+=int(n.weight)
                    print("account_tot="+str(account_tot))   
                    if len(nodemod)!=0:
                        print(nodemod,"&",len(nodemod))
                        for check_name in nodemod:
                            check_name_summary = check_name.get_ancestors()
                            check = True
                            print(len(check_name_summary),"/",len(tempo))
                            if len(check_name_summary)==len(tempo):
                                for line,tempo_name in enumerate(tempo):
                                    print(tempo_name.name)
                                    print(check_name_summary[line].name)
                                    if tempo_name.name!=check_name_summary[line].name:
                                        check=False
                            else:
                                check=False
                            if check:
                                account_mod+=int(n.weight)
                                print("account_mod="+str(account_mod))
            score.append(account_mod)
            score_tot.append(account_tot)
            sim_index.append(account_mod/account_tot)
    Final_result = pd.DataFrame({'WTS_list':WTS_list,'model_list':model_list,
                                 'Nb_param_mod':param_model, 'score':score,
                                 'score_tot':score_tot, 'sim_index':sim_index})
    Final_result.to_csv(path_result+'Similarity_index.csv', index=False, sep=";")