# OVERVIEW:

This program generates an excel sheet for the production, production price, consumption, con
sumption price, pipeline capacity, and pipeline flow for the United States, Canada, Mexico, 
and Rest of the World. These statistics are generated per defined region in each country, an
d for a defined range of years (limited between 2015-2050). Each statistic is calculated off
a formal model or derived model. This program uses csv readers to read from excels and CSVs
and pandas to write to excels.

# IMPORTANT TO-DO:

Download all excels and CSVs in 'Include/Files to Download'
Edit fields in Arrays.py to change outputs and match information in 'Include/Files to Downlo
ad'

# STRUCTURE:

* Do not edit any files other than Arrays.py

# Include/All
* Excel Files/CSVs of data to be included in these models. In the Include file there is an 'All Files' word document that details how to obtain these Excel Files/CSVs and what should be changed in these data files.

# Prod_Cons_Flow_Cap.py
* Main file that is run during the program. This inherits from all other files. Functions written in other files are included and executed here

# Prod_Cons_Flow_Cap.exe
* Executable version of above

# Arrays.py
* All .py files inherit from this
* Data from Excels and CSVs are stored in dictionaries here. Generally, nested dictionaries of the form dict_name[Producion Statistic/Consumption Sector][Region][Year] are used to store the data. Nested dictionaries of the form dict_name[Region From][Region To][Year] are used for pipes. Only edit the sections outlined that can be edited
* Metadata (Regions, Years, Sectors) are stored as 1D Arrays
* dict_name is usually (country)_(prod/cons)_([price])_([raw]), such as usa_prod_rawfor US raw production data or can_cons_price for CAN final consumption price data
* Lookup Dictionaries are nested dictionaries that return acronyms from full names andvice versa.
* Keywords are specific words within excel document that must be correctly supplied inorder for the program to read the correct data.
* The phrase (For 'FileName') is written beside some keywords or array. The keyword isto help read data from FileName (Most likely the keyword can be found on the left columns)
* Canadian provinces form Canadian regions, US States form US Regions, and Mexican cities belong to Mexican regions.

# Functions.py
* General functions used throughout the program. This file inherits Arrays.py and is inherited by all other files.
* Funtions exist to generate absolute file paths, convert excels to CSVs, obtain year data from files, aggregate model data, write final data, style excel sheets, and convert units.

# CAN_Functions.py, USA_Functions.py, MEX_Functions.py, ROW_Functions.py
* These files inherit from Functions.py and Arrays.py and are inerited by Prod_Cons_Flow_Cap.py.
* Each file generates model data for production, consumption, production price, and consumption price of each region (each process written as a function). Some processesare split between functions (such as prod_1, prod_2, prod_3)

# Pip_Cap_Functions.py
* This file inherits from Functions.py and Arrays.py and is inherited by Prod_Cons_Flow_Cap.py
* Generates Pipeline Capacity data and Pipeline Flow data between regions. Some processes are split between functions.

# Regressions
* CostLinReg looks at past pipeline cost, length, and flow data to create a linear regression model for (cost/capacity)/length. Exponents for each variable were optimizedwith cross validation. Coefficients of best fit model are used in StateRegressions
* StateRegressions pulls coordinate data for the most populous cities in each state, Canadian province, and Mexican region parsed from Wikipedia. Coordinates are pulled using Geopy. Distances between states are calcualted pairwise between coordinates with Geopy as well. Results from CostLinReg are used to predict (Cost/Capacity)/Mile ofpotential pipeline between pairs of states. An investment model is later run to predict the annual investment cost of the pipelines as well.
