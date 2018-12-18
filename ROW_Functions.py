# ROW_Functions generates dictionaries for ROW Production and Consumption
########################################################################################################################
########################################################################################################################
########################################################################################################################
import os
import csv
import Functions as Fx
import Arrays as Ar


########################################################################################################################
########################################################################################################################
# Production ###########################################################################################################
########################################################################################################################
########################################################################################################################
# Reads production for the rest of world from World_total_natural_gas_production_by_region.csv
#
def prod_1():
    f_row_prod_csv = open(Fx.include('World_total_natural_gas_production_by_region.csv'), 'r')
    file_reader = csv.reader(f_row_prod_csv, delimiter=',')
    year_shift = 0
    # Enter data into dictionary by statistic, region, then year
    for row in file_reader:
        if Fx.year_sh(row, ''):
            year_shift = Fx.year_sh(row, '')
        if row[0] in [Ar.united_states, Ar.canada, Ar.mexico]:
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    for region in Ar.row_regions_acronyms:
                        Ar.row_prod['ONS'][region][index + Ar.years[0] - year_shift] -= float(element)
        if row[0] == Ar.total_world:
            for index, element in enumerate(row):
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
# Creates Rest of World Consumption
def cons_1():
    f_row_cons_csv = open(Fx.include('World_natural_gas_consumption_by_region.csv'), 'r')
    file_reader = csv.reader(f_row_cons_csv, delimiter=',')
    year_shift = 0
    # Enter data into dictionary by statistic, region, then year
    for row in file_reader:
        if Fx.year_sh(row, ''):
            year_shift = Fx.year_sh(row, '')
        if row[0] in [Ar.united_states, Ar.canada, Ar.mexico]:
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    for region in Ar.row_regions_acronyms:
                        Ar.row_cons_ratio[region][index + Ar.years[0] - year_shift] -= float(element)
        if row[0] == Ar.total_world:
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    for region in Ar.row_regions_acronyms:
                        Ar.row_cons_ratio[region][index + Ar.years[0] - year_shift] += float(element)
    f_row_cons_csv.close()


########################################################################################################################
# Creates Rest of World Consumption
def cons_2():
    f_row_cons = open(Fx.include('Delivered_energy_consumption_by_end-use_sector_and_fuel.csv'), 'r')
    file_reader = csv.reader(f_row_cons, delimiter=',')
    cons_sector_temp = ''
    year_shift = 0
    for row in file_reader:
        if Fx.year_sh(row, ''):
            year_shift = Fx.year_sh(row, '')
        if row[0] == Ar.resource and cons_sector_temp != '':
            for index, element in enumerate(row):
                for region in Ar.row_regions_acronyms:
                    if index + Ar.years[0] - year_shift in Ar.years:
                        if Ar.row_cons[cons_sector_temp][region][index + Ar.years[0] - year_shift] == 0:
                            Ar.row_cons[cons_sector_temp][region][index + Ar.years[0] - year_shift] = float(element)
                        if cons_sector_temp == Ar.all_sectors:
                            Ar.row_cons_ratio[region][index + Ar.years[0] - year_shift] /= float(element)
        elif row[0] in Ar.cons_sectors:
            cons_sector_temp = row[0]
    for cons_sector in Ar.cons_sectors:
        for region in Ar.row_regions_acronyms:
            for year in Ar.years:
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
