import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression

def Perf_comparison(input_directory,input_d_2,path_result,limit_KGE):
    period=["Calibration","Evaluation"]
    file_name_index="Similarity_index.csv" #file where similarity index and KGE are written
    
    data_simindex=pd.read_csv(input_d_2+file_name_index,delimiter=";")
    coord_wts=pd.read_csv(input_directory+"Localisation_BV_Knoben.csv",delimiter=";")
    
    for period_line in period:
        data_KGE=pd.read_csv(input_directory+"KGE_Q_"+period_line+".txt",delimiter=";")
        data_KGE.rename(columns={'05_ihacres_6p_1s': '05_ihacres_7p_1s'}, inplace=True)
        data_KGE_period=[]
        for row in range(len(data_simindex)):
            tempo=data_KGE.loc[data_KGE['Gauge_ID']==data_simindex['WTS_list'][row], "m_"+data_KGE.columns==data_simindex['model_list'][row]].values[0]
            if len(tempo)==1 and tempo>=limit_KGE:
                tempo=tempo.item()
            else:
                tempo=np.nan
            data_KGE_period.append(tempo)
        data_simindex[period_line]=data_KGE_period
    data_simindex = data_simindex[data_simindex['Calibration'].notna()]
    data_simindex = data_simindex[data_simindex['Evaluation'].notna()]
    data_simindex['ratio_nb_param']=data_simindex['Nb_param_mod']/max(data_simindex['Nb_param_mod'])
    
    data_coord_perf=coord_wts[['gauge_id','gauge_lat','gauge_lon']]    
    Value_correlation = pd.DataFrame()
    for line_period in period:
        data_coord_perf['Corr_'+line_period]=np.nan
        data_coord_perf['P_Value_'+line_period]=np.nan
        x_simindex=data_simindex['sim_index']
        y_simindex=data_simindex[line_period]
        nb_param=data_simindex['Nb_param_mod']
        corr_eval = {'x': x_simindex, 'y': y_simindex}
        corr_eval = pd.DataFrame(corr_eval)
        corr_eval = corr_eval.dropna()
        if len(corr_eval)>1:
            r, p_value = pearsonr(corr_eval['x'],corr_eval['y'])
            plt.scatter(x_simindex, y_simindex, c=nb_param, edgecolor='k')
            plt.colorbar(label='Nb parameter model')
            plt.title("Correlation: r="+str(round(r, 3))+" - p.value="+str(round(p_value, 3)))
            plt.savefig(path_result+'Total/Simindex_KGE_'+line_period+'.jpeg', dpi=300, bbox_inches='tight')
            plt.close()
    
        list_corr=[]
        list_corr_pval=[]
        for line_mod in data_simindex['model_list'].unique():
            row_index=data_simindex['model_list']==line_mod
            x_simindex=data_simindex['sim_index'][row_index]
            y_simindex=data_simindex[line_period][row_index]
            nb_param=data_simindex['Nb_param_mod'][row_index]
            corr_eval = {'x': x_simindex, 'y': y_simindex}
            corr_eval = pd.DataFrame(corr_eval)
            corr_eval = corr_eval.dropna()
            if len(corr_eval)>1:
                r, p_value = pearsonr(corr_eval['x'],corr_eval['y'])
                list_corr.append(r)
                if p_value <=0.05:
                    list_corr_pval.append(r)
                plt.scatter(x_simindex, y_simindex, c=nb_param, edgecolor='k')
                plt.colorbar(label='Nb parameter model')
                plt.title("Correlation: r="+str(round(r, 3))+" - p.value="+str(round(p_value, 3)))
                plt.savefig(path_result+'Per_Model/Simindex_KGE_'+line_mod+'_'+line_period+'.jpeg', dpi=300, bbox_inches='tight')
                plt.close()
        list_corr=sorted(list_corr, key=lambda x: (not math.isnan(x), x))
        plt.scatter([range(len(list_corr))],list_corr)
        plt.savefig(path_result+'Recap_coef_pearson_per_model'+'_'+line_period+'_'+'.jpeg', dpi=300, bbox_inches='tight')
        plt.close()
        list_corr_pval=sorted(list_corr_pval, key=lambda x: (not math.isnan(x), x))
        plt.scatter([range(len(list_corr_pval))],list_corr_pval)
        plt.savefig(path_result+'Recap_coef_pearson_per_model'+'_'+line_period+'_'+'_with_pval.jpeg', dpi=300, bbox_inches='tight')
        plt.close()
    
        
        list_corr=[] 
        list_corr_pval=[]
        list_corr_bil_simind_ratparam=[]        
        bilin_coef_a=[]
        bilin_coef_b=[]
        bilin_coef_c=[]
        for line_wts in data_simindex['WTS_list'].unique():
            row_index=data_simindex['WTS_list']==line_wts
            x_simindex=data_simindex['sim_index'][row_index]
            y_simindex=data_simindex[line_period][row_index]
            nb_param=data_simindex['Nb_param_mod'][row_index]
            corr_eval = {'x': x_simindex, 'y': y_simindex}
            corr_eval = pd.DataFrame(corr_eval)
            corr_eval = corr_eval.dropna()
            if len(corr_eval)>1:
                r, p_value = pearsonr(corr_eval['x'],corr_eval['y'])
                list_corr.append(r)
                data_coord_perf.loc[data_coord_perf['gauge_id']==line_wts,'Corr_'+line_period]=r
                data_coord_perf.loc[data_coord_perf['gauge_id']==line_wts,'P_Value_'+line_period]=p_value
                if p_value <=0.05:
                    list_corr_pval.append(r)
                    
                plt.scatter(x_simindex, y_simindex, c=nb_param, edgecolor='k')
                plt.colorbar(label='Nb parameter model')
                plt.xlabel('Similarity index')
                plt.ylabel('KGE(Q) (modelling performance)')
                plt.title("Correlation: r="+str(round(r, 3))+" - p.value="+str(round(p_value, 3)))
                plt.savefig(path_result+'Per_WTS/Simindex_KGE_'+str(line_wts)+'_'+line_period+'.jpeg', dpi=300, bbox_inches='tight')
                plt.close()
                
                X = np.column_stack((data_simindex['sim_index'][row_index], data_simindex['ratio_nb_param'][row_index], data_simindex['sim_index'][row_index] * data_simindex['ratio_nb_param'][row_index])) # Features: x, y, and x*y interaction term
                model = LinearRegression()
                model.fit(X, data_simindex[line_period][row_index]) # Fit model to features and target
                z_pred = model.predict(X)
                r, _ = pearsonr(data_simindex[line_period][row_index], z_pred)
                list_corr_bil_simind_ratparam.append(r)
    
                #Bilinear regression with variable transformee     
                #ratio_param_modifie=np.mean(data_simindex['sim_index'][row_index])+np.std(data_simindex['sim_index'][row_index], ddof=1)/np.std(data_simindex['ratio_nb_param'][row_index], ddof=1)*(data_simindex['ratio_nb_param'][row_index]-np.mean(data_simindex['ratio_nb_param'][row_index]))
                #X = np.column_stack((data_simindex['sim_index'][row_index], ratio_param_modifie, data_simindex['sim_index'][row_index] * ratio_param_modifie)) # Features: x, y, and x*y interaction term
                sim_index_mod=(data_simindex['sim_index'][row_index]-np.std(data_simindex['sim_index'][row_index]))/np.mean(data_simindex['sim_index'][row_index])
                nb_param_mod=(data_simindex['Nb_param_mod'][row_index]-np.std(data_simindex['Nb_param_mod'][row_index]))/np.mean(data_simindex['Nb_param_mod'][row_index])
                X = np.column_stack((sim_index_mod, nb_param_mod)) # Features: x and y
                model = LinearRegression()
                if (np.count_nonzero(sim_index_mod == 0)!=len(sim_index_mod))&(np.isnan(sim_index_mod).sum()!=len(sim_index_mod)):
                    model.fit(X, data_simindex[line_period][row_index]) # Fit model to features and target
                    bilin_coef_a.append(model.coef_[0])
                    bilin_coef_b.append(model.coef_[1])
                    #bilin_coef_c.append(model.coef_[2])
        list_corr=sorted(list_corr, key=lambda x: (not math.isnan(x), x))
        Value_correlation[line_period]=list_corr
        plt.scatter([range(len(list_corr))],list_corr)
        plt.ylabel('Pearson correlation')
        plt.xlabel('Amount of watershed')
        plt.title("Period: "+str(line_period))
        plt.savefig(path_result+'Recap_coef_pearson_per_wts'+'_'+line_period+'_'+'.jpeg', dpi=300, bbox_inches='tight')
        plt.close()
        list_corr_pval=sorted(list_corr_pval, key=lambda x: (not math.isnan(x), x))
        plt.scatter([range(len(list_corr_pval))],list_corr_pval)
        plt.ylabel('Pearson correlation')
        plt.xlabel('Amount of watershed')
        plt.title("Period: "+str(line_period))
        plt.savefig(path_result+'Recap_coef_pearson_per_wts'+'_'+line_period+'_'+'_with_pval.jpeg', dpi=300, bbox_inches='tight')
        plt.close()
        list_corr_bil_simind_ratparam=sorted(list_corr_bil_simind_ratparam, key=lambda x: (not math.isnan(x), x))
        plt.scatter([range(len(list_corr_bil_simind_ratparam))],list_corr_bil_simind_ratparam)
        plt.title("Bilinear relation with sim. index and parameter")  # Set the title
        plt.savefig(path_result+'Recap_coef_pearson_per_wts'+'_'+line_period+'_'+'_bilinear.jpeg', dpi=300, bbox_inches='tight')
        plt.close()
        slope, intercept = np.polyfit(bilin_coef_a, bilin_coef_b, 1)
        plt.scatter(bilin_coef_a,bilin_coef_b)
        plt.xlabel("Coef a (sim_index)")
        plt.ylabel("Coef b (nb_param)")
        plt.title("Coef Bilinear relation with sim. index and parameter, slope = "+str(round(slope,3)))  # Set the title
        plt.savefig(path_result+'Coef_bilin_a_and_b_model_per_wts'+'_'+line_period+'.jpeg', dpi=300, bbox_inches='tight')
        plt.close()
        #slope, intercept = np.polyfit(bilin_coef_a, bilin_coef_c, 1)
        #plt.scatter(bilin_coef_a,bilin_coef_c)
        #plt.xlabel("Coef a (sim_index)")
        #plt.ylabel("Coef c (interaction sim_index/ratio_nb_param)")
        #plt.title("Coef Bilinear relation with sim. index and parameter, slope = "+str(round(slope,3)))  # Set the title
        #plt.savefig(path_result+'Coef_bilin_a_and_c_model_per_wts'+'_'+line_period+'_'+'.jpeg', dpi=300, bbox_inches='tight')
        #plt.close()
        #slope, intercept = np.polyfit(bilin_coef_c, bilin_coef_b, 1)
        #plt.scatter(bilin_coef_c,bilin_coef_b)
        #plt.xlabel("Coef c (interaction sim_index/ratio_nb_param)")
        #plt.ylabel("Coef b (ratio_nb_param)")
        #plt.title("Coef Bilinear relation with sim. index and parameter, slope = "+str(round(slope,3)))  # Set the title
        #plt.savefig(path_result+'Coef_bilin_b_and_c_model_per_wts'+'_'+line_period+'_'+'.jpeg', dpi=300, bbox_inches='tight')
        #plt.close()
    
    data_coord_perf.to_csv(path_result+'Corr_coordinate_WTS.csv', index=False, sep=";")
    
    for line_period in period:
        print(line_period)
        condition = Value_correlation[line_period].abs() > 0.7
        filtered_Value_correlation = Value_correlation[condition]
        num_rows = filtered_Value_correlation.shape[0]
        print("amount watershed with corr. > 0.7: "+str(num_rows))
        condition = (Value_correlation[line_period].abs() <= 0.7) & (Value_correlation[line_period].abs() > 0.4)
        filtered_Value_correlation = Value_correlation[condition]
        num_rows = filtered_Value_correlation.shape[0]
        print("amount watershed with corr. <= 0.7 and > 0.4: "+str(num_rows))
        condition = Value_correlation[line_period].abs() <= 0.4 
        filtered_Value_correlation = Value_correlation[condition]
        num_rows = filtered_Value_correlation.shape[0]
        print("amount watershed with corr. <= 0.4: "+str(num_rows))
