# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 13:00:19 2025

@author: Julien Augas
"""

import os 
import check_folder

#Parameters
distance=450562 #meters (distance between a watershed forom HPD what is only at the same ecoregion lvl2 than a watershed of CAMELS/Knoben)
limit_KGE=-5 #limit inferior for KGE conserved in the sample 


#0 - Creation Result forler + check if all needed library are installed
import check_folder
check_folder.check_mod()
check_folder.Check_Phase_zero()

#1 - Analysis of the distance between the watersheds where modeling performances were evaluated by Knoben et al. (2020) and the watersheds where hydrological processes were identified (summarized by McMillan et al. (2022)). They are categorized, based on the level of ecoregion where both watershed belong. 
check_folder.Check_Phase_one()
import Phase_one
input_d = os.path.dirname(os.getcwd())+'/Input/'
result_d = os.path.dirname(os.getcwd())+'/Result/Phase_one/Distance_between_watersheds'
Phase_one.Distance_between_watersheds(input_d,result_d)

#2 - Based on the threshold determined by the user, on the distance between 2 watershed that belong on the same ecoregion level2, and by considering all the watershed that belong on the same ecoregion level3, the processes identified on the watersheds from the article of McMillan et al. (2022) are spread to their associated watersheds from Knoben et al. (2020).
check_folder.Check_Phase_two()
import Phase_two
input_d = os.path.dirname(os.getcwd())+'/Input/'
result_d = os.path.dirname(os.getcwd())+'/Result/Phase_two/Synthesis'
Phase_two.Synthesis_Combination_watershed_HPD_Knoben(distance,input_d,result_d)
result_d = os.path.dirname(os.getcwd())+'/Result/Phase_two/Association'
Phase_two.Association_Phenom_BV_Knoben_HPD(input_d,result_d)
input_d = os.path.dirname(os.getcwd())+'/Result/Phase_two/Association/'
result_d = os.path.dirname(os.getcwd())+'/Result/Phase_two/Density_plot_distance/'
Phase_two.Density_plot_distance(input_d,result_d)

#3 - For each combination of watershed/model, the value of their similariy index is evaluated.
check_folder.Check_Phase_three()
import Phase_three
result_d = os.path.dirname(os.getcwd())+'/Result/Phase_three/Tree_creat/'
input_d = os.path.dirname(os.getcwd())+'/Input/'
Phase_three.Tree_creation(input_d,input_d,result_d,'model') #For models
input_d2 = os.path.dirname(os.getcwd())+'/Result/Phase_two/Synthesis/'
Phase_three.Tree_creation(input_d,input_d2,result_d,'WTS') #For watershed
result_d = os.path.dirname(os.getcwd())+'/Result/Phase_three/Tree_compa/'
input_d = os.path.dirname(os.getcwd())+'/Input/'
input_d_3 = os.path.dirname(os.getcwd())+'/Result/Phase_three/Tree_creat/'
Phase_three.Tree_comparison(input_d,input_d_3,result_d) 

#4 - The hydrological modeling performances are compared with their similarity indexes, for each watershed.
check_folder.Check_Phase_four()
import Phase_four
input_d = os.path.dirname(os.getcwd())+'/Input/'
input_d_2 = os.path.dirname(os.getcwd())+'/Result/Phase_three/Tree_compa/'
result_d = os.path.dirname(os.getcwd())+'/Result/Phase_four/KGE_comparison/'
Phase_four.Perf_comparison(input_d,input_d_2,result_d,limit_KGE) 

#5 - The correlations of the different relation evaluated on the point 4 are compared with the characteristics of the watersheds, provided by the CAMELS dataset.
check_folder.Check_Phase_five()
import Phase_five
input_d = os.path.dirname(os.getcwd())+'/Input/'
input_d_2 = os.path.dirname(os.getcwd())+'/Result/Phase_four/KGE_comparison/'
result_d = os.path.dirname(os.getcwd())+'/Result/Phase_five/Corr_properties_WTS/'
Phase_five.Corr_properties_WTS(input_d,input_d_2,result_d) 
input_d_3 = os.path.dirname(os.getcwd())+'/Result/Phase_five/Corr_properties_WTS/'
result_d = os.path.dirname(os.getcwd())+'/Result/Phase_five/heatmap_charact_WTS/'
Phase_five.Heatmap_charact_WTS(input_d,input_d_2,input_d_3,result_d) 
