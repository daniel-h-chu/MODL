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
    can_prod_raw_province_temp = ''
    year_shift = 0
    for row in file_reader:
        if row[0] in Ar.canadian_provinces_full:
            can_prod_raw_province_temp = row[0]
        if Fx.year_sh(row, '_'):
            year_shift = Fx.year_sh(row, '_')
        if row[0] == 'Total' and can_prod_raw_province_temp != '':
            for index, element in enumerate(row):
                if index+Ar.years[0]-year_shift in Ar.years:
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
    f_can_prod_price_csv = open(Fx.include('Natural_Gas_Imports_and_Exports.csv'), 'r')
    file_reader = csv.reader(f_can_prod_price_csv, delimiter=',')
    year_shift = 0
    for row in file_reader:
        if Fx.year_sh(row, ''):
            year_shift = Fx.year_sh(row, '')
        # SPECIAL STATISTIC FOR CANADIAN PRICE
        if row[0] == "From Canada":
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    for region in Ar.canadian_regions_acronyms:
                        Ar.can_prod_price['ONS'][region][index + Ar.years[0] - year_shift] = float(element)
    f_can_prod_price_csv.close()


########################################################################################################################
# Aggregates the raw data into the "Total" key by summing up the production for Offshore and Onshore
def prod_price_2():
    for region in Ar.canadian_regions_acronyms:
        for year in Ar.years:
            Ar.can_prod_price["Total"][region][year] = sum([Ar.can_prod_price[stat][region][year] for stat in
                                                            Ar.prod_stats_acronyms if stat != "Total"]) / sum(
                [1 for stat
                 in Ar.prod_stats_acronyms if Ar.can_prod_price[stat][region][year] != 0 and stat != "Total"])


########################################################################################################################
########################################################################################################################
# Consumption Raw Data #################################################################################################
########################################################################################################################
########################################################################################################################
# Create the Canadian Population dictionary using data from '1710000501-eng.csv'
# can_pop_ratio_raw stores the raw population amounts
# can_pop_ratio stores the proportion of the province's population to Canada's population
def cons_1():
    f_can_pop_csv = open(Fx.include('1710000501-eng.csv'), 'r')
    file_reader = csv.reader(f_can_pop_csv, delimiter='\t')
    for row in file_reader:
        try:
            if row[0] in Ar.canadian_provinces_full:
                Ar.can_pop_ratio_raw[Ar.provinces_dict[row[0]]] = row[-1].replace(",", "")
        except IndexError:
            continue
    for region in Ar.canadian_regions_acronyms:
        Ar.can_pop_ratio[region] = sum([float(Ar.can_pop_ratio_raw[province]) for province in
                                        Ar.provinces_to_regions[region]]) / sum([float(Ar.can_pop_ratio_raw[province])
                                                                                 for province in
                                                                                 Ar.canadian_provinces_acronyms])
    f_can_pop_csv.close()


########################################################################################################################
# Create the Canadian Consumption dictionary (Minus Electricity) by reading in information from End_-_Use_Demand.csv
# can_cons stores the consumption data for canadian regions
# cons_sector_temp keeps track of the current consumption sector
# year_shift tracks of where the list of years begins in the data file
def cons_2():
    f_can_end_dem_csv = open(Fx.include('End_-_Use_Demand.csv'), 'r')
    file_reader = csv.reader(f_can_end_dem_csv, delimiter=',')
    cons_sector_temp = ''
    year_shift = 0
    for row in file_reader:
        if row[0] in Ar.cons_sectors:
            cons_sector_temp = row[0]
        if Fx.year_sh(row, '_'):
            year_shift = Fx.year_sh(row, '_')
        if cons_sector_temp != '' and row[0] == Ar.resource:
            for index, element in enumerate(row):
                if index+Ar.years[0]-year_shift in Ar.years:
                    for region in Ar.canadian_regions_acronyms:
                        Ar.can_cons[cons_sector_temp][region][index + Ar.years[0] - year_shift] = float(element) * \
                                                                                                  Ar.can_pop_ratio[
                                                                                                      region]
    f_can_end_dem_csv.close()
    os.remove(Fx.include('End_-_Use_Demand.csv'))


########################################################################################################################
# Gets data for Canadian electricity consumption from Primary_Energy_Demand.csv
# cons_sector_temp keeps track of whether the current sector is 'Electric Generation'
# year_shift tracks of where the list of years begins in the data file
def cons_3():
    f_can_eng_dem_csv = open(Fx.include('Primary_Energy_Demand.csv'), 'r')
    file_reader = csv.reader(f_can_eng_dem_csv, delimiter=',')
    cons_sector_temp = ''
    year_shift = 0
    for row in file_reader:
        # SPECIAL STATISTIC FOR ELECTRICITY
        if row[0] == 'Electric Generation':
            cons_sector_temp = row[0]
        if Fx.year_sh(row, '_'):
            year_shift = Fx.year_sh(row, '_')
        if cons_sector_temp != '' and row[0] == Ar.resource:
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    Ar.can_cons_eng_dem[index + Ar.years[0] - year_shift] = float(element)
    f_can_eng_dem_csv.close()
    os.remove(Fx.include('Primary_Energy_Demand.csv'))


########################################################################################################################
# Create the Canadian Consumption for Electric Power using 'Electric_Generation.csv'
# can_cons_province_temp keeps track of current province
# year_shift tracks of where the list of years begins in the data file
def cons_4():
    f_can_elc_gen_csv = open(Fx.include('Electricity_Generation.csv'), 'r')
    file_reader = csv.reader(f_can_elc_gen_csv, delimiter=',')
    can_cons_province_temp = ''
    year_shift = 0
    for row in file_reader:
        if row[0] in Ar.canadian_provinces_full:
            can_cons_province_temp = row[0]
        if Fx.year_sh(row, '_'):
            year_shift = Fx.year_sh(row, '_')
        if can_cons_province_temp != '' and row[0] == Ar.resource:
            for index, element in enumerate(row):
                if index+Ar.years[0]-year_shift in Ar.years:
                    Ar.can_elc_gen_ratio_raw[Ar.provinces_dict[can_cons_province_temp]][
                        index + Ar.years[0] - year_shift] = float(element)
    for region in Ar.canadian_regions_acronyms:
        for year in Ar.years:
            try:
                Ar.can_elc_gen_ratio[region][year] = sum(
                    [float(Ar.can_elc_gen_ratio_raw[province][year]) for province in
                     Ar.provinces_to_regions[region]]) / \
                                                     sum([float(Ar.can_elc_gen_ratio_raw[province][year]) for province
                                                          in Ar.canadian_provinces_acronyms])
            except TypeError:
                Ar.can_elc_gen_ratio[region][year] = 0
            except ZeroDivisionError:
                Ar.can_elc_gen_ratio[region][year] = 0
    for region in Ar.canadian_regions_acronyms:
        for year in Ar.years:
            try:
                # SPECIAL STATISTIC FOR ELECTRIC POWER
                Ar.can_cons["Electric Power"][region][year] = Ar.can_cons_eng_dem[year] * \
                                                              Ar.can_elc_gen_ratio[region][year]
            except TypeError:
                Ar.can_cons["Electric Power"][region][year] = 0
    f_can_elc_gen_csv.close()
    os.remove(Fx.include('Electricity_Generation.csv'))


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
    f_can_cons_price_csv = open(Fx.include('End_-_Use_Prices.csv'), 'r')
    file_reader = csv.reader(f_can_cons_price_csv, delimiter=',')
    year_shift = 0
    for row in file_reader:
        if Fx.year_sh(row, '_'):
            year_shift = Fx.year_sh(row, '_')
        if row[0] == Ar.resource:
            for index, element in enumerate(row):
                if index+Ar.years[0]-year_shift in Ar.years:
                    # SPECIAL STATISTIC FOR RESIDENTIAL
                    for region in Ar.canadian_regions_acronyms:
                        Ar.can_cons_price['Residential'][region][index + Ar.years[0] - year_shift] = float(element)
    f_can_cons_price_csv.close()
    for cons_sector in [cons_sector for cons_sector in Ar.cons_sectors if cons_sector != 'All Sectors']:
        for can_region in Ar.canadian_regions_acronyms:
            for year in Ar.years:
                try:
                    Ar.can_cons_price[cons_sector][can_region][year] = Ar.can_cons_price['Residential'][can_region][
                                                                           year] * sum(
                        [Ar.usa_cons_price[cons_sector][nangam_region][year] for nangam_region in
                         Ar.can_cons_nangam_regions]) / sum([Ar.usa_cons_price['Residential'][
                                                                                nangam_region][year] for nangam_region
                                                            in Ar.can_cons_nangam_regions])
                except TypeError:
                    Ar.can_cons_price[cons_sector][can_region][year] = 0
    for region in Ar.canadian_regions_acronyms:
        for year in Ar.years:
            try:
                Ar.can_cons_price['All Sectors'][region][year] = sum([Ar.can_cons[cons_sector][region][year] *
                                                                      Ar.can_cons_price[cons_sector][region][year] for
                                                                      cons_sector in Ar.cons_sectors if cons_sector !=
                                                                     'All Sectors']) / \
                                                                 sum([Ar.can_cons[cons_sector][region][year] for
                                                                      cons_sector in Ar.cons_sectors if cons_sector !=
                                                                     'All Sectors'])
            except ZeroDivisionError:
                Ar.can_cons_price['All Sectors'][region][year] = 0


########################################################################################################################
# Aggregates the data into the "All Sectors" key by summing up consumption prices, weighted by consumption, for
# consumption sectors then dividing by total consumption
def cons_price_2():
    for region in Ar.canadian_regions_acronyms:
        for year in Ar.years:
            try:
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
