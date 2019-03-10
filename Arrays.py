# Arrays is the base file of this program. Arrays stores all arrays and dictionaries used by all functions
########################################################################################################################
########################################################################################################################
########################################################################################################################

########################################################################################################################
# All (Things that can be changed) #####################################################################################
########################################################################################################################

# Consumption Sectors (To Be Read from Excel Sheets) {All Sectors, Residential, and Electric Power must be included}
cons_sectors = ['All Sectors', 'Residential', 'Commercial', 'Industrial', 'Transportation', 'Electric Power']
# Acronyms of Production Stats (To Be Read from Excel Sheets) {All three statistics must be included}
prod_stats_acronyms = ['ONS', 'OFS', 'Total']
# Years to be calculated {2015, 2016, or 2017 must be included}
years = [year for year in range(2018, 2051)]

# Custom Data ##########################################################################################################
# See 'Files to Download' on how to enter data to these arrays

# Alaska Consumption 2015 from NG_CONS_SUM_DCU_SAK_A (Same order as cons_sectors)
usa_cons_als = [333602, 18574, 18472, 4864 + 223246 + 37615 + 615, 10, 30207]
# Alaska Consumption Prices (Same order as cons_sectors)
usa_cons_price_als = [0, 9.81, 8.34, 5.06, 15.71, 6.65]
# Consumption Prices [0, E28, I28, M28, E28, M28] from mex_consumption_price or [0, Avg Residential Public Price, Avg
# Commercial Public Price, Avg Industrial Public Price, Avg Residential Public Price, Avg Industrial Public Price]
mex_cons_price_raw = [0, 9.73, 5.34, 4.02, 9.73, 4.02]

# US Geography #########################################################################################################

# Full names of NEMS regions (For Lower_48_Natural_Gas_Production_and_Supply_Prices_by_Supply_Region)
nems_regions_full = ['East', 'Gulf Coast', 'Midcontinent', 'Southwest', 'Dakotas/Rocky Mountains', 'West Coast',
                     'Alaska']
# Acronyms of NEMS regions (In same order as above) (For NEMS_TO_NANGAM_)
nems_regions_acronyms = ['NES', 'NGC', 'NMC', 'NSW', 'NRM', 'NWC', 'NAH']
# Full names of NANGAM regions
nangam_regions_full = ['Alaska & Hawaii', 'Gulf of Mexico', 'Pacific', 'Mountain', 'West North Central',
                       'East North Central', 'West South Central', 'East South Central', 'Middle Atlantic',
                       'South Atlantic', 'New England']
# Acronyms of NANGAM regions (For NEMS_TO_NANGAM_) {AHW should be included}
nangam_regions_acronyms = ['AHW', 'GOM', 'PCF', 'MNT', 'WNC', 'ENC', 'WSC', 'ESC', 'MAT', 'SAT', 'NEN']
# Full names of US States (For EIA-StatetoStateCapacity)
usa_states_full = ['Gulf of Mexico', 'Gulf of Mexico - Deepwater', 'Alabama', 'Alaska', 'Arizona', 'Arkansas',
                   'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia',
                   'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',  'Kansas', 'Kentucky', 'Louisiana', 'Maine',
                   'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana',
                   'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina',
                   'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
                   'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
                   'West Virginia', 'Wisconsin', 'Wyoming']
# Acronyms of US States (In same order as above) (For EIA-StatetoStateCapacity)
usa_states_acronyms = ['GOM', 'GMD', 'ALB', 'ALS', 'ARZ', 'ARK', 'CAL', 'COL', 'CON', 'DEL', 'WDC', 'FLR', 'GRG', 'HWI',
                       'IDH', 'ILN', 'IND', 'IOW', 'KNS', 'KNT', 'LSN', 'MAN', 'MAR', 'MAS', 'MCH', 'MNS', 'MSI', 'MSU',
                       'MON', 'NBR', 'NVD', 'NHM', 'NJS', 'NMX', 'NYK', 'NCL', 'NDK', 'OHO', 'OKL', 'ORG', 'PEN', 'RIL',
                       'SCL', 'SDK', 'TNS', 'TEX', 'UTH', 'VMT', 'VGN', 'WAS', 'WVG', 'WIS', 'WYO']
# Acronyms of US States (In same order as above) (For EIA-NaturalGasPipelineProjects)
usa_states_acronyms2 = ['GM', 'GD', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL',
                        'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
                        'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT',
                        'VA', 'WA', 'WV', 'WI', 'WY']
# Acronyms of states per NANGAM region (For EIA-StatetoStateCapacity in sorting states into respective NANGAM regions)
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

# Full names of Canadian Provinces (For 1710000501-eng, Natural_Gas_Production, EIA-StatetoStateCapacity, and
# Electricity_Generation )
canadian_provinces_full = ['Newfoundland and Labrador', 'Prince Edward Island', 'Nova Scotia', 'New Brunswick',
                           'Quebec', 'Ontario', 'Manitoba', 'Alberta', 'British Columbia', 'Saskatchewan',
                           'Yukon', 'Northwest Territories', 'Nunavut']
# Acronyms of Canadian Provinces (In same order as above) (For Printing)
canadian_provinces_acronyms = ['NLL', 'PEI', 'NSC', 'NBW', 'QBC', 'ONT', 'MTB', 'ABR', 'BCL', 'SAS', 'YKN', 'NWT', 'NUN'
                               ]
# Acronyms of Canadian Provinces (2 Characters, same order as above) (For Printing)
canadian_provinces_acronyms2 = ['NL', 'PE', 'NS', 'NB', 'QC', 'ON', 'MB', 'AB', 'BC', 'SK', 'YT', 'NT', 'NU']
# Full names of Canadian regions (For printing)
canadian_regions_full = ['Canada East', 'Canada West']
# Acronyms of Canadian regions (For Printing)
canadian_regions_acronyms = ['CAE', 'CAW']
# Regions Defined by Provinces (For EIA-StatetoStateCapacity)
provinces_to_regions = {
    'CAE': ['NLL', 'PEI', 'NSC', 'NBW', 'QBC', 'ONT'],
    'CAW': ['MTB', 'ABR', 'BCL', 'SAS', 'YKN', 'NWT', 'NUN']
}

# Mexico Geography #####################################################################################################

# Full names of Mexican Regions (For reg_bal_mex)
mex_regions_full = ['Mexico North West', 'Mexico North East', 'Mexico Interior West', 'Mexico Interior',
                    'Mexico South West']
# Acronyms of Mexican Regions (In same order as above) (For reg_bal_mex)
mex_regions_acronyms = ['MNW', 'MNE', 'MIW', 'MIN', 'MSW']
# Mexican cities per NANGAM region (For EIA-StatetoStateCapacity)
cities_to_regions = {
    'MNW': ['Sonora', 'Chihuahua', 'Baja California', 'Baja Calif. Norte'],
    'MNE': ['Tamaulipas', 'Reynosa', 'Mexico', 'Coahuila'],
    'MIW': ['Rio Grande'],
    'MIN': [],
    'MSW': []
}

# Rest of World Geography ##############################################################################################

# Full names of Rest of World Regions (For printing and aggregate data)
row_regions_full = ['Rest of World']
# Acronyms of Rest of World Regions (For printing and aggregate data)
row_regions_acronyms = ['ROW']

# Month and State Level Data ###########################################################################################

# List of Months
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# Consumption Sectors (For new_output, in same order as cons_sectors)
cons_sectors_months = ['Total', 'Residential', 'Commercial', 'Industrial', 'Vehicle', 'Electric']

########################################################################################################################
# All (Misc. Consult the Data before Changing) #########################################################################
########################################################################################################################

# US NANGAM regions used for Canadian Consumption price calculations (For Canadian Consumption)
can_cons_nangam_regions = ['PCF', 'MNT', 'WNC', 'ENC', 'NEN']
# Production Statistics to be Printed on Excel Sheet (For printing)
prod_stats_print = ['Onshore', 'Offshore', 'Total']
# Consumption Sectors to be Printed on Excel Sheet (For printing)
cons_sectors_print = ['Total Consumption', 'Residential Sector', 'Commercial Sector', 'Industrial Sector',
                      'Transportation Sector', 'Electric Sector']

# Keywords #############################################################################################################

usa_prod_split = 'Supply Prices'  # Statistic Keyword for Price (For Lower_48_Natural_Gas_Production_and_Supply_Prices_)
resource = "Natural Gas"  # Resource Keyword (For Energy_Consumption_by_Sector_and_Source, Delivered_energy_consumption_
# by_end-use_sector_and_fuel, Primary_Energy_Demand, End_-_Use_Demand, End_-_Use_Prices, Electricity_Generation)
price_resource = 'Price of Natural Gas'  # Price Resource Keyword in NG_PRI_SUM_A_EPG0_PCS_DMCF_M and others
production = "Production"  # Production Keyword (For reg_bal_mex)
total_world = 'Total World'  # Total World Keyword (For World_total_natural_gas_production_by_region and World_natural_g
# as_consumption_by_region)
united_states = 'United States'  # US Keyword (For World_total_natural_gas_production_by_region and World_total_natural_
# gas_consumption_by_region)
canada = 'Canada'  # Canada Keyword (For World_total_natural_gas_production_by_region and World_total_natural_
# gas_consumption_by_region)
mexico = 'Mexico'  # Mexico Keyword (For World_total_natural_gas_production_by_region and World_total_natural_
# gas_consumption_by_region)
electric_generation = 'Electric Generation'  # Electricity Generation Keyword (For Primary_Energy_Demand)
from_mexico = 'From Mexico'  # From Mexico Keyword (For Natural_Gas_Imports_and_Exports)
from_canada = 'From Canada'  # From Canada Keyword (For Natural_Gas_Imports_and_Exports)
all_sectors = 'All Sectors'  # All Sectors Keyword (For Delivered_energy_consumption_by_end-use_sector_and_fuel)
total = 'Total'  # Total Keyword (For Natural_Gas_Production)
region_from = 'Region From'  # Region From Keyword (For mex_pip_cap_bcfd and can_pip_cap)
region_to = 'Region To'  # Region To Keyword (For mex_pip_cap_bcfd and can_pip_cap)
state_from = 'State From'  # State From Keyword (For EIA-StatetoStateCapacity)
state_to = 'State To'  # State To Keyword (For EIA-StatetoStateCapacity)
county_from = 'County From'  # County From Keyword (For EIA-StatetoStateCapacity)
county_to = 'County To'  # County To Keyword (For EIA-StatetoStateCapacity)
capacity = 'Capacity'  # Capacity Keyword (For EIA-StatetoStateCapacity, mex_pip_cap_bcfd, can_pip_cap)
capacity_year = 'year'  # Capacity Year Keyword (For EIA-StatetoStateCapacity)
operating = 'Operating'  # Operating Keyword (For mex_pip_cap_bcfd)
status = 'Status'  # Status Keyword (For mex_pip_cap_bcfd)
r_into = 'Into '  # Into Keyword (For Primary_Natural_Gas_Flows_Entering_NGTDM_Region_from_Neighboring_Regions)
r_from = ' From:'  # From Keyword (For Primary_Natural_Gas_Flows_Entering_NGTDM_Region_from_Neighboring_Regions)
usa_to_can = 'Pipeline Exports to Canada'  # USA to CAN Pipe Exports (For Natural_Gas_Imports_and_Exports)
can_to_can = 'Average annual flows (BCF/day)'  # CAN to CAN Pipe Flow (For can_pip_cap)
imports = 'Imports'  # MEX Imports Keyword (For reg_bal_mex)
exports = 'Exports'  # MEX Exports Keyword (For reg_bal_mex)
lng_imports = 'Liquefied Natural Gas Imports'  # Liquid Natural Gas Imports Keyword (Natural_Gas_Imports_and_Exports)
lng_exports = 'Liquefied Natural Gas Exports'  # Liquid Nstural Gas Exports Keyword (Natural_Gas_Imports_and_Exports)
completed = 'Completed'  # Status Keyword (For EIA-NAturalGasPipelineProjects)
last_updated_date = 'Last Updated Date'  # Last Updated Date Keyword (For EIA-NaturalGasPipelineProjects)
to = 'To'  # State to Keyword (For can-pip-cap)
frm = 'From'  # State From Keyword (For can-pip-cap)

########################################################################################################################
########################################################################################################################
########################################################################################################################
# (DO NOT EDIT BEYOND HERE) ############################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

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
provinces_dict = create_lookup_dict(canadian_provinces_full, canadian_provinces_acronyms)  # Prov Full to Prov Acronyms
reverse_provinces_dict = create_lookup_dict(canadian_provinces_acronyms, canadian_provinces_full)  # Prov Acro to Full
mex_cons_price_dict = create_lookup_dict(cons_sectors, mex_cons_price_raw)  # Cons Price Raw Data to ConsPrice Dict
print_full_dict = create_lookup_dict(all_regions_acronyms, all_regions_full)  # Acronyms to Full All Regions
reverse_full_dict = create_lookup_dict(all_regions_full, all_regions_acronyms)  # Full to Acronyms All Regions
states_dict = create_lookup_dict(usa_states_full, usa_states_acronyms)  # State Full to State Acronyms
states2_dict = create_lookup_dict(usa_states_acronyms2, usa_states_acronyms)  # State Acronyms 2 Char to State Acronyms
provinces2_dict = create_lookup_dict(canadian_provinces_acronyms2, canadian_provinces_acronyms)  # Can 2 char to 3 char
stat_print_dict = create_lookup_dict(prod_stats_acronyms, prod_stats_print)  # Stat Acronym to Stat Printed
sector_print_dict = create_lookup_dict(cons_sectors, cons_sectors_print)  # Sector Acronym to Sector Printed
print_dict = stat_print_dict.copy()  # Sector/Stat Acronym to Sector/Stat Printed
print_dict.update(sector_print_dict)
cons_month_dict = create_lookup_dict(cons_sectors_months, cons_sectors)  # Consumption Sectors Month Data Dict

# Aggregate Dictionary #################################################################################################

all_dict = create_dict([['Production', 'Production Price', 'Consumption', 'Consumption Price'],
                        ['Mexico', 'Canada', 'USA', 'ROW', 'Total'], years])  # Aggregate Dictionary
planned = []
planned_cols = []
all_prod = {}  # All Production
all_cons = {}  # All Consumption
all_to_states_dict = {mex_region: [mex_region] for mex_region in mex_regions_acronyms + row_regions_acronyms}
all_to_states_dict.update(states_to_regions)  # All states/provinces/regions
all_to_states_dict.update(provinces_to_regions)  # All states/provinces/regions
all_states_dict = {mex_regions_full[index]: mex_regions_acronyms[index] for index in range(len(mex_regions_acronyms))}
all_states_dict.update({'Rest of World': 'ROW'})
all_states_dict.update(provinces_dict)
all_states_dict.update(states_dict)

# Monthify and Statify #################################################################################################

states_full = usa_states_full + mex_regions_full + canadian_provinces_full + row_regions_full  # List of States Full
states_acronyms = usa_states_acronyms + mex_regions_acronyms + canadian_provinces_acronyms + row_regions_acronyms  # Acr
states_acronyms2 = usa_states_acronyms2 + mex_regions_acronyms + canadian_provinces_acronyms2 + row_regions_acronyms
states_acronyms_to_2_dict = create_lookup_dict(states_acronyms, states_acronyms2)  # Lookup dictionary for 2 letter abr
prod_state_month = create_dict([states_acronyms, range(1, 13)])  # Production State and Month Transform Data
cons_state_month = create_dict([cons_sectors, states_acronyms, range(1, 13)])  # Consumption State and Month Trans Data
all_prod_month = create_dict([prod_stats_acronyms, states_acronyms, years, range(1, 13)])  # Production State Month Data
all_cons_month = create_dict([cons_sectors, states_acronyms, years, range(1, 13)])  # Consumption State and Month Data
years_months = []  # Monthly Timeline
for year in years:
    years_months += [str(month) + '-' + str(year) for month in months]
all_prod_raw = {}
all_cons_raw = {}
usa_cons_price_raw = create_dict([cons_sectors, states_acronyms2, months])  # State by State Consumption Price Data
all_prod = create_dict([prod_stats_acronyms, states_acronyms2, years_months])  # Production Year + Month Index
all_cons = create_dict([cons_sectors, states_acronyms2, years_months])  # Consumption Year + Month Index
all_prod_price = create_dict([prod_stats_acronyms, states_acronyms2, years_months])  # Production Price Year + Month Idx
all_cons_price = create_dict([cons_sectors, states_acronyms2, years_months])  # Consumption Price Year + Month Index
print_full_dict_state = {states_acronyms_to_2_dict[all_states_dict[state]]: state for state in list(all_states_dict)}

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
can_cons_raw = create_dict([cons_sectors, canadian_provinces_full, years])  # CAN Consumption Province Level
can_cons_eng_dem = create_dict([years])  # CAN Energy Consumption
can_elc_gen_ratio_raw = create_dict([canadian_provinces_acronyms, years])  # CAN Electricity Generation Raw Data
can_elc_gen_ratio = create_dict([canadian_regions_acronyms, years])  # CAN Electricity Generation
can_cons_price = create_dict([cons_sectors, canadian_regions_acronyms, years])  # CAN Consumption Price
can_cons_price_raw = create_dict([cons_sectors, canadian_provinces_full, years])  # CAN Consumption Price Prov Lvl

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

pip_cap = create_dict([states_acronyms2, states_acronyms2])  # Pipe Capacity
pip_flow_raw = create_dict([all_regions_acronyms, all_regions_acronyms, years])
pip_flow = create_dict([states_acronyms2, states_acronyms2, years_months])  # Pipe Flow
pip_flow_state = create_dict([states_acronyms2, states_acronyms2])  # Pipe Flow by State
mex_to_usa_dict = create_dict([mex_regions_acronyms, usa_states_acronyms2])  # Mexico to USA Pipe Flow
usa_to_mex_dict = create_dict([usa_states_acronyms2, mex_regions_acronyms])  # USA to Mexico Pipe Flow
pip_flow_lng = create_dict([states_acronyms2, states_acronyms2, years_months])  # Pipe Flow LNG
pip_flow_lng_raw = create_dict([states_acronyms2, states_acronyms2])  # LNG Pipe Exports Raw
