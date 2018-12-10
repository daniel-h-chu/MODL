# Arrays is the base file of this program. Arrays stores all arrays and dictionaries used by all functions
########################################################################################################################
########################################################################################################################
########################################################################################################################

########################################################################################################################
# All (Things that can be changed) #####################################################################################
########################################################################################################################

# Consumption Sectors
cons_sectors = ['All Sectors', 'Residential', 'Commercial', 'Industrial', 'Transportation', 'Electric Power']
# Acronyms of Production Stats
prod_stats_acronyms = ['ONS', 'OFS', 'Total']
# Years to be calculated
years = [year for year in range(2015, 2051)]

# Custom Data ##########################################################################################################

# Alaska Consumption 2015 from NG_CONS_SUM_DCU_SAK_A (Same order as cons_sectors)
usa_cons_als = [333602, 18574, 18472, 4864 + 223246 + 37615 + 615, 10, 30207]
# Alaska Consumption Prices (Same order as cons_sectors)
usa_cons_price_als = [0, 9.81, 8.34, 5.06, 15.71, 6.65]
# Consumption Prices [0, E28, I28, M28, E28, M28] from mex_consumption_price or [0, Avg Residential Public Price, Avg
# Commercial Public Price, Avg Industrial Public Price, Avg Residential Public Price, Avg Industrial Public Price]
mex_cons_price_raw = [0, 9.73, 5.34, 4.02, 9.73, 4.02]

# US Geography #########################################################################################################

# Full names of NEMS regions
nems_regions_full = ['East', 'Gulf Coast', 'Midcontinent', 'Southwest', 'Dakotas/Rocky Mountains', 'West Coast',
                     'Alaska']
# Acronyms of NEMS regions (In same order as above)
nems_regions_acronyms = ['NES', 'NGC', 'NMC', 'NSW', 'NRM', 'NWC', 'NAH']
# Full names of NANGAM regions
nangam_regions_full = ['Alaska & Hawaii', 'Gulf of Mexico', 'Pacific', 'Mountain', 'West North Central',
                       'East North Central', 'West South Central', 'East South Central', 'Middle Atlantic',
                       'South Atlantic', 'New England']
# Acronyms of NANGAM regions
nangam_regions_acronyms = ['AHW', 'GOM', 'PCF', 'MNT', 'WNC', 'ENC', 'WSC', 'ESC', 'MAT', 'SAT', 'NEN']
# Full names of US States
usa_states_full = ['Gulf of Mexico', 'Gulf of Mexico - Deepwater', 'Alabama', 'Alaska', 'Arizona', 'Arkansas',
                   'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia',
                   'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',  'Kansas', 'Kentucky', 'Louisiana', 'Maine',
                   'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana',
                   'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina',
                   'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
                   'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
                   'West Virginia', 'Wisconsin', 'Wyoming']
# Acronyms of US States (In same order as above)
usa_states_acronyms = ['GOM', 'GMD', 'ALB', 'ALS', 'ARZ', 'ARK', 'CAL', 'COL', 'CON', 'DEL', 'WDC', 'FLR', 'GRG', 'HWI',
                       'IDH', 'ILN', 'IND', 'IOW', 'KNS', 'KNT', 'LSN', 'MAN', 'MAR', 'MAS', 'MCH', 'MNS', 'MSI', 'MSU',
                       'MON', 'NBR', 'NVD', 'NHM', 'NJS', 'NMX', 'NYK', 'NCL', 'NDK', 'OHO', 'OKL', 'ORG', 'PEN', 'RIL',
                       'SCL', 'SDK', 'TNS', 'TEX', 'UTH', 'VMT', 'VGN', 'WAS', 'WVG', 'WIS', 'WYO']
# Acronyms of states per NANGAM region
states_to_regions = {
    'AHW': ['ALS', 'HWI'],
    'GOM': ['GOM', 'GMD'],
    'PCF': ['CAL', 'ORG', 'WAS'],
    'MNT': ['ARZ', 'COL', 'IDH', 'MON', 'NVD', 'NMX', 'UTH', 'WYO'],
    'WNC': ['IOW', 'KNS', 'MNS', 'NBR', 'NDK', 'SDK'],
    'ENC': ['ILN', 'IND', 'MCH', 'OHO', 'WIS'],
    'WSC': ['ARK', 'LSN', 'MSU', 'OKL', 'TEX'],
    'ESC': ['ALB', 'KNT', 'MSI', 'TNS'],
    'MAT': ['NJS', 'NYK', 'PEN'],
    'SAT': ['DEL', 'WDC', 'FLR', 'GRG', 'MAR', 'NCL', 'SCL', 'VGN', 'WVG'],
    'NEN': ['CON', 'MAN', 'MAS', 'NHM', 'RIL', 'VMT']
}

# Canada Geography #####################################################################################################

canadian_provinces_full = ['Newfoundland and Labrador', 'Prince Edward Island', 'Nova Scotia', 'New Brunswick',
                           'Quebec', 'Ontario', 'Manitoba', 'Alberta', 'British Columbia', 'Saskatchewan',
                           'Yukon', 'Northwest Territories', 'Nunavut']
# Acronyms of Canadian Provinces (In same order as above)
canadian_provinces_acronyms = ['NLL', 'PEI', 'NSC', 'NBW', 'QBC', 'ONT', 'MTB', 'ABR', 'BCL', 'SAS', 'YKN', 'NWT', 'NUN'
                               ]
# Full names of Canadian regions
canadian_regions_full = ['Canada East', 'Canada West']
# Acronyms of Canadian regions
canadian_regions_acronyms = ['CAE', 'CAW']
# Regions Defined by Provinces
provinces_to_regions = {
    'CAE': ['NLL', 'PEI', 'NSC', 'NBW', 'QBC', 'ONT'],
    'CAW': ['MTB', 'ABR', 'BCL', 'SAS', 'YKN', 'NWT', 'NUN']
}

# Mexico Geography #####################################################################################################

# Full names of Mexican Regions
mex_regions_full = ['Mexico North West', 'Mexico North East', 'Mexico Interior West', 'Mexico Interior',
                    'Mexico South West']
# Acronyms of Mexican Regions (In same order as above)
mex_regions_acronyms = ['MNW', 'MNE', 'MIW', 'MIN', 'MSW']
# Mexican cities per NANGAM region (For st2st)
cities_to_regions = {
    'MNW': ['Sonora', 'Chihuahua', 'Baja California', 'Baja Calif. Norte'],
    'MNE': ['Tamaulipas', 'Reynosa', 'Mexico', 'Coahuila'],
    'MIW': ['Rio Grande'],
    'MIN': [],
    'MSW': []
}

# Rest of World Geography ##############################################################################################

# Full names of Rest of World Regions
row_regions_full = ['Rest of World']
# Acronyms of Rest of World Regions
row_regions_acronyms = ['ROW']

########################################################################################################################
# All (Misc. Consult the Data before Changing) #########################################################################
########################################################################################################################

# United States ########################################################################################################

usa_prod_split = 'Supply Prices'  # Statistic Keyword for Price
resource = "Natural Gas"  # Resource Keyword
gasoline = "Gasoline"  # Gasoline Keyword

# Full Names of US Production Stats Keywords (Same order as Production Stats)
usa_prod_stats_full = ['Lower 48 Onshore', 'Lower 48 Offshore', 'Lower 48 Combined']
# USA Production price stats to be calculated Keywords (Should be same as production stats)
usa_prod_price_stats = ['Lower 48 Onshore Price', 'Lower 48 Offshore Price', 'Lower 48 Offshore Price Combined']

# Canada ###############################################################################################################

# US NANGAM regions used for consumption price calculations
can_cons_nangam_regions = ['PCF', 'MNT', 'WNC', 'ENC', 'NEN']

# Mexico ###############################################################################################################

production = "Production"  # Production Keyword

# Consumption Sectors (Same order as Consumption Sectors)
mex_cons_sectors = ['Consumption', 'Residential Sector', 'Commercial Sector', 'Industrial Sector',
                    'Transportation Sector', 'Electric Sector']

# Rest of World ########################################################################################################

total_world = 'Total World'  # Total World Keyword
united_states = 'United States'  # US Keyword
canada = 'Canada'  # Canada Keyword
mexico = 'Mexico'  # Mexico Keyword
all_sectors = 'All Sectors'  # All Sectors Keyword

# Piping Capacity ######################################################################################################

region_from = 'Region From'  # Region From Keyword ()
region_to = 'Region To'  # Region To Keyword
state_from = 'State From'  # State From Keyword (For st2st)
state_to = 'State To'  # State To Keyword (For st2st)
county_from = 'County From'  # County From Keyword (For st2st Mexican Pipes)
county_to = 'County To'  # County To Keyword (For st2st Mexican Pipes)
capacity_mmcfd = 'Capacity (mmcfd)'  # Capacity MMCFD Keyword (For st2st Capacity)
capacity_mex_bcfd = 'Average Volume MMCF/day)'  # Capacity MMCF Keyword (For mex_pip_cap_mmcfd)
capacity_can_bcfd = 'Average annual Capacity (BCF/day)'  # Capacity BCFD Keyword (For can_pip_cap)
capacity_year = 'year'  # Capacity Year Keyword (For st2st)
operating = 'Operating'  # Operating Keyword (For mex_pip_cap_mmcfd)
status = 'Status'  # Status Keyword (For mex_pip_cap_mmcfd)

# Piping Flow ##########################################################################################################

r_into = 'Into '  # Into Keyword (For Primary_Natural_Gas_Flows_Entering_NGTDM_Region_from_Neighboring_Regions)
r_from = ' From:'  # From Keyword (For Primary_Natural_Gas_Flows_Entering_NGTDM_Region_from_Neighboring_Regions)
usa_to_can = 'Pipeline Exports to Canada'  # USA to CAN Pipe Exports (For Natural_Gas_Imports_and_Exports)
can_to_can = 'Average annual flows (BCF/day)'  # CAN to CAN Pipe Flow (For can_pip_cap)
imports = 'Imports'  # MEX Imports Keyword (For reg_bal_mex)
exports = 'Exports'  # MEX Exports Keyword (For reg_bal_mex)

# Aggregate Printing ###################################################################################################

prod_stats_print = ['Onshore', 'Offshore', 'Total']  # Production Statistics to be Printed on Excel Sheet
cons_sectors_print = ['Total Consumption', 'Residential Sector', 'Commercial Sector', 'Industrial Sector',
                      'Transportation Sector', 'Electric Sector']  # Consumption Sectors to be Printed on Excel Sheet

########################################################################################################################
########################################################################################################################
########################################################################################################################
# All Regions ##########################################################################################################

# Full Name All Regions
all_regions_full = mex_regions_full + canadian_regions_full + nangam_regions_full + row_regions_full
# Acronyms All Region
all_regions_acronyms = mex_regions_acronyms + canadian_regions_acronyms + nangam_regions_acronyms + row_regions_acronyms


# Create Dictionary Functions ##########################################################################################

# Creates a dictionary based on a list of parameters ex. d = create_dict([nangam_regions_acronyms, years]) allows for
# access with d['NEN'][2023]

def create_dict(params):
    dictionary = dict.fromkeys(params[0])
    if len(params) > 1:
        for key in dictionary:
            dictionary[key] = create_dict(params[1:])
        return dictionary
    else:
        for key in dictionary:
            dictionary[key] = 0
        return dictionary


# Creates a dictionary to look up matching values ex. d = create_lookup_dict([nangam_regions_acronyms,
# nangam_regions_full]) allows for d['NEN'] to return 'New England'

def create_lookup_dict(param1, param2):
    dictionary = dict.fromkeys(param1)
    for index, p1 in enumerate(param1):
        dictionary[p1] = param2[index]
    return dictionary


# Lookup Dictionaries ##################################################################################################

nems_dict = create_lookup_dict(nems_regions_full, nems_regions_acronyms)  # NEMS Full to NEMS Acronyms
nangam_dict = create_lookup_dict(nangam_regions_full, nangam_regions_acronyms)  # NANGAM Full to NANGAM Acronyms
price_dict = create_lookup_dict(usa_prod_price_stats, usa_prod_stats_full)  # Price to Stat Full
stat_dict = create_lookup_dict(usa_prod_stats_full, prod_stats_acronyms)  # Stat Full to Stat Acronyms
stat_price_dict = create_lookup_dict(usa_prod_price_stats, prod_stats_acronyms)  # Stat Full to Stat Acronyms
provinces_dict = create_lookup_dict(canadian_provinces_full, canadian_provinces_acronyms)  # Prov Full to Prov Acronyms
mex_cons_price_dict = create_lookup_dict(cons_sectors, mex_cons_price_raw)  # Cons Price Raw Data to ConsPrice Dict
mex_cons_dict = create_lookup_dict(mex_cons_sectors, cons_sectors)  # MEX Consumption Sectors to All Consumption Sectors
print_full_dict = create_lookup_dict(all_regions_acronyms, all_regions_full)  # Acronyms to Full All Regions
reverse_full_dict = create_lookup_dict(all_regions_full, all_regions_acronyms)  # Full to Acronyms All Regions
states_dict = create_lookup_dict(usa_states_full, usa_states_acronyms)  # State Full to State Acronyms
stat_print_dict = create_lookup_dict(prod_stats_acronyms, prod_stats_print)  # Stat Acronym to Stat Printed
sector_print_dict = create_lookup_dict(cons_sectors, cons_sectors_print)  # Sector Acronym to Sector Printed
print_dict = stat_print_dict.copy()  # Sector/Stat Acronym to Sector/Stat Printed
print_dict.update(sector_print_dict)

# United States ########################################################################################################

nem_to_nan = create_dict([prod_stats_acronyms, nangam_regions_acronyms, nems_regions_acronyms])  # NEMS to NANGAM Matrix
usa_prod_raw = create_dict([prod_stats_acronyms, nems_regions_acronyms, years])  # Production Raw Data
usa_prod = create_dict([prod_stats_acronyms, nangam_regions_acronyms, years])  # USA Production
usa_prod_price_raw = create_dict([prod_stats_acronyms, nems_regions_acronyms, years])  # USA Production Price Raw Data
usa_prod_price_value = create_dict([prod_stats_acronyms, nems_regions_acronyms, years])  # USA Production Price Value
usa_prod_price = create_dict([prod_stats_acronyms, nangam_regions_acronyms, years])  # USA Production Price
usa_cons = create_dict([cons_sectors, nangam_regions_acronyms, years])  # USA Consumption
usa_cons_total = create_dict([years])  # USA Consumption Total to calculate Alaska and Hawaii Consumption
usa_cons_price = create_dict([cons_sectors, nangam_regions_acronyms, years])  # USA Consumption Price

# Canada ###############################################################################################################

can_prod_raw = create_dict([prod_stats_acronyms, canadian_provinces_acronyms, years])  # CAN Production Raw Data
can_prod = create_dict([prod_stats_acronyms, canadian_regions_acronyms, years])  # CAN Production
can_prod_price = create_dict([prod_stats_acronyms, canadian_regions_acronyms, years])  # CAN Production Price
can_pop_ratio_raw = create_dict([canadian_provinces_acronyms])  # CAN Population Ratio Raw Data
can_pop_ratio = create_dict([canadian_regions_acronyms])  # CAN Population Ratio
can_cons = create_dict([cons_sectors, canadian_regions_acronyms, years])  # CAN Consumption
can_cons_eng_dem = create_dict([years])  # CAN Energy Consumption
can_elc_gen_ratio_raw = create_dict([canadian_provinces_acronyms, years])  # CAN Electricity Generation Raw Data
can_elc_gen_ratio = create_dict([canadian_regions_acronyms, years])  # CAN Electricity Generation
can_cons_price = create_dict([cons_sectors, canadian_regions_acronyms, years])  # CAN ConsumptionPrice

# Mexico ###############################################################################################################

mex_prod = create_dict([prod_stats_acronyms, mex_regions_acronyms, years])  # MEX Production
mex_prod_price = create_dict([prod_stats_acronyms, mex_regions_acronyms, years])  # MEX Production Price
mex_cons = create_dict([cons_sectors, mex_regions_acronyms, years])  # MEX Consumption
mex_cons_price = create_dict([cons_sectors, mex_regions_acronyms, years])  # MEX Consumption Price

# Rest of World ########################################################################################################

row_prod = create_dict([prod_stats_acronyms, row_regions_acronyms, years])  # ROW Production
row_prod_price = create_dict([prod_stats_acronyms, row_regions_acronyms, years])  # ROW Production Price
row_cons = create_dict([cons_sectors, row_regions_acronyms, years])  # ROW Consumption
row_cons_ratio = create_dict([row_regions_acronyms, years])  # ROW Consumption to Total World Consumption
row_cons_price = create_dict([cons_sectors, row_regions_acronyms, years])  # ROW Consumption Price

# Pipe Flow and Capacity ###############################################################################################

pip_cap = create_dict([all_regions_acronyms, all_regions_acronyms])  # Pipe Capacity
pip_flow = create_dict([all_regions_acronyms, all_regions_acronyms, years])  # Pipe Flow
mex_to_usa_dict = create_dict([mex_regions_acronyms, nangam_regions_acronyms])  # Mexico to USA Pipe Flow
usa_to_mex_dict = create_dict([nangam_regions_acronyms, mex_regions_acronyms])  # USA to Mexico Pipe Flow

# Aggregate Dictionary #################################################################################################

all_dict = create_dict([['Production', 'Production Price', 'Consumption', 'Consumption Price'],
                        ['Mexico', 'Canada', 'USA', 'ROW', 'Total'], years])  # Aggregate Dictionary
