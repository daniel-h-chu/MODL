# Functions lists out main functions used repeatedly in the USA, CAN, MEX, and Prod_Cons files
########################################################################################################################
########################################################################################################################
########################################################################################################################
# Import Statements
import pandas as pd
import Arrays as Ar
import os
import sys
import csv

config_name = 'myapp.cfg'

# determine if application is a script file or frozen exe

########################################################################################################################
# Absolute Path of program for file reference functions
directory = os.path.dirname(__file__)


# File Include Function


# Returns the absolute file path of an excel or csv file given the name of the file
def include(name):
    # If program is run from commandline or executable
    if os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])))[-4:] == 'dist':
        return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))) +
                            "/Include/All 2018/" + name)
    # If program is run using an IDE like Pycharm
    return os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])) + "/Include/All 2018/" + name)


# Converts an xlsx file to a csv file given a sheet name
def to_csv(name, sheet, csvname=''):
    if csvname == '':
        try:
            xls = pd.read_excel(include(name + ".xlsx"), sheet, date_parser=None, date_format='%Y')
            xls.to_csv(include(name + ".csv"), index=False, date_format='%Y')
        except FileNotFoundError:
            xls = pd.read_excel(include(name + ".xls"), sheet, date_parser=None, date_format='%Y')
            xls.to_csv(include(name + ".csv"), index=False, date_format='%Y')
    else:
        try:
            xls = pd.read_excel(include(name + ".xlsx"), sheet, date_parser=None, date_format='%Y')
            xls.to_csv(include(name + csvname + ".csv"), index=False, date_format='%Y')
        except FileNotFoundError:
            xls = pd.read_excel(include(name + ".xls"), sheet, date_parser=None, date_format='%Y')
            xls.to_csv(include(name + csvname + ".csv"), index=False, date_format='%Y')


# Checks how many years the input data file is shifted (if years[0] = 2015 is in column 5, then year_shift is set to 5)
# row is row of file_reader
# char is the string in the first cell of the row containing all the years (ex, ['_', 2015, 2016,...]
def year_sh(row, char):
    if row[0] == char:
        for index, element in enumerate(row):
            try:
                element_float = float(element)
            except ValueError:
                element_float = 0
            # If the year is equal to the first year in years then will return how much the year is shifted from the zer
            # oeth column
            if Ar.years[0] == element_float:
                return index
        return 0


# Aggregate all Produciton and Consumption Price among all Countries of the World by summing correct dictionaries of
# data for each country and then summing between multiple countries.
def aggregate():
    for year in Ar.years:
        # Create all_dict with all aggregate data (all_dict[Statistic][Country][Year][Sector])
        for country in ['Mexico', 'Canada', 'USA', 'ROW', 'Total']:
            Ar.all_dict['Production'][country][year] = dict.fromkeys(Ar.prod_stats_acronyms)
            Ar.all_dict['Production Price'][country][year] = dict.fromkeys(Ar.prod_stats_acronyms)
            Ar.all_dict['Consumption'][country][year] = dict.fromkeys(Ar.cons_sectors)
            Ar.all_dict['Consumption Price'][country][year] = dict.fromkeys(Ar.cons_sectors)
        # Aggregate Production
        for prod_stat in Ar.prod_stats_acronyms:
            Ar.all_dict['Production']['Mexico'][year][prod_stat] = sum([Ar.mex_prod[prod_stat][region][year] for
                                                                        region in Ar.mex_regions_acronyms])
            Ar.all_dict['Production']['Canada'][year][prod_stat] = sum([Ar.can_prod[prod_stat][region][year] for
                                                                        region in Ar.canadian_regions_acronyms])
            Ar.all_dict['Production']['USA'][year][prod_stat] = sum([Ar.usa_prod[prod_stat][region][year] for
                                                                     region in Ar.nangam_regions_acronyms])
            Ar.all_dict['Production']['ROW'][year][prod_stat] = sum([Ar.row_prod[prod_stat][region][year] for
                                                                     region in Ar.row_regions_acronyms])
            Ar.all_dict['Production']['Total'][year][prod_stat] = \
                sum([Ar.all_dict['Production'][country][year][prod_stat]
                     for country in ['Mexico', 'Canada', 'USA', 'ROW']])
        # Aggregate Production Price as an avearage of production price of individual regions weighted by production
        for prod_stat in Ar.prod_stats_acronyms:
            try:
                Ar.all_dict['Production Price']['Mexico'][year][prod_stat] = \
                    sum([Ar.mex_prod_price[prod_stat][region][year] * Ar.mex_prod[prod_stat][region][year] for
                         region in Ar.mex_regions_acronyms]) / Ar.all_dict['Production']['Mexico'][year][prod_stat]
            except ZeroDivisionError:
                Ar.all_dict['Production Price']['Mexico'][year][prod_stat] = 0
            try:
                Ar.all_dict['Production Price']['Canada'][year][prod_stat] = \
                    sum([Ar.can_prod_price[prod_stat][region][year] * Ar.can_prod[prod_stat][region][year] for
                         region in Ar.canadian_regions_acronyms]) / Ar.all_dict['Production']['Canada'][year][prod_stat]
            except ZeroDivisionError:
                Ar.all_dict['Production Price']['Canada'][year][prod_stat] = 0
            try:
                Ar.all_dict['Production Price']['USA'][year][prod_stat] = \
                    sum([Ar.usa_prod_price[prod_stat][region][year] * Ar.usa_prod[prod_stat][region][year] for
                         region in Ar.nangam_regions_acronyms]) / Ar.all_dict['Production']['USA'][year][prod_stat]
            except ZeroDivisionError:
                Ar.all_dict['Production Price']['USA'][year][prod_stat] = 0
            try:
                Ar.all_dict['Production Price']['ROW'][year][prod_stat] = \
                    sum([Ar.row_prod_price[prod_stat][region][year] * Ar.row_prod[prod_stat][region][year] for
                         region in Ar.row_regions_acronyms]) / Ar.all_dict['Production']['ROW'][year][prod_stat]
            except ZeroDivisionError:
                Ar.all_dict['Production Price']['ROW'][year][prod_stat] = 0
            try:
                Ar.all_dict['Production Price']['Total'][year][prod_stat] = \
                    sum([Ar.all_dict['Production'][country][year][prod_stat] *
                         Ar.all_dict['Production Price'][country][year][prod_stat]
                         for country in ['Mexico', 'Canada', 'USA', 'ROW']]) / \
                    Ar.all_dict['Production']['Total'][year][prod_stat]
            except ZeroDivisionError:
                Ar.all_dict['Production Price']['Total'][year][prod_stat] = 0
        # Aggregate consumption
        for cons_sector in Ar.cons_sectors:
            Ar.all_dict['Consumption']['Mexico'][year][cons_sector] = sum([Ar.mex_cons[cons_sector][region][year] for
                                                                           region in Ar.mex_regions_acronyms])
            Ar.all_dict['Consumption']['Canada'][year][cons_sector] = sum([Ar.can_cons[cons_sector][region][year] for
                                                                           region in Ar.canadian_regions_acronyms])
            Ar.all_dict['Consumption']['USA'][year][cons_sector] = sum([Ar.usa_cons[cons_sector][region][year] for
                                                                        region in Ar.nangam_regions_acronyms])
            Ar.all_dict['Consumption']['ROW'][year][cons_sector] = sum([Ar.row_cons[cons_sector][region][year] for
                                                                        region in Ar.row_regions_acronyms])
            Ar.all_dict['Consumption']['Total'][year][cons_sector] = \
                sum([Ar.all_dict['Consumption'][country][year][cons_sector]
                     for country in ['Mexico', 'Canada', 'USA', 'ROW']])

        # Aggregate Consumption Price as an avearage of consumption price of individual regions weighted by consumption
        for cons_sector in Ar.cons_sectors:
            try:
                Ar.all_dict['Consumption Price']['Mexico'][year][cons_sector] = \
                    sum([Ar.mex_cons_price[cons_sector][region][year] * Ar.mex_cons[cons_sector][region][year] for
                         region in Ar.mex_regions_acronyms]) / Ar.all_dict['Consumption']['Mexico'][year][cons_sector]
            except ZeroDivisionError:
                Ar.all_dict['Consumption Price']['Mexico'][year][cons_sector] = 0
            try:
                Ar.all_dict['Consumption Price']['Canada'][year][cons_sector] = \
                    sum([Ar.can_cons_price[cons_sector][region][year] * Ar.can_cons[cons_sector][region][year] for
                         region in Ar.canadian_regions_acronyms]) / \
                    Ar.all_dict['Consumption']['Canada'][year][cons_sector]
            except ZeroDivisionError:
                Ar.all_dict['Consumption Price']['Canada'][year][cons_sector] = 0
            try:
                Ar.all_dict['Consumption Price']['USA'][year][cons_sector] = \
                    sum([Ar.usa_cons_price[cons_sector][region][year] * Ar.usa_cons[cons_sector][region][year] for
                         region in Ar.nangam_regions_acronyms]) / Ar.all_dict['Consumption']['USA'][year][cons_sector]
            except ZeroDivisionError:
                Ar.all_dict['Consumption Price']['USA'][year][cons_sector] = 0
            try:
                Ar.all_dict['Consumption Price']['ROW'][year][cons_sector] = \
                    sum([Ar.row_cons_price[cons_sector][region][year] * Ar.row_cons[cons_sector][region][year] for
                         region in Ar.row_regions_acronyms]) / Ar.all_dict['Consumption']['ROW'][year][cons_sector]
            except ZeroDivisionError:
                Ar.all_dict['Consumption Price']['ROW'][year][cons_sector] = 0
            try:
                Ar.all_dict['Consumption Price']['Total'][year][cons_sector] = \
                    sum([Ar.all_dict['Consumption'][country][year][cons_sector] *
                         Ar.all_dict['Consumption Price'][country][year][cons_sector]
                         for country in ['Mexico', 'Canada', 'USA', 'ROW']]) / \
                    Ar.all_dict['Consumption']['Total'][year][cons_sector]
            except ZeroDivisionError:
                Ar.all_dict['Consumption Price']['Total'][year][cons_sector] = 0


# Writes all regions' production, production price, consumption, or consumption price
# writer is an ExcelWriter pandas object
# lines is information listed in an array that goes before the data lines = ['Production', '2015'] prints 'Production'
# on the first row first column and '2015' on the second row first column
# usa_dict, can_dict, and mex_dict are dictionaries with data to be printed
# iterable1 is the first list of keys in the previous dictionaries
# iterable3 is the third list of keys in the previous dictionaries (usually years)
# sheet is the excel sheet to write in
def write_all(writer, lines, usa_dict, can_dict, mex_dict, row_dict, iterable1, iterable3, sheet, sheet_name, agg=True,
              iterable2=Ar.all_regions_acronyms, print_full_dict=Ar.print_full_dict, print_dict=Ar.print_dict,
              ):
    dictionary = dict.fromkeys(iterable1)
    # Create a production/consumption (price) dictionary that contains data for all countries' regions
    for key in iterable1:
        dictionary[key] = {}
        dictionary[key].update(mex_dict[key])
        dictionary[key].update(can_dict[key])
        dictionary[key].update(usa_dict[key])
        dictionary[key].update(row_dict[key])
    wb = writer.book
    # Excel Formats
    f1 = wb.add_format({
        'italic': True,
        'border': 0})
    f2 = wb.add_format({
        'bold': True,
        'border': 1})
    f3 = wb.add_format({
        'bold': True,
        'border': 0})
    df = pd.DataFrame({})
    df.to_excel(writer, sheet_name=sheet_name)
    ws = writer.sheets[sheet_name]
    # Write initial lines/comments about the excel sheet
    ws.write_column(0, 0, lines)
    for index, i1 in enumerate(iterable1):
        ws.write_column(len(lines) + index * (len(iterable2) + 15) + 1, 0, [print_full_dict[i2] for i2 in iterable2],
                        f1)
        ws.write_column(len(lines) + index * (len(iterable2) + 15) + 1, 1, ['DNG'] * len(iterable2))
        # If production (4 columns of metadata)
        if iterable1 == Ar.prod_stats_acronyms:
            ws.write_row(len(lines) + index * (len(iterable2) + 15), 0, [print_dict[i1], '', '', ''] + iterable3, f2)
            ws.write_column(len(lines) + index * (len(iterable2) + 15) + 1, 2, [i1] * len(iterable2))
            ws.write_column(len(lines) + index * (len(iterable2) + 15) + 1, 3, [i2 for i2 in iterable2], f3)
            for index2, i3 in enumerate(iterable3):
                ws.write_column(len(lines) + index * (len(iterable2) + 15) + 1, index2 + 4,
                                [dictionary[i1][i2][i3] for i2 in iterable2])
            if agg:
                ws.write_row(len(lines) + (1 + index) * (len(iterable2) + 15) - 13, 0, ['Aggregate'], f3)
                ws.write_row(len(lines) + (1 + index) * (len(iterable2) + 15) - 8, 0, ['Total'], f3)
                for _index, country in enumerate(['Mexico', 'Canada', 'USA', 'ROW']):
                    ws.write_row(len(lines) + (1 + index) * (len(iterable2) + 15) - 12 + _index, 0,
                                 ['', 'DNG', country, '']
                                 + [Ar.all_dict[sheet][country][year][i1] for year in Ar.years])
                ws.write_row(len(lines) + (1 + index) * (len(iterable2) + 15) - 7, 0, ['', 'DNG', 'Total', ''] +
                             [Ar.all_dict[sheet]['Total'][year][i1] for year in Ar.years])
        # If consumption (3 Columns of metadata)
        else:
            ws.write_row(len(lines) + index * (len(iterable2) + 15), 0, [print_dict[i1], '', ''] + iterable3, f2)
            ws.write_column(len(lines) + index * (len(iterable2) + 15) + 1, 2, [i2 for i2 in iterable2], f3)
            for index2, i3 in enumerate(iterable3):
                ws.write_column(len(lines) + index * (len(iterable2) + 15) + 1, index2 + 3,
                                [dictionary[i1][i2][i3] for i2 in iterable2])
            if agg:
                ws.write_row(len(lines) + (1 + index) * (len(iterable2) + 15) - 13, 0, ['Aggregate'], f3)
                ws.write_row(len(lines) + (1 + index) * (len(iterable2) + 15) - 8, 0, ['Total'], f3)
                for _index, country in enumerate(['Mexico', 'Canada', 'USA', 'ROW']):
                    ws.write_row(len(lines) + (1 + index) * (len(iterable2) + 15) - 12 + _index, 0,
                                 ['', 'DNG', country] +
                                 [Ar.all_dict[sheet][country][year][i1] for year in Ar.years])
                ws.write_row(len(lines) + (1 + index) * (len(iterable2) + 15) - 7, 0, ['', 'DNG', 'Total'] +
                             [Ar.all_dict[sheet]['Total'][year][i1] for year in Ar.years])


# Expend columns in the list of excel sheets (sheet_list) using an ExcelWriter pandas object (writer)
def style_sheet(writer, sheet_list):
    for sheet in sheet_list:
        ws = writer.sheets[sheet]
        ws.set_column('A:A', 20)


# Writes piping capacity between all regions
# writer is an ExcelWriter pandas object
# lines is information listed in an array that goes before the data lines = ['Production', '2015'] prints 'Production'
# on the first row first column and '2015' on the second row first column
# sheet is the excel sheet to write in
def write_cap(writer, lines, sheet):
    wb = writer.book
    f1 = wb.add_format({
        'italic': True,
        'border': 0})
    f2 = wb.add_format({
        'bold': True,
        'border': 1})
    df = pd.DataFrame({})
    df.to_excel(writer, sheet_name=sheet)
    ws = writer.sheets[sheet]
    ws.write_column(0, 0, lines)
    # Write metadata
    ws.write_column(len(lines), 0, [''] + [region_full for region_full in Ar.states_full], f1)
    ws.write_column(len(lines), 1, [''] + [region_acronym for region_acronym in Ar.states_acronyms2], f2)
    ws.write_row(len(lines) - 1, 2, [region_full for region_full in Ar.states_full], f1)
    ws.write_row(len(lines), 2, [region_acronym for region_acronym in Ar.states_acronyms2], f2)
    for index, region_acronym in enumerate(Ar.states_acronyms2):
        # Write data by individual columns
        ws.write_column(1 + len(lines), index + 2, [Ar.pip_cap[region_acronym][region_acronym2] for region_acronym2 in
                                                    Ar.states_acronyms2])
    pd.DataFrame(Ar.planned, columns=Ar.planned_cols).to_excel(writer, sheet_name='Proposed Pipelines', index=False)


# Writes piping flow between all regions
# writer is an ExcelWriter pandas object
# lines is information listed in an array that goes before the data lines = ['Production', '2015'] prints 'Production'
# on the first row first column and '2015' on the second row first column
# sheet is the excel sheet to write in
def write_flow(writer, lines, sheet, dictionary):
    wb = writer.book
    f1 = wb.add_format({
        'italic': True,
        'border': 0})
    f2 = wb.add_format({
        'bold': True,
        'border': 1})
    df = pd.DataFrame({})
    df.to_excel(writer, sheet_name=sheet)
    ws = writer.sheets[sheet]
    ws.write_column(0, 0, lines)
    ws.write_row(len(lines), 0, ['Region To (Name)', 'Region From (Name)', 'Units', 'Region To', 'Region From'] +
                 Ar.years_months, f2)
    index = len(lines) + 1
    for state_from in Ar.states_acronyms2:
        for state_to in Ar.states_acronyms2:
            try:
                if dictionary[state_from][state_to][Ar.years_months[0]] != 0:
                    # Write metadata and data as rows
                    ws.write_row(index, 0,
                                 [Ar.print_full_dict_state[state_to], Ar.print_full_dict_state[state_from], 'Bcd/d'],
                                 f1)
                    ws.write_row(index, 3, [state_to, state_from], f2)
                    ws.write_row(index, 5,
                                 [dictionary[state_from][state_to][month_year] for month_year in Ar.years_months])
                    index += 1
                # print(state_from, state_to)
            except KeyError:
                continue
    ws.set_column('A:B', 20)


# Multiply all data in a dictionary by a factor
# dictionary is the dictionary of data to be converted
# degree is the number of keys in the dictionary (typically 3)
# factor is the factor to be multiplied by
def convert(dictionary, degree, factor):
    if degree > 1:
        for key in dictionary.keys():
            convert(dictionary[key], degree - 1, factor)
    else:
        for key in dictionary.keys():
            dictionary[key] *= factor


def return_dict(usa_dict, can_dict, mex_dict, row_dict, iterable1):
    dictionary = dict.fromkeys(iterable1)
    # Create a production/consumption (price) dictionary that contains data for all countries' regions
    for key in iterable1:
        dictionary[key] = {}
        dictionary[key].update(mex_dict[key])
        dictionary[key].update(can_dict[key])
        dictionary[key].update(usa_dict[key])
        dictionary[key].update(row_dict[key])
    return dictionary


def monthify_statify():
    f_prod_state = open(include('new_output_production.csv'), 'r')
    file_reader = csv.reader(f_prod_state, delimiter=',')
    year_shift = 1
    for row in file_reader:
        if row[0] in Ar.states_full:
            for index, element in enumerate(row):
                if 12 >= index - year_shift >= 1:
                    Ar.prod_state_month[Ar.all_states_dict[row[0]]][index - year_shift] = float(element)
    f_prod_state.close()
    f_cons_state = open(include('new_output_consumption.csv'), 'r')
    file_reader = csv.reader(f_cons_state, delimiter=',')
    year_shift = 1
    temp_sector = ''
    for row in file_reader:
        if row[0] in Ar.cons_sectors_months:
            temp_sector = Ar.cons_month_dict[row[0]]
        if row[0] in Ar.states_full:
            for index, element in enumerate(row):
                if 12 >= index - year_shift >= 1:
                    Ar.cons_state_month[temp_sector][Ar.all_states_dict[row[0]]][index - year_shift] = float(element)
    f_cons_state.close()
    Ar.all_prod_raw = return_dict(Ar.usa_prod, Ar.can_prod, Ar.mex_prod, Ar.row_prod, Ar.prod_stats_acronyms)
    for prod_stat in Ar.prod_stats_acronyms:
        for state in Ar.states_acronyms:
            for region in Ar.all_to_states_dict.keys():
                if state in Ar.all_to_states_dict[region]:
                    for year in Ar.years:
                        for month in range(1, 13):
                            if state in Ar.mex_regions_acronyms + Ar.row_regions_acronyms:
                                Ar.all_prod_month[prod_stat][state][year][month] = Ar.all_prod_raw[prod_stat][state][
                                                                                       year] / 12
                                continue
                            try:
                                Ar.all_prod_month[prod_stat][state][year][month] = \
                                    Ar.prod_state_month[state][month] * Ar.all_prod_raw[prod_stat][region][
                                        year] / sum(
                                        [sum([Ar.prod_state_month[state][month] for month in range(1, 13)]) for
                                         state in Ar.all_to_states_dict[region]])
                            except ZeroDivisionError:
                                Ar.all_prod_month[prod_stat][state][year][month] = 0
    Ar.all_cons_raw = return_dict(Ar.usa_cons, Ar.can_cons, Ar.mex_cons, Ar.row_cons, Ar.cons_sectors)
    for cons_sector in Ar.cons_sectors:
        for state in Ar.states_acronyms:
            for region in Ar.all_to_states_dict.keys():
                if state in Ar.all_to_states_dict[region]:
                    for year in Ar.years:
                        for month in range(1, 13):
                            if state in Ar.mex_regions_acronyms + Ar.row_regions_acronyms:
                                Ar.all_cons_month[cons_sector][state][year][month] = \
                                    Ar.all_cons_raw[cons_sector][state][
                                    year] / 12
                                continue
                            try:
                                Ar.all_cons_month[cons_sector][state][year][month] = \
                                    Ar.cons_state_month[cons_sector][state][month] * \
                                    Ar.all_cons_raw[cons_sector][region][
                                        year] / sum(
                                        [sum([Ar.cons_state_month[cons_sector][state][month] for month in range(1, 13)])
                                         for
                                         state in Ar.all_to_states_dict[region]])
                            except ZeroDivisionError:
                                Ar.all_cons_month[cons_sector][state][year][month] = 0
    for state, state2 in zip(Ar.states_acronyms, Ar.states_acronyms2):
        for cons_sector in Ar.cons_sectors:
            for year in Ar.years:
                for month in range(1, 13):
                    try:
                        Ar.all_cons[cons_sector][state2][str(Ar.months[month - 1]) + '-' + str(year)] = \
                            Ar.all_cons_month[cons_sector][state][year][month]
                    except KeyError:
                        continue
        for prod_stat in Ar.prod_stats_acronyms:
            for year in Ar.years:
                for month in range(1, 13):
                    try:
                        Ar.all_prod[prod_stat][state2][str(Ar.months[month - 1]) + '-' + str(year)] = \
                            Ar.all_prod_month[prod_stat][state][year][month]
                    except KeyError:
                        continue
    for province in Ar.canadian_provinces_acronyms2:
        for year in Ar.years:
            for month in Ar.months:
                try:
                    Ar.all_cons_price["All Sectors"][province][month + '-' + str(year)] = sum(
                        [Ar.all_cons_price[cons_sector][province][month + '-' + str(year)] *
                         Ar.all_cons[cons_sector][province][month + '-' + str(year)] for
                         cons_sector in Ar.cons_sectors if cons_sector
                         != "All Sectors"]) / sum(
                        [Ar.all_cons[cons_sector][province][month + '-' + str(year)] for cons_sector
                         in Ar.cons_sectors if
                         cons_sector != "All Sectors" and Ar.all_cons_price[cons_sector][province][
                             month + '-' + str(year)] != 0])
                except ZeroDivisionError:
                    continue
    for cons_sector, file_name in zip(['Commercial', 'Transportation', 'Electric Power', 'Industrial', 'Residential'],
                                      ['NG_PRI_SUM_A_EPG0_PCS_DMCF_M.csv', 'NG_PRI_SUM_A_EPG0_PDV_DMCF_A.csv',
                                       'NG_PRI_SUM_A_EPG0_PEU_DMCF_M.csv', 'NG_PRI_SUM_A_EPG0_PIN_DMCF_M.csv',
                                       'NG_PRI_SUM_A_EPG0_PRS_DMCF_M.csv']):
        f_cons_price_state = open(include(file_name))
        file_reader_imp = csv.reader(f_cons_price_state, delimiter=',')
        locations = []
        cons_price_state_raw = []
        for index, row in enumerate(file_reader_imp):
            if index == 2:
                locations = row
            if row[0][:4] == str(Ar.years[0] - 1):
                cons_price_state_raw.append(row)
            if row[0][:4] == '2012' and cons_sector == 'Transportation':
                cons_price_state_raw.append(row)
        for index, element in enumerate(locations):
            for index2, month in enumerate(Ar.months):
                try:
                    if cons_sector == 'Transportation':
                        temp_state = element[:element.find(Ar.resource) - 1]
                        Ar.usa_cons_price_raw[cons_sector][
                            Ar.states_acronyms_to_2_dict[Ar.all_states_dict[temp_state]]][month] = \
                            float(cons_price_state_raw[0][index])
                    if element.find(Ar.price_resource) == -1:
                        temp_state = element[:element.find(Ar.resource) - 1]
                        Ar.usa_cons_price_raw[cons_sector][
                            Ar.states_acronyms_to_2_dict[Ar.all_states_dict[temp_state]]][month] = \
                            float(cons_price_state_raw[index2][index])
                    else:
                        temp_state = element[:element.find(Ar.price_resource) - 1]
                        Ar.usa_cons_price_raw[cons_sector][
                            Ar.states_acronyms_to_2_dict[Ar.all_states_dict[temp_state]]][month] = \
                            float(cons_price_state_raw[index2][index])
                except ValueError:
                    continue
                except KeyError:
                    continue
                except IndexError:
                    continue
        for state in Ar.usa_states_acronyms2:
            for year in Ar.years:
                for month in Ar.months:
                    for nangam_region in Ar.nangam_regions_acronyms:
                        if Ar.states2_dict[state] in Ar.states_to_regions[nangam_region]:
                            try:
                                Ar.all_cons_price[cons_sector][state][month + '-' + str(year)] = \
                                    Ar.usa_cons_price_raw[cons_sector][state][month] / \
                                    Ar.usa_cons_price[cons_sector][nangam_region][
                                        Ar.years[0]] * Ar.usa_cons_price[cons_sector][nangam_region][year]
                            except ZeroDivisionError:
                                continue
        for mex_region in Ar.mex_regions_acronyms:
            for year in Ar.years:
                for month in Ar.months:
                    Ar.all_cons_price[cons_sector][mex_region][month + '-' + str(year)] = \
                        Ar.mex_cons_price[cons_sector][mex_region][year]
        for row_region in Ar.row_regions_acronyms:
            for year in Ar.years:
                for month in Ar.months:
                    Ar.all_cons_price[cons_sector][row_region][month + '-' + str(year)] = \
                        Ar.row_cons_price[cons_sector][row_region][year]
    for state in Ar.states_acronyms2:
        for month_year in Ar.years_months:
            try:
                Ar.all_cons_price["All Sectors"][state][month_year] = sum(
                    [Ar.all_cons[cons_sector][state][month_year] * Ar.all_cons_price[cons_sector][state][month_year] for
                     cons_sector in Ar.cons_sectors]) / sum(
                    [Ar.all_cons[cons_sector][state][month_year] for cons_sector in Ar.cons_sectors if
                     cons_sector != "All Sectors" and Ar.all_cons_price[cons_sector][state][month_year] != 0])
            except ZeroDivisionError:
                continue
    for prod_stat in Ar.prod_stats_acronyms:
        for year in Ar.years:
            for month in Ar.months:
                for state in Ar.usa_states_acronyms2:
                    for nangam_region in Ar.nangam_regions_acronyms:
                        if Ar.states2_dict[state] in Ar.states_to_regions[nangam_region]:
                            Ar.all_prod_price[prod_stat][state][month + '-' + str(year)] = \
                                Ar.usa_prod_price[prod_stat][nangam_region][
                                    year]
                for province in Ar.canadian_provinces_acronyms2:
                    for canadian_region in Ar.canadian_regions_acronyms:
                        if Ar.provinces2_dict[province] in Ar.provinces_to_regions[canadian_region]:
                            Ar.all_prod_price[prod_stat][province][month + '-' + str(year)] = \
                                Ar.can_prod_price[prod_stat][canadian_region][year]
                for mex_region in Ar.mex_regions_acronyms:
                    Ar.all_prod_price[prod_stat][mex_region][month + '-' + str(year)] = \
                        Ar.mex_prod_price[prod_stat][mex_region][year]
                for row_region in Ar.row_regions_acronyms:
                    Ar.all_prod_price[prod_stat][row_region][month + '-' + str(year)] = \
                        Ar.row_prod_price[prod_stat][row_region][year]
    writer = pd.ExcelWriter(include('Monthly Output.xlsx'), engine='xlsxwriter')
    empty_prod_dict = {prod_stat: {} for prod_stat in Ar.prod_stats_acronyms}
    empty_cons_dict = {cons_sector: {} for cons_sector in Ar.cons_sectors}
    # Write all Production Data
    write_all(writer, ['Production', 'BCF/Day', str(Ar.years[0]) + ' to ' + str(Ar.years[-1]), '', '', '', ''],
              Ar.all_prod, empty_prod_dict, empty_prod_dict, empty_prod_dict, Ar.prod_stats_acronyms, Ar.years_months,
              'Production', sheet_name='Production Monthly', iterable2=list(Ar.all_prod['Total'].keys()),
              print_full_dict=Ar.print_full_dict_state, agg=False)
    write_all(writer,
              ['Production Price', '$Million/BCF', str(Ar.years[0]) + ' to ' + str(Ar.years[-1]), '', '', '', ''],
              Ar.all_prod_price, empty_prod_dict, empty_prod_dict, empty_prod_dict, Ar.prod_stats_acronyms,
              Ar.years_months, 'Production Price', sheet_name='Production Price',
              iterable2=list(Ar.all_prod_price['Total'].keys()), print_full_dict=Ar.print_full_dict_state, agg=False)
    # Write all Consumption Data
    write_all(writer, ['Consumption', 'BCF/Day', str(Ar.years[0]) + ' to ' + str(Ar.years[-1]), '', '', '', ''],
              Ar.all_cons, empty_cons_dict, empty_cons_dict, empty_cons_dict, Ar.cons_sectors, Ar.years_months,
              'Consumption', sheet_name='Consumption Monthly', iterable2=list(Ar.all_cons['All Sectors'].keys()),
              print_full_dict=Ar.print_full_dict_state, agg=False)
    write_all(writer,
              ['Consumption Price', '$Million/BCF', str(Ar.years[0]) + ' to ' + str(Ar.years[-1]), '', '', '',
               ''], Ar.all_cons_price, empty_cons_dict, empty_cons_dict, empty_cons_dict,
              Ar.cons_sectors, Ar.years_months, 'Consumption Price', sheet_name='Consumption Price',
              iterable2=list(Ar.all_cons_price['All Sectors'].keys()), print_full_dict=Ar.print_full_dict_state,
              agg=False)
    writer.save()
    file = os.path.join(include('Monthly Output.xlsx'))
    os.startfile(file)
