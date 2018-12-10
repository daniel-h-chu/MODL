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
# US Pipe Capacity #####################################################################################################
########################################################################################################################
########################################################################################################################
# US Pipe Capacity
def pip_cap_1():
    f_usa_pip_cap = open(Fx.include('EIA-StatetoStateCapacity.csv'), 'r')
    file_reader = csv.reader(f_usa_pip_cap, delimiter=',')
    pip_state_from_ind = -99999
    pip_state_to_ind = -99999
    pip_county_from_ind = -99999
    pip_county_to_ind = -99999
    pip_capacity_ind = -99999
    for row in file_reader:
        if row[0] == Ar.capacity_year:
            for index, element in enumerate(row):
                if element == Ar.state_from and pip_state_from_ind == -99999:
                    pip_state_from_ind = index
                if element == Ar.state_to and pip_state_to_ind == -99999:
                    pip_state_to_ind = index
                if element == Ar.county_from and pip_county_from_ind == -99999:
                    pip_county_from_ind = index
                if element == Ar.county_to and pip_county_to_ind == -99999:
                    pip_county_to_ind = index
                if element == Ar.capacity_mmcfd and pip_capacity_ind == -99999:
                    pip_capacity_ind = index
        try:
            if float(row[0]) == Ar.years[0]:
                region_from = ''
                region_to = ''
                if row[pip_state_from_ind] == Ar.mexico:
                    for region in Ar.cities_to_regions:
                        if row[pip_county_from_ind] in Ar.cities_to_regions[region]:
                            region_from = region
                if row[pip_state_from_ind] in Ar.usa_states_full:
                    for region in Ar.states_to_regions:
                        if Ar.states_dict[row[pip_state_from_ind]] in Ar.states_to_regions[region]:
                            region_from = region
                if row[pip_state_from_ind] in Ar.canadian_provinces_full:
                    for region in Ar.provinces_to_regions:
                        if Ar.provinces_dict[row[pip_state_from_ind]] in Ar.provinces_to_regions[region]:
                            region_from = region
                if row[pip_state_to_ind] == Ar.mexico:
                    for region in Ar.cities_to_regions:
                        if row[pip_county_to_ind] in Ar.cities_to_regions[region]:
                            region_to = region
                if row[pip_state_to_ind] in Ar.usa_states_full:
                    for region in Ar.states_to_regions:
                        if Ar.states_dict[row[pip_state_to_ind]] in Ar.states_to_regions[region]:
                            region_to = region
                if row[pip_state_to_ind] in Ar.canadian_provinces_full:
                    for region in Ar.provinces_to_regions:
                        if Ar.provinces_dict[row[pip_state_to_ind]] in Ar.provinces_to_regions[region]:
                            region_to = region
                if region_from != '' and region_to != '':
                    Ar.pip_cap[region_from][region_to] += float(row[pip_capacity_ind]) / 1000
        except ValueError:
            continue
    f_usa_pip_cap.close()
    os.remove(Fx.include('EIA-StatetoStateCapacity.csv'))


########################################################################################################################
########################################################################################################################
# Mexico Pipe Capacity #################################################################################################
########################################################################################################################
########################################################################################################################
# Mexico Pipe Capacity
def pip_cap_2():
    f_mex_pip_cap = open(Fx.include('mex_pip_cap_bcfd.csv'), 'r')
    file_reader = csv.reader(f_mex_pip_cap, delimiter=',')
    pip_region_from_ind = -99999
    pip_region_to_ind = -99999
    pip_capacity_ind = -99999
    pip_status_ind = -99999
    for row in file_reader:
        if row[0] == '':
            for index, element in enumerate(row):
                if element == Ar.region_from and pip_region_to_ind == -99999:
                    pip_region_from_ind = index
                if element == Ar.region_to and pip_region_to_ind == -99999:
                    pip_region_to_ind = index
                if element == Ar.capacity_mex_bcfd and pip_capacity_ind == -99999:
                    pip_capacity_ind = index
                if element == Ar.status and pip_status_ind == -99999:
                    pip_status_ind = index
        try:
            if row[pip_region_from_ind] in Ar.all_regions_acronyms and row[pip_region_to_ind] in \
                    Ar.all_regions_acronyms and row[pip_status_ind] == Ar.operating:
                Ar.pip_cap[row[pip_region_from_ind]][row[pip_region_to_ind]] += float(row[pip_capacity_ind])
                Ar.pip_cap[row[pip_region_to_ind]][row[pip_region_from_ind]] += float(row[pip_capacity_ind])
        except IndexError:
            continue
        except ValueError:
            continue
    f_mex_pip_cap.close()
    os.remove(Fx.include('mex_pip_cap_bcfd.csv'))


########################################################################################################################
########################################################################################################################
# Canada Pipe Capacity #################################################################################################
########################################################################################################################
########################################################################################################################
# Canada Pipe Capacity
def pip_cap_3():
    f_can_pip_cap = open(Fx.include('can_pip_cap.csv'), 'r')
    file_reader = csv.reader(f_can_pip_cap, delimiter=',')
    pip_region_from_ind = -99999
    pip_region_to_ind = -99999
    pip_capacity_ind = -99999
    for row in file_reader:
        if row[0] == '':
            for index, element in enumerate(row):
                if element == Ar.region_from and pip_region_from_ind == -99999:
                    pip_region_from_ind = index
                if element == Ar.region_to and pip_region_to_ind == -99999:
                    pip_region_to_ind = index
                if element == Ar.capacity_can_bcfd and pip_capacity_ind == -99999:
                    pip_capacity_ind = index
        try:
            if row[pip_region_from_ind] in Ar.all_regions_acronyms and row[pip_region_to_ind] in \
                    Ar.all_regions_acronyms:
                Ar.pip_cap[row[pip_region_from_ind]][row[pip_region_to_ind]] += float(row[pip_capacity_ind])
        except IndexError:
            continue
    f_can_pip_cap.close()


########################################################################################################################
########################################################################################################################
# Other Pipe Capacity ##################################################################################################
########################################################################################################################
########################################################################################################################
# Remove Intra-Regional Pipe Capacity
def pip_cap_4():
    for region in Ar.all_regions_acronyms:
        Ar.pip_cap[region][region] = 0


########################################################################################################################
########################################################################################################################
# US Pipe Flow #########################################################################################################
########################################################################################################################
########################################################################################################################
# USA to USA Pipe Flow
def pip_flow_1():
    f_usa_pip_flow = open(Fx.include('Primary_Natural_Gas_Flows_Entering_NGTDM_Region_from_Neighboring_Regions.csv'),
                          'r')
    file_reader = csv.reader(f_usa_pip_flow, delimiter=',')
    year_shift = 0
    region_to_temp = ''
    for row in file_reader:
        if Fx.year_sh(row, ''):
            year_shift = Fx.year_sh(row, '')
        subcategory = False
        for region_to in Ar.all_regions_full:
            if row[0] == Ar.r_into + region_to + Ar.r_from:
                region_to_temp = Ar.reverse_full_dict[region_to]
                subcategory = True
        if row[0] in Ar.all_regions_full and region_to_temp != '' and not subcategory:
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    Ar.pip_flow[Ar.reverse_full_dict[row[0]]][region_to_temp][index + Ar.years[0] - year_shift] += \
                        float(element)/365
    f_usa_pip_flow.close()


########################################################################################################################
########################################################################################################################
# Mexico Pipe Flow #####################################################################################################
########################################################################################################################
########################################################################################################################
# MEX and USA Pipe Flow
def pip_flow_2():
    f_mex_pip_flow = open(Fx.include('reg_bal_mex.csv'), 'r')
    file_reader = csv.reader(f_mex_pip_flow, delimiter=',')
    mex_pipe_region_temp = ''
    year_shift = 0
    for mexico_region in Ar.mex_regions_acronyms:
        mex_to_usa_sum = sum([Ar.pip_cap[mexico_region][nangam_region] for nangam_region in Ar.nangam_regions_acronyms])
        usa_to_mex_sum = sum([Ar.pip_cap[nangam_region][mexico_region] for nangam_region in Ar.nangam_regions_acronyms])
        for nangam_region in Ar.nangam_regions_acronyms:
            try:
                Ar.mex_to_usa_dict[mexico_region][nangam_region] = Ar.pip_cap[mexico_region][nangam_region] /\
                                                                   mex_to_usa_sum
            except ZeroDivisionError:
                Ar.mex_to_usa_dict[mexico_region][nangam_region] = 0
            try:
                Ar.usa_to_mex_dict[nangam_region][mexico_region] = Ar.pip_cap[nangam_region][mexico_region] / \
                                                                   usa_to_mex_sum
            except ZeroDivisionError:
                Ar.usa_to_mex_dict[nangam_region][mexico_region] = 0
    for row in file_reader:
        if row[0] in Ar.mex_regions_acronyms:
            mex_pipe_region_temp = row[0]
        if Fx.year_sh(row, ''):
            year_shift = Fx.year_sh(row, '')
        if mex_pipe_region_temp != '' and row[0] == Ar.exports:
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    for nangam_region in Ar.nangam_regions_acronyms:
                        try:
                            Ar.pip_flow[mex_pipe_region_temp][nangam_region][index + Ar.years[0] - year_shift] = \
                                float(element) * Ar.mex_to_usa_dict[mex_pipe_region_temp][nangam_region] / 1000
                        except ValueError:
                            continue
        if mex_pipe_region_temp != '' and row[0] == Ar.imports:
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    for nangam_region in Ar.nangam_regions_acronyms:
                        try:
                            Ar.pip_flow[nangam_region][mex_pipe_region_temp][index + Ar.years[0] - year_shift] = \
                                float(element) * Ar.usa_to_mex_dict[nangam_region][mex_pipe_region_temp] / 1000
                        except ValueError:
                            continue
    f_mex_pip_flow.close()
    os.remove(Fx.include('reg_bal_mex.csv'))


########################################################################################################################
########################################################################################################################
# Canada Pipe Flow #####################################################################################################
########################################################################################################################
########################################################################################################################
# USA to CAN Pipe Flow
def pip_flow_3():
    f_can_pip_flow = open(Fx.include('Natural_Gas_Imports_and_Exports.csv'), 'r')
    file_reader = csv.reader(f_can_pip_flow, delimiter=',')
    year_shift = 0
    usa_to_can_sum = 0
    for canadian_region in Ar.canadian_regions_acronyms:
        for nangam_region in Ar.nangam_regions_acronyms:
            usa_to_can_sum += Ar.pip_cap[nangam_region][canadian_region]
    for row in file_reader:
        if Fx.year_sh(row, ''):
            year_shift = Fx.year_sh(row, '')
        if row[0] == Ar.usa_to_can:
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    for canadian_region in Ar.canadian_regions_acronyms:
                        for nangam_region in Ar.nangam_regions_acronyms:
                            Ar.pip_flow[nangam_region][canadian_region][index + Ar.years[0] - year_shift] += \
                                float(element) * 1000/365 * Ar.pip_cap[nangam_region][canadian_region] / usa_to_can_sum
    f_can_pip_flow.close()


# CAN to CAN Pipe Flow #################################################################################################
#
def pip_flow_4():
    f_can_pip_cap = open(Fx.include('can_pip_cap.csv'), 'r')
    file_reader = csv.reader(f_can_pip_cap, delimiter=',')
    pip_region_from_ind = -99999
    pip_region_to_ind = -99999
    pip_flow_ind = -99999
    for row in file_reader:
        if row[0] == '':
            for index, element in enumerate(row):
                if element == Ar.region_from and pip_region_from_ind == -99999:
                    pip_region_from_ind = index
                if element == Ar.region_to and pip_region_to_ind == -99999:
                    pip_region_to_ind = index
                if element == Ar.can_to_can and pip_flow_ind == -99999:
                    pip_flow_ind = index
        try:
            if row[pip_region_from_ind] in Ar.all_regions_acronyms and row[pip_region_to_ind] in \
                    Ar.all_regions_acronyms:
                for year in Ar.years:
                    Ar.pip_flow[row[pip_region_from_ind]][row[pip_region_to_ind]][year] += float(row[pip_flow_ind])
        except IndexError:
            continue
    f_can_pip_cap.close()
    os.remove(Fx.include('can_pip_cap.csv'))


########################################################################################################################
########################################################################################################################
# Other Pipe Flow ######################################################################################################
########################################################################################################################
########################################################################################################################
# Remove Intra-Regional Pipe Flow
def pip_flow_5():
    for region in Ar.all_regions_acronyms:
        for year in Ar.years:
            Ar.pip_flow[region][region][year] = 0
