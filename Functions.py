# Functions lists out main functions used repeatedly in the USA, CAN, MEX, and Prod_Cons files
########################################################################################################################
########################################################################################################################
########################################################################################################################
# Import Statements
import pandas as pd
import Arrays as Ar
import os
import sys

config_name = 'myapp.cfg'

# determine if application is a script file or frozen exe

########################################################################################################################
# Absolute Path of program for file reference functions
directory = os.path.dirname(__file__)
# File Include Function


# Returns the absolute file path of an excel or csv file given the name of the file
def include(name):
    if os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])))[-4:] == 'dist':
        return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))) +
                            "/Include/All/" + name)
    return os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])) + "/Include/All/" + name)


# Converts an xlsx file to a csv file given a sheet name
def to_csv(name, sheet):
    xls = pd.read_excel(include(name + ".xlsx"), sheet, date_parser=None)
    xls.to_csv(include(name + ".csv"), index=False)


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
            if Ar.years[0] == element_float:
                return index
        return 0


def aggregate():
    for year in Ar.years:
        for country in ['Mexico', 'Canada', 'USA', 'ROW', 'Total']:
            Ar.all_dict['Production'][country][year] = dict.fromkeys(Ar.prod_stats_acronyms)
            Ar.all_dict['Production Price'][country][year] = dict.fromkeys(Ar.prod_stats_acronyms)
            Ar.all_dict['Consumption'][country][year] = dict.fromkeys(Ar.cons_sectors)
            Ar.all_dict['Consumption Price'][country][year] = dict.fromkeys(Ar.cons_sectors)
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
def write_all(writer, lines, usa_dict, can_dict, mex_dict, row_dict, iterable1, iterable3, sheet):
    dictionary = dict.fromkeys(iterable1)
    for key in iterable1:
        dictionary[key] = {}
        dictionary[key].update(mex_dict[key])
        dictionary[key].update(can_dict[key])
        dictionary[key].update(usa_dict[key])
        dictionary[key].update(row_dict[key])
    iterable2 = Ar.all_regions_acronyms
    wb = writer.book
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
    df.to_excel(writer, sheet_name=sheet)
    ws = writer.sheets[sheet]
    ws.write_column(0, 0, lines)
    for index, i1 in enumerate(iterable1):
        ws.write_column(len(lines) + index * (len(iterable2) + 15) + 1, 0, [Ar.print_full_dict[i2] for i2 in iterable2],
                        f1)
        ws.write_column(len(lines) + index * (len(iterable2) + 15) + 1, 1, ['DNG'] * len(iterable2))
        if iterable1 == Ar.prod_stats_acronyms:
            ws.write_row(len(lines) + index * (len(iterable2) + 15), 0, [Ar.print_dict[i1], '', '', ''] + iterable3, f2)
            ws.write_column(len(lines) + index * (len(iterable2) + 15) + 1, 2, [i1] * len(iterable2))
            ws.write_column(len(lines) + index * (len(iterable2) + 15) + 1, 3, [i2 for i2 in iterable2], f3)
            for index2, i3 in enumerate(iterable3):
                ws.write_column(len(lines) + index * (len(iterable2) + 15) + 1, index2 + 4,
                                [dictionary[i1][i2][i3] for i2 in iterable2])
            ws.write_row(len(lines) + (1 + index) * (len(iterable2) + 15) - 13, 0, ['Aggregate'], f3)
            ws.write_row(len(lines) + (1 + index) * (len(iterable2) + 15) - 8, 0, ['Total'], f3)
            for _index, country in enumerate(['Mexico', 'Canada', 'USA', 'ROW']):
                ws.write_row(len(lines) + (1 + index) * (len(iterable2) + 15) - 12 + _index, 0, ['', 'DNG', country, '']
                             + [Ar.all_dict[sheet][country][year][i1] for year in Ar.years])
            ws.write_row(len(lines) + (1 + index) * (len(iterable2) + 15) - 7, 0, ['', 'DNG', 'Total', ''] +
                         [Ar.all_dict[sheet]['Total'][year][i1] for year in Ar.years])
        else:
            ws.write_row(len(lines) + index * (len(iterable2) + 15), 0, [Ar.print_dict[i1], '', ''] + iterable3, f2)
            ws.write_column(len(lines) + index * (len(iterable2) + 15) + 1, 2, [i2 for i2 in iterable2], f3)
            for index2, i3 in enumerate(iterable3):
                ws.write_column(len(lines) + index * (len(iterable2) + 15) + 1, index2 + 3,
                                [dictionary[i1][i2][i3] for i2 in iterable2])
            ws.write_row(len(lines) + (1 + index) * (len(iterable2) + 15) - 13, 0, ['Aggregate'], f3)
            ws.write_row(len(lines) + (1 + index) * (len(iterable2) + 15) - 8, 0, ['Total'], f3)
            for _index, country in enumerate(['Mexico', 'Canada', 'USA', 'ROW']):
                ws.write_row(len(lines) + (1 + index) * (len(iterable2) + 15) - 12 + _index, 0, ['', 'DNG', country] +
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
    ws.write_column(len(lines), 0, [''] + [region_full for region_full in Ar.all_regions_full], f1)
    ws.write_column(len(lines), 1, [''] + [region_acronym for region_acronym in Ar.all_regions_acronyms], f2)
    ws.write_row(len(lines) - 1, 2, [region_full for region_full in Ar.all_regions_full], f1)
    ws.write_row(len(lines), 2, [region_acronym for region_acronym in Ar.all_regions_acronyms], f2)
    for index, region_acronym in enumerate(Ar.all_regions_acronyms):
        ws.write_column(1 + len(lines), index + 2, [Ar.pip_cap[region_acronym][region_acronym2] for region_acronym2 in
                                                    Ar.all_regions_acronyms])


# Writes piping flow between all regions
# writer is an ExcelWriter pandas object
# lines is information listed in an array that goes before the data lines = ['Production', '2015'] prints 'Production'
# on the first row first column and '2015' on the second row first column
# sheet is the excel sheet to write in
def write_flow(writer, lines, sheet):
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
                 Ar.years, f2)
    index = len(lines) + 1
    for region_from in Ar.all_regions_acronyms:
        for region_to in Ar.all_regions_acronyms:
            if Ar.pip_flow[region_from][region_to][Ar.years[0]] != 0:
                ws.write_row(index, 0, [Ar.print_full_dict[region_to], Ar.print_full_dict[region_from], 'Bcd/d'], f1)
                ws.write_row(index, 3, [region_to, region_from], f2)
                ws.write_row(index, 5, [Ar.pip_flow[region_from][region_to][year] for year in Ar.years])
                index += 1
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
