import pandas as pd



def Distance_between_watersheds(input_directory,path_result):
    content_distance = pd.read_csv(input_directory +"Distance_Knoben_HPD.csv",delimiter=";")
    content_eco_HPD = pd.read_csv(input_directory+"Compa_Eco_HPD.csv",delimiter=";")
    content_eco_knob = pd.read_csv(input_directory+"Compa_Eco_Knobentopo.csv",delimiter=";")
    
    list_bv_done=[]
    nb_no_conection_lvlthree=0 #Nb of watershed in Knoben dataset where there is no watershed in HPD in the same ecoregion lvl3
    nb_no_conection_lvltwo=0 #Nb of watershed in Knoben dataset where there is no watershed in HPD in the same ecoregion lvl2 and lvl3
    nb_no_conection_lvlone=0 #Nb of watershed in Knoben dataset where there is no watershed in HPD in the same ecoregion lvl1, lvl2 and lvl3
    nb_no_conection_lvlthree_list_id=[] #list of watershed in Knoben dataset where there is no watershed in HPD in the same ecoregion lvl3
    trash=0
    for line_Knoben in content_distance.index:
        id_BV_knoben=content_distance['gauge_id'][line_Knoben]
        #Verifier si le BV a deja ete traite
        if not id_BV_knoben in list_bv_done:
            recap = content_distance[content_distance['gauge_id'][line_Knoben] == content_distance['gauge_id']]
            list_bv_done.append(id_BV_knoben)
            print("Watershed Knoben done:"+str(len(list_bv_done)))
            file_name=path_result+str(id_BV_knoben)+".txt"
            f = open(file_name, "w")
            f.write("Distances (m) with watersheds (HPD) with same ecoregion level 3: "+str(content_distance['NA_L3CODE'][line_Knoben])+"\n")
            #retrouver les BV avec le meme ecoregion lvl3 que Knoben, ecrire le nombre et extraire les distances
            lvltrois = content_eco_HPD[content_eco_HPD['NA_L3CODE'] == content_distance['NA_L3CODE'][line_Knoben]]
            nb_no_conection_lvlthree = Writing_distance(lvltrois,nb_no_conection_lvlthree,f,recap)
            if (len(lvltrois.index)==0):
                nb_no_conection_lvlthree_list_id.append(id_BV_knoben)
    
            #retrouver les BV avec le meme ecoregion lvl2 que Knoben (autre que lvl3), ecrire le nombre et extraire les distances
            f.write("Distances (m) with watersheds (HPD) with same ecoregion level 2: "+str(content_distance['NA_L2CODE'][line_Knoben])+"\n")
            lvldeux = content_eco_HPD[(content_eco_HPD['NA_L2CODE'] == content_distance['NA_L2CODE'][line_Knoben]) & (content_eco_HPD['NA_L3CODE'] != content_distance['NA_L3CODE'][line_Knoben])]
            if (len(lvltrois.index)==0):
                nb_no_conection_lvltwo = Writing_distance(lvldeux,nb_no_conection_lvltwo,f,recap)
            else:
                trash = Writing_distance(lvldeux,0,f,recap)
    
            #retrouver les BV avec le meme ecoregion lvl1 que Knoben (autre que lvl2), ecrire le nombre et extraire les distances
            f.write("Distances (m) with watersheds (HPD) with same ecoregion level 1: "+str(content_distance['NA_L1CODE'][line_Knoben])+"\n")
            lvlun = content_eco_HPD[(content_eco_HPD['NA_L1CODE'] == content_distance['NA_L1CODE'][line_Knoben]) & (content_eco_HPD['NA_L2CODE'] != content_distance['NA_L2CODE'][line_Knoben])]
            if (len(lvltrois.index)==0) and (len(lvldeux.index)==0):
                nb_no_conection_lvlone = Writing_distance(lvlun,nb_no_conection_lvlone,f,recap)
            else:
                trash = Writing_distance(lvlun,0,f,recap)
    
            #retrouver les BV hors ecoregion lvl1 que Knoben, ecrire le nombre et extraire les distances
            f.write("Distances (m) with watersheds (HPD) out of ecoregion level 1: "+str(content_distance['NA_L1CODE'][line_Knoben])+"\n")
            lvlunexc = content_eco_HPD[content_eco_HPD['NA_L1CODE'] != content_distance['NA_L1CODE'][line_Knoben]]
            trash = Writing_distance(lvlunexc,0,f,recap)
    
            f.close()
    
    g = open(path_result+'Summary_Stat.txt','w')
    g.write("Nb watershed Knoben without HPD watershed connection lvl3: "+str(nb_no_conection_lvlthree)+"/"+str(len(list_bv_done))+"\n")
    g.write("Nb watershed Knoben without HPD watershed connection lvl3 and lvl2: "+str(nb_no_conection_lvltwo)+"/"+str(len(list_bv_done))+"\n")
    g.write("Nb watershed Knoben without HPD watershed connection lvl3, lvl 2 and lvl1: "+str(nb_no_conection_lvlone)+"/"+str(len(list_bv_done))+"\n")
    
    
    ###Calcul distance polygone including watersheds Knoben and HPD
    #how many polygon including watershed Knoben touch polygon HPD with same ecoregion lvl2 but different ecoregion lvl2
    list_BV_polygon_lvl2_no_lvl3_dist0=[]
    list_BV_polygon_lvl3_dist0=[]
    list_BV_polygon_lvl2_dist0=[]
    list_BV_polygon_lvl1_dist0=[]
    list_BV_polygon_lvl1_no2_no3_dist0=[]
    list_BV_polygon_lvl2_no_lvl3=[]
    list_BV_polygon_lvl3=[]
    list_BV_polygon_lvl2=[]
    list_BV_polygon_lvl1=[]
    list_BV_polygon_lvl1_no2_no3=[]
    content_distance_polygon = pd.read_csv(input_directory+"Ecoregionslvl3_HPD_Knoben_distance_polygon.csv",delimiter=";",decimal=",")
    content_HPD_polygon = pd.read_csv(input_directory+"Ecoregionslvl3_HPD_WSHD_properties.csv",delimiter=";",decimal=",")
    content_Knoben_polygon = pd.read_csv(input_directory+"Ecoregionslvl3_Knoben_WSHD_properties.csv",delimiter=";",decimal=",")
    for i in range(len(content_distance_polygon)):
        print(str(i)+"/"+str(len(content_distance_polygon)))
        lvlone_hpd=content_HPD_polygon.loc[(content_HPD_polygon['TARGET_FID'].index+1)==content_distance_polygon['IN_FID'][i],'NA_L1CODE']
        lvltwo_hpd=content_HPD_polygon.loc[(content_HPD_polygon['TARGET_FID'].index+1)==content_distance_polygon['IN_FID'][i],'NA_L2CODE']
        lvlthree_hpd=content_HPD_polygon.loc[(content_HPD_polygon['TARGET_FID'].index+1)==content_distance_polygon['IN_FID'][i],'NA_L3CODE']
        lvlone_knoben=content_Knoben_polygon.loc[(content_Knoben_polygon['TARGET_FID'].index+1)==content_distance_polygon['NEAR_FID'][i],'NA_L1CODE']
        lvltwo_knoben=content_Knoben_polygon.loc[(content_Knoben_polygon['TARGET_FID'].index+1)==content_distance_polygon['NEAR_FID'][i],'NA_L2CODE']
        lvlthree_knoben=content_Knoben_polygon.loc[(content_Knoben_polygon['TARGET_FID'].index+1)==content_distance_polygon['NEAR_FID'][i],'NA_L3CODE']
        if content_distance_polygon['NEAR_DIST'][i]==0:
            if (lvltwo_hpd.iloc[0]==lvltwo_knoben.iloc[0] and lvlthree_hpd.iloc[0]!=lvlthree_knoben.iloc[0]):
                BV_Knoben=content_Knoben_polygon.loc[(content_Knoben_polygon['TARGET_FID'].index+1)==content_distance_polygon['NEAR_FID'][i],'gauge_id']
                if str(BV_Knoben.iloc[0]) not in list_BV_polygon_lvl2_no_lvl3_dist0:
                    list_BV_polygon_lvl2_no_lvl3_dist0.append(str(BV_Knoben.iloc[0]))
            if (lvltwo_hpd.iloc[0]==lvltwo_knoben.iloc[0] and lvlthree_hpd.iloc[0]==lvlthree_knoben.iloc[0]):
                BV_Knoben=content_Knoben_polygon.loc[(content_Knoben_polygon['TARGET_FID'].index+1)==content_distance_polygon['NEAR_FID'][i],'gauge_id']
                if str(BV_Knoben.iloc[0]) not in list_BV_polygon_lvl3_dist0:
                    list_BV_polygon_lvl3_dist0.append(str(BV_Knoben.iloc[0]))
            if (lvltwo_hpd.iloc[0]==lvltwo_knoben.iloc[0]):
                BV_Knoben=content_Knoben_polygon.loc[(content_Knoben_polygon['TARGET_FID'].index+1)==content_distance_polygon['NEAR_FID'][i],'gauge_id']
                if str(BV_Knoben.iloc[0]) not in list_BV_polygon_lvl2_dist0:
                    list_BV_polygon_lvl2_dist0.append(str(BV_Knoben.iloc[0]))
            if (lvlone_hpd.iloc[0]==lvlone_knoben.iloc[0]):
                BV_Knoben=content_Knoben_polygon.loc[(content_Knoben_polygon['TARGET_FID'].index+1)==content_distance_polygon['NEAR_FID'][i],'gauge_id']
                if str(BV_Knoben.iloc[0]) not in list_BV_polygon_lvl1_dist0:
                    list_BV_polygon_lvl1_dist0.append(str(BV_Knoben.iloc[0]))
            if (lvlone_hpd.iloc[0]==lvlone_knoben.iloc[0] and lvltwo_hpd.iloc[0]!=lvltwo_knoben.iloc[0] and lvlthree_hpd.iloc[0]!=lvlthree_knoben.iloc[0]):
                BV_Knoben=content_Knoben_polygon.loc[(content_Knoben_polygon['TARGET_FID'].index+1)==content_distance_polygon['NEAR_FID'][i],'gauge_id']
                if str(BV_Knoben.iloc[0]) not in list_BV_polygon_lvl1_no2_no3_dist0:
                    list_BV_polygon_lvl1_no2_no3_dist0.append(str(BV_Knoben.iloc[0]))
        if (lvltwo_hpd.iloc[0]==lvltwo_knoben.iloc[0] and lvlthree_hpd.iloc[0]!=lvlthree_knoben.iloc[0]):
            BV_Knoben=content_Knoben_polygon.loc[(content_Knoben_polygon['TARGET_FID'].index+1)==content_distance_polygon['NEAR_FID'][i],'gauge_id']
            if str(BV_Knoben.iloc[0]) not in list_BV_polygon_lvl2_no_lvl3:
                list_BV_polygon_lvl2_no_lvl3.append(str(BV_Knoben.iloc[0]))
        if (lvltwo_hpd.iloc[0]==lvltwo_knoben.iloc[0] and lvlthree_hpd.iloc[0]==lvlthree_knoben.iloc[0]):
            BV_Knoben=content_Knoben_polygon.loc[(content_Knoben_polygon['TARGET_FID'].index+1)==content_distance_polygon['NEAR_FID'][i],'gauge_id']
            if str(BV_Knoben.iloc[0]) not in list_BV_polygon_lvl3:
                list_BV_polygon_lvl3.append(str(BV_Knoben.iloc[0]))
        if (lvltwo_hpd.iloc[0]==lvltwo_knoben.iloc[0]):
            BV_Knoben=content_Knoben_polygon.loc[(content_Knoben_polygon['TARGET_FID'].index+1)==content_distance_polygon['NEAR_FID'][i],'gauge_id']
            if str(BV_Knoben.iloc[0]) not in list_BV_polygon_lvl2:
                list_BV_polygon_lvl2.append(str(BV_Knoben.iloc[0]))
        if (lvlone_hpd.iloc[0]==lvlone_knoben.iloc[0]):
            BV_Knoben=content_Knoben_polygon.loc[(content_Knoben_polygon['TARGET_FID'].index+1)==content_distance_polygon['NEAR_FID'][i],'gauge_id']
            if str(BV_Knoben.iloc[0]) not in list_BV_polygon_lvl1:
                list_BV_polygon_lvl1.append(str(BV_Knoben.iloc[0]))
        if (lvlone_hpd.iloc[0]==lvlone_knoben.iloc[0] and lvltwo_hpd.iloc[0]!=lvltwo_knoben.iloc[0] and lvlthree_hpd.iloc[0]!=lvlthree_knoben.iloc[0]):
            BV_Knoben=content_Knoben_polygon.loc[(content_Knoben_polygon['TARGET_FID'].index+1)==content_distance_polygon['NEAR_FID'][i],'gauge_id']
            if str(BV_Knoben.iloc[0]) not in list_BV_polygon_lvl1_no2_no3:
                list_BV_polygon_lvl1_no2_no3.append(str(BV_Knoben.iloc[0]))
    
    g.write("\n")
    g.write("Calcul distance with polygon"+"\n")
    g.write("Nb watershed Knoben with HPD watershed connection lvl2, but no lvl3, and distance=0: "+str(len(list_BV_polygon_lvl2_no_lvl3_dist0))+"/"+str(len(list_bv_done))+"\n")
    g.write("Nb watershed Knoben with HPD watershed connection lvl2, but no lvl3, and distance>=0: "+str(len(list_BV_polygon_lvl2_no_lvl3))+"/"+str(len(list_bv_done))+"\n")
    g.write("Nb watershed Knoben with HPD watershed connection lvl2 and distance=0: "+str(len(list_BV_polygon_lvl2_dist0))+"/"+str(len(list_bv_done))+"\n")
    g.write("Nb watershed Knoben with HPD watershed connection lvl2 and distance>=0: "+str(len(list_BV_polygon_lvl2))+"/"+str(len(list_bv_done))+"\n")
    g.write("Nb watershed Knoben with HPD watershed connection lvl3 and distance=0: "+str(len(list_BV_polygon_lvl3_dist0))+"/"+str(len(list_bv_done))+"\n")
    g.write("Nb watershed Knoben with HPD watershed connection lvl3 and distance>=0: "+str(len(list_BV_polygon_lvl3))+"/"+str(len(list_bv_done))+"\n")
    
    
    ##Unicite des BV de Knoben dans les contraintes
    g.write("\n")
    g.write("Unicity watersheds used by Knoben with polygon, based on distance contraints"+"\n")
    g.write("Nb watershed Knoben with HPD watershed connection lvl3 and distance=0: "+str(len(list_BV_polygon_lvl3_dist0))+"/"+str(len(list_bv_done))+"\n")
    list_unique=list_BV_polygon_lvl3_dist0
    list_tempo=[]
    for i in list_BV_polygon_lvl3:
        if i not in list_unique:
            list_tempo.append(i)
            list_unique.append(i)
    g.write("Nb watershed Knoben with HPD watershed connection lvl3 and distance>0: "+str(len(list_tempo))+"/"+str(len(list_bv_done))+"\n")
    list_tempo=[]
    for i in list_BV_polygon_lvl2_no_lvl3_dist0:
        if i not in list_unique:
            list_tempo.append(i)
            list_unique.append(i)
    g.write("Nb watershed Knoben with HPD watershed connection lvl2, but no lvl3, and distance=0: "+str(len(list_tempo))+"/"+str(len(list_bv_done))+"\n")
    list_tempo=[]
    for i in list_BV_polygon_lvl2_no_lvl3:
        if i not in list_unique:
            list_tempo.append(i)
            list_unique.append(i)
    g.write("Nb watershed Knoben with HPD watershed connection lvl2, but no lvl3, and distance>0: "+str(len(list_tempo))+"/"+str(len(list_bv_done))+"\n")
    list_tempo=[]
    for i in list_BV_polygon_lvl1_no2_no3_dist0:
        if i not in list_unique:
            list_tempo.append(i)
            list_unique.append(i)
    g.write("Nb watershed Knoben with HPD watershed connection lvl1, but not lvl2 and lvl3, and distance=0: "+str(len(list_tempo))+"/"+str(len(list_bv_done))+"\n")
    list_tempo=[]
    for i in list_BV_polygon_lvl1_no2_no3:
        if i not in list_unique:
            list_tempo.append(i)
            list_unique.append(i)
    g.write("Nb watershed Knoben with HPD watershed connection lvl1, but not lvl2 and lvl3, and distance>0: "+str(len(list_tempo))+"/"+str(len(list_bv_done))+"\n")
    
    g.close()
    
def Writing_distance(database_eco_HPD,count_BV,f,recap):
    if (len(database_eco_HPD.index)==0):
        f.write("No corresponding watersheds.\n")
        count_BV=count_BV+1
    else:
        f.write("ID_BV_HPD;Distance(m)\n")
        for line_lvl in database_eco_HPD.index:
            index_BV=0
            BV_done=[]
            for i in range(len(recap)):
                if recap.iloc[i]['NEAR_FID']==(line_lvl+1):
                    index_BV=i
            if not(database_eco_HPD['id'][line_lvl] in BV_done):
                BV_done.append(database_eco_HPD['id'][line_lvl])
                f.write(str(database_eco_HPD['id'][line_lvl])+";"+recap.iloc[index_BV]['NEAR_DIST']+"\n")
    f.write("\n")
    return count_BV
