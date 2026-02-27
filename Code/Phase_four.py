import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import pearsonr, linregress
from sklearn.linear_model import LinearRegression
import seaborn as sns
from matplotlib.colors import ListedColormap

def Perf_comparison(input_directory,input_d_2,path_result,limit_KGE):
    period=["Calibration","Evaluation"]
    file_name_index="Similarity_index.csv" #file where similarity index and KGE are written
    file_name_index_proc="Similarity_index_subsetmodel.csv" #file where similarity index and KGE are written

    data_simindex=pd.read_csv(input_d_2+file_name_index,delimiter=";")
    data_simindex_proc=pd.read_csv(input_d_2+file_name_index_proc,delimiter=";")
    coord_wts=pd.read_csv(input_directory+"CAMELS_Data/Localisation_BV_Knoben.csv",delimiter=";")
    
    #Evaluation of ratio_nb_param
    for period_line in period:
        data_KGE=pd.read_csv(input_directory+"Model_Data/KGE_Q_"+period_line+".txt",delimiter=";")
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
        data_simindex_proc[period_line]=data_KGE_period
    data_simindex = data_simindex[data_simindex['Calibration'].notna()]
    data_simindex = data_simindex[data_simindex['Evaluation'].notna()]
    data_simindex['ratio_nb_param']=data_simindex['Nb_param_mod']/max(data_simindex['Nb_param_mod'])
    data_simindex_proc = data_simindex_proc[data_simindex_proc['Calibration'].notna()]
    data_simindex_proc = data_simindex_proc[data_simindex_proc['Evaluation'].notna()]
    
    data_coord_perf=coord_wts[['gauge_id','gauge_lat','gauge_lon']].copy()    
    data_coord_perf_snow=coord_wts[['gauge_id','gauge_lat','gauge_lon']].copy()    
    data_coord_perf_no_snow_wts_and_mod=coord_wts[['gauge_id','gauge_lat','gauge_lon']].copy()    
    data_coord_perf_subsurf=coord_wts[['gauge_id','gauge_lat','gauge_lon']].copy()    
    data_coord_perf_gwt=coord_wts[['gauge_id','gauge_lat','gauge_lon']].copy()    
    Value_correlation = pd.DataFrame()
    for line_period in period:
        data_coord_perf['Corr_'+line_period]=np.nan
        data_coord_perf['P_Value_'+line_period]=np.nan
        data_coord_perf_snow['Corr_'+line_period]=np.nan
        data_coord_perf_snow['P_Value_'+line_period]=np.nan
        data_coord_perf_no_snow_wts_and_mod['Corr_'+line_period]=np.nan
        data_coord_perf_no_snow_wts_and_mod['P_Value_'+line_period]=np.nan
        data_coord_perf_subsurf['Corr_'+line_period]=np.nan
        data_coord_perf_subsurf['P_Value_'+line_period]=np.nan
        data_coord_perf_gwt['Corr_'+line_period]=np.nan
        data_coord_perf_gwt['P_Value_'+line_period]=np.nan
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
        list_slope=[]
        list_wts_snow=[]
        list_corr_snow=[]
        list_corr_nosnow=[]
        corrtot_wts_snow=[]
        slopetot_wts_snow=[]
        list_wts_subsurf=[]
        list_corr_subsurf=[]
        list_corr_nosubsurf=[]
        corrtot_wts_subsurf=[]
        slopetot_wts_subsurf=[]
        list_wts_gwt=[]
        list_corr_gwt=[]
        list_corr_nogwt=[]
        corrtot_wts_gwt=[]
        slopetot_wts_gwt=[]
        corrtot_wts_no_snow_wts_and_mod=[]
        slopetot_wts_no_snow_wts_and_mod=[]
        list_corr_bil_simind_ratparam=[]        
        bilin_coef_a=[]
        bilin_coef_b=[]
        bilin_coef_c=[]
        r2_bilin=[]
        #Evaluation correlation
        for line_wts in data_simindex['WTS_list'].unique():
            row_index=data_simindex[data_simindex['WTS_list'] == line_wts].index
            x_simindex=data_simindex['sim_index'][row_index]
            y_simindex=data_simindex[line_period][row_index]
            nb_param=data_simindex['Nb_param_mod'][row_index]
            corr_eval = {'x': x_simindex, 'y': y_simindex}
            corr_eval = pd.DataFrame(corr_eval)
            corr_eval = corr_eval.dropna()
            if len(corr_eval)>1:
                slopetot, _ , r_value_tot, p_value_tot , _  = linregress(corr_eval['x'],corr_eval['y'])
                list_corr.append(r_value_tot)
                list_slope.append(slopetot)
                data_coord_perf.loc[data_coord_perf['gauge_id']==line_wts,'Corr_'+line_period]=r_value_tot
                data_coord_perf.loc[data_coord_perf['gauge_id']==line_wts,'P_Value_'+line_period]=p_value
                plt.scatter(x_simindex, y_simindex, c=nb_param, edgecolor='k')
                cbar = plt.colorbar()
                cbar.set_label('Nb parameter model', rotation=-90, labelpad=15)  
                plt.xlabel('Similarity index')
                plt.ylabel('KGE(Q) (modelling performance)')
                plt.title("Correlation: r="+str(round(r_value_tot, 3))+" - p.value="+str(round(p_value, 3)))
                plt.savefig(path_result+'Per_WTS/general/Simindex_KGE_'+str(line_wts)+'_'+line_period+'.jpeg', dpi=300, bbox_inches='tight')
                plt.close()
                
                X = np.column_stack((data_simindex['sim_index'][row_index], data_simindex['ratio_nb_param'][row_index], data_simindex['sim_index'][row_index] * data_simindex['ratio_nb_param'][row_index])) # Features: x, y, and x*y interaction term
                model = LinearRegression()
                model.fit(X, data_simindex[line_period][row_index]) # Fit model to features and target
                z_pred = model.predict(X)
                slope, _ , r_value, _ , _  = linregress(data_simindex[line_period][row_index], z_pred)
                list_corr_bil_simind_ratparam.append(r_value)
    
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
                    r2_bilin.append(model.score(X, data_simindex[line_period][row_index]))
                if data_simindex_proc['snow_proc_wts'][row_index[0]]==1:
                    Plot_per_charact(data_simindex_proc,data_coord_perf_snow,data_coord_perf,line_wts,
                                         line_period,list_corr_snow,list_corr_nosnow,r_value_tot,p_value_tot,
                                         path_result,list_wts_snow,corrtot_wts_snow,slopetot_wts_snow,slopetot,'Snow')

                if data_simindex_proc['subsurf_proc_wts'][row_index[0]]==1:
                    Plot_per_charact(data_simindex_proc,data_coord_perf_subsurf,data_coord_perf,line_wts,
                                         line_period,list_corr_subsurf,list_corr_nosubsurf,r_value_tot,p_value_tot,
                                         path_result,list_wts_subsurf,corrtot_wts_subsurf,slopetot_wts_subsurf,slopetot,'Subsurf')
                    
                if data_simindex_proc['gwt_proc_wts'][row_index[0]]==1:
                    Plot_per_charact(data_simindex_proc,data_coord_perf_gwt,data_coord_perf,line_wts,
                                         line_period,list_corr_gwt,list_corr_nogwt,r_value_tot,p_value_tot,
                                         path_result,list_wts_gwt,corrtot_wts_gwt,slopetot_wts_gwt,slopetot,'GWT')
                    
                if data_simindex_proc['snow_proc_wts'][row_index[0]]==0:
                    row_index=data_simindex_proc[(data_simindex_proc['WTS_list'] == line_wts)].index #&(data_simindex_proc['snow_proc_mod'] == 0)
                    x_simindex=data_simindex_proc['sim_index'][row_index]
                    y_simindex=data_simindex_proc[line_period][row_index]
                    corr_eval = {'x': x_simindex, 'y': y_simindex}
                    corr_eval = pd.DataFrame(corr_eval)
                    corr_eval = corr_eval.dropna()
                    if len(corr_eval)>1:
                        slopetot, _ , r_value_tot, p_value_tot , _  = linregress(corr_eval['x'],corr_eval['y'])
                        corrtot_wts_no_snow_wts_and_mod.append(r_value_tot)
                        slopetot_wts_no_snow_wts_and_mod.append(slopetot)
                        data_coord_perf_no_snow_wts_and_mod.loc[data_coord_perf_no_snow_wts_and_mod['gauge_id']==line_wts,'Corr_'+line_period]=r_value_tot
                        data_coord_perf_no_snow_wts_and_mod.loc[data_coord_perf_no_snow_wts_and_mod['gauge_id']==line_wts,'P_Value_'+line_period]=p_value_tot
                        plt.scatter(x_simindex, y_simindex, c='blue', edgecolor='k')
                        cbar = plt.colorbar()
                        cbar.set_label('Nb parameter model', rotation=-90, labelpad=15)  
                        plt.xlabel('Similarity index')
                        plt.ylabel('KGE(Q) (modelling performance)')
                        plt.title("Correlation: r="+str(round(r_value_tot, 3))+" - p.value="+str(round(p_value, 3)))
                        plt.savefig(path_result+'Per_WTS/WTS_nosnow_mod_nosnow/Simindex_KGE_'+str(line_wts)+'_'+line_period+'.jpeg', dpi=300, bbox_inches='tight')
                        plt.close()
                                    
        Corr_slope_df=pd.DataFrame({"Correlation":list_corr,"Slope":list_slope})
        Corr_slope_df_snow = pd.DataFrame({"Correlation":corrtot_wts_snow,"Slope":slopetot_wts_snow})
        Corr_slope_df_subsurf = pd.DataFrame({"Correlation":corrtot_wts_subsurf,"Slope":slopetot_wts_subsurf})
        Corr_slope_df_gwt = pd.DataFrame({"Correlation":corrtot_wts_gwt,"Slope":slopetot_wts_gwt})
        Corr_slope_df_nosnow_WTS = pd.DataFrame({"Correlation":corrtot_wts_no_snow_wts_and_mod,"Slope":slopetot_wts_no_snow_wts_and_mod})
        list_corr=sorted(list_corr, key=lambda x: (not math.isnan(x), x))
        Value_correlation[line_period]=list_corr
        Compa_snow = pd.DataFrame({'WTS_list':list_wts_snow,'Total':corrtot_wts_snow,'With_snow':list_corr_snow,'Without_snow':list_corr_nosnow})
        Compa_subsurf = pd.DataFrame({'WTS_list':list_wts_subsurf,'Total':corrtot_wts_subsurf,'With_subsurf':list_corr_subsurf,'Without_subsurf':list_corr_nosubsurf})
        Compa_gwt = pd.DataFrame({'WTS_list':list_wts_gwt,'Total':corrtot_wts_gwt,'With_gwt':list_corr_gwt,'Without_gwt':list_corr_nogwt})

        #Amount of watershed falling in 
        print(line_period)
        condition = Value_correlation[line_period].abs() > 0.7
        filtered_Value_correlation = Value_correlation[condition]
        num_rows_strong = filtered_Value_correlation.shape[0]
        print("amount watershed with corr. > 0.7: "+str(num_rows_strong))
        condition = (Value_correlation[line_period].abs() <= 0.7) & (Value_correlation[line_period].abs() > 0.4)
        filtered_Value_correlation = Value_correlation[condition]
        num_rows_medium = filtered_Value_correlation.shape[0]
        print("amount watershed with corr. <= 0.7 and > 0.4: "+str(num_rows_medium))
        condition = Value_correlation[line_period].abs() <= 0.4 
        filtered_Value_correlation = Value_correlation[condition]
        num_rows_weak = filtered_Value_correlation.shape[0]
        print("amount watershed with corr. <= 0.4: "+str(num_rows_weak))
        num_rows_strong=num_rows_strong/len(Value_correlation[line_period])
        num_rows_medium=num_rows_medium/len(Value_correlation[line_period])
        num_rows_weak=num_rows_weak/len(Value_correlation[line_period])
        
        #Figure fraction watersheds in function of Pearson correlation
        plt.scatter(list_corr,[np.arange(0.0, 1.0+1/len(list_corr), 1/(len(list_corr)-1))])
        plt.fill_between(x=[-0.4,0.4], y1=0, y2=num_rows_weak, color='red', alpha=0.2,  edgecolor='none')
        plt.axhline(y=num_rows_weak, color='black', linestyle='--', label='Threshold')
        plt.text(-0.4, num_rows_weak-0.05, "Weak correlation: "+str(round(num_rows_weak*100,2))+"%", color='black', va='center', ha='left')
        plt.fill_between(x=[0.4,0.7], y1=0, y2=num_rows_weak+num_rows_medium, color='green', alpha=0.2, edgecolor='none')
        plt.fill_between(x=[-0.4,0.4], y1=num_rows_weak, y2=num_rows_weak+num_rows_medium, color='green', alpha=0.2,  edgecolor='none')
        plt.axhline(y=num_rows_weak+num_rows_medium, color='black', linestyle='--', label='Threshold')
        plt.text(-0.4, num_rows_weak+num_rows_medium-0.05, "Moderate correlation: "+str(round(num_rows_medium*100,2))+"%", color='black', va='center', ha='left')
        plt.fill_between(x=[0.7,1], y1=0, y2=1, color='blue', alpha=0.2, edgecolor='none')
        plt.fill_between(x=[-0.4,0.7], y1=num_rows_weak+num_rows_medium, y2=1, color='blue', alpha=0.2, edgecolor='none')
        plt.text(-0.4, 0.95, "Strong correlation: "+str(round(num_rows_strong*100,2))+"%", color='black', va='center', ha='left')
        plt.xlabel('Pearson correlation')
        plt.ylabel('Fraction of watersheds')
        plt.savefig(path_result+'Recap_coef_pearson_per_wts'+'_'+line_period+'.jpeg', dpi=300, bbox_inches='tight')
        plt.close()
        
        #Figure slope linear regression in function of Pearson correlation
        #all watershed
        plt.scatter(Corr_slope_df['Correlation'],Corr_slope_df['Slope'])
        plt.xlabel('Pearson correlation')
        plt.fill_between(x=[-0.4,0.4], y1=min(Corr_slope_df['Slope'])-0.1, y2=max(Corr_slope_df['Slope'])+0.1, color='red', alpha=0.2,  edgecolor='none')
        plt.fill_between(x=[0.4,0.7], y1=min(Corr_slope_df['Slope'])-0.1, y2=max(Corr_slope_df['Slope'])+0.1, color='green', alpha=0.2, edgecolor='none')
        plt.fill_between(x=[-0.4,min(Corr_slope_df['Correlation'])-0.1], y1=min(Corr_slope_df['Slope'])-0.1, y2=max(Corr_slope_df['Slope'])+0.1, color='green', alpha=0.2, edgecolor='none')
        plt.fill_between(x=[0.7,1], y1=min(Corr_slope_df['Slope'])-0.1, y2=max(Corr_slope_df['Slope'])+0.1, color='blue', alpha=0.2, edgecolor='none')
        plt.ylabel('Linear regression slope')
        plt.savefig(path_result+'Slope_test/Compa_corr_slope'+'_'+line_period+'.jpeg', dpi=300, bbox_inches='tight')
        plt.close()
        #watershed snow-dominated only
        plt.scatter(Corr_slope_df_snow['Correlation'],Corr_slope_df_snow['Slope'])
        plt.xlabel('Pearson correlation')
        plt.ylabel('Linear regression slope')
        plt.fill_between(x=[-0.4,0.4], y1=min(Corr_slope_df_snow['Slope'])-0.1, y2=max(Corr_slope_df_snow['Slope'])+0.1, color='red', alpha=0.2,  edgecolor='none')
        plt.fill_between(x=[0.4,0.7], y1=min(Corr_slope_df_snow['Slope'])-0.1, y2=max(Corr_slope_df_snow['Slope'])+0.1, color='green', alpha=0.2, edgecolor='none')
        plt.fill_between(x=[0.7,1], y1=min(Corr_slope_df_snow['Slope'])-0.1, y2=max(Corr_slope_df_snow['Slope'])+0.1, color='blue', alpha=0.2, edgecolor='none')
        plt.savefig(path_result+'Slope_test/Compa_corr_slope'+'_'+line_period+'_wts_snow.jpeg', dpi=300, bbox_inches='tight')
        plt.close()
        #watershed subsurface-dominated only
        plt.scatter(Corr_slope_df_subsurf['Correlation'],Corr_slope_df_subsurf['Slope'])
        plt.xlabel('Pearson correlation')
        plt.ylabel('Linear regression slope')
        plt.fill_between(x=[-0.4,0.4], y1=min(Corr_slope_df_subsurf['Slope'])-0.1, y2=max(Corr_slope_df_subsurf['Slope'])+0.1, color='red', alpha=0.2,  edgecolor='none')
        plt.fill_between(x=[0.4,0.7], y1=min(Corr_slope_df_subsurf['Slope'])-0.1, y2=max(Corr_slope_df_subsurf['Slope'])+0.1, color='green', alpha=0.2, edgecolor='none')
        plt.fill_between(x=[0.7,1], y1=min(Corr_slope_df_subsurf['Slope'])-0.1, y2=max(Corr_slope_df_subsurf['Slope'])+0.1, color='blue', alpha=0.2, edgecolor='none')
        plt.savefig(path_result+'Slope_test/Compa_corr_slope'+'_'+line_period+'_wts_subsurf.jpeg', dpi=300, bbox_inches='tight')
        plt.close()
        #watershed groundwater-dominated only
        plt.scatter(Corr_slope_df_gwt['Correlation'],Corr_slope_df_gwt['Slope'])
        plt.xlabel('Pearson correlation')
        plt.ylabel('Linear regression slope')
        plt.fill_between(x=[-0.4,0.4], y1=min(Corr_slope_df_gwt['Slope'])-0.1, y2=max(Corr_slope_df_gwt['Slope'])+0.1, color='red', alpha=0.2,  edgecolor='none')
        plt.fill_between(x=[0.4,0.7], y1=min(Corr_slope_df_gwt['Slope'])-0.1, y2=max(Corr_slope_df_gwt['Slope'])+0.1, color='green', alpha=0.2, edgecolor='none')
        plt.fill_between(x=[0.7,1], y1=min(Corr_slope_df_gwt['Slope'])-0.1, y2=max(Corr_slope_df_gwt['Slope'])+0.1, color='blue', alpha=0.2, edgecolor='none')
        plt.savefig(path_result+'Slope_test/Compa_corr_slope'+'_'+line_period+'_wts_gwt.jpeg', dpi=300, bbox_inches='tight')
        plt.close()
        #watershed no snow and model no snow only
        plt.scatter(Corr_slope_df_nosnow_WTS['Correlation'],Corr_slope_df_nosnow_WTS['Slope'])
        plt.xlabel('Pearson correlation')
        plt.ylabel('Linear regression slope')
        plt.fill_between(x=[-0.4,0.4], y1=min(Corr_slope_df_nosnow_WTS['Slope'])-0.1, y2=max(Corr_slope_df_nosnow_WTS['Slope'])+0.1, color='red', alpha=0.2,  edgecolor='none')
        plt.fill_between(x=[0.4,0.7], y1=min(Corr_slope_df_nosnow_WTS['Slope'])-0.1, y2=max(Corr_slope_df_nosnow_WTS['Slope'])+0.1, color='green', alpha=0.2, edgecolor='none')
        plt.fill_between(x=[-0.4,min(Corr_slope_df_nosnow_WTS['Correlation'])-0.1], y1=min(Corr_slope_df_nosnow_WTS['Slope'])-0.1, y2=max(Corr_slope_df_nosnow_WTS['Slope'])+0.1, color='green', alpha=0.2, edgecolor='none')
        plt.fill_between(x=[0.7,1], y1=min(Corr_slope_df_nosnow_WTS['Slope'])-0.1, y2=max(Corr_slope_df_nosnow_WTS['Slope'])+0.1, color='blue', alpha=0.2, edgecolor='none')
        plt.savefig(path_result+'Slope_test/Compa_corr_slope'+'_'+line_period+'_wts_nosnow_WTS_and_mod.jpeg', dpi=300, bbox_inches='tight')
        plt.close()
        
        #Figure Bilinear relationship 
        list_corr_bil_simind_ratparam=sorted(list_corr_bil_simind_ratparam, key=lambda x: (not math.isnan(x), x))
        plt.scatter([range(len(list_corr_bil_simind_ratparam))],list_corr_bil_simind_ratparam)
        plt.title("Bilinear relation with sim. index and parameter")  # Set the title
        plt.savefig(path_result+'Recap_coef_pearson_per_wts'+'_'+line_period+'_'+'_multilinear.jpeg', dpi=300, bbox_inches='tight')
        plt.close()
        slope, intercept = np.polyfit(bilin_coef_a, bilin_coef_b, 1)
        sc=plt.scatter(bilin_coef_a,bilin_coef_b,c=r2_bilin)
        cbar=plt.colorbar(sc, label='R² (multilinear model)')
        cbar.set_label('R² (multilinear model)', rotation=-90, labelpad=15)  
        plt.xlabel("Coef a (sim_index)")
        plt.ylabel("Coef b (nb_param)")
        plt.title("Coef Multilinear linear relation with sim. index and parameter, slope = "+str(round(slope,3)))  # Set the title
        plt.savefig(path_result+'/Multilinear_reg_test/Coef_bilin_a_and_b_model_per_wts'+'_'+line_period+'.jpeg', dpi=300, bbox_inches='tight')
        plt.close()
        with open(path_result + "/Multilinear_reg_test/Multilinear_results_"+line_period+".txt", "w") as f:
            f.write("Multilinear model results\n")
            f.write("======================\n")
            f.write(f"Average abs(Coef a): {np.mean(np.abs(bilin_coef_a))}\n")
            f.write(f"Average abs(Coef b): {np.mean(np.abs(bilin_coef_b))}\n")
        print("Multilin. relationship: Average from abs. Coef a (sim_index): "+str(sum(abs(x) for x in bilin_coef_a) / len(bilin_coef_a)))
        print("Multilin. relationship: Average from abs. Coef b (nb_param): "+str(sum(abs(x) for x in bilin_coef_b) / len(bilin_coef_b)))

        #Figure comparison correlation snow processes
        Compa_snow=pd.DataFrame(Compa_snow).set_index('WTS_list')
        Compa_snow = Compa_snow.sort_values(['Total','With_snow'], ascending=[True, True])
        cmap = ListedColormap(['red', 'green', 'blue'])
        bounds = [-0.4, 0.4, 0.7, 1]
        norm = plt.matplotlib.colors.BoundaryNorm(bounds, cmap.N)
        plt.figure(figsize=(24, 8))
        sns.heatmap(Compa_snow, annot=False, cmap=cmap, norm=norm,
            linewidths=.5, cbar=False) #fmt=".2f",
        plt.title("Watershed Correlation Heatmap (Discrete Colors)")
        plt.savefig(path_result+'Processes_Snow_compa'+'_'+line_period+'.jpeg', dpi=300, bbox_inches='tight')
        plt.close()
        #Figure comparison correlation subsurf processes
        Compa_subsurf=pd.DataFrame(Compa_subsurf).set_index('WTS_list')
        Compa_subsurf = Compa_subsurf.sort_values(['Total','With_subsurf'], ascending=[True, True])
        cmap = ListedColormap(['red', 'green', 'blue'])
        bounds = [-0.4, 0.4, 0.7, 1]
        norm = plt.matplotlib.colors.BoundaryNorm(bounds, cmap.N)
        plt.figure(figsize=(24, 8))
        sns.heatmap(Compa_subsurf, annot=False, cmap=cmap, norm=norm,
            linewidths=.5, cbar=False) #fmt=".2f",
        plt.title("Watershed Correlation Heatmap (Discrete Colors)")
        plt.savefig(path_result+'Processes_subsurf_compa'+'_'+line_period+'.jpeg', dpi=300, bbox_inches='tight')
        plt.close()
        #Figure comparison correlation groundwater processes
        Compa_gwt=pd.DataFrame(Compa_gwt).set_index('WTS_list')
        Compa_gwt = Compa_gwt.sort_values(['Total','With_gwt'], ascending=[True, True])
        cmap = ListedColormap(['red', 'green', 'blue'])
        bounds = [-0.4, 0.4, 0.7, 1]
        norm = plt.matplotlib.colors.BoundaryNorm(bounds, cmap.N)
        plt.figure(figsize=(24, 8))
        sns.heatmap(Compa_gwt, annot=False, cmap=cmap, norm=norm,
            linewidths=.5, cbar=False) #fmt=".2f",
        plt.title("Watershed Correlation Heatmap (Discrete Colors)")
        plt.savefig(path_result+'Processes_gwt_compa'+'_'+line_period+'.jpeg', dpi=300, bbox_inches='tight')
        plt.close()
                
    data_coord_perf.to_csv(path_result+'Corr_coordinate_WTS.csv', index=False, sep=";")
    data_coord_perf_snow.to_csv(path_result+'Corr_coordinate_WTS_snow.csv', index=False, sep=";")
    data_coord_perf_subsurf.to_csv(path_result+'Corr_coordinate_WTS_subsurf.csv', index=False, sep=";")
    data_coord_perf_gwt.to_csv(path_result+'Corr_coordinate_WTS_gwt.csv', index=False, sep=";")
    data_coord_perf_no_snow_wts_and_mod.to_csv(path_result+'Corr_coordinate_WTS_nosnow_WTS_and_mod.csv', index=False, sep=";")


def Plot_per_charact(data_simindex_proc,data_coord_perf_proc,data_coord_perf,line_wts,
                     line_period,list_corr,list_corr_no,r_value_tot,p_value_tot,
                     path_result,list_wts,corrtot_wts,slopetot_wts,slopetot,proc):
    config = {
        "GWT":     ("gwt_proc_mod",     "gwt_mod",     "No_gwt_mod",     "test_wts_gwt"),
        "Snow":    ("snow_proc_mod",    "Snow_mod",    "No_Snow_mod",    "test_wts_snow"),
        "Subsurf": ("subsurf_proc_mod", "subsurf_mod", "No_subsurf_mod", "test_wts_subsurf")
    }
    name_proc, label_with_mod, label_without_mod, adresse = config[proc]

    row_index=data_simindex_proc[(data_simindex_proc['WTS_list'] == line_wts) &
                                      (data_simindex_proc[name_proc] == 1)].index
    x_simindex=data_simindex_proc['sim_index'][row_index]
    y_simindex=data_simindex_proc[line_period][row_index]
    if len(set(x_simindex))>1 and len(set(y_simindex))>1:
        corr_eval = {'x': x_simindex, 'y': y_simindex}
        corr_eval = pd.DataFrame(corr_eval)
        corr_eval = corr_eval.dropna()
        slope, _ , r_value, _ , _  = linregress(corr_eval['x'],corr_eval['y'])
        plt.scatter(x_simindex, y_simindex, c="blue", label=label_with_mod)
        row_index=data_simindex_proc[(data_simindex_proc['WTS_list'] == line_wts) &
                                     (data_simindex_proc[name_proc] == 0)].index
        x_simindex=data_simindex_proc['sim_index'][row_index]
        y_simindex=data_simindex_proc[line_period][row_index]
        if len(set(x_simindex))>1 and len(set(y_simindex))>1:
            list_corr.append(r_value)
            corr_eval = {'x': x_simindex, 'y': y_simindex}
            corr_eval = pd.DataFrame(corr_eval)
            corr_eval = corr_eval.dropna()
            slope, _ , r_valueno, _ , _  = linregress(corr_eval['x'],corr_eval['y'])
            list_corr_no.append(r_valueno)
            plt.scatter(x_simindex, y_simindex, c="red", label=label_without_mod)
            plt.xlabel('Similarity index')
            plt.ylabel('KGE(Q) (modelling performance)')
            plt.title("Correlation tot="+str(round(r_value_tot, 3))+" - p.value="+str(round(p_value_tot, 3)))
            plt.legend()
            plt.savefig(path_result+'Per_WTS/'+adresse+'/Simindex_KGE_'+str(line_wts)+'_'+line_period+'.jpeg', dpi=300, bbox_inches='tight')
            plt.close()
            list_wts.append(line_wts)
            corrtot_wts.append(r_value_tot) 
            slopetot_wts.append(slopetot)
            data_coord_perf_proc.loc[data_coord_perf['gauge_id']==line_wts,'Corr_'+line_period]=r_value_tot
            data_coord_perf_proc.loc[data_coord_perf['gauge_id']==line_wts,'P_Value_'+line_period]=p_value_tot
        else:
            plt.close()