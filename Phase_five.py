import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from pathlib import Path
from pandas.api.types import is_string_dtype
import numpy as np
import seaborn as sns

def Corr_properties_WTS(input_directory,input_d_2,path_result):
    period=["Calibration","Evaluation"]
    properties=['elev_mean','slope_mean','area_geospa_fabric_']
    properties_file=['camels_clim','camels_hydro','camels_soil','camels_topo','camels_vege']
    remove_list=['gauge_id','gauge_lat','gauge_lon']
    
    Corr_data=pd.read_csv(input_d_2+"Corr_coordinate_WTS.csv",delimiter=";",decimal=".")
    
    Corr_data = Corr_data.dropna()
      
    list_prop_gene=[]
    corr_calib=[]
    corr_valid=[]
    corr_calib_pval=[]
    pval_cal=[]
    corr_valid_pval=[]
    pval_val=[]
    corr_calib_pvalcor0=[]
    pval_calcor0=[]
    corr_valid_pvalcor0=[]
    pval_valcor0=[]
    for line_file_properties in properties_file:
        Pro_data=pd.read_csv(input_directory+line_file_properties+".txt",delimiter=";")
    
        name_col=Pro_data.columns
        name_col = [x for x in name_col if x not in remove_list]
        Corr_data = Corr_data.merge(Pro_data, on='gauge_id', how='inner')  # Only matching rows
        
        folder_path = Path(path_result+line_file_properties)
        folder_path.mkdir(parents=True, exist_ok=True)
        
        for line_column in name_col:
            if not is_string_dtype(Corr_data[line_column]):
                list_prop_gene.append(line_column)
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
                
                ###With P_value
                indices_cal = Corr_data.index[Corr_data['P_Value_Calibration'] <= 0.05].tolist()
                indices_val = Corr_data.index[Corr_data['P_Value_Evaluation'] <= 0.05].tolist()
                fig, axes = plt.subplots(1, 2, figsize=(10, 4))
                # Plot data in each subplot
                r, p_value = pearsonr(Corr_data[line_column][indices_cal], Corr_data['Corr_Calibration'][indices_cal])
                axes[0].scatter(Corr_data[line_column][indices_cal], Corr_data['Corr_Calibration'][indices_cal], color='blue')
                axes[0].set_title(period[0]+": Corr="+str(round(r, 3))+" - p.value="+str(round(p_value, 3)))
                axes[0].set_ylabel("Corr (KGE vs simindex) per WTS")  # Set individual y-axis label
                axes[0].set_xlabel(line_column)  # Set individual y-axis label
                corr_calib_pval.append(r)
                pval_cal.append(p_value)
                r, p_value = pearsonr(Corr_data[line_column][indices_val], Corr_data['Corr_Evaluation'][indices_val])
                axes[1].scatter(Corr_data[line_column][indices_val], Corr_data['Corr_Evaluation'][indices_val], color='red')
                axes[1].set_title(period[1]+": Corr="+str(round(r, 3))+" - p.value="+str(round(p_value, 3)))
                axes[1].set_ylabel("Corr (KGE vs simindex) per WTS")  # Set individual y-axis label
                axes[1].set_xlabel(line_column)  # Set individual y-axis label
                corr_valid_pval.append(r)
                pval_val.append(p_value)
                # Adjust layout
                plt.tight_layout()
                plt.savefig(path_result+line_file_properties+'/Correlation_'+line_column+'p_value.jpeg', dpi=300, bbox_inches='tight')
                plt.close()
                
                ###With P_value ad cor =0 si mauvais
                Corr_data2=Corr_data.copy()
                indices_cal = Corr_data2.index[Corr_data2['P_Value_Calibration'] > 0.05].tolist()
                indices_val = Corr_data2.index[Corr_data2['P_Value_Evaluation'] > 0.05].tolist()
                Corr_data2.loc[indices_cal,'Corr_Calibration']=0
                Corr_data2.loc[indices_val,'Corr_Evaluation']=0
                fig, axes = plt.subplots(1, 2, figsize=(10, 4))
                # Plot data in each subplot
                r, p_value = pearsonr(Corr_data2[line_column], Corr_data2['Corr_Calibration'])
                axes[0].scatter(Corr_data2[line_column], Corr_data2['Corr_Calibration'], color='blue')
                axes[0].set_title(period[0]+": Corr="+str(round(r, 3))+" - p.value="+str(round(p_value, 3)))
                axes[0].set_ylabel("Corr (KGE vs simindex) per WTS")  # Set individual y-axis label
                axes[0].set_xlabel(line_column)  # Set individual y-axis label
                corr_calib_pvalcor0.append(r)
                pval_calcor0.append(p_value)
                r, p_value = pearsonr(Corr_data2[line_column], Corr_data2['Corr_Evaluation'])
                axes[1].scatter(Corr_data2[line_column], Corr_data2['Corr_Evaluation'], color='red')
                axes[1].set_title(period[1]+": Corr="+str(round(r, 3))+" - p.value="+str(round(p_value, 3)))
                axes[1].set_ylabel("Corr (KGE vs simindex) per WTS")  # Set individual y-axis label
                axes[1].set_xlabel(line_column)  # Set individual y-axis label
                corr_valid_pvalcor0.append(r)
                pval_valcor0.append(p_value)
                # Adjust layout
                plt.tight_layout()
                plt.savefig(path_result+line_file_properties+'/Correlation_'+line_column+'p_value_cor0.jpeg', dpi=300, bbox_inches='tight')
                plt.close()
    
    
    ##Summary sans pvalue
    summary_corr = pd.DataFrame({'Properties': list_prop_gene, 'Calibration': corr_calib,
                                 'Validation': corr_valid})
    summary_corr=summary_corr.dropna()
    summary_corr['mean']=(summary_corr['Calibration']+summary_corr['Validation'])/2
    summary_corr = summary_corr.sort_values(by='mean')
    plt.bar(summary_corr['Properties'],summary_corr['Calibration'], color='blue')
    plt.title('Correlation for Calibration period')
    plt.xticks(rotation=90,fontsize=8)
    plt.ylabel('Pearson correlation')
    plt.xlabel('Characteristic (WTS CAMELS)')
    for i in range(len(summary_corr)):
        plt.axvline(x=i - 0.5, color='gray', linestyle='--', alpha=0.6)  # Adjust x for better alignment
    plt.savefig(path_result+'Summary_Correlation_through_prop_WTS_calib.jpeg', dpi=300, bbox_inches='tight')
    plt.close()
    plt.bar(summary_corr['Properties'],summary_corr['Validation'], color='red')
    plt.title('Correlation for Evaluation period')
    plt.xticks(rotation=90,fontsize=8)
    plt.ylabel('Pearson correlation')
    plt.xlabel('Characteristic (WTS CAMELS)')
    for i in range(len(summary_corr)):
        plt.axvline(x=i - 0.5, color='gray', linestyle='--', alpha=0.6)  # Adjust x for better alignment
    plt.savefig(path_result+'Summary_Correlation_through_prop_WTS_eval.jpeg', dpi=300, bbox_inches='tight')
    plt.close()
    print(summary_corr)
    summary_corr.to_csv(path_result+'Summary_charact_corr.txt', sep=';', index=False)
    
    
    ##Summary avec pvalue
    summary_corr_pval = pd.DataFrame({'Properties': list_prop_gene, 'Calibration': corr_calib_pval, 'pval_cal':pval_cal,
                                 'Validation': corr_valid_pval, 'pval_eval':pval_val})
    summary_corr_pval=summary_corr_pval.dropna()
    summary_corr_pval['mean']=(summary_corr_pval['Calibration']+summary_corr_pval['Validation'])/2
    summary_corr_pval = summary_corr_pval.sort_values(by='mean')
    indices_cal = summary_corr_pval.index[summary_corr_pval['pval_cal'] <= 0.05].tolist()
    indices_val = summary_corr_pval.index[summary_corr_pval['pval_eval'] <= 0.05].tolist()
    plt.bar(summary_corr_pval['Properties'][indices_cal],summary_corr_pval['Calibration'][indices_cal], color='blue')
    plt.title('Correlation for Calibration period with pvalue <= 0.05')
    plt.xticks(rotation=90,fontsize=8)
    plt.ylabel('Pearson correlation')
    plt.xlabel('Characteristic (WTS CAMELS)')
    for i in range(len(indices_cal)):
        plt.axvline(x=i - 0.5, color='gray', linestyle='--', alpha=0.6)  # Adjust x for better alignment
    plt.savefig(path_result+'Summary_Correlation_through_prop_WTS_calib_pval.jpeg', dpi=300, bbox_inches='tight')
    plt.close()
    plt.bar(summary_corr_pval['Properties'][indices_val],summary_corr_pval['Validation'][indices_val], color='red')
    plt.title('Correlation for Evaluation period with pvalue <= 0.05')
    plt.xticks(rotation=90,fontsize=8)
    plt.ylabel('Pearson correlation')
    plt.xlabel('Characteristic (WTS CAMELS)')
    for i in range(len(indices_val)):
        plt.axvline(x=i - 0.5, color='gray', linestyle='--', alpha=0.6)  # Adjust x for better alignment
    plt.savefig(path_result+'Summary_Correlation_through_prop_WTS_eval_pval.jpeg', dpi=300, bbox_inches='tight')
    plt.close()
    summary_corr_pval=summary_corr_pval.drop(columns='mean')
    
    
    ##Summary avec pvalue and cor = 0 si mauvais
    summary_corr_pval0 = pd.DataFrame({'Properties': list_prop_gene, 'Calibration': corr_calib_pvalcor0, 'pval_cal':pval_calcor0,
                                 'Validation': corr_valid_pvalcor0, 'pval_eval':pval_valcor0})
    summary_corr_pval0=summary_corr_pval0.dropna()
    summary_corr_pval0['mean']=(summary_corr_pval0['Calibration']+summary_corr_pval0['Validation'])/2
    summary_corr_pval0 = summary_corr_pval0.sort_values(by='mean')
    indices_cal = summary_corr_pval0.index[summary_corr_pval0['pval_cal'] > 0.05].tolist()
    indices_val = summary_corr_pval0.index[summary_corr_pval0['pval_eval'] > 0.05].tolist()
    summary_corr_pval0.loc[indices_cal,'Calibration']=0
    summary_corr_pval0.loc[indices_val,'Validation']=0
    plt.bar(summary_corr_pval0['Properties'],summary_corr_pval0['Calibration'], color='blue')
    plt.title('Correlation for Calibration period with pvalue <= 0.05')
    plt.xticks(rotation=90,fontsize=8)
    plt.ylabel('Pearson correlation')
    plt.xlabel('Characteristic (WTS CAMELS)')
    for i in range(len(summary_corr_pval0)):
        plt.axvline(x=i - 0.5, color='gray', linestyle='--', alpha=0.6)  # Adjust x for better alignment
    plt.savefig(path_result+'Summary_Correlation_through_prop_WTS_calib_pval_withcor0.jpeg', dpi=300, bbox_inches='tight')
    plt.close()
    plt.bar(summary_corr_pval0['Properties'],summary_corr_pval0['Validation'], color='red')
    plt.title('Correlation for Evaluation period with pvalue <= 0.05')
    plt.xticks(rotation=90,fontsize=8)
    plt.ylabel('Pearson correlation')
    plt.xlabel('Characteristic (WTS CAMELS)')
    for i in range(len(summary_corr_pval0)):
        plt.axvline(x=i - 0.5, color='gray', linestyle='--', alpha=0.6)  # Adjust x for better alignment
    plt.savefig(path_result+'Summary_Correlation_through_prop_WTS_eval_pval_withcor0.jpeg', dpi=300, bbox_inches='tight')
    plt.close()
    summary_corr_pval0=summary_corr_pval0.drop(columns='mean')
    
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
    Corr_data=Corr_data.drop(Corr_charac['Properties'],axis=1)
    result=Corr_data.corr(numeric_only=True)
    
    plt.figure(figsize=(8, 6))
    pl=sns.heatmap(result,cmap="coolwarm",vmin=-1, vmax=1)
    pl.set_xticklabels(pl.get_xticklabels(), rotation=45, ha='right', fontsize=6)
    pl.set_yticklabels(pl.get_yticklabels(), rotation=0, va='center', fontsize=6)
    plt.savefig(path_result + "Heatmap.tiff")
    plt.close()