# USA_Functions generates dictionaries for US Production, Production Price, Consumption, and Consumption Price
########################################################################################################################
########################################################################################################################
########################################################################################################################
import os
import csv
import Functions as Fx
import Arrays as Ar
import urllib
import urllib.request
import urllib.error


########################################################################################################################
########################################################################################################################
# US Pipe Capacity #####################################################################################################
########################################################################################################################
########################################################################################################################
# Pipeline Capacity between US Regions with other US Regions, Mexican Regions, or Canadian Regions. Data is read from
# EIA-StatetoStateCapacity.csv and only pipelines with the same year as the base year (Ar.years[0]) are selected. To and
# from provinces/states/cities are sorted by country so that they can contribute to the correct region's data
def pip_cap_1():
    f_usa_pip_cap = open(Fx.include('EIA-StatetoStateCapacity.csv'), 'r')
    file_reader = csv.reader(f_usa_pip_cap, delimiter=',')
    # Set columns indices to look for to and from states and counties as well as pipeline capacity
    pip_state_from_ind = -99999
    pip_state_to_ind = -99999
    pip_county_from_ind = -99999
    pip_county_to_ind = -99999
    pip_capacity_ind = -99999
    pip_capacity_year_ind = -99999
    for row in file_reader:
        if Ar.capacity_year in row:
            for index, element in enumerate(row):
                # Found column indices based on keywords found in the row
                if element == Ar.state_from and pip_state_from_ind == -99999:
                    pip_state_from_ind = index
                if element == Ar.state_to and pip_state_to_ind == -99999:
                    pip_state_to_ind = index
                if element == Ar.county_from and pip_county_from_ind == -99999:
                    pip_county_from_ind = index
                if element == Ar.county_to and pip_county_to_ind == -99999:
                    pip_county_to_ind = index
                if element == Ar.capacity and pip_capacity_ind == -99999:
                    pip_capacity_ind = index
                if element == Ar.capacity_year and pip_capacity_year_ind == -99999:
                    pip_capacity_year_ind = index
        try:
            # If pipeline is active in base year
            # HARDCODED YEAR BASED ON DATA YEAR
            if float(row[pip_capacity_year_ind]) == Ar.years[0] - 1:
                # What region the pipeline is from and what region the pipeline goes to
                region_from = ''
                region_to = ''
                # If the pipeline originates from mexico, lookup region based on city
                if row[pip_state_from_ind] == Ar.mexico:
                    for region in Ar.cities_to_regions:
                        if row[pip_county_from_ind] in Ar.cities_to_regions[region]:
                            region_from = region
                # If the pipeline originates from the US, lookup region based on state
                if row[pip_state_from_ind] in Ar.usa_states_full:
                    region_from = Ar.states_acronyms_to_2_dict[Ar.states_dict[row[pip_state_from_ind]]]
                # If the pipeline originates from Canada, lookup region based on province
                if row[pip_state_from_ind] in Ar.canadian_provinces_full:
                    region_from = Ar.states_acronyms_to_2_dict[Ar.provinces_dict[row[pip_state_from_ind]]]
                # If the pipeline goes to mexico, lookup region based on city
                if row[pip_state_to_ind] == Ar.mexico:
                    for region in Ar.cities_to_regions:
                        if row[pip_county_to_ind] in Ar.cities_to_regions[region]:
                            region_to = region
                # If the pipeline goes to the US, lookup region based on state
                if row[pip_state_to_ind] in Ar.usa_states_full:
                    region_to = Ar.states_acronyms_to_2_dict[Ar.states_dict[row[pip_state_to_ind]]]
                # If the pipeline goes to Canada, lookup region based on province
                if row[pip_state_to_ind] in Ar.canadian_provinces_full:
                    region_to = Ar.states_acronyms_to_2_dict[Ar.provinces_dict[row[pip_state_to_ind]]]
                # Fill pip_cap by adding pipeline capacity to the total pipeline capacity between two regions
                if region_from != '' and region_to != '':
                    Ar.pip_cap[region_from][region_to] += float(row[pip_capacity_ind]) / 1000
        except ValueError:
            continue
        except IndexError:
            continue
    f_usa_pip_cap.close()
    os.remove(Fx.include('EIA-StatetoStateCapacity.csv'))

    # Projected Pipelines

    f_usa_pip_cap = open(Fx.include('EIA-NaturalGasPipelineProjects.csv'), 'r')
    file_reader = csv.reader(f_usa_pip_cap, delimiter=',')
    # Set columns indices to look for to and from states and counties as well as pipeline capacity
    pip_state_from_ind = -99999
    pip_state_to_ind = -99999
    pip_capacity_ind = -99999
    pip_status_ind = -99999
    pip_capacity_year_ind = -99999
    for row in file_reader:
        if Ar.capacity_year in row:
            for index, element in enumerate(row):
                # Found column indices based on keywords found in the row
                if element == Ar.state_from and pip_state_from_ind == -99999:
                    pip_state_from_ind = index
                if element == Ar.state_to and pip_state_to_ind == -99999:
                    pip_state_to_ind = index
                if element == Ar.status and pip_status_ind == -99999:
                    pip_status_ind = index
                if element == Ar.capacity and pip_capacity_ind == -99999:
                    pip_capacity_ind = index
                if element == Ar.capacity_year and pip_capacity_year_ind == -99999:
                    pip_capacity_year_ind = index
            Ar.planned_cols = row
        try:
            # If pipeline is active in base year
            # HARDCODED YEAR FROM DATA
            if float(row[pip_capacity_year_ind]) <= 2018 and row[pip_status_ind] == Ar.completed:
                # What region the pipeline is from and what region the pipeline goes to
                if row[pip_state_from_ind] in Ar.usa_states_acronyms2 and row[pip_state_to_ind] in \
                        Ar.usa_states_acronyms2:
                    region_from = row[pip_state_from_ind]
                    region_to = row[pip_state_to_ind]
                    Ar.pip_cap[region_from][region_to] += float(row[pip_capacity_ind]) / 1000
            else:
                Ar.planned.append(row)
        except ValueError:
            continue
        except IndexError:
            continue
    f_usa_pip_cap.close()
    os.remove(Fx.include('EIA-NaturalGasPipelineProjects.csv'))


########################################################################################################################
########################################################################################################################
# Mexico Pipe Capacity #################################################################################################
########################################################################################################################
########################################################################################################################
# Pipeline capacity between Meixco regions from mex_pip_cap_bcfd.csv where to and from data is directly fed into the pip
# eline capacity dictionary. Only operating pipes contribute to regional data
def pip_cap_2():
    f_mex_pip_cap = open(Fx.include('mex_pip_cap_bcfd.csv'), 'r')
    file_reader = csv.reader(f_mex_pip_cap, delimiter=',')
    # Set columns indices to look for to and from regions as well as pipeline capacity and status
    pip_region_from_ind = -99999
    pip_region_to_ind = -99999
    pip_capacity_ind = -99999
    pip_status_ind = -99999
    for row in file_reader:
        if row[0] == '':
            for index, element in enumerate(row):
                # Found column indices based on keywords found in the row
                if element == Ar.region_from and pip_region_to_ind == -99999:
                    pip_region_from_ind = index
                if element == Ar.region_to and pip_region_to_ind == -99999:
                    pip_region_to_ind = index
                if element == Ar.capacity and pip_capacity_ind == -99999:
                    pip_capacity_ind = index
                if element == Ar.status and pip_status_ind == -99999:
                    pip_status_ind = index
        try:
            # If the pipeline between two mexican regions is operating, then add the capacity for pipelines going in
            # both directions (region from -> region to and region to -> region from)
            if row[pip_region_from_ind] in Ar.all_regions_acronyms and row[pip_region_to_ind] in \
                    Ar.all_regions_acronyms and row[pip_status_ind] == Ar.operating:
                Ar.pip_cap[row[pip_region_from_ind]][row[pip_region_to_ind]] += float(row[pip_capacity_ind])
                Ar.pip_cap[row[pip_region_to_ind]][row[pip_region_from_ind]] += float(row[pip_capacity_ind])
        except IndexError:
            continue
        except ValueError:
            continue
        except KeyError:
            if row[pip_region_to_ind] in Ar.nangam_regions_acronyms:
                for state in Ar.states_to_regions[row[pip_region_to_ind]]:
                    Ar.pip_cap[Ar.states_acronyms_to_2_dict[state]][row[pip_region_from_ind]] += float(
                        row[pip_capacity_ind]) / len(
                        Ar.states_to_regions[row[pip_region_to_ind]])
                    Ar.pip_cap[row[pip_region_from_ind]][Ar.states_acronyms_to_2_dict[state]] += float(
                        row[pip_capacity_ind]) / len(
                        Ar.states_to_regions[row[pip_region_to_ind]])
            if row[pip_region_from_ind] in Ar.nangam_regions_acronyms:
                for state in Ar.states_to_regions[row[pip_region_from_ind]]:
                    Ar.pip_cap[Ar.states_acronyms_to_2_dict[state]][row[pip_region_to_ind]] += float(
                        row[pip_capacity_ind]) / len(
                        Ar.states_to_regions[row[pip_region_from_ind]])
                    Ar.pip_cap[row[pip_region_to_ind]][Ar.states_acronyms_to_2_dict[state]] += float(
                        row[pip_capacity_ind]) / len(
                        Ar.states_to_regions[row[pip_region_from_ind]])
    f_mex_pip_cap.close()
    os.remove(Fx.include('mex_pip_cap_bcfd.csv'))


########################################################################################################################
########################################################################################################################
# Canada Pipe Capacity #################################################################################################
########################################################################################################################
########################################################################################################################
# Pipeline capacity between Canada regions from can_pip_cap.csv where to and from data is directly fed into the pip
# eline capacity dictionary. Only operating pipes contribute to regional data
def pip_cap_3():
    f_can_pip_cap = open(Fx.include('can_pip_cap.csv'), 'r')
    file_reader = csv.reader(f_can_pip_cap, delimiter=',')
    # Set columns indices to look for to and from regions as well as pipeline capacity
    pip_region_from_ind = -99999
    pip_region_to_ind = -99999
    pip_capacity_ind = -99999
    for row in file_reader:
        if row[0] == '':
            for index, element in enumerate(row):
                # Found column indices based on keywords found in the row
                if element == Ar.frm and pip_region_from_ind == -99999:
                    pip_region_from_ind = index
                if element == Ar.to and pip_region_to_ind == -99999:
                    pip_region_to_ind = index
                if element == Ar.capacity and pip_capacity_ind == -99999:
                    pip_capacity_ind = index
        try:
            # Add to pipe capacity for pipes region from -> region to
            if row[pip_region_from_ind] in Ar.states_full and row[pip_region_to_ind] in \
                    Ar.states_full:
                Ar.pip_cap[Ar.states_acronyms_to_2_dict[Ar.all_states_dict[row[pip_region_from_ind]]]][
                    Ar.states_acronyms_to_2_dict[Ar.all_states_dict[row[pip_region_to_ind]]]]\
                    += float(row[pip_capacity_ind])
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
    for region in Ar.states_acronyms2:
        Ar.pip_cap[region][region] = 0


########################################################################################################################
########################################################################################################################
# US Pipe Flow #########################################################################################################
########################################################################################################################
########################################################################################################################
# USA to USA and USA to Canada Pipe Flow. Pipe flow is directly read from Primary_Natural_Gas_Flows_Entering_NGTDM_Regio
# n_from_Neighboring_Regions.csv. If a flow goes through a region, then the flow is counted twice: once of the original
# region to the intermediate region and once of the intermediate region to the final region (manually done)
def pip_flow_1():
    for state in Ar.states_acronyms2:
        try:
            # urllib.request.urlretrieve("https://www.eia.gov/dnav/ng/xls/NG_MOVE_IST_A2DCU_S" + state + "_A.xls",
            #                           Fx.include('Flow_' + state + ".xls"))
            Fx.to_csv('Flow_' + state, 'Data 1', '_Imports')
            Fx.to_csv('Flow_' + state, 'Data 2', '_Exports')
            f_usa_pip_flow_state_imp = open(Fx.include('Flow_' + state + '_Imports.csv'))
            f_usa_pip_flow_state_exp = open(Fx.include('Flow_' + state + '_Exports.csv'))
            file_reader_imp = csv.reader(f_usa_pip_flow_state_imp, delimiter=',')
            file_reader_exp = csv.reader(f_usa_pip_flow_state_exp, delimiter=',')
            locations = []
            imports = []
            for index, row in enumerate(file_reader_imp):
                if index == 2:
                    locations = row
                if row[0][:4] == str(Ar.years[0] - 1):
                    imports = row
            for index, element in enumerate(locations):
                try:
                    temp_state = element[element.index('From') + 5:element.index('(') - 1]
                    Ar.pip_flow_state[Ar.states_acronyms_to_2_dict[Ar.all_states_dict[temp_state]]][state] = \
                        float(imports[index])
                except ValueError:
                    continue
                except KeyError:
                    continue
            for index, row in enumerate(file_reader_exp):
                if index == 2:
                    locations = row
                if row[0][:4] == str(Ar.years[0] - 1):
                    imports = row
            for index, element in enumerate(locations):
                try:
                    temp_state = element[element.index('To') + 3:element.index('(') - 1]
                    Ar.pip_flow_state[state][Ar.states_acronyms_to_2_dict[Ar.all_states_dict[temp_state]]] = \
                        float(imports[index])
                except ValueError:
                    continue
                except KeyError:
                    continue
            f_usa_pip_flow_state_imp.close()
            f_usa_pip_flow_state_exp.close()
        except urllib.error.HTTPError:
            continue
        except FileNotFoundError:
            continue
    f_usa_pip_flow = open(
        Fx.include('Primary_Natural_Gas_Flows_Entering_Natural_Gas_Supply_Region_from_Neighboring_Regions.csv'),
        'r')
    file_reader = csv.reader(f_usa_pip_flow, delimiter=',')
    year_shift = 0
    # What destination region we are dealing with
    region_to_temp = ''
    for row in file_reader:
        if Fx.year_sh(row, ''):
            # Read in correct data based on year
            year_shift = Fx.year_sh(row, '')
        subcategory = False
        # Check if the current data is of form "Into region from:"
        for region_to in Ar.all_regions_full:
            if row[0] == Ar.r_into + region_to + Ar.r_from:
                # Set the destination region that we are dealing with
                region_to_temp = Ar.reverse_full_dict[region_to]
                subcategory = True
        if row[0] in Ar.all_regions_full and region_to_temp != '' and not subcategory:
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    # Fill in pipe flow for region_from -> region_to for all years with pipe flow data divided by 365 to
                    # obtain flow per year
                    Ar.pip_flow_raw[Ar.reverse_full_dict[row[0]]][region_to_temp][index + Ar.years[0] - year_shift] += \
                        float(element)/365
    f_usa_pip_flow.close()
    for state in Ar.states_acronyms2:
        try:
            os.remove(Fx.include('Flow_' + state + '_Imports.csv'))
            os.remove(Fx.include('Flow_' + state + '_Exports.csv'))
        except FileNotFoundError:
            continue


########################################################################################################################
########################################################################################################################
# Mexico Pipe Flow #####################################################################################################
########################################################################################################################
########################################################################################################################
# Pipeline flow from the United States to Mexico modeled off flow to each Meixcan region being proportional to capacity
# to each Mexican region and flow from Mexico to US is modeled congruently. Total pipeline flow/exports are read from
# reg_bal_mex.csv
def pip_flow_2():
    f_mex_pip_flow = open(Fx.include('reg_bal_mex.csv'), 'r')
    file_reader = csv.reader(f_mex_pip_flow, delimiter=',')
    # What mexican region we are dealing with
    mex_pipe_region_temp = ''
    year_shift = 0
    for mexico_region in Ar.mex_regions_acronyms:
        # Set pipeline flow proportionate to the pipeline capacity of US regions to MEX regions and MEX regions to US
        # regions
        mex_to_usa_sum = sum([Ar.pip_cap[mexico_region][state] for state in Ar.usa_states_acronyms2])
        usa_to_mex_sum = sum([Ar.pip_cap[state][mexico_region] for state in Ar.usa_states_acronyms2])
        for state in Ar.usa_states_acronyms2:
            try:
                # Ratio of exports from mexican regions for each mexican region (ratios for different nangam regions sum
                # to one)
                Ar.mex_to_usa_dict[mexico_region][state] = Ar.pip_cap[mexico_region][state] /\
                                                                   mex_to_usa_sum
            except ZeroDivisionError:
                Ar.mex_to_usa_dict[mexico_region][state] = 0
            try:
                # Ratio of imports to mexican regions for each mexican region (ratios for different nangam regions sum
                # to one)
                Ar.usa_to_mex_dict[state][mexico_region] = Ar.pip_cap[state][mexico_region] / \
                                                                   usa_to_mex_sum
            except ZeroDivisionError:
                Ar.usa_to_mex_dict[state][mexico_region] = 0
    for row in file_reader:
        if row[0] in Ar.mex_regions_acronyms:
            # Set current mexican region we are dealing with
            mex_pipe_region_temp = row[0]
        if Fx.year_sh(row, ''):
            # Read in correct data based on year
            year_shift = Fx.year_sh(row, '')
        if mex_pipe_region_temp != '' and row[0] == Ar.exports:
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    for state in Ar.states_acronyms2:
                        # Set pip_flow with pipe flow data for each mexican region, nangam region, and year as the total
                        # exports from Mexican regions distributed over the ratios provided by each nangam
                        # region divided by 1000 for units
                        try:
                            for month in Ar.months:
                                Ar.pip_flow[mex_pipe_region_temp][state][
                                    month + '-' + str(index + Ar.years[0] - year_shift)] = \
                                    float(element) * Ar.mex_to_usa_dict[mex_pipe_region_temp][state] / 1000 / 12
                        except ValueError:
                            continue
                        except KeyError:
                            continue
        if mex_pipe_region_temp != '' and row[0] == Ar.imports:
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    for state in Ar.usa_states_acronyms2:
                        # Set pip_flow with pipe flow data for each mexican region, nangam region, and year as the total
                        # imports to Mexican regions distributed over the ratios provided by each nangam
                        # region divided by 1000 for units
                        try:
                            for month in Ar.months:
                                Ar.pip_flow[state][mex_pipe_region_temp][
                                    month + '-' + str(index + Ar.years[0] - year_shift)] = \
                                    float(element) * Ar.usa_to_mex_dict[state][mex_pipe_region_temp] / 1000 / 12
                        except ValueError:
                            continue
                        except KeyError:
                            continue
                            # print('KeyError2 ' + state + ' ' + mex_pipe_region_temp)
    f_mex_pip_flow.close()
    os.remove(Fx.include('reg_bal_mex.csv'))


########################################################################################################################
########################################################################################################################
# Canada Pipe Flow #####################################################################################################
########################################################################################################################
########################################################################################################################
# Pipeline flow from the United States to Canada modeled off flow to each Canadian region being proportional to capacity
# to each Canadian region. Total pipeline flow/exports are read from Natural_Gas_Imports_and_Exports.csv
def pip_flow_3():
    f_can_pip_flow = open(Fx.include('Natural_Gas_Imports_and_Exports.csv'), 'r')
    file_reader = csv.reader(f_can_pip_flow, delimiter=',')
    year_shift = 0
    usa_to_can_sum = 0
    for province in Ar.canadian_provinces_acronyms2:
        for state in Ar.usa_states_acronyms2:
            # Sum total pipe capacity from United States to Canada
            usa_to_can_sum += Ar.pip_cap[state][province]
    for row in file_reader:
        if Fx.year_sh(row, ''):
            # Read in correct data based on year
            year_shift = Fx.year_sh(row, '')
        if row[0] == Ar.usa_to_can:
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    for province in Ar.canadian_provinces_acronyms2:
                        for state in Ar.usa_states_acronyms2:
                            for month in Ar.months:
                                # Set pipe flow from a nangam region to canadian region proportional to the capacity frm
                                # the nangam region to canadian region (total exports from us to canada times the ratio
                                # the capacity between two regions over the capacity between the two countries)
                                Ar.pip_flow[state][province][month + '-' + str(index + Ar.years[0] - year_shift)] += \
                                    float(element) * 1000/365/12 * Ar.pip_cap[state][province] / usa_to_can_sum
    f_can_pip_flow.close()


# CAN to CAN Pipe Flow #################################################################################################
# Pipeline flow between Canada regions from can_pip_cap.csv where to and from data is directly fed into the pipeline flo
# dictionary.
def pip_flow_4():
    f_can_pip_cap = open(Fx.include('can_pip_cap.csv'), 'r')
    file_reader = csv.reader(f_can_pip_cap, delimiter=',')
    # Set columns indices to look for to and from regions as well as pipeline flow
    pip_region_from_ind = -99999
    pip_region_to_ind = -99999
    pip_state_from_ind = -99999
    pip_state_to_ind = -99999
    pip_flow_ind = -99999
    for row in file_reader:
        if row[0] == '':
            for index, element in enumerate(row):
                # Found column indices based on keywords found in the row
                if element == Ar.region_from and pip_region_from_ind == -99999:
                    pip_region_from_ind = index
                if element == Ar.region_to and pip_region_to_ind == -99999:
                    pip_region_to_ind = index
                if element == Ar.frm and pip_state_from_ind == -99999:
                    pip_state_from_ind = index
                if element == Ar.to and pip_state_to_ind == -99999:
                    pip_state_to_ind = index
                if element == Ar.can_to_can and pip_flow_ind == -99999:
                    pip_flow_ind = index
        try:
            # Add to pipeline flow for region_from -> region_To for each year
            if row[pip_state_from_ind] in Ar.states_full and row[pip_state_to_ind] in Ar.states_full:
                Ar.pip_flow_state[Ar.states_acronyms_to_2_dict[Ar.all_states_dict[row[pip_state_from_ind]]]][
                    Ar.states_acronyms_to_2_dict[Ar.all_states_dict[row[pip_state_to_ind]]]] += float(
                    row[pip_flow_ind])
            if row[pip_region_from_ind] in Ar.all_regions_acronyms and row[pip_region_to_ind] in \
                    Ar.all_regions_acronyms:
                for year in Ar.years:
                    Ar.pip_flow_raw[row[pip_region_from_ind]][row[pip_region_to_ind]][year] += \
                        float(row[pip_flow_ind])
        except IndexError:
            continue
    f_can_pip_cap.close()
    os.remove(Fx.include('can_pip_cap.csv'))


########################################################################################################################
########################################################################################################################
# Other Pipe Flow ######################################################################################################
########################################################################################################################
########################################################################################################################
# Remove Intra-Regional Pipe Flow and Calculate Monthly/State Data
def pip_flow_5():
    for region in Ar.all_regions_acronyms:
        for region2 in Ar.all_regions_acronyms:
            for state in Ar.all_to_states_dict[region]:
                for state2 in Ar.all_to_states_dict[region2]:
                    for year in Ar.years:
                        for month in Ar.months:
                            try:
                                Ar.pip_flow[Ar.states_acronyms_to_2_dict[state]][Ar.states_acronyms_to_2_dict[state2]][
                                    month + '-' + str(year)] += Ar.pip_flow_raw[region][region2][
                                                                    year] * \
                                                                Ar.pip_flow_state[Ar.states_acronyms_to_2_dict[state]][
                                                                    Ar.states_acronyms_to_2_dict[
                                                                        state2]] / sum(
                                    [sum(
                                        [Ar.pip_flow_state[Ar.states_acronyms_to_2_dict[state]][
                                             Ar.states_acronyms_to_2_dict[state2]] for state2 in
                                         Ar.all_to_states_dict[region2]])
                                        for state in Ar.all_to_states_dict[region]]) / 12
                            except ZeroDivisionError:
                                try:
                                    Ar.pip_flow[Ar.states_acronyms_to_2_dict[state]][
                                        Ar.states_acronyms_to_2_dict[state2]][
                                        month + '-' + str(year)] += Ar.pip_flow_raw[region][region2][
                                                                        year] * \
                                                                    Ar.pip_cap[Ar.states_acronyms_to_2_dict[state]][
                                                                        Ar.states_acronyms_to_2_dict[state2]] / sum(
                                        [sum(
                                            [Ar.pip_cap[Ar.states_acronyms_to_2_dict[state]][
                                                 Ar.states_acronyms_to_2_dict[state2]] for state2 in
                                             Ar.all_to_states_dict[region2]])
                                            for state in Ar.all_to_states_dict[region]]) / 12
                                except ZeroDivisionError:
                                    Ar.pip_flow[Ar.states_acronyms_to_2_dict[state]][
                                        Ar.states_acronyms_to_2_dict[state2]][
                                        month + '-' + str(year)] += Ar.pip_flow_raw[region][region2][
                                                                        year] / len(
                                        Ar.all_to_states_dict[region]) / len(Ar.all_to_states_dict[region2]) / 12
    for state in Ar.states_acronyms2:
        for month_year in Ar.years_months:
            Ar.pip_flow[state][state][month_year] = 0


########################################################################################################################
########################################################################################################################
# LNG Pipe Flow ########################################################################################################
########################################################################################################################
########################################################################################################################
# USA LNG Imports and Exports
def pip_flow_6():
    f_usa_pip_lng = open(Fx.include('NG_MOVE_POE2_A_EPG0_ENG_MMCF_A.csv'), 'r')
    file_reader = csv.reader(f_usa_pip_lng, delimiter=',')
    lng_points = []
    pip_lng_raw = []
    for index, row in enumerate(file_reader):
        if index == 2:
            lng_points = row
        if row[0][:4] == str(Ar.years[0] - 1):
            pip_lng_raw = row
    for index, element in enumerate(lng_points):
        try:
            temp_state = element[element.index(',') + 2:element.index(',') + 4].upper()
            if 'Mexico' in element:
                Ar.pip_flow_lng_raw[temp_state]['MNW'] += float(
                    pip_lng_raw[index])
            elif 'Canada' in element:
                Ar.pip_flow_lng_raw[temp_state]['ON'] += float(
                    pip_lng_raw[index])
            else:
                Ar.pip_flow_lng_raw[temp_state]['ROW'] += float(
                    pip_lng_raw[index])
        except ValueError:
            continue
    f_usa_pip_lng.close()
    os.remove(Fx.include('NG_MOVE_POE2_A_EPG0_ENG_MMCF_A.csv'))
    f_usa_pip_lng = open(Fx.include('NG_MOVE_POE1_A_EPG0_IML_MMCF_A.csv'), 'r')
    file_reader = csv.reader(f_usa_pip_lng, delimiter=',')
    lng_points = []
    pip_lng_raw = []
    for index, row in enumerate(file_reader):
        if index == 2:
            lng_points = row
        if row[0][:4] == str(Ar.years[0] - 1):
            pip_lng_raw = row
    for index, element in enumerate(lng_points):
        try:
            temp_state = element[element.index(',') + 2:element.index(',') + 4].upper()  # State name from , (ex.: , MD)
            if 'Mexico' in element:
                Ar.pip_flow_lng_raw['MNW'][temp_state] += float(
                    pip_lng_raw[index])
            elif 'Canada' in element:
                Ar.pip_flow_lng_raw['ON'][temp_state] += float(
                    pip_lng_raw[index])
            else:
                Ar.pip_flow_lng_raw['ROW'][temp_state] += float(
                    pip_lng_raw[index])
        except ValueError:
            continue
    f_usa_pip_lng.close()
    os.remove(Fx.include('NG_MOVE_POE1_A_EPG0_IML_MMCF_A.csv'))


# USA LNG Imports/Exports ##############################################################################################
# Takes ratios of raw LNG import and export data and applies them to projections
def pip_flow_7():
    f_lng_imports_exports_csv = open(Fx.include('Natural_Gas_Imports_and_Exports.csv'), 'r')
    file_reader = csv.reader(f_lng_imports_exports_csv, delimiter=',')
    year_shift = 0
    for row in file_reader:
        if Fx.year_sh(row, ''):
            # Read in correct data based on year
            year_shift = Fx.year_sh(row, '')
        # SPECIAL STATISTIC FOR MEXICAN PRICE
        if row[0] == Ar.lng_imports:
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    for month in Ar.months:
                        for state_from in [state for state in Ar.states_acronyms2 if state not in
                                           Ar.usa_states_acronyms2]:
                            for state_to in Ar.usa_states_acronyms2:
                                Ar.pip_flow_lng[state_from][state_to][month + '-' +
                                                                      str(index + Ar.years[0] - year_shift)] = float(
                                    element) * Ar.pip_flow_lng_raw[state_from][state_to] / sum(
                                    [sum(dct.values()) for dct in Ar.pip_flow_lng_raw.values()]) / 12
        if row[0] == Ar.lng_exports:
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    for month in Ar.months:
                        for state_from in Ar.usa_states_acronyms2:
                            for state_to in [state for state in Ar.states_acronyms2 if state not in
                                             Ar.usa_states_acronyms2]:
                                Ar.pip_flow_lng[state_from][state_to][month + '-' +
                                                                      str(index + Ar.years[0] - year_shift)] = float(
                                    element) * Ar.pip_flow_lng_raw[state_from][state_to] / sum(
                                    [sum(dct.values()) for dct in Ar.pip_flow_lng_raw.values()]) / 12
    f_lng_imports_exports_csv.close()


# USA LNG Imports/Exports Units ########################################################################################
# Convert TCF/Year to BCF/Day
def pip_flow_8():
    Fx.convert(Ar.pip_flow_lng, 3, 1000/365)
