import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from pathlib import Path
from pandas.api.types import is_string_dtype
import numpy as np
import seaborn as sns
from matplotlib.patches import Patch  # for custom legend handles
import textwrap

def Corr_properties_WTS(input_directory,input_d_2,path_result):
    period=["Calibration","Evaluation"]
    properties=['elev_mean','slope_mean','area_geospa_fabric_']
    properties_file=['camels_clim','camels_hydro','camels_soil','camels_topo','camels_vege']
    remove_list=['gauge_id','gauge_lat','gauge_lon']
    
    Corr_data=pd.read_csv(input_d_2+"Corr_coordinate_WTS.csv",delimiter=";",decimal=".")
    Corr_data_snow=pd.read_csv(input_d_2+"Corr_coordinate_WTS_snow.csv",delimiter=";",decimal=".")
    Corr_data_snow = Corr_data_snow.dropna()
    Corr_data_nosnow_WTS_and_mod=pd.read_csv(input_d_2+"Corr_coordinate_WTS_nosnow_WTS_and_mod.csv",delimiter=";",decimal=".")
    Corr_data_nosnow_WTS_and_mod = Corr_data_nosnow_WTS_and_mod.dropna()
    convertname=pd.read_csv(input_directory+"Conversion_name_camels_attributes.txt",sep=";")

    list_prop_gene=[]
    list_prop_gene_full=[]
    list_prop_gene_group=[]
    corr_calib=[]
    corr_valid=[]
    list_prop_gene_nosnow_WTS_and_mod =[]
    list_prop_gene_full_nosnow_WTS_and_mod =[]
    list_prop_gene_group_nosnow_WTS_and_mod =[]
    corr_calib_nosnow_WTS_and_mod =[]
    corr_valid_nosnow_WTS_and_mod =[]
    for line_file_properties in properties_file:
        Pro_data=pd.read_csv(input_directory+line_file_properties+".txt",delimiter=";")
    
        name_col=Pro_data.columns
        name_col = [x for x in name_col if x not in remove_list]
        Corr_data = Corr_data.merge(Pro_data, on='gauge_id', how='inner')  # Only matching rows
        Corr_data_snow = Corr_data_snow.merge(Pro_data, on='gauge_id', how='inner')  # Only matching rows
        Corr_data_snow = Corr_data_snow.dropna()
        Corr_data_nosnow_WTS_and_mod = Corr_data_nosnow_WTS_and_mod.merge(Pro_data, on='gauge_id', how='inner')  # Only matching rows
        Corr_data_nosnow_WTS_and_mod = Corr_data_nosnow_WTS_and_mod.dropna()
        
        folder_path = Path(path_result+line_file_properties)
        folder_path.mkdir(parents=True, exist_ok=True)
        
        for line_column in name_col:
            if not is_string_dtype(Corr_data[line_column]):
                list_prop_gene.append(line_column)
                list_prop_gene_full.append(convertname.loc[convertname['Abbrev'] == line_column, 'Full_name'].iloc[0])
                list_prop_gene_group.append(convertname.loc[convertname['Abbrev'] == line_column, 'Category'].iloc[0])
                list_prop_gene_nosnow_WTS_and_mod.append(line_column)
                list_prop_gene_full_nosnow_WTS_and_mod.append(convertname.loc[convertname['Abbrev'] == line_column, 'Full_name'].iloc[0])
                list_prop_gene_group_nosnow_WTS_and_mod.append(convertname.loc[convertname['Abbrev'] == line_column, 'Category'].iloc[0])
                fig, axes = plt.subplots(1, 2, figsize=(10, 4))
                # Plot data in each subplot
                mask = ~np.isnan(Corr_data[line_column]) & ~np.isnan(Corr_data['Corr_Calibration'])
                r, p_value = pearsonr(Corr_data[line_column][mask], Corr_data['Corr_Calibration'][mask])
                axes[0].scatter(Corr_data[line_column], Corr_data['Corr_Calibration'], color='blue')
                axes[0].set_title(period[0]+": Corr="+str(round(r, 3))+" - p.value="+str(round(p_value, 3)))
                axes[0].set_ylabel("Corr (KGE vs simindex) per WTS")  # Set individual y-axis label
                axes[0].set_xlabel(line_column)  # Set individual y-axis label
                corr_calib.append(r)
                mask = ~np.isnan(Corr_data[line_column]) & ~np.isnan(Corr_data['Corr_Calibration'])
                r, p_value = pearsonr(Corr_data[line_column][mask], Corr_data['Corr_Evaluation'][mask])
                axes[1].scatter(Corr_data[line_column], Corr_data['Corr_Evaluation'], color='red')
                axes[1].set_title(period[1]+": Corr="+str(round(r, 3))+" - p.value="+str(round(p_value, 3)))
                axes[1].set_ylabel("Corr (KGE vs simindex) per WTS")  # Set individual y-axis label
                axes[1].set_xlabel(line_column)  # Set individual y-axis label
                corr_valid.append(r)
                # Adjust layout
                plt.tight_layout()
                plt.savefig(path_result+line_file_properties+'/Correlation_'+line_column+'.jpeg', dpi=300, bbox_inches='tight')
                plt.close()
                
                ##Separated plot
                index_conv=convertname[convertname['Abbrev']==line_column].index
                if not index_conv.empty:
                    name_charact = ' '.join(convertname['Full_name'][index_conv])
                else:
                    name_charact = line_column
                print(name_charact)
                mask = ~np.isnan(Corr_data[line_column]) & ~np.isnan(Corr_data['Corr_Calibration'])
                r, p_value = pearsonr(Corr_data[line_column][mask], Corr_data['Corr_Calibration'][mask])
                plt.scatter(Corr_data[line_column], Corr_data['Corr_Calibration'])
                plt.title("Correlation="+str(round(r, 3))+" - p.value="+str(round(p_value, 3)))
                plt.ylabel("Correlation (KGE vs Similarity Index)")  # Set individual y-axis label
                plt.xlabel(name_charact)  # Set individual y-axis label
                plt.grid(False)
                plt.savefig(path_result+line_file_properties+'/Correlation_'+line_column+"_"+period[0]+'.jpeg', dpi=300, bbox_inches='tight')
                plt.close()
                mask = ~np.isnan(Corr_data[line_column]) & ~np.isnan(Corr_data['Corr_Calibration'])
                r, p_value = pearsonr(Corr_data[line_column][mask], Corr_data['Corr_Evaluation'][mask])
                plt.scatter(Corr_data[line_column], Corr_data['Corr_Evaluation'])
                plt.title("Correlation="+str(round(r, 3))+" - p.value="+str(round(p_value, 3)))
                plt.ylabel("Correlation (KGE vs Similarity Index)")  # Set individual y-axis label
                plt.xlabel(name_charact)  # Set individual y-axis label
                plt.grid(False)
                plt.savefig(path_result+line_file_properties+'/Correlation_'+line_column+"_"+period[1]+'.jpeg', dpi=300, bbox_inches='tight')
                plt.close()
                
                #for fraction of snow in watershed snow-dominated
                if (line_column=="frac_snow"):
                    mask = ~np.isnan(Corr_data_snow[line_column]) & ~np.isnan(Corr_data_snow['Corr_Calibration'])
                    r, p_value = pearsonr(Corr_data_snow[line_column][mask], Corr_data_snow['Corr_Calibration'][mask])
                    plt.scatter(Corr_data_snow[line_column], Corr_data_snow['Corr_Calibration'])
                    plt.title("Correlation="+str(round(r, 3))+" - p.value="+str(round(p_value, 3)))
                    plt.ylabel("Correlation (KGE vs Similarity Index)")  # Set individual y-axis label
                    plt.xlabel(name_charact)  # Set individual y-axis label
                    plt.savefig(path_result+line_file_properties+'/Correlation_'+line_column+"_"+period[0]+'_wts_snow.jpeg', dpi=300, bbox_inches='tight')
                    plt.close()
                    mask = ~np.isnan(Corr_data_snow[line_column]) & ~np.isnan(Corr_data_snow['Corr_Calibration'])
                    r, p_value = pearsonr(Corr_data_snow[line_column][mask], Corr_data_snow['Corr_Evaluation'][mask])
                    plt.scatter(Corr_data_snow[line_column], Corr_data_snow['Corr_Evaluation'])
                    plt.title("Correlation="+str(round(r, 3))+" - p.value="+str(round(p_value, 3)))
                    plt.ylabel("Correlation (KGE vs Similarity Index)")  # Set individual y-axis label
                    plt.xlabel(name_charact)  # Set individual y-axis label
                    plt.savefig(path_result+line_file_properties+'/Correlation_'+line_column+"_"+period[1]+'_wts_snow.jpeg', dpi=300, bbox_inches='tight')
                    plt.close()
                    
                #for only watershd no snow and mod no snow
                mask = ~np.isnan(Corr_data_nosnow_WTS_and_mod[line_column]) & ~np.isnan(Corr_data_nosnow_WTS_and_mod['Corr_Calibration'])
                r, p_value = pearsonr(Corr_data_nosnow_WTS_and_mod[line_column][mask], Corr_data_nosnow_WTS_and_mod['Corr_Calibration'][mask])
                corr_calib_nosnow_WTS_and_mod.append(r)
                plt.scatter(Corr_data_nosnow_WTS_and_mod[line_column], Corr_data_nosnow_WTS_and_mod['Corr_Calibration'])
                plt.title("Correlation="+str(round(r, 3))+" - p.value="+str(round(p_value, 3)))
                plt.ylabel("Correlation (KGE vs Similarity Index)")  # Set individual y-axis label
                plt.xlabel(name_charact)  # Set individual y-axis label
                plt.savefig(path_result+line_file_properties+'/Correlation_'+line_column+"_"+period[0]+'_nosnow_WTS and mod.jpeg', dpi=300, bbox_inches='tight')
                plt.close()
                mask = ~np.isnan(Corr_data_nosnow_WTS_and_mod[line_column]) & ~np.isnan(Corr_data_nosnow_WTS_and_mod['Corr_Calibration'])
                r, p_value = pearsonr(Corr_data_nosnow_WTS_and_mod[line_column][mask], Corr_data_nosnow_WTS_and_mod['Corr_Evaluation'][mask])
                corr_valid_nosnow_WTS_and_mod.append(r)
                plt.scatter(Corr_data_nosnow_WTS_and_mod[line_column], Corr_data_nosnow_WTS_and_mod['Corr_Evaluation'])
                plt.title("Correlation="+str(round(r, 3))+" - p.value="+str(round(p_value, 3)))
                plt.ylabel("Correlation (KGE vs Similarity Index)")  # Set individual y-axis label
                plt.xlabel(name_charact)  # Set individual y-axis label
                plt.savefig(path_result+line_file_properties+'/Correlation_'+line_column+"_"+period[1]+'_nosnow_WTS and mod.jpeg', dpi=300, bbox_inches='tight')
                plt.close()

    
    ##Summary
    summary_corr = pd.DataFrame({'Properties': list_prop_gene_full, 'Calibration': corr_calib,
                                 'Validation': corr_valid, 'Category':list_prop_gene_group})
    summary_corr_no_snow = pd.DataFrame({'Properties': list_prop_gene_full_nosnow_WTS_and_mod, 'Calibration': corr_calib_nosnow_WTS_and_mod,
                                 'Validation': corr_valid_nosnow_WTS_and_mod, 'Category':list_prop_gene_group_nosnow_WTS_and_mod})
    group_colors = {'Climate':'orange','Hydrology':'green','Land Cover':'purple','Soil':'red','Topography':'blue'}
    colors = [group_colors[a] for a in summary_corr['Category']]
    summary_corr=summary_corr.dropna()
    summary_corr['mean']=(summary_corr['Calibration']+summary_corr['Validation'])/2
    summary_corr = summary_corr.sort_values(by='Calibration')
    plt.subplots(figsize=(10, 6))
    plt.barh(summary_corr['Properties'],summary_corr['Calibration'], color=colors)
    plt.ylabel('Pearson correlation')
    plt.xlabel('Watershed Attribute')
    wrapped_labels = ["\n".join(textwrap.wrap(l, width=50)) for l in summary_corr['Properties']]
    plt.yticks(range(len(summary_corr['Properties'])), wrapped_labels)
    legend_handles = [Patch(facecolor=color, label=group) for group, color in group_colors.items()]
    plt.legend(handles=legend_handles,bbox_to_anchor=(1.05, 1), loc='upper left',title='Category')    #for i in range(len(summary_corr)):
    plt.tight_layout()
    plt.savefig(path_result+'Summary_Correlation_through_prop_WTS_calib.jpeg', dpi=300, bbox_inches='tight')
    plt.close()
    summary_corr = summary_corr.sort_values(by='Validation')
    colors = [group_colors[a] for a in summary_corr['Category']]
    plt.subplots(figsize=(11, 7))
    spacing_x_label=[i * 2.1 for i in range(len(summary_corr['Properties']))]
    plt.bar(spacing_x_label,summary_corr['Validation'], color=colors, width=1.4)
    wrapped_labels = ["\n".join(textwrap.wrap(l, width=45)) for l in summary_corr['Properties']]
    plt.xticks(spacing_x_label, wrapped_labels, rotation=90,fontsize=8)
    plt.xlabel('Pearson correlation')
    plt.ylabel('Watershed Attribute')
    plt.axhline(y=0.4, color='black', linestyle='--', label='Threshold')
    plt.text(0,0.45, "Moderate correlation", color='black', va='center', ha='left')
    plt.text(0,0.35, "Weak correlation", color='black', va='center', ha='left')
    plt.axhline(y=-0.4, color='black', linestyle='--', label='Threshold')
    plt.text(max(spacing_x_label), -0.45,"Moderate correlation", color='black', va='center', ha='right')
    plt.text(max(spacing_x_label), -0.35, "Weak correlation", color='black', va='center', ha='right')
    legend_handles = [Patch(facecolor=color, label=group) for group, color in group_colors.items()]
    plt.legend(handles=legend_handles,bbox_to_anchor=(1.05, 1), loc='upper left',title='Category')    #for i in range(len(summary_corr)):
    plt.tight_layout()
    plt.savefig(path_result+'Summary_Correlation_through_prop_WTS_eval.jpeg', dpi=300, bbox_inches='tight')
    plt.close()
    print(summary_corr)
    summary_corr.to_csv(path_result+'Summary_charact_corr.txt', sep=';', index=False)
    
    #Separation per category's watershed
    summary_corr = summary_corr.sort_values(['Category', 'Validation'], ascending=[True, True])
    fig, axs = plt.subplots(5,1,figsize=(9, 15))
    for i, cat in enumerate(summary_corr['Category'].unique()):
        filtered_df=summary_corr[summary_corr['Category']==cat]
        spacing_x_label=[i * 2.1 for i in range(len(filtered_df['Properties']))]
        bars=axs[i].barh(spacing_x_label,filtered_df['Validation'], color=group_colors[cat], height =1.4)
        wrapped_labels = ["\n".join(textwrap.wrap(l, width=50)) for l in filtered_df['Properties']]
        axs[i].set_yticks(spacing_x_label)
        axs[i].set_yticklabels(wrapped_labels, fontsize=10)
        axs[i].set_xlabel('Pearson correlation')
        axs[i].set_xlim(min(summary_corr['Validation'])-0.05, max(summary_corr['Validation'])+0.05)
        axs[i].set_ylabel('Watershed Attribute:\n'+cat)
        axs[i].axvline(x=0.4, color='black', linestyle='--', label='Threshold')
        axs[i].text(0.45, 0,"Moderate \ncorrelation", color='black', va='center', ha='left')
        axs[i].text(0.35, 0,"Weak \ncorrelation", color='black', va='center', ha='right')
        axs[i].axvline(x=-0.4, color='black', linestyle='--', label='Threshold')
        axs[i].text(-0.35,max(spacing_x_label), "Weak \ncorrelation", color='black', va='center', ha='left')
        ymin, ymax = axs[i].get_ylim()
        axs[i].fill_between(x=[-0.7,-0.4], y1=ymin, y2=ymax, color='green', alpha=0.2,  edgecolor='none')
        axs[i].fill_between(x=[0.4,0.7], y1=ymin, y2=ymax, color='green', alpha=0.2,  edgecolor='none')
        axs[i].fill_between(x=[-0.4,0.4], y1=ymin, y2=ymax, color='red', alpha=0.2,  edgecolor='none')
        axs[i].grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(path_result+'Summary_Correlation_through_prop_WTS_eval_per_category.jpeg', dpi=300, bbox_inches='tight')
    plt.close()
    #Same but for only watershed no snow and modele no snow
    summary_corr_no_snow = summary_corr_no_snow.sort_values(['Category', 'Validation'], ascending=[True, True])
    fig, axs = plt.subplots(5,1,figsize=(9, 15))
    for i, cat in enumerate(summary_corr_no_snow['Category'].unique()):
        filtered_df=summary_corr_no_snow[summary_corr_no_snow['Category']==cat]
        spacing_x_label=[i * 2.1 for i in range(len(filtered_df['Properties']))]
        bars=axs[i].barh(spacing_x_label,filtered_df['Validation'], color=group_colors[cat], height =1.4)
        wrapped_labels = ["\n".join(textwrap.wrap(l, width=50)) for l in filtered_df['Properties']]
        axs[i].set_yticks(spacing_x_label)
        axs[i].set_yticklabels(wrapped_labels, fontsize=10)
        axs[i].set_xlabel('Pearson correlation')
        axs[i].set_xlim(min(summary_corr_no_snow['Validation'])-0.05, max(summary_corr_no_snow['Validation'])+0.05)
        axs[i].set_ylabel('Watershed Attribute:\n'+cat)
        axs[i].axvline(x=0.4, color='black', linestyle='--', label='Threshold')
        axs[i].text(0.45, 0,"Moderate \ncorrelation", color='black', va='center', ha='left')
        axs[i].text(0.35, 0,"Weak \ncorrelation", color='black', va='center', ha='right')
        axs[i].axvline(x=-0.4, color='black', linestyle='--', label='Threshold')
        axs[i].text(-0.35,max(spacing_x_label), "Weak \ncorrelation", color='black', va='center', ha='left')
        ymin, ymax = axs[i].get_ylim()
        axs[i].fill_between(x=[-0.7,-0.4], y1=ymin, y2=ymax, color='green', alpha=0.2,  edgecolor='none')
        axs[i].fill_between(x=[0.4,0.7], y1=ymin, y2=ymax, color='green', alpha=0.2,  edgecolor='none')
        axs[i].fill_between(x=[-0.4,0.4], y1=ymin, y2=ymax, color='red', alpha=0.2,  edgecolor='none')
        axs[i].grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(path_result+'Summary_Correlation_through_prop_WTS_eval_per_category_nosnow_WTS_and_mod.jpeg', dpi=300, bbox_inches='tight')
    plt.close()
       
   
def Heatmap_charact_WTS(input_directory,input_d_2,input_d_3,path_result):
    period=["Calibration","Evaluation"]
    properties=['elev_mean','slope_mean','area_geospa_fabric_']
    properties_file=['camels_clim','camels_hydro','camels_soil','camels_topo','camels_vege']
    remove_list=['gauge_id','gauge_lat_x','gauge_lon_x','Corr_Calibration','P_Value_Calibration','Corr_Evaluation','P_Value_Evaluation']
    
    Corr_data=pd.read_csv(input_d_2+"Corr_coordinate_WTS.csv",delimiter=";",decimal=".")
    
    Corr_data = Corr_data.dropna()

    Corr_charac=pd.read_csv(input_d_3+"Summary_charact_corr.txt",delimiter=";")
    Corr_charac = Corr_charac[Corr_charac['mean'].between(-0.3,0.3)]

    for line_file_properties in properties_file:
        Pro_data=pd.read_csv(input_directory+line_file_properties+".txt",delimiter=";")
    
        name_col=Pro_data.columns
        name_col = [x for x in name_col if x not in remove_list]
        Corr_data = Corr_data.merge(Pro_data, on='gauge_id', how='inner')  # Only matching rows
    
    Corr_data=Corr_data.drop(remove_list,axis=1)
    cols_to_drop = [col for col in Corr_charac['Properties'] if col in Corr_data.columns]
    Corr_data=Corr_data.drop(cols_to_drop,axis=1)
    result=Corr_data.corr(numeric_only=True)
    
    plt.figure(figsize=(8, 6))
    pl=sns.heatmap(result,cmap="coolwarm",vmin=-1, vmax=1)
    pl.set_xticklabels(pl.get_xticklabels(), rotation=45, ha='right', fontsize=6)
    pl.set_yticklabels(pl.get_yticklabels(), rotation=0, va='center', fontsize=6)
    plt.savefig(path_result + "Heatmap.tiff")
    plt.close()
    
