import pandas as pd
from ete3 import Tree, TreeStyle, TextFace, NodeStyle, CircleFace, RectFace
import sys
import copy
import os

def Tree_creation(input_directory,input_directory2,path_result,category):
    list_pheno=["Store_Phenom","Flux_Phenom"] #
    if category == 'WTS':
        name_data="Flux_Knoben_WTS.csv" 
        prov_watershed_name="Knoben_WTS"  ##Name to add for extracting all unique name of watershed which will create a tree
        name_BV_column='BV_Knoben'  #Name of the column where the name of watershed/model appears
        name_category="/WTS/"
    elif category == 'model':
        name_data="Flux_Knoben_models.csv"  
        prov_watershed_name="Knoben_mod"   ##Name to add for extracting all unique name of watershed which will create a tree
        name_BV_column='Model_Knoben'   #Name of the column where the name of watershed/model appears
        name_category="/model/"
    
    ##Import excel file with tree components per watershed
    content = pd.read_csv(input_directory2+name_data,sep=";")
    convertname=pd.read_csv(input_directory+"HPD_Data/Conversion_name_process.txt",sep=";")
    
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
                                line_recaptot = ' '.join(convertname['Full_name'][index_conv])
                            else:
                                sys.exit(str(check_unit)+'/'+str(len(unicity))+'-'+str(row)+'/'+str(len(content))+'-'+line_recap)
                            tempo = t
                            phenom = line_recap.split('.')
                            phenomtot = line_recaptot.split('.')
                            for nb,elt in enumerate(phenom):
                                node=phenom[nb]
                                nm_tot=phenomtot[nb]
                                check_test = True
                                if len(tempo.get_children())==0:
                                    tempo = tempo.add_child(name=node) #, dist=1.0
                                    tempo.add_features(weight=0)
                                    tempo.add_features(to_update=1)
                                    tempo.add_features(name_tot=nm_tot)
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
                                    tempo.add_features(name_tot=nm_tot)
            for node in t.iter_descendants("postorder"): 
                if node.to_update==1:
                    node.weight=node.weight+1
                    node.to_update=0
        for node in t.iter_descendants("postorder"):
            if node.name!="":
                node.name_tot=node.name_tot.replace("\\n", "\n")

        print(t.get_ascii())
        t.write(format=1, outfile=path_result+name_category+str(watershed_nb)+".nw",features=["weight","name_tot"]) #,"dist"
        amount_wts_per_wts_knoben.loc[len(amount_wts_per_wts_knoben)] = [watershed_nb, amount_wts]
    amount_wts_per_wts_knoben.to_csv(path_result+'amount_wts_per_wts_knoben.csv', index=False)


    ##Exemple pour illustration
    if category =='WTS':
        list_wts=[unicity[6],unicity[269]] #6:BV1123000, 269:6043500
    else:
        list_wts=[unicity[6],unicity[36]] #6:GR4J, 36:HBV
#    list_wts=unicity #For vizualising each tree
    for watershed_nb in list_wts:  
        t = Tree(path_result+name_category+str(watershed_nb)+".nw",format=1)
        
        # Define a base size and scaling factor
        scale_factor = 10
        total_length = 20
                   
        def layout(node):
            if node.name!="":
                node.name=node.name.replace("_", "\n")
                node.dist= total_length - 2*int(node.weight)*scale_factor
                name_face = TextFace(node.name+" ("+node.weight+")",fsize=15)  # Style the text 
                node.add_face(name_face, column=0, position="branch-top") # Attach name to the top of the branch
                nstyle = CircleFace(radius=int(node.weight)*scale_factor, color="Blue", style="sphere")
                nstyle.opacity = 0.3
                node.add_face(nstyle, column=0, position="branch-right")

            
        ts = TreeStyle()
        ts.show_leaf_name = False  # Show leaf names
        ts.show_scale = False  # Disable scale bar
        ts.show_branch_support = False  # Show internal node names
        ts.layout_fn = layout  # Apply the custom layout function
        ts.force_topology = True
        ts.scale = 300  # Increase this value to make branches appear longer
        
        # Show tree
        t.render(path_result+"Graph_tree_"+str(watershed_nb)+".svg", tree_style=ts,dpi=300, units='mm', w=100)  

def Tree_comparison(input_directory,input_d_tree,path_result):
    unicity_BV = os.listdir(input_d_tree+"/WTS")
    unicity_model = os.listdir(input_d_tree+"/model")
    caract_model=pd.read_csv(input_directory+"Model_Data/Caracteristic_Models.csv",delimiter=";")
    
    ##test pour comparer les arbres
    WTS_list=[]
    model_list=[]
    param_model=[]
    score=[]
    score_tot=[]
    sim_index=[]
    snow_proc_wts=[]
    snow_proc_mod=[]
    subsurf_proc_wts=[]
    subsurf_proc_mod=[]
    gwt_proc_wts=[]
    gwt_proc_mod=[]
    for nb_wts in range(len(unicity_BV)):
        testref=Tree(input_d_tree+"/WTS/"+str(unicity_BV[nb_wts]),format=1)
        nodemod = testref.search_nodes(name='Surface')

        for nb_mod in range(len(unicity_model)):
            print(str(nb_wts)+"/"+str(len(unicity_BV))+"-"+str(nb_mod)+"/"+str(len(unicity_model)))
            testmod=Tree(input_d_tree+"/model/"+str(unicity_model[nb_mod]),format=1)
            WTS_list.append(unicity_BV[nb_wts].replace(".nw",""))
            model_list.append(unicity_model[nb_mod].replace(".nw",""))
            param_model.append(caract_model.loc[caract_model['Model']==unicity_model[nb_mod].replace(".nw",""),'Nb_parameter'].item())     

            account_tot=0
            account_mod=0
            snow_wts_test=0
            snow_mod_test=0
            subsurf_wts_test=0
            subsurf_mod_test=0
            gwt_wts_test=0
            gwt_mod_test=0
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
                    if n.name=='Snow':
                        snow_wts_test=1
                    elif n.name=='Sub':
                        subsurf_wts_test=1
                    elif n.name=='GW':
                        gwt_wts_test=1
            for n in testmod.traverse("postorder"):
                if n.name=='Snow':
                    snow_mod_test=1
                elif n.name=='Sub':
                    subsurf_mod_test=1
                elif n.name=='GW':
                    gwt_mod_test=1    
            score.append(account_mod)
            score_tot.append(account_tot)
            sim_index.append(account_mod/account_tot)
            snow_proc_wts.append(snow_wts_test)
            snow_proc_mod.append(snow_mod_test)
            subsurf_proc_wts.append(subsurf_wts_test)
            subsurf_proc_mod.append(subsurf_mod_test)
            gwt_proc_wts.append(gwt_wts_test)
            gwt_proc_mod.append(gwt_mod_test)
    Final_result = pd.DataFrame({'WTS_list':WTS_list,'model_list':model_list,
                                 'Nb_param_mod':param_model, 'score':score,
                                 'score_tot':score_tot, 'sim_index':sim_index})
    Final_result.to_csv(path_result+'Similarity_index.csv', index=False, sep=";")
    Final_result_processes = pd.DataFrame({'WTS_list':WTS_list,'model_list':model_list,
                                 'sim_index':sim_index,'snow_proc_wts':snow_proc_wts,
                                 'snow_proc_mod':snow_proc_mod,'subsurf_proc_wts':subsurf_proc_wts,
                                 'subsurf_proc_mod':subsurf_proc_mod,'gwt_proc_wts':gwt_proc_wts,
                                 'gwt_proc_mod':gwt_proc_mod})
    Final_result_processes.to_csv(path_result+'Similarity_index_subsetmodel.csv', index=False, sep=";")

def Tree_model_watershed(input_directory3,path_result):
    list_pheno=["Store_Phenom","Flux_Phenom"] #
    name_data_WTS="Flux_Knoben_WTS.csv" 
    prov_WTS_name="Knoben_WTS"  ##Name to add for extracting all unique name of watershed which will create a tree
    name_WTS_column='BV_Knoben'  #Name of the column where the name of watershed/model appears
    name_data_model="Flux_Knoben_models.csv"  
    prov_model_name="Knoben_mod"   ##Name to add for extracting all unique name of watershed which will create a tree
    name_model_column='Model_Knoben'   #Name of the column where the name of watershed/model appears
    
    ##Determinating unicity watershed in .csv file:
    list_wts = os.listdir(input_directory3+"/WTS")
    list_model = os.listdir(input_directory3+"/model")
    list_wts=[list_wts[6]] #6:BV1123000 269:6043500 143:2077200
    list_model=[list_model[6],list_model[36]] #6:GR4J, 36:HBV, 45:prms_18p_7s
        
    for watershed_nb in list_wts:  
        t_wts1 = Tree(input_directory3+"/WTS/"+str(watershed_nb),format=1)


        max_weight=0
        for node_model in t_wts1.traverse():
            if node_model.name!="":
                max_weight=max(max_weight,int(node_model.weight))
        max_weight=max_weight+1 #to avoid that the circle overlap the branch of the node with the highest weight
        
        for model_nb in list_model:
            t_wts=copy.deepcopy(t_wts1)
            t_model = Tree(input_directory3+"/model/"+str(model_nb),format=1)
        
            # Define a base size and scaling factor
            ts = TreeStyle()
            ts.scale = 100  # Increase this value to make branches appear longer
            total_visual_length = 300  # in "pixels"

        
            def layout(node):
                if node.name!="":
                    node.name_tot=node.name_tot.replace("_", "\n")
                    circle_radius = (int(node.weight)/ max_weight) * total_visual_length /2 * 0.4
                    branch_length = total_visual_length - circle_radius*2
                    node.dist = branch_length / ts.scale
                    name_face = TextFace(f"{node.name_tot} ({int(node.weight)})", fsize=13)
                    node.add_face(name_face, column=0, position="branch-top")
                    nstyle2 = CircleFace(radius=circle_radius, color="Blue", style="sphere")
                    nstyle2.opacity = 0.3
                    node.add_face(nstyle2, column=0, position="branch-right")
                    if len(t_model.search_nodes(name=node.name))!= 0:
                        parent_wts = node.up
                        parent_model = t_model.search_nodes(name=node.name)[0]
                        parent_model = parent_model.up                        
                        if parent_wts.name==parent_model.name:
                            r = RectFace(branch_length, 100, "Darkgreen", "Darkgreen")
                            r.opacity = 0.3
                            node.add_face(r, column=0, position="float")

            ts.show_leaf_name = False  # Show leaf names
            ts.show_scale = False  # Disable scale bar
            ts.show_branch_support = False  # Show internal node names
            ts.layout_fn = layout  # Apply the custom layout function
            ts.force_topology = False
            ts.branch_vertical_margin = 20   # (pixels)

          
            custom_order = ["Surface", "Subsurface", "Channel"]   
            order_rank = {name: i for i, name in enumerate(custom_order)}
            def sort_by_custom(node):
                node.children.sort(key=lambda c: order_rank.get(getattr(c, "name_tot", ""), 999999))
                for child in node.children:
                    sort_by_custom(child)
            sort_by_custom(t_wts)
            
            # Show tree
            t_wts.render(path_result+"Graph_tree_"+str(watershed_nb)+"_"+str(model_nb)+".svg", tree_style=ts,dpi=300)#, units='mm', w=100)  

