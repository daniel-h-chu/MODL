# ROW_Functions generates dictionaries for ROW Production and Consumption
########################################################################################################################
########################################################################################################################
########################################################################################################################
import csv
import Functions as Fx
import Arrays as Ar


########################################################################################################################
########################################################################################################################
# Production ###########################################################################################################
########################################################################################################################
########################################################################################################################
# Reads production directly for the rest of world from World_total_natural_gas_production_by_region.csv
def prod_1():
    f_row_prod_csv = open(Fx.include('World_total_natural_gas_production_by_region.csv'), 'r')
    file_reader = csv.reader(f_row_prod_csv, delimiter=',')
    year_shift = 0
    # Enter data into dictionary by statistic, region, then year
    for row in file_reader:
        if Fx.year_sh(row, ''):
            # Read in correct data based on year
            year_shift = Fx.year_sh(row, '')
        if row[0] in [Ar.united_states, Ar.canada, Ar.mexico]:
            for index, element in enumerate(row):
                # Subtract from rest of world production for each year if country is US, MEX, or CAN
                if index + Ar.years[0] - year_shift in Ar.years:
                    for region in Ar.row_regions_acronyms:
                        Ar.row_prod['ONS'][region][index + Ar.years[0] - year_shift] -= float(element)
        if row[0] == Ar.total_world:
            for index, element in enumerate(row):
                # Add to rest of world production for each year if country is US, MEX, or CAN
                if index + Ar.years[0] - year_shift in Ar.years:
                    for region in Ar.row_regions_acronyms:
                        Ar.row_prod['ONS'][region][index + Ar.years[0] - year_shift] += float(element)
    f_row_prod_csv.close()


########################################################################################################################
# Aggregates the raw data into the "Total" key by summing up the production for Offshore and Onshore
def prod_2():
    for region in Ar.row_regions_acronyms:
        for year in Ar.years:
            Ar.row_prod["Total"][region][year] = sum([Ar.row_prod[stat][region][year] for stat in
                                                      Ar.prod_stats_acronyms if stat != "Total"])


########################################################################################################################
########################################################################################################################
# Consumption ##########################################################################################################
########################################################################################################################
########################################################################################################################
# Reads total consumption for the rest of the world by subtracting out US, MEX, and CAN consumption from world total fro
# m World_natural_gas_consumption_by_region.csv
def cons_1():
    f_row_cons_csv = open(Fx.include('World_natural_gas_consumption_by_region.csv'), 'r')
    file_reader = csv.reader(f_row_cons_csv, delimiter=',')
    year_shift = 0
    # Enter data into dictionary by statistic, region, then year
    for row in file_reader:
        if Fx.year_sh(row, ''):
            # Read in correct data based on year
            year_shift = Fx.year_sh(row, '')
        if row[0] in [Ar.united_states, Ar.canada, Ar.mexico]:
            for index, element in enumerate(row):
                # Subtract from rest of world consumption for each year if country is US, MEX, or CAN
                if index + Ar.years[0] - year_shift in Ar.years:
                    for region in Ar.row_regions_acronyms:
                        Ar.row_cons_ratio[region][index + Ar.years[0] - year_shift] -= float(element)
        if row[0] == Ar.total_world:
            for index, element in enumerate(row):
                # Add to rest of world consumption for each year if country is US, MEX, or CAN
                if index + Ar.years[0] - year_shift in Ar.years:
                    for region in Ar.row_regions_acronyms:
                        Ar.row_cons_ratio[region][index + Ar.years[0] - year_shift] += float(element)
    f_row_cons_csv.close()


########################################################################################################################
# Computes the ratio of consumption for different sectors, then multiplies ratios with previous values for total rest of
# world consumption. Data retrieved from Delivered_energy_consumption_by_end-use_sector_and_fuel.csv
def cons_2():
    f_row_cons = open(Fx.include('Delivered_energy_consumption_by_end-use_sector_and_fuel.csv'), 'r')
    file_reader = csv.reader(f_row_cons, delimiter=',')
    # What consumption sector we are dealing with
    cons_sector_temp = ''
    year_shift = 0
    for row in file_reader:
        if Fx.year_sh(row, ''):
            # Read in correct data based on year
            year_shift = Fx.year_sh(row, '')
        if row[0] == Ar.resource and cons_sector_temp != '':
            for index, element in enumerate(row):
                for region in Ar.row_regions_acronyms:
                    if index + Ar.years[0] - year_shift in Ar.years:
                        # Set data for row_cons for consumption for each year for the rest of the world
                        if Ar.row_cons[cons_sector_temp][region][index + Ar.years[0] - year_shift] == 0:
                            Ar.row_cons[cons_sector_temp][region][index + Ar.years[0] - year_shift] = float(element)
                        # Get sector ratios by dividing consumption in an individual sector by total consumption
                        if cons_sector_temp == Ar.all_sectors:
                            Ar.row_cons_ratio[region][index + Ar.years[0] - year_shift] /= float(element)
        elif row[0] in Ar.cons_sectors:
            # Set the current sector we are dealing with
            cons_sector_temp = row[0]
    for cons_sector in Ar.cons_sectors:
        for region in Ar.row_regions_acronyms:
            for year in Ar.years:
                # Multiply the total consumption for the rest of the world by ratios that separate it into sectors
                Ar.row_cons[cons_sector][region][year] *= Ar.row_cons_ratio[region][year]
    f_row_cons.close()


########################################################################################################################
########################################################################################################################
# Convert Units ########################################################################################################
########################################################################################################################
########################################################################################################################
# Convert TCF/Year to BCF/Day (1000/365 Conversion Factor)
def conversion():
    Fx.convert(Ar.row_prod, 3, 1000 / 365)
    Fx.convert(Ar.row_cons, 3, 1000 / 365)
