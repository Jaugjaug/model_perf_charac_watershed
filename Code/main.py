# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 13:00:19 2025

@author: Julien Augas
"""
#need to use Python version 3.12 or earlier where cgi is still included.

import os 
import check_folder

#Parameters
distance=450562 #meters (distance between a watershed forom HPD what is only at the same ecoregion lvl2 than a watershed of CAMELS/Knoben)
limit_KGE=-5 #limit inferior for KGE conserved in the sample 
containt_lvl2_exc = True ##If True, does not consider ecoregion lvl2 if presence of watershed in ecoregion lvl3  
includeLVL2=True ##Include watershed in same ecoregion lvl2 but that are not in the same ecoregion lvl3?
adress_input = os.path.dirname(os.getcwd())+'/Input/'
adress_phaseone =os.path.dirname(os.getcwd())+'/Result/Phase_one/'
adress_phasetwo =os.path.dirname(os.getcwd())+'/Result/Phase_two/'
adress_phasethree =os.path.dirname(os.getcwd())+'/Result/Phase_three/'
adress_phasefour =os.path.dirname(os.getcwd())+'/Result/Phase_four/'
adress_phasefive =os.path.dirname(os.getcwd())+'/Result/Phase_five/'


#0 - Creation Result forler + check if all needed library are installed
import check_folder
check_folder.check_mod()
check_folder.Check_Phase_zero()

#1 - Analysis of the distance between the watersheds where modeling performances were evaluated by Knoben et al. (2020) and the watersheds where hydrological processes were identified (summarized by McMillan et al. (2022)). They are categorized, based on the level of ecoregion where both watershed belong. 
check_folder.Check_Phase_one()
import Phase_one
Phase_one.Distance_between_watersheds(adress_input,adress_phaseone+'Distance_between_watersheds/')

#2 - Based on the threshold determined by the user, on the distance between 2 watershed that belong on the same ecoregion level2, and by considering all the watershed that belong on the same ecoregion level3, the processes identified on the watersheds from the article of McMillan et al. (2022) are spread to their associated watersheds from Knoben et al. (2020).
check_folder.Check_Phase_two()
import Phase_two
Phase_two.Synthesis_Combination_watershed_HPD_Knoben(includeLVL2,
                                                     distance,
                                                     containt_lvl2_exc,
                                                     adress_input,
                                                     adress_phasetwo+'Synthesis/')
Phase_two.Association_Phenom_BV_Knoben_HPD(adress_input,
                                           adress_phasetwo+'Association/')
Phase_two.Density_plot_distance(adress_phasetwo+'Association/',
                                adress_phasetwo+'Density_plot_distance/')

#3 - For each combination of watershed/model, the value of their similariy index is evaluated.
check_folder.Check_Phase_three()
import Phase_three
Phase_three.Tree_creation(adress_input,
                          adress_input+'Model_Data/',
                          adress_phasethree+'Tree_creat/',
                          'model') #For models
Phase_three.Tree_creation(adress_input,
                          adress_phasetwo+'Synthesis/',
                          adress_phasethree+'Tree_creat/',
                          'WTS') #For watershed
Phase_three.Tree_comparison(adress_input,
                            adress_phasethree+'Tree_creat/',
                            adress_phasethree+'Tree_compa/') 
Phase_three.Tree_model_watershed(adress_phasethree+'Tree_creat/',
                                 adress_phasethree+'Tree_compa_graph/') #For watershed

#4 - The hydrological modeling performances are compared with their similarity indexes, for each watershed.
check_folder.Check_Phase_four()
import Phase_four
Phase_four.Perf_comparison(adress_input,
                           adress_phasethree+'Tree_compa/',
                           adress_phasefour+'KGE_comparison/',
                           limit_KGE) 

#5 - The correlations of the different relation evaluated on the point 4 are compared with the characteristics of the watersheds, provided by the CAMELS dataset.
check_folder.Check_Phase_five()
import Phase_five
Phase_five.Corr_properties_WTS(adress_input,
                               adress_phasefour+'KGE_comparison/',
                               adress_phasefive+'Corr_properties_WTS/') 
Phase_five.Heatmap_charact_WTS(adress_input,
                               adress_phasefour+'KGE_comparison/',
                               adress_phasefive+'Corr_properties_WTS/',
                               adress_phasefive+'heatmap_charact_WTS/') 
