import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
from matplotlib import pyplot as plt # import libraries
import numpy as np
import scipy

def Association_Phenom_BV_Knoben_HPD(input_directory,path_result):
  
    content_distance = pd.read_csv(input_directory+"Distance_Knoben_HPD.csv",delimiter=";")
    content_eco_HPD = pd.read_csv(input_directory+"Compa_Eco_HPD.csv",delimiter=";")
    content_eco_knob = pd.read_csv(input_directory+"Compa_Eco_Knobentopo.csv",delimiter=";")
    
    df = pd.DataFrame()
    unique_BV_Knoben=content_eco_knob['gauge_id'].unique() #Unicite des BV
    BV_knob = content_eco_knob[['gauge_id','NA_L3CODE','NA_L2CODE']]
    
    resultat=pd.DataFrame(columns=['ID_BV_Knoben','Eco-lvl3_K','Eco_lvl2_K','ID_BV_HPD','Eco-lvl3_HPD','Eco-lvl2_HPD',
                                   'store_id','flux_id','Distance','Commentary','Valide','Code_Map'])
    
    index_row=0
    for index_k, row_k in BV_knob.iterrows():
        print(index_k)
        tempo_HPD = content_eco_HPD[content_eco_HPD['NA_L2CODE']==BV_knob['NA_L2CODE'][index_k]]
        if len(tempo_HPD)!=0:
            for j, row_hpd in enumerate(tempo_HPD.iterrows()):
                index_dist=[i for i in range(len(content_distance)) if (content_distance['gauge_id'][i]==BV_knob['gauge_id'][index_k]) and (content_distance['NEAR_FID'][i]==(tempo_HPD.index[j]+1))]
                if tempo_HPD['NA_L3CODE'][tempo_HPD.index[j]]==BV_knob['NA_L3CODE'][index_k]:
                    resultat.loc[index_row]=pd.Series({'ID_BV_Knoben':BV_knob['gauge_id'][index_k],
                                                   'Eco-lvl3_K':BV_knob['NA_L3CODE'][index_k],
                                                   'Eco_lvl2_K':BV_knob['NA_L2CODE'][index_k],
                                                   'ID_BV_HPD':tempo_HPD['id'][tempo_HPD.index[j]],
                                                   'Eco-lvl3_HPD':tempo_HPD['NA_L3CODE'][tempo_HPD.index[j]],
                                                   'Eco-lvl2_HPD':tempo_HPD['NA_L2CODE'][tempo_HPD.index[j]],
                                                   'store_id':tempo_HPD['store_id_list'][tempo_HPD.index[j]],
                                                   'flux_id':tempo_HPD['flux_id_list'][tempo_HPD.index[j]],
                                                   'Distance':content_distance.loc[index_dist]['NEAR_DIST'].item(),
                                                   'Commentary':'ok',
                                                   'Valide':'ok',
                                                   'Code_Map':'.'})
                elif tempo_HPD['NA_L2CODE'][tempo_HPD.index[j]]==BV_knob['NA_L2CODE'][index_k]:
                    resultat.loc[index_row]=pd.Series({'ID_BV_Knoben':BV_knob['gauge_id'][index_k],
                                                   'Eco-lvl3_K':BV_knob['NA_L3CODE'][index_k],
                                                   'Eco_lvl2_K':BV_knob['NA_L2CODE'][index_k],
                                                   'ID_BV_HPD':tempo_HPD['id'][tempo_HPD.index[j]],
                                                   'Eco-lvl3_HPD':tempo_HPD['NA_L3CODE'][tempo_HPD.index[j]],
                                                   'Eco-lvl2_HPD':tempo_HPD['NA_L2CODE'][tempo_HPD.index[j]],
                                                   'store_id':tempo_HPD['store_id_list'][tempo_HPD.index[j]],
                                                   'flux_id':tempo_HPD['flux_id_list'][tempo_HPD.index[j]],
                                                   'Distance':content_distance.loc[index_dist,'NEAR_DIST'].item(),
                                                   'Commentary':'TBC',
                                                   'Valide':'TBC',
                                                   'Code_Map':'TBC'})
                index_row=index_row+1
        
    resultat.to_csv(path_result+'/Association_Dom_Phen_BV_Knoben.txt', sep=';', index=False)

def Density_plot_distance(input_directory,path_result):
    content_distance = pd.read_csv(input_directory+"Association_Dom_Phen_BV_Knoben.txt",delimiter=";")  ##Ne contient que les BV de HPD et Knoben partageant les memes ecoregions lvl2 ou lvl3
    
    content_distance['Distance']=content_distance['Distance'].str.replace(',', '.').astype(float)
    contentlvl3 = content_distance.loc[content_distance['Eco-lvl3_K']==content_distance['Eco-lvl3_HPD'],'Distance']
    contentlvl2 = content_distance.loc[(content_distance['Eco_lvl2_K']==content_distance['Eco-lvl2_HPD']) & (content_distance['Eco-lvl3_K']!=content_distance['Eco-lvl3_HPD']),'Distance']
    
    BD_width = 0.01
    sns.set_style('whitegrid')
    sns.kdeplot(content_distance.loc[content_distance['Eco-lvl3_K']==content_distance['Eco-lvl3_HPD'],'Distance'], bw_method=BD_width, color='r', shade=True, label='LVL3').legend(loc="upper right")
    sns.kdeplot(content_distance.loc[(content_distance['Eco_lvl2_K']==content_distance['Eco-lvl2_HPD']) & (content_distance['Eco-lvl3_K']!=content_distance['Eco-lvl3_HPD']),'Distance'], bw_method=BD_width, color='b', shade=True, label='LVL2').legend(loc="upper right")
    plt.xlabel('Distance (m)')
    #plt.gcf().set_size_inches(16, 13)
    plt.savefig(path_result + "Histogram_distance_BW="+str(BD_width)+".tiff")
    plt.close()
    
    sns.set_style('whitegrid')
    sns.kdeplot(content_distance.loc[content_distance['Eco-lvl3_K']==content_distance['Eco-lvl3_HPD'],'Distance'], cumulative=True, bw_method=BD_width, color='r', shade=True, label='LVL3').legend(loc="upper right")
    sns.kdeplot(content_distance.loc[(content_distance['Eco_lvl2_K']==content_distance['Eco-lvl2_HPD']) & (content_distance['Eco-lvl3_K']!=content_distance['Eco-lvl3_HPD']),'Distance'], cumulative=True, bw_method=BD_width, color='b', shade=True, label='LVL2').legend(loc="upper right")
    plt.xlabel('Distance (m)')
    #plt.gcf().set_size_inches(16, 13)
    plt.savefig(path_result + "Histogram_distance_BW="+str(BD_width)+"_cumul.tiff")
    plt.close()
    
    BD_width = 0.1
    sns.set_style('whitegrid')
    sns.kdeplot(content_distance.loc[content_distance['Eco-lvl3_K']==content_distance['Eco-lvl3_HPD'],'Distance'], bw_method=BD_width, color='r', shade=True, label='LVL3').legend(loc="upper right")
    sns.kdeplot(content_distance.loc[(content_distance['Eco_lvl2_K']==content_distance['Eco-lvl2_HPD']) & (content_distance['Eco-lvl3_K']!=content_distance['Eco-lvl3_HPD']),'Distance'], bw_method=BD_width, color='b', shade=True, label='LVL2').legend(loc="upper right")
    plt.xlabel('Distance (m)')
    #plt.gcf().set_size_inches(16, 13)
    plt.savefig(path_result + "Histogram_distance_BW="+str(BD_width)+".tiff")
    plt.close()
    
    sns.set_style('whitegrid')
    sns.kdeplot(content_distance.loc[content_distance['Eco-lvl3_K']==content_distance['Eco-lvl3_HPD'],'Distance'], cumulative=True, bw_method=BD_width, color='r', shade=True, label='LVL3').legend(loc="upper right")
    sns.kdeplot(content_distance.loc[(content_distance['Eco_lvl2_K']==content_distance['Eco-lvl2_HPD']) & (content_distance['Eco-lvl3_K']!=content_distance['Eco-lvl3_HPD']),'Distance'], cumulative=True, bw_method=BD_width, color='b', shade=True, label='LVL2').legend(loc="upper right")
    plt.xlabel('Distance (m)')
    #plt.gcf().set_size_inches(16, 13)
    plt.savefig(path_result + "Histogram_distance_BW="+str(BD_width)+"_cumul.tiff")
    plt.close()
    
    BD_width = 0.5
    sns.set_style('whitegrid')
    sns.kdeplot(content_distance.loc[content_distance['Eco-lvl3_K']==content_distance['Eco-lvl3_HPD'],'Distance'], bw_method=BD_width, color='r', shade=True, label='LVL3').legend(loc="upper right")
    sns.kdeplot(content_distance.loc[(content_distance['Eco_lvl2_K']==content_distance['Eco-lvl2_HPD']) & (content_distance['Eco-lvl3_K']!=content_distance['Eco-lvl3_HPD']),'Distance'], bw_method=BD_width, color='b', shade=True, label='LVL2').legend(loc="upper right")
    plt.xlabel('Distance (m)')
    #plt.gcf().set_size_inches(16, 13)
    plt.savefig(path_result + "Histogram_distance_BW="+str(BD_width)+".tiff")
    plt.close()
    
    sns.set_style('whitegrid')
    sns.kdeplot(content_distance.loc[content_distance['Eco-lvl3_K']==content_distance['Eco-lvl3_HPD'],'Distance'], cumulative=True, bw_method=BD_width, color='r', shade=True, label='LVL3').legend(loc="upper right")
    sns.kdeplot(content_distance.loc[(content_distance['Eco_lvl2_K']==content_distance['Eco-lvl2_HPD']) & (content_distance['Eco-lvl3_K']!=content_distance['Eco-lvl3_HPD']),'Distance'], cumulative=True, bw_method=BD_width, color='b', shade=True, label='LVL2').legend(loc="upper right")
    plt.xlabel('Distance (m)')
    #plt.gcf().set_size_inches(16, 13)
    plt.savefig(path_result + "Histogram_distance_BW="+str(BD_width)+"_cumul.tiff")
    plt.close()
    
    list_perc=[0.8,0.9,0.95,0.99]
    g = open(path_result+'Summary_Stat_Histogram.txt','w')
    for i in list_perc:
        dist=np.quantile(content_distance.loc[content_distance['Eco-lvl3_K']==content_distance['Eco-lvl3_HPD'],'Distance'],i)
        g.write("For the percentile (%):"+str(i*100)+", the distance between watersheds in HPD and Knoben datasets in the same lvl3 ecoregion is: "+str(round(dist)/1000)+"km"+"\n")
    g.close()

def Synthesis_Combination_watershed_HPD_Knoben(distance,input_directory,path_result):
    ##Data
    content_distance_polygon = pd.read_csv(input_directory+"Ecoregionslvl3_HPD_Knoben_distance_polygon.csv",delimiter=";",decimal=",")
    content_HPD_polygon = pd.read_csv(input_directory+"Ecoregionslvl3_HPD_WSHD_properties.csv",delimiter=";",decimal=",")
    content_Knoben_polygon = pd.read_csv(input_directory+"Ecoregionslvl3_Knoben_WSHD_properties.csv",delimiter=";",decimal=",")
    content_distance = pd.read_csv(input_directory +"Distance_Knoben_HPD.csv",delimiter=";")
    content_distance['NEAR_DIST']=content_distance['NEAR_DIST'].str.replace(',', '.').astype(float)
    content_eco_HPD = pd.read_csv(input_directory+"Compa_Eco_HPD.csv",delimiter=";")
    content_eco_knob = pd.read_csv(input_directory+"Compa_Eco_Knobentopo.csv",delimiter=";")
    
    containt_lvl2_exc = True ##If True, does not consider ecoregion lvl2 if presence of watershed in ecoregion lvl3  
       
    df = pd.DataFrame({'Watershed' : content_distance['gauge_id'].unique(), 'LVL3' : np.repeat(0, len(content_distance['gauge_id'].unique())), 'LVL2' : np.repeat(0, len(content_distance['gauge_id'].unique()))})
    recap_phenom=[]
    for line_pr, BV in enumerate(df['Watershed']):
        print("Progress (%): ",str(line_pr/len(df)*100))
        ##BV HPD Appartient meme ecoregion lvl3 que Knoben?
        init3=[]
        ##BV HPD Appartient meme ecoregion lvl2 (hors lvl3) que Knoben, et inferieur distance?
        init2=[]
        for line,i in enumerate(content_distance['gauge_id']):
            contraint_BV = i == BV
    
            contrainte_LVL2 = content_distance['NA_L2CODE'][line]==content_eco_HPD['NA_L2CODE'][content_distance['NEAR_FID'][line]-1]
            contrainte_LVL3 = content_distance['NA_L3CODE'][line]==content_eco_HPD['NA_L3CODE'][content_distance['NEAR_FID'][line]-1]
    
            contrainte_unicity2 = (content_distance['NEAR_FID'][line]-1) in init2    
            contrainte_unicity3 = (content_distance['NEAR_FID'][line]-1) in init3    
    
            contrainte_dist = float(content_distance['NEAR_DIST'][line])<=distance
            index_hpd_polyg = content_HPD_polygon.index[content_HPD_polygon['JOIN_FID'] == (content_distance['NEAR_FID'][line])].tolist()
            index_knob_polyg = content_Knoben_polygon.index[content_Knoben_polygon['gauge_id']==BV].tolist()
            contrainte_polygon_dist = content_distance_polygon.loc[(content_distance_polygon['IN_FID']==(index_hpd_polyg[0]+1)) & (content_distance_polygon['NEAR_FID']==(index_knob_polyg[0]+1)),'NEAR_DIST'] == 0 ##distance polygone = 0
    
            if (contraint_BV and contrainte_LVL3 and not contrainte_unicity3):
                init3.append(content_distance['NEAR_FID'][line]-1)
            if (contraint_BV and contrainte_LVL2 and not contrainte_LVL3 and 
                    not contrainte_unicity2 and contrainte_dist):
                init2.append(content_distance['NEAR_FID'][line]-1)
        df.loc[df['Watershed']==BV,'LVL3']=len(init3)
        if len(init3)!=0:
            for bv_init3 in init3:
                recap_phenom.append({
                    'BV_Knoben': BV,
                    'BV_HPD': bv_init3+1,
                    'Store_Phenom': content_eco_HPD['store_id_list'][bv_init3],
                    'Flux_Phenom': content_eco_HPD['flux_id_list'][bv_init3]
                })
        if containt_lvl2_exc and len(init3)!=0:
            df.loc[df['Watershed']==BV,'LVL2']=0        
        else:
            df.loc[df['Watershed']==BV,'LVL2']=len(init2)
            for bv_init2 in init2:
                recap_phenom.append({
                    'BV_Knoben': BV,
                    'BV_HPD': bv_init2+1,
                    'Store_Phenom': content_eco_HPD['store_id_list'][bv_init2],
                    'Flux_Phenom': content_eco_HPD['flux_id_list'][bv_init2]
                })
    df['Amount_HPD_Watershed']=df['LVL3']+df['LVL2']
    recap_phenom=pd.DataFrame(recap_phenom)
    recap_phenom.to_csv(path_result+'/Flux_Knoben_WTS.csv', index=False, sep=";")
    
    plt.hist(df['Amount_HPD_Watershed'])
    
    summary_df_null = pd.DataFrame({'Nb_Watershed' : ['0','>0'], 'Amount' : [0,0]})
    summary_df_null.loc[summary_df_null['Nb_Watershed']=='0','Amount']=df['Amount_HPD_Watershed'].value_counts().get(0, 0)
    summary_df_null.loc[summary_df_null['Nb_Watershed']=='>0','Amount']=len(df)-df['Amount_HPD_Watershed'].value_counts().get(0, 0)
    
    summary_df_non_nul = pd.DataFrame({'Nb_Watershed' : df['Amount_HPD_Watershed'].unique(), 'Amount' : np.repeat(0, len(df['Amount_HPD_Watershed'].unique()))})
    summary_df_non_nul = summary_df_non_nul[summary_df_non_nul['Nb_Watershed']>0]
    for i in summary_df_non_nul['Nb_Watershed']:
        summary_df_non_nul.loc[summary_df_non_nul['Nb_Watershed']==i,'Amount']= df['Amount_HPD_Watershed'].value_counts().get(i, 0)
    
    summary_df_non_nul=summary_df_non_nul.sort_values(by=['Nb_Watershed'], ascending=False)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 5))
    fig.subplots_adjust(wspace=0)
    # pie chart parameters
    overall_ratios = summary_df_null['Amount']
    labels = summary_df_null['Nb_Watershed']
    explode = [0.1, 0]
    # rotate so that first wedge is split by the x-axis
    angle = -180 * overall_ratios[0]
    wedges, *_ = ax1.pie(overall_ratios, autopct='%1.1f%%', startangle=angle,
                         labels=labels, explode=explode, colors=["orange","deepskyblue"])
    
    
    # bar chart parameters
    Wat_ratios = summary_df_non_nul['Amount']
    Wat_labels = summary_df_non_nul['Nb_Watershed']
    bottom = 1
    width = .2
    
    # Adding from the top matches the legend.
    for j, (height, label) in enumerate(reversed([*zip(Wat_ratios, Wat_labels)])):
        bottom -= height
        bc = ax2.bar(0, height, width, bottom=bottom, color='C0', label=label,
                     alpha=0.9/(len(summary_df_non_nul)) * j+0.1)
        ax2.bar_label(bc, labels=[f"{height}"], label_type='center')
    
    ax2.set_title('Nb watersheds Knoben')
    ax2.legend(title = "Nb Wat. HPD")
    ax2.axis('off')
    ax2.set_xlim(- 2.5 * width, 2.5 * width)
    
    fig.savefig(path_result+'/to_store.jpeg', bbox_inches='tight')
