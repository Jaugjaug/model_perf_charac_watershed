# model_perf_charac_watershed
Code for analyzing data for the article from Augas and McMillan (2025?)

The topic of this article is about to compare the structure of conceptual hydrological models with their hydrological performance. The influence of the phenomena modeled by models on their performance is also compared with characteristics of watersheds.

Features:
The code is composed by 5 phases:
1 - Analysis of the distance between the watersheds where modeling performances were evaluated by Knoben et al. (2020) and the watersheds where hydrological processes were identified ('HPD', summarized by McMillan et al. (2022)). They are categorized, based on the level of ecoregion where both watershed belong. 
2 - Based on the threshold determined by the user, on the distance between 2 watershed that belong on the same ecoregion level2, and by considering all the watershed that belong on the same ecoregion level3, the processes identified on the watersheds from the article of McMillan et al. (2022) are spread to their associated watersheds from Knoben et al. (2020).
3 - For each combination of watershed/model, the value of their similariy index is evaluated.
4 - The hydrological modeling performances are compared with their similarity indexes, for each watershed.
5 - The correlations of the different relation evaluated on the point 4 are compared with the characteristics of the watersheds, provided by the CAMELS dataset.

Prerequisites:
- List of libraries needed: pandas, seaborn, matplotlib, numpy, ete3, math, scipy, sklearn, pathlib
- Creation of "Input" folder
- Input files: 
	- ID of models
	- Amount of parameter for each model
	- List of phenomena considered for each models
	- ID of watersheds from Knoben's dataset
	- Localization of watersheds from Knoben's dataset
	- Ecoregion (level 1, 2 and 3 for watershed from Knoben 's dataset)
	- Ecoregion (level 1, 2 and 3 for watershed from HPD database)
	- Distance between each combination of watershed from Knoben's dataset and from HPD database
	- Performance for each model on each watershed (Calibration and Evaluation periods)
	- Characteristics from CAMELS dataset

License:
MIT License

Authors and Acknowledgments:
Julien Augas, SDSU
Hllary McMillan, SDSU

References:
- Environmental Protection Agency. 2010. “Ecoregions of North America.” https://www.epa.gov/eco-research/ecoregions-north-america.
- Knoben, W.J.M., Freer, J.E., Peel, M.C., Fowler, K.J.A., Woods, R.A., 2020. A Brief Analysis of Conceptual Model Structure Uncertainty Using 36 Models and 559 Catchments. Water Resources Research 56, e2019WR025975. https://doi.org/10.1029/2019WR025975
- McMillan, H., 2022. A taxonomy of hydrological processes and watershed function. Hydrological Processes 36, e14537. https://doi.org/10.1002/hyp.14537




