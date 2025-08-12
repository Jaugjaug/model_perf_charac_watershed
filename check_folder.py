# -*- coding: utf-8 -*-
import os

##Check if all needed module are installed
def check_mod():
    try:
        import pandas
        print("module 'pandas' is installed")
    except ModuleNotFoundError:
        print("module 'pandas' is not installed")
    try:
        import seaborn
        print("module 'seaborn' is installed")
    except ModuleNotFoundError:
        print("module 'seaborn' is not installed")
    try:
        import matplotlib
        print("module 'matplotlib' is installed")
    except ModuleNotFoundError:
        print("module 'matplotlib' is not installed")
    try:
        import numpy
        print("module 'numpy' is installed")
    except ModuleNotFoundError:
        print("module 'numpy' is not installed")
    try:
        import ete3
        print("module 'ete3' is installed")
    except ModuleNotFoundError:
        print("module 'ete3' is not installed")   
    try:
        import math
        print("module 'math' is installed")
    except ModuleNotFoundError:
        print("module 'math' is not installed")  
    try:
        import scipy
        print("module 'scipy' is installed")
    except ModuleNotFoundError:
        print("module 'scipy' is not installed")  
    try:
        import sklearn
        print("module 'sklearn' is installed")
    except ModuleNotFoundError:
        print("module 'sklearn' is not installed")  
    try:
        import pathlib
        print("module 'pathlib' is installed")
    except ModuleNotFoundError:
        print("module 'pathlib' is not installed")  
        
##Check existence of all subfolder results and needed input files.
#Global
def Check_Phase_zero():
    path=os.path.dirname(os.getcwd())
    path_input=path+'/Input/'
    if not os.path.isdir(path+'/Result'):
        os.makedirs(path+'/Result')
    path_result=path+'/Result/'

##Check existance folders/input files for Phase 1
def Check_Phase_one():
    path_input=os.path.dirname(os.getcwd())+'/Input/'
    if not os.path.isfile(path_input +"Distance_Knoben_HPD.csv"):
        print("P1 - The file 'Distance_Knoben_HPD.csv' is missing")
    if not os.path.isfile(path_input +"Compa_Eco_HPD.csv"):
        print("P1 - The file 'Compa_Eco_HPD.csv' is missing")
    if not os.path.isfile(path_input +"Compa_Eco_HPD.csv"):
        print("P1 - The file 'Compa_Eco_HPD.csv' is missing")    
    path_result=os.path.dirname(os.getcwd())+'/Result/'
    if not os.path.isdir(path_result+'/Phase_one/Distance_between_watersheds'):
        os.makedirs(path_result+'/Phase_one/Distance_between_watersheds')
    if not os.path.isdir(path_result+'/Phase_one/Density_plot_distance'):
        os.makedirs(path_result+'/Phase_one/Density_plot_distance')

def Check_Phase_two():
    path_result=os.path.dirname(os.getcwd())+'/Result/'
    if not os.path.isdir(path_result+'/Phase_two/Density_plot_distance'):
        os.makedirs(path_result+'/Phase_two/Density_plot_distance')
    if not os.path.isdir(path_result+'/Phase_two/Synthesis'):
        os.makedirs(path_result+'/Phase_two/Synthesis')
    if not os.path.isdir(path_result+'/Phase_two/Association'):
        os.makedirs(path_result+'/Phase_two/Association')
        
def Check_Phase_three():
    path_input=os.path.dirname(os.getcwd())+'/Input/'
    if not os.path.isfile(path_input +"Caracteristic_Models.csv"):
        print("P3 - The file 'Caracteristic_Models.csv' is missing") 
    path_result=os.path.dirname(os.getcwd())+'/Result/'
    if not os.path.isdir(path_result+'/Phase_three/Tree_creat'):
        os.makedirs(path_result+'/Phase_three/Tree_creat')  
    if not os.path.isdir(path_result+'/Phase_three/Tree_compa'):
        os.makedirs(path_result+'/Phase_three/Tree_compa')  

def Check_Phase_four():
    path_result=os.path.dirname(os.getcwd())+'/Result/'
    if not os.path.isdir(path_result+'/Phase_four/KGE_comparison'):
        os.makedirs(path_result+'/Phase_four/KGE_comparison')    
    if not os.path.isdir(path_result+'/Phase_four/KGE_comparison/Total'):
        os.makedirs(path_result+'/Phase_four/KGE_comparison/Total')   
    if not os.path.isdir(path_result+'/Phase_four/KGE_comparison/Per_Model'):
        os.makedirs(path_result+'/Phase_four/KGE_comparison/Per_Model')   
    if not os.path.isdir(path_result+'/Phase_four/KGE_comparison/Per_WTS'):
        os.makedirs(path_result+'/Phase_four/KGE_comparison/Per_WTS')   

def Check_Phase_five():
    path_result=os.path.dirname(os.getcwd())+'/Result/'
    if not os.path.isdir(path_result+'/Phase_five/Corr_properties_WTS'):
        os.makedirs(path_result+'/Phase_five/Corr_properties_WTS')  
    if not os.path.isdir(path_result+'/Phase_five/heatmap_charact_WTS'):
        os.makedirs(path_result+'/Phase_five/heatmap_charact_WTS')  