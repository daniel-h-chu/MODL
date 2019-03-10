# CAN_Functions generates dictionaries for Canadian Production, Production Price, Consumption, and Consumption Price
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
# Create the Canadian Production dictionary by reading in information from Natural_Gas_Production.csv
# can_prod_raw stores the raw production data for individual provinces
# can_prod_raw_province_temp keeps track of current province
# year_shift tracks of where the list of years begins in the data file
def prod_1():
    f_can_prod_csv = open(Fx.include('Natural_Gas_Production.csv'), 'r')
    file_reader = csv.reader(f_can_prod_csv, delimiter=',')
    # What province we are dealing with
    can_prod_raw_province_temp = ''
    year_shift = 0
    for row in file_reader:
        if row[0] in Ar.canadian_provinces_full:
            # Set current province that we are dealing with
            can_prod_raw_province_temp = row[0]
        if Fx.year_sh(row, '_'):
            # Read in correct data based on year
            year_shift = Fx.year_sh(row, '_')
        if row[0] == Ar.total and can_prod_raw_province_temp != '':
            for index, element in enumerate(row):
                if index+Ar.years[0]-year_shift in Ar.years:
                    # Fill can_prod_raw with raw production data for each canadian province and year
                    Ar.can_prod_raw['ONS'][Ar.provinces_dict[can_prod_raw_province_temp]][
                        index + Ar.years[0] - year_shift] = float(element)
    f_can_prod_csv.close()
    # Combine the data from different provinces into two canadian regions
    # can_prod stores the production data for the two canadian regions by checking if a province is in a region using
    # the provinces_to_regions dictionary
    for canadian_region in Ar.canadian_regions_acronyms:
        for year in Ar.years:
                Ar.can_prod['ONS'][canadian_region][year] = sum([Ar.can_prod_raw['ONS'][province][year] for province in
                                                                 Ar.canadian_provinces_acronyms if province in
                                                                 Ar.provinces_to_regions[canadian_region] and
                                                                 Ar.can_prod_raw['ONS'][province][year] is not None])
    
    os.remove(Fx.include('Natural_Gas_Production.csv'))


########################################################################################################################
# Aggregates the raw data into the "Total" key by summing up the production for Offshore and Onshore
def prod_2():
    for region in Ar.canadian_regions_acronyms:
        for year in Ar.years:
            Ar.can_prod["Total"][region][year] = sum([Ar.can_prod[stat][region][year] for stat in
                                                      Ar.prod_stats_acronyms if stat != "Total"])


########################################################################################################################
########################################################################################################################
# Production Price #####################################################################################################
########################################################################################################################
########################################################################################################################
# Create the Canadian Production Price dictionary by reading in information from Natural_Gas_Imports_and_Exports.csv
# can_prod_price stores the production price data for Canadian regions
# year_shift tracks of where the list of years begins in the data file
def prod_price_1():
    for region in Ar.canadian_regions_acronyms:
        for year in Ar.years:
            for prod_stat in Ar.prod_stats_acronyms:
                Ar.can_prod_price[prod_stat][region][year] = 0
    f_can_prod_price_csv = open(Fx.include('Natural_Gas_Imports_and_Exports.csv'), 'r')
    file_reader = csv.reader(f_can_prod_price_csv, delimiter=',')
    year_shift = 0
    for row in file_reader:
        if Fx.year_sh(row, ''):
            # Read in correct data based on year
            year_shift = Fx.year_sh(row, '')
        # SPECIAL STATISTIC FOR CANADIAN PRICE
        if row[0] == Ar.from_canada:
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    for region in Ar.canadian_regions_acronyms:
                        # Fill can_prod_price with production price data for each canadian region and year
                        Ar.can_prod_price['ONS'][region][index + Ar.years[0] - year_shift] = float(element)
    f_can_prod_price_csv.close()


########################################################################################################################
# Aggregates the raw data into the "Total" key by summing up the production for Offshore and Onshore
def prod_price_2():
    for region in Ar.canadian_regions_acronyms:
        for year in Ar.years:
            # Note this is an unweighted average of production price
            try:
                Ar.can_prod_price["Total"][region][year] = sum([Ar.can_prod_price[stat][region][year] for stat in
                                                                Ar.prod_stats_acronyms if stat != "Total"]) / sum(
                    [1 for stat
                     in Ar.prod_stats_acronyms if Ar.can_prod_price[stat][region][year] != 0 and stat != "Total"])
            except ZeroDivisionError:
                Ar.can_prod_price["Total"][region][year] = 0


########################################################################################################################
########################################################################################################################
# Consumption Raw Data #################################################################################################
########################################################################################################################
########################################################################################################################
# Create the Canadian Consumption dictionary (Minus Electricity) by reading in information from End_-_Use_Demand.csv
# can_cons stores the consumption data for canadian regions
# cons_sector_temp keeps track of the current consumption sector
# year_shift tracks of where the list of years begins in the data file
def cons_2():
    for province in Ar.canadian_provinces_full:
        f_can_end_dem_csv = open(Fx.include('End_-_Use_Demand_' + province + '.csv'), 'r')
        file_reader = csv.reader(f_can_end_dem_csv, delimiter=',')
        # What consumption sector we are dealing with
        cons_sector_temp = ''
        year_shift = 0
        for row in file_reader:
            if row[0] in Ar.cons_sectors:
                # Set current consumption sector that we are dealing with
                cons_sector_temp = row[0]
            if Fx.year_sh(row, '_'):
                # Read in correct data based on year
                year_shift = Fx.year_sh(row, '_')
            if cons_sector_temp != '' and row[0] == Ar.resource:
                for index, element in enumerate(row):
                    if index+Ar.years[0]-year_shift in Ar.years:
                        Ar.can_cons_raw[cons_sector_temp][province][index+Ar.years[0]-year_shift] = float(element)
                        for region in Ar.canadian_regions_acronyms:
                            if Ar.provinces_dict[province] in Ar.provinces_to_regions[region]:
                                Ar.can_cons[cons_sector_temp][region][index+Ar.years[0]-year_shift] += float(element)
        f_can_end_dem_csv.close()
        os.remove(Fx.include('End_-_Use_Demand_' + province + '.csv'))


########################################################################################################################
# Gets data for Canadian electricity consumption from Primary_Energy_Demand.csv
# cons_sector_temp keeps track of whether the current sector is 'Electric Generation'
# year_shift tracks of where the list of years begins in the data file
def cons_3():
    for province in Ar.canadian_provinces_full:
        f_can_eng_dem_csv = open(Fx.include('Primary_Energy_Demand_' + province + '.csv'), 'r')
        file_reader = csv.reader(f_can_eng_dem_csv, delimiter=',')
        # What consumption sector we are dealing with
        cons_sector_temp = ''
        year_shift = 0
        for row in file_reader:
            # SPECIAL STATISTIC FOR ELECTRICITY
            if row[0] == Ar.electric_generation:
                # Set consumption sector only if it is electricity generation
                cons_sector_temp = row[0]
            if Fx.year_sh(row, '_'):
                # Read in correct data based on year
                year_shift = Fx.year_sh(row, '_')
            if cons_sector_temp != '' and row[0] == Ar.resource:
                for index, element in enumerate(row):
                    if index + Ar.years[0] - year_shift in Ar.years:
                        for region in Ar.canadian_regions_acronyms:
                            if Ar.provinces_dict[province] in Ar.provinces_to_regions[region]:
                                # Fill total canadian consumption energy demand with data for each year
                                Ar.can_cons['Electric Power'][region][index+Ar.years[0]-year_shift] += float(element)
        f_can_eng_dem_csv.close()
        os.remove(Fx.include('Primary_Energy_Demand_' + province + '.csv'))


########################################################################################################################
# Aggregates the data into the "All Sectors" key by summing up consumption for consumption sectors
def cons_5():
    for region in Ar.canadian_regions_acronyms:
        for year in Ar.years:
            Ar.can_cons["All Sectors"][region][year] = sum([Ar.can_cons[cons_sector][region][year] for cons_sector in
                                                            Ar.cons_sectors if cons_sector != "All Sectors"])


########################################################################################################################
########################################################################################################################
# Consumption Price ####################################################################################################
########################################################################################################################
########################################################################################################################
# Create the Canadian Consumption Price dictionary by reading in information from End_-_Use_Prices.csv file
# Residential Consumption Price Read Directly, All other sectors calculated using US Consumption Prices for certain
# regions as benchmarks. Total Consumption Price calculated as weighted average using consumption
# can_cons_price stores the consumption price data for canadian regions
# cons_province_temp keeps track of the current province
# year_shift tracks of where the list of years begins in the data file
def cons_price_1():
    for cons_sector in ['Residential', 'Commercial', 'Industrial']:
        f_can_cons_price_csv = open(Fx.include('End_-_Use_Prices_' + cons_sector + '.csv'), 'r')
        file_reader = csv.reader(f_can_cons_price_csv, delimiter=',')
        year_shift = 0
        province_temp = ''
        for row in file_reader:
            if Fx.year_sh(row, '_'):
                # Read in correct data based on year
                year_shift = Fx.year_sh(row, '_')
            if row[0] in Ar.canadian_provinces_full:
                province_temp = row[0]
            if row[0] == Ar.resource and province_temp != '':
                for index, element in enumerate(row):
                    if index+Ar.years[0]-year_shift in Ar.years:
                        Ar.can_cons_price_raw[cons_sector][province_temp][index + Ar.years[0] - year_shift] = \
                            float(element)
                        for month in Ar.months:
                            Ar.all_cons_price[cons_sector][
                                Ar.states_acronyms_to_2_dict[Ar.all_states_dict[province_temp]]][
                                month + '-' + str(index + Ar.years[0] - year_shift)] = float(element)
        f_can_cons_price_csv.close()
        for year in Ar.years:
            for region in Ar.canadian_regions_acronyms:
                for province in Ar.provinces_to_regions[region]:
                    Ar.can_cons_price[cons_sector][region][year] += \
                        Ar.can_cons_raw[cons_sector][Ar.reverse_provinces_dict[province]][year] * \
                        Ar.can_cons_price_raw[cons_sector][Ar.reverse_provinces_dict[province]][year]
                try:
                    Ar.can_cons_price[cons_sector][region][year] /= Ar.can_cons[cons_sector][region][year]
                except ZeroDivisionError:
                    Ar.can_cons_price[cons_sector][region][year] = 0
    for cons_sector in ['Transportation', 'Electric Power']:
        for can_province in Ar.canadian_provinces_acronyms2:
            for year in Ar.years:
                for month in Ar.months:
                    try:
                        Ar.all_cons_price[cons_sector][can_province][month + '-' + str(year)] = \
                            Ar.all_cons_price['Industrial'][can_province][
                                month + '-' + str(year)] * sum(
                                [Ar.usa_cons_price[cons_sector][nangam_region][year] for nangam_region in
                                 Ar.can_cons_nangam_regions]) / sum([Ar.usa_cons_price['Industrial'][
                                                                         nangam_region][year] for nangam_region
                                                                     in Ar.can_cons_nangam_regions])
                    except TypeError:
                        continue
        for can_region in Ar.canadian_regions_acronyms:
            for year in Ar.years:
                try:
                    # Fill in can_cons_price with consumption price data for all years and regions based on the ratio of
                    # consumption price in other sectors to residential sector for select nangam regions as a benchmark
                    Ar.can_cons_price[cons_sector][can_region][year] = Ar.can_cons_price['Industrial'][can_region][
                                                                           year] * sum(
                        [Ar.usa_cons_price[cons_sector][nangam_region][year] for nangam_region in
                         Ar.can_cons_nangam_regions]) / sum([Ar.usa_cons_price['Industrial'][
                                                                                nangam_region][year] for nangam_region
                                                            in Ar.can_cons_nangam_regions])
                except TypeError:
                    Ar.can_cons_price[cons_sector][can_region][year] = 0


########################################################################################################################
# Aggregates the data into the "All Sectors" key by summing up consumption prices, weighted by consumption, for
# consumption sectors then dividing by total consumption
def cons_price_2():
    for region in Ar.canadian_regions_acronyms:
        for year in Ar.years:
            try:
                # Average consumption price per region weighted by consumption
                Ar.can_cons_price["All Sectors"][region][year] = sum([Ar.can_cons_price[cons_sector][region][year] *
                                                                      Ar.can_cons[cons_sector][region][year] for
                                                                      cons_sector in Ar.cons_sectors if cons_sector
                                                                      != "All Sectors"]) / sum(
                    [Ar.can_cons[cons_sector][region][year] for cons_sector
                     in Ar.cons_sectors if cons_sector != "All Sectors"])
            except ZeroDivisionError:
                Ar.can_cons_price["All Sectors"][region][year] = 0


########################################################################################################################
########################################################################################################################
# Convert Units ########################################################################################################
########################################################################################################################
########################################################################################################################
# Convert PJ/Year to BCF/Day (0.948/365 Conversion Factor)
def conversion():
    Fx.convert(Ar.can_cons, 3, 0.948 / 365)
