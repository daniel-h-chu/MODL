# USA_Functions generates dictionaries for US Production, Production Price, Consumption, and Consumption Price
########################################################################################################################
########################################################################################################################
########################################################################################################################
import os
import csv
import Functions as Fx
import Arrays as Ar


########################################################################################################################
########################################################################################################################
# Production Raw Data ##################################################################################################
########################################################################################################################
########################################################################################################################
# Create the US Production dictionary by reading in information from
# Lower_48_Natural_Gas_Production_and_Supply_Prices_by_Supply_Region.csv
# usa_prod_raw stores raw US Production data in a dictionary
# prod_stat_temp keeps track of the current statistic for which data is being entered into
# year_shift tracks of where the list of years begins in the data file
def prod_1():
    f_usa_prod_csv = open(Fx.include('Lower_48_Natural_Gas_Production_and_Supply_Prices_by_Supply_Region.csv'), 'r')
    file_reader = csv.reader(f_usa_prod_csv, delimiter=',')
    # Whether we are dealing with onshore or offshore
    prod_stat_temp = ''
    year_shift = 0
    # Enter data into dictionary by statistic, region, then year
    for row in file_reader:
        if Fx.year_sh(row, ''):
            # Read in correct data based on year
            year_shift = Fx.year_sh(row, '')
        if row[0] in Ar.nems_regions_full and prod_stat_temp != '':
            for index, element in enumerate(row):
                # Fill usa_prod_raw with production data for NEMS regions for correct years
                if index + Ar.years[0] - year_shift in Ar.years:
                    Ar.usa_prod_raw[prod_stat_temp][Ar.nems_dict[row[0]]][index + Ar.years[0] - year_shift] = \
                        float(element)
        # Whether we are dealing with onshroe or offshore
        elif row[0] in Ar.prod_stats_acronyms:
            prod_stat_temp = row[0]
        # Stop reading data past this point (Production Price data after this point)
        elif row[0] == Ar.usa_prod_split:
            prod_stat_temp = ''
    f_usa_prod_csv.close()


########################################################################################################################
# Gathers data for ALASKA and HAWAII Production from Oil_and_Gas_Supply.csv
# usa_prod_raw stores raw US Production data in a dictionary
# prod_stat_temp keeps track of the current statistic for which data is being entered into
# year_shift tracks of where the list of years begins in the data file
def prod_2():
    f_usa_prod_ahw_csv = open(Fx.include('Oil_and_Gas_Supply.csv'), 'r')
    file_reader = csv.reader(f_usa_prod_ahw_csv, delimiter=',')
    # Whether we are dealing with onshore or offshore
    prod_stat_temp = ''
    year_shift = 0
    for row in file_reader:
        if Fx.year_sh(row, ''):
            # Read in correct data based on year
            year_shift = Fx.year_sh(row, '')
        if row[0] in Ar.nems_regions_full and prod_stat_temp != '':
            for index, element in enumerate(row):
                for stat in Ar.prod_stats_acronyms:  # Alaska only has offshore data, so it is used in both ofs and ons
                    # Fill usa_prod_raw AHW with production data for NEMS regions for correct years
                    if index + Ar.years[0] - year_shift in Ar.years:
                        Ar.usa_prod_raw[stat][Ar.nems_dict[row[0]]][index + Ar.years[0] - year_shift] = float(element)
        # Whether we are dealing with onshore or offshore
        elif row[0] in Ar.prod_stats_acronyms:
            prod_stat_temp = row[0]
    f_usa_prod_ahw_csv.close()


########################################################################################################################
# Gathers data for conversion matrix from NEMS data to NANGAM data in NEMS_TO_NANGAM_(ONS/OFS).csv files
# nem_to_nan stores the conversion matrices for both onshore and offshore
def prod_3():
    # NO TOTAL CSV FILE
    for stat in [stat for stat in Ar.prod_stats_acronyms if stat != 'Total']:
        # read from NEMS_TO_NANGAM_OFFSHORE and NEMS_TO_NANGAM_ONSHORE
        f_nem_to_nan_csv = open(Fx.include('NEMS_TO_NANGAM_' + stat + '.csv'), 'r')
        file_reader = csv.reader(f_nem_to_nan_csv, delimiter=',')
        for row in file_reader:
            if row[1] in Ar.nangam_regions_acronyms:
                # Fill nem_to_nan matrix with conversion ratios between NEMS and NANGAM Regions
                for element, nems_region in zip(row[3:], Ar.nems_regions_acronyms):
                    Ar.nem_to_nan[stat][row[1]][nems_region] = float(element)
        f_nem_to_nan_csv.close()
        os.remove(Fx.include('NEMS_TO_NANGAM_' + stat + '.csv'))


########################################################################################################################
########################################################################################################################
# Production Calculations ##############################################################################################
########################################################################################################################
########################################################################################################################
# Matrix Multiply the raw production data for NEMS regions into final production data for NANGAM regions
# usa_prod final US Production data in a dictionary
def prod_4():
    for stat in Ar.prod_stats_acronyms:
        for nangam_region in Ar.nangam_regions_acronyms:
            for index, year in enumerate(Ar.years):
                dotsum = 0
                # Transform NEMS data with a NEMS to NANGAM Conversion Matrix (Matrix Multiplication)
                for nems_region, nems_conversion in zip(Ar.usa_prod_raw[stat], Ar.nem_to_nan[stat][nangam_region]):
                    dotsum += Ar.usa_prod_raw[stat][nems_region][year] * \
                              Ar.nem_to_nan[stat][nangam_region][nems_conversion]
                    Ar.usa_prod[stat][nangam_region][year] = dotsum


########################################################################################################################
# Aggregates the raw data into the "Total" key by summing up the production for Offshore and Onshore
def prod_5():
    for nangam_region in Ar.nangam_regions_acronyms:
        for year in Ar.years:
            Ar.usa_prod["Total"][nangam_region][year] = sum([Ar.usa_prod[stat][nangam_region][year] for stat in
                                                             Ar.prod_stats_acronyms if stat != "Total"])


########################################################################################################################
########################################################################################################################
# Production Price Raw Data ############################################################################################
########################################################################################################################
########################################################################################################################
# Create the US Production Price dictionary by reading in information from
# Lower_48_Natural_Gas_Production_and_Supply_Prices_by_Supply_Region.csv
# usa_prod_raw stores raw US Production Price data in a dictionary
# prod_stat_temp keeps track of the current statistic for which data is being entered into
# year_shift tracks of where the list of years begins in the data file
def prod_price_1():
    f_usa_prod_price_csv = open(Fx.include('Lower_48_Natural_Gas_Production_and_Supply_Prices_by_Supply_Region.csv'),
                                'r')
    file_reader = csv.reader(f_usa_prod_price_csv, delimiter=',')
    # Whether we are dealing with onshore or offshore
    prod_stat_temp = ''
    prod_temp = ''
    # Enter data into dictionary by statistic, region, then year
    for row in file_reader:
        if row[0] in Ar.nems_regions_full and prod_stat_temp != '' and prod_temp != '':
            Ar.usa_prod_price_raw[prod_stat_temp][Ar.nems_dict[row[0]]] = dict.fromkeys(Ar.years)
            for index, element in enumerate(row[4:-1]):
                if index+2015 in Ar.years:
                    # Fill raw price data for each nems region for specific years
                    Ar.usa_prod_price_raw[prod_stat_temp][Ar.nems_dict[row[0]]][index + 2015] = float(element)
        # Production Statistic is Onshore or Offshore
        elif row[0] in Ar.prod_stats_acronyms:
            prod_stat_temp = row[0]
        # Make sure we are looking at price not just production
        elif row[0] == Ar.usa_prod_split:
            prod_temp = row[0]
    f_usa_prod_price_csv.close()


########################################################################################################################
# Calculate Production Value by multiplying production price raw data and production final data
# usa_prod_value stores US Production Price value data in a dictionary
def prod_price_2():
    for stat in Ar.prod_stats_acronyms:
        for region in Ar.nems_regions_acronyms:
            for year in Ar.years:
                # Numerical multiplication for production price value for each nems region and year
                Ar.usa_prod_price_value[stat][region][year] = Ar.usa_prod_raw[stat][region][year] * \
                                                              Ar.usa_prod_price_raw[stat][region][year]


########################################################################################################################
# Matrix Multiply Production Price Value to convert from NEMS to NANGAM
def prod_price_3():
    for stat in Ar.prod_stats_acronyms:
        for nangam_region in Ar.nangam_regions_acronyms:
            for index, year in enumerate(Ar.years):
                dotsum = 0
                # Matrix multiply nems prices with nem_to_nangam transform matrix to obtain final prices usa_prod_price
                for nems_region, nems_conversion in zip(Ar.usa_prod_price_value[stat],
                                                        Ar.nem_to_nan[stat][nangam_region]):
                    dotsum += Ar.usa_prod_price_value[stat][nems_region][year] * \
                              Ar.nem_to_nan[stat][nangam_region][nems_conversion]
                # No Price Data
                if Ar.usa_prod[stat][nangam_region][year] == 0:
                    Ar.usa_prod_price[stat][nangam_region][year] = 0
                else:
                    Ar.usa_prod_price[stat][nangam_region][year] = dotsum / \
                                                                   Ar.usa_prod[stat][nangam_region][year]


########################################################################################################################
# Aggregates the production price data into the "Total" key by averaging the production prices for Offshore and Onshore
def prod_price_4():
    for region in Ar.nangam_regions_acronyms:
        for year in Ar.years:
            try:
                # Average production price weighted by production
                Ar.usa_prod_price["Total"][region][year] = sum([Ar.usa_prod_price[stat][region][year] for stat in
                                                                Ar.prod_stats_acronyms if stat != "Total"]) / sum(
                 [1 for stat
                  in Ar.prod_stats_acronyms if Ar.usa_prod_price[stat][region][year] != 0 and stat != "Total"])
            # No production data
            except ZeroDivisionError:
                Ar.usa_prod_price["Total"][region][year] = 0


########################################################################################################################
########################################################################################################################
# Consumption ##########################################################################################################
########################################################################################################################
########################################################################################################################
# Create the US Consumption dictionary by reading in information from
# Natural_Gas_Consumption_by_End-Use_Sector_and_Census_Division.csv
# usa_Cons stores US Consumption data in a dictionary
# cons_sector_temp keeps track of the current consumption sector for which data is being entered into
# year_shift tracks of where the list of years begins in the data file
def cons_1():
    f_usa_cons_csv = open(Fx.include('Natural_Gas_Consumption_by_End-Use_Sector_and_Census_Division.csv'), 'r')
    file_reader = csv.reader(f_usa_cons_csv, delimiter=',')
    # What current consumption sector we are dealing with
    cons_sector_temp = ''
    year_shift = 0
    for row in file_reader:
        if Fx.year_sh(row, ''):
            # Read in correct data based on year
            year_shift = Fx.year_sh(row, '')
        if row[0] in Ar.cons_sectors:
            # Set current consumption sector
            cons_sector_temp = row[0]
        if cons_sector_temp != '' and row[0] in Ar.nangam_regions_full:
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    # Fill usa_cons with consumption data for each nangam region and year
                    Ar.usa_cons[cons_sector_temp][Ar.nangam_dict[row[0]]][index + Ar.years[0] - year_shift] = \
                        float(element)
    f_usa_cons_csv.close()


########################################################################################################################
# Gather US Consumption Data for Alaska and Hawaii from Energy_Consumption_by_Sector_and_Source.csv
# usa_cons stores US Consumption data in a dictionary
# cons_sector_temp keeps track of the current consumption sector for which data is being entered into
# year_shift tracks of where the list of years begins in the data file
def cons_2():
    for element, sector in zip(Ar.usa_cons_als, Ar.cons_sectors):
        Ar.usa_cons[sector]["AHW"][Ar.years[0]] = element / 1000000
    f_usa_cons_total_csv = open(Fx.include('Energy_Consumption_by_Sector_and_Source.csv'), 'r')
    file_reader = csv.reader(f_usa_cons_total_csv, delimiter=',')
    # What current consumption sector we are dealing with
    cons_sector_temp = ''
    year_shift = 0
    for row in file_reader:
        if Fx.year_sh(row, ''):
            # Read in correct data based on year
            year_shift = Fx.year_sh(row, '')
        if row[0] in Ar.cons_sectors:
            # Set the current consumption sector only if it reads residential
            cons_sector_temp = ''
        if row[0] == 'Residential':
            cons_sector_temp = row[0]
        if cons_sector_temp != '' and row[0] == Ar.resource:
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    # Obtain total consumption for US residential sector for each year
                    Ar.usa_cons_total[index + Ar.years[0] - year_shift] = float(element)
    f_usa_cons_total_csv.close()
    for cons_sector in Ar.cons_sectors:
        for index, year in enumerate(Ar.years):
            if index > 0:
                # Calculate Alaska consumption by calculating the ratio for Alaska consumption (by subtracting out every
                # other region from us total) from one year to the next, then multiplying the ratio to the first year
                Ar.usa_cons[cons_sector]['AHW'][year] = Ar.usa_cons[cons_sector]['AHW'][Ar.years[index - 1]] * \
                                                        (Ar.usa_cons_total[year] -
                                                         sum([Ar.usa_cons[cons_sector][nangam_region][year] for
                                                              nangam_region in Ar.nangam_regions_acronyms if
                                                              nangam_region
                                                              != 'AHW'])) / (Ar.usa_cons_total[Ar.years[index - 1]] -
                                                                             sum([Ar.usa_cons[cons_sector][
                                                                                      nangam_region][
                                                                                      Ar.years[index - 1]]
                                                                                  for nangam_region in
                                                                                  Ar.nangam_regions_acronyms if
                                                                                  nangam_region != 'AHW']))


########################################################################################################################
########################################################################################################################
# Consumption Prices ###################################################################################################
########################################################################################################################
########################################################################################################################
# Gather US Consumption Price Data from Natural_Gas_Delivered_Prices_by_End-Use_Sector_and_Census_Division.csv
# usa_cons_price stores US Consumption price data in a dictionary
# cons_sector_temp keeps track of the current consumption sector for which data is being entered into
# year_shift tracks of where the list of years begins in the data file
def cons_price_1():
    f_usa_cons_price_csv = open(Fx.include('Natural_Gas_Delivered_Prices_by_End-Use_Sector_and_Census_Division.csv'),
                                'r')
    file_reader = csv.reader(f_usa_cons_price_csv, delimiter=',')
    # What current consumption sector we are dealing with
    cons_sector_temp = ''
    year_shift = 0
    for row in file_reader:
        if Fx.year_sh(row, ''):
            # Read in correct data based on year
            year_shift = Fx.year_sh(row, '')
        if row[0] in Ar.cons_sectors:
            # Set the current consumption sector
            cons_sector_temp = row[0]
        if cons_sector_temp != '' and row[0] in Ar.nangam_regions_full:
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    # Fill usa_cons_price with consumption price data for each nangam region and year. Electric Power mu
                    # st be converted by a factor of 1000/365
                    if cons_sector_temp != 'Electric Power':
                        Ar.usa_cons_price[cons_sector_temp][Ar.nangam_dict[row[0]]][index + Ar.years[0] - year_shift] =\
                            float(element)
                    else:  # Special Conversion for Electric Power
                        Ar.usa_cons_price[cons_sector_temp][Ar.nangam_dict[row[0]]][index + Ar.years[0] - year_shift] =\
                            float(element) * 1000/365
    f_usa_cons_price_csv.close()


########################################################################################################################
# Calculate US Consumption Price Data for Alaska and Hawaii from as the weighted average of consumption prices of all
# other NANGAM regions
# usa_cons_price stores US Consumption Price data in a dictionary
def cons_price_2():
    for year in Ar.years:
        for element, sector in zip(Ar.usa_cons_price_als, Ar.cons_sectors):
            Ar.usa_cons_price[sector]["AHW"][year] = element
            # Alaska all sector average price as average of other sectors weighted by consumption
            Ar.usa_cons_price['All Sectors']['AHW'][year] = sum([Ar.usa_cons[cons_sector]['AHW'][year] *
                                                                 Ar.usa_cons_price[cons_sector]['AHW'][year] for
                                                                 cons_sector in
                                                                 Ar.cons_sectors if
                                                                 cons_sector != 'All Sectors']) / sum(
                [Ar.usa_cons[cons_sector]['AHW'][year] for cons_sector in Ar.cons_sectors if cons_sector !=
                 'All Sectors'])

    # Alternate Model for Alaska/Hawaii Consumption Price using average ratio of consumption prices
    '''for index, year in enumerate([year for year in a.years if year != a.years[0]], 1):
        for sector in a.cons_sectors:
            sum_price_prev = sum([a.usa_cons[sector][nangam_region][a.years[index-1]] for nangam_region in
                                  a.nangam_regions_acronyms if nangam_region != "AHW"])
            sum_cons_prev = sum([a.usa_cons[sector][nangam_region][a.years[index-1]] *
                                 a.usa_cons_price[sector][nangam_region][a.years[index-1]]
                                for nangam_region in a.nangam_regions_acronyms if nangam_region != "AHW"])
            sum_price_cur = sum([a.usa_cons[sector][nangam_region][year] for nangam_region in a.nangam_regions_acronyms
                                 if nangam_region != "AHW"])
            sum_cons_cur = sum([a.usa_cons[sector][nangam_region][year] * a.usa_cons_price[sector][nangam_region][year]
                                for nangam_region in a.nangam_regions_acronyms if nangam_region != "AHW"])
            a.usa_cons_price[sector]["AHW"][a.years[index]] = a.usa_cons_price[sector]["AHW"][a.years[index-1]] *\
                ((sum_cons_cur/sum_price_cur)/(sum_cons_prev/sum_price_prev)) ** (a.years[index] - a.years[index-1])'''


########################################################################################################################
########################################################################################################################
# Convert Units ########################################################################################################
########################################################################################################################
########################################################################################################################
# Convert TCF/Year to BCF/Day (1000/365 Conversion Factor)
def conversion():
    Fx.convert(Ar.usa_prod, 3, 1000 / 365)
    Fx.convert(Ar.usa_cons, 3, 1000 / 365)
