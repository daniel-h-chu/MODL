# MEX_Functions generates dictionaries for Mexican Production, Production Price, Consumption, and Consumption Price
########################################################################################################################
########################################################################################################################
########################################################################################################################
import csv
import Functions as Fx
import Arrays as Ar


########################################################################################################################
########################################################################################################################
# Production Raw Data ##################################################################################################
########################################################################################################################
########################################################################################################################
# Create the Mexican Production dictionary by reading in information from reg_bal_mex.csv
# mex_prod stores the Production Data for Mexico
# mex_prod_region_temp keeps track of the current province for which data is being entered into
# year_shift tracks of where the list of years begins in the data file
def prod_1():
    f_mex_csv = open(Fx.include('reg_bal_mex.csv'), 'r')
    file_reader = csv.reader(f_mex_csv, delimiter=',')
    # What region we are dealing with
    mex_prod_region_temp = ''
    year_shift = 0
    for row in file_reader:
        if row[0] in Ar.mex_regions_acronyms:
            mex_prod_region_temp = row[0]
        if Fx.year_sh(row, ''):
            # Read in correct data based on year
            year_shift = Fx.year_sh(row, '')
        if mex_prod_region_temp != '' and row[0] == Ar.production:
            for index, element in enumerate(row):
                if index+Ar.years[0]-year_shift in Ar.years:
                    try:
                        Ar.mex_prod['ONS'][mex_prod_region_temp][index + Ar.years[0] - year_shift] = float(element)
                    except TypeError:
                        Ar.mex_prod['ONS'][mex_prod_region_temp][index + Ar.years[0] - year_shift] = 0
                    except ValueError:
                        Ar.mex_prod['ONS'][mex_prod_region_temp][index + Ar.years[0] - year_shift] = 0
    f_mex_csv.close()


########################################################################################################################
# Aggregates the raw data into the "Total" key by summing up the production for Offshore and Onshore
def prod_2():
    for region in Ar.mex_regions_acronyms:
        for year in Ar.years:
            Ar.mex_prod["Total"][region][year] = sum([Ar.mex_prod[stat][region][year] for stat in
                                                      Ar.prod_stats_acronyms if stat != "Total"])


########################################################################################################################
########################################################################################################################
# Production Price #####################################################################################################
########################################################################################################################
########################################################################################################################
# Create the Mexican Production Price dictionary by reading in information from Natural_Gas_Imports_and_Exports.csv
# mex_cons stores the Production Price Data for Mexico
# year_shift tracks of where the list of years begins in the data file
def prod_price_1():
    f_mex_prod_price_csv = open(Fx.include('Natural_Gas_Imports_and_Exports.csv'), 'r')
    file_reader = csv.reader(f_mex_prod_price_csv, delimiter=',')
    year_shift = 0
    for row in file_reader:
        if Fx.year_sh(row, ''):
            # Read in correct data based on year
            year_shift = Fx.year_sh(row, '')
        # SPECIAL STATISTIC FOR MEXICAN PRICE
        if row[0] == "From Mexico":
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    for region in Ar.mex_regions_acronyms:
                        if Ar.mex_prod['ONS'][region][index + Ar.years[0] - year_shift] != 0:
                            Ar.mex_prod_price['ONS'][region][index + Ar.years[0] - year_shift] = float(element)
                        else:
                            Ar.mex_prod_price['ONS'][region][index + Ar.years[0] - year_shift] = 0
    f_mex_prod_price_csv.close()


########################################################################################################################
# Aggregates the raw data into the "Total" key by summing up the production for Offshore and Onshore
def prod_price_2():
    for region in Ar.mex_regions_acronyms:
        for year in Ar.years:
            prod_price_sum = sum([Ar.mex_prod_price[stat][region][year] for stat in Ar.prod_stats_acronyms if stat !=
                                  "Total"])
            if prod_price_sum != 0:
                Ar.mex_prod_price["Total"][region][year] = prod_price_sum / sum([1 for stat in Ar.prod_stats_acronyms if
                                                                                 Ar.mex_prod_price[stat][region][
                                                                                     year] != 0 and stat != "Total"])


########################################################################################################################
########################################################################################################################
# Consumption Raw Data #################################################################################################
########################################################################################################################
########################################################################################################################
# Create the Mexican Consumption dictionary by reading in information from reg_bal_mex.csv
# mex_cons stores the Consumption Data for Mexico
# mex_cons_region_temp keeps track of the current province for which data is being entered into
# year_shift tracks of where the list of years begins in the data file
def cons_1():
    f_mex_csv = open(Fx.include('reg_bal_mex.csv'), 'r')
    file_reader = csv.reader(f_mex_csv, delimiter=',')
    # What Mexican Region we are dealing with
    mex_cons_region_temp = ''
    year_shift = 0
    for row in file_reader:
        if row[0] in Ar.mex_regions_acronyms:
            mex_cons_region_temp = row[0]
        if Fx.year_sh(row, ''):
            # Read in correct data based on year
            year_shift = Fx.year_sh(row, '')
        if mex_cons_region_temp != '' and row[0] in Ar.cons_sectors:
            for index, element in enumerate(row):
                if index+Ar.years[0]-year_shift in Ar.years:
                    try:
                        Ar.mex_cons[row[0]][mex_cons_region_temp][index + Ar.years[0] - year_shift] = float(element)
                    except TypeError:
                        Ar.mex_cons[row[0]][mex_cons_region_temp][index + Ar.years[0] - year_shift] = 0
                    except ValueError:
                        Ar.mex_cons[row[0]][mex_cons_region_temp][index + Ar.years[0] - year_shift] = 0
    f_mex_csv.close()


########################################################################################################################
########################################################################################################################
# Consumption Price ####################################################################################################
########################################################################################################################
########################################################################################################################
# Creatomg the Mexican Consumption Price Dictionary using the mex_cons_price_dict array defined in Arrays.py
# mex_cons_price stores the Consumption Price Data for Mexico
def cons_price_1():
    for cons_sector in Ar.cons_sectors:
        for region in Ar.mex_regions_acronyms:
            for year in Ar.years:
                try:
                    Ar.mex_cons_price[cons_sector][region][year] = Ar.mex_cons_price_dict[cons_sector]
                except KeyError:
                    Ar.mex_cons_price[cons_sector][region][year] = 0


########################################################################################################################
# Aggregates the data into the "All Sectors" key by summing up consumption prices for consumption sectors (weighted by
# consumption) and dividing by total consumption
def cons_price_2():
    for region in Ar.mex_regions_acronyms:
        for year in Ar.years:
            try:
                Ar.mex_cons_price["All Sectors"][region][year] = sum([Ar.mex_cons_price[cons_sector][region][year] *
                                                                      Ar.mex_cons[cons_sector][region][year] for
                                                                      cons_sector in Ar.cons_sectors if
                                                                      cons_sector != "All Sectors"]) / sum(
                    [Ar.mex_cons[cons_sector][region][year] for cons_sector
                     in Ar.cons_sectors if cons_sector != "All Sectors"])
            except ZeroDivisionError:
                Ar.mex_cons_price["All Sectors"][region][year] = 0


########################################################################################################################
########################################################################################################################
# Convert Units ########################################################################################################
########################################################################################################################
########################################################################################################################
# Convert MCF/Day to BCF/Day (1/1000 Conversion Factor)
def conversion():
    Fx.convert(Ar.mex_prod, 3, 1 / 1000)
    Fx.convert(Ar.mex_cons, 3, 1 / 1000)
