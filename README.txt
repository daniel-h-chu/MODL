OVERVIEW:

This program generates an excel sheet for the production, production price, consumption, con
sumption price, pipeline capacity, and pipeline flow for the United States, Canada, Mexico, 
and Rest of the World. These statistics are generated per defined region in each country, an
d for a defined range of years (limited between 2015-2050). Each statistic is calculated off
a formal model or derived model. This program uses csv readers to read from excels and CSVs
and pandas to write to excels.

IMPORTANT TO-DO:

Download all excels and CSVs in 'Include/Files to Download'
Edit fields in Arrays.py to change outputs and match information in 'Include/Files to Downlo
ad'

STRUCTURE:

 * Do not edit any files other than Arrays.py

Include/All
      - Excel Files/CSVs of data to be included in these models. In the Include file there i
	s an 'All Files' word document that details how to obtain these Excel Files/CSVs and
	what should be changed in these data files.

Prod_Cons_Flow_Cap.py
      - Main file that is run during the program. This inherits from all other files. Functi
	ons written in other files are included and executed here
	
Prod_Cons_Flow_Cap.exe
      - Executable version of above

Arrays.py
      - All .py files inherit from this
      - Data from Excels and CSVs are stored in dictionaries here. Generally, nested diction
	aries of the form dict_name[Producion Statistic/Consumption Sector][Region][Year] ar
	e used to store the data. Nested dictionaries of the form dict_name[Region From][Reg
	ion To][Year] are used for pipes. Only edit the sections outlined that can be edited
      - Metadata (Regions, Years, Sectors) are stored as 1D Arrays
      - dict_name is usually (country)_(prod/cons)_([price])_([raw]), such as usa_prod_raw
	for US raw production data or can_cons_price for CAN final consumption price data
      -	Lookup Dictionaries are nested dictionaries that return acronyms from full names and
	vice versa.
      - Keywords are specific words within excel document that must be correctly supplied in
	order for the program to read the correct data.
      - For some field, I wrote (For 'FileName') beside a keyword or array. The keyword is
	to help read data from FileName (Most likely the keyword can be found on the left co
	lumns)

Functions.py
      - General functions used throughout the program. This file inherits Arrays.py and is i
	nherited by all other files.
      - Funtions exist to generate absolute file paths, convert excels to CSVs, obtain year 
	data from files, aggregate model data, write final data, style excel sheets, and con
	vert units.

CAN_Functions.py, USA_Functions.py, MEX_Functions.py, ROW_Functions.py
      - These files inherit from Functions.py and Arrays.py and are inerited by Prod_Cons_Fl
	ow_Cap.py.
      - Each file generates model data for production, consumption, production price, and co
	nsumption price of each region (each process written as a function). Some processes
	are split between functions (such as prod_1, prod_2, prod_3)

Pip_Cap_Functions.py
      - This file inherits from Functions.py and Arrays.py and is inherited by Prod_Cons_Flo
	w_Cap.py
      - Generates Pipeline Capacity data and Pipeline Flow data between regions. Some proces
	ses are split between functions.