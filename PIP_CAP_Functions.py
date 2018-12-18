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
    for row in file_reader:
        if row[0] == Ar.capacity_year:
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
        try:
            # If pipeline is active in base year
            if float(row[0]) == Ar.years[0]:
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
                    for region in Ar.states_to_regions:
                        if Ar.states_dict[row[pip_state_from_ind]] in Ar.states_to_regions[region]:
                            region_from = region
                # If the pipeline originates from Canada, lookup region based on province
                if row[pip_state_from_ind] in Ar.canadian_provinces_full:
                    for region in Ar.provinces_to_regions:
                        if Ar.provinces_dict[row[pip_state_from_ind]] in Ar.provinces_to_regions[region]:
                            region_from = region
                # If the pipeline goes to mexico, lookup region based on city
                if row[pip_state_to_ind] == Ar.mexico:
                    for region in Ar.cities_to_regions:
                        if row[pip_county_to_ind] in Ar.cities_to_regions[region]:
                            region_to = region
                # If the pipeline goes to the US, lookup region based on state
                if row[pip_state_to_ind] in Ar.usa_states_full:
                    for region in Ar.states_to_regions:
                        if Ar.states_dict[row[pip_state_to_ind]] in Ar.states_to_regions[region]:
                            region_to = region
                # If the pipeline goes to Canada, lookup region based on province
                if row[pip_state_to_ind] in Ar.canadian_provinces_full:
                    for region in Ar.provinces_to_regions:
                        if Ar.provinces_dict[row[pip_state_to_ind]] in Ar.provinces_to_regions[region]:
                            region_to = region
                # Fill pip_cap by adding pipeline capacity to the total pipeline capacity between two regions
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
                if element == Ar.region_from and pip_region_from_ind == -99999:
                    pip_region_from_ind = index
                if element == Ar.region_to and pip_region_to_ind == -99999:
                    pip_region_to_ind = index
                if element == Ar.capacity and pip_capacity_ind == -99999:
                    pip_capacity_ind = index
        try:
            # Add to pipe capacity for pipes region from -> region to
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
# USA to USA and USA to Canada Pipe Flow. Pipe flow is directly read from Primary_Natural_Gas_Flows_Entering_NGTDM_Regio
# n_from_Neighboring_Regions.csv. If a flow goes through a region, then the flow is counted twice: once of the original
# region to the intermediate region and once of the intermediate region to the final region (manually done)
def pip_flow_1():
    f_usa_pip_flow = open(Fx.include('Primary_Natural_Gas_Flows_Entering_NGTDM_Region_from_Neighboring_Regions.csv'),
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
                    Ar.pip_flow[Ar.reverse_full_dict[row[0]]][region_to_temp][index + Ar.years[0] - year_shift] += \
                        float(element)/365
    f_usa_pip_flow.close()


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
        mex_to_usa_sum = sum([Ar.pip_cap[mexico_region][nangam_region] for nangam_region in Ar.nangam_regions_acronyms])
        usa_to_mex_sum = sum([Ar.pip_cap[nangam_region][mexico_region] for nangam_region in Ar.nangam_regions_acronyms])
        for nangam_region in Ar.nangam_regions_acronyms:
            try:
                # Ratio of exports from mexican regions for each mexican region (ratios for different nangam regions sum
                # to one)
                Ar.mex_to_usa_dict[mexico_region][nangam_region] = Ar.pip_cap[mexico_region][nangam_region] /\
                                                                   mex_to_usa_sum
            except ZeroDivisionError:
                Ar.mex_to_usa_dict[mexico_region][nangam_region] = 0
            try:
                # Ratio of imports to mexican regions for each mexican region (ratios for different nangam regions sum
                # to one)
                Ar.usa_to_mex_dict[nangam_region][mexico_region] = Ar.pip_cap[nangam_region][mexico_region] / \
                                                                   usa_to_mex_sum
            except ZeroDivisionError:
                Ar.usa_to_mex_dict[nangam_region][mexico_region] = 0
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
                    for nangam_region in Ar.nangam_regions_acronyms:
                        # Set pip_flow with pipe flow data for each mexican region, nangam region, and year as the total
                        # exports from Mexican regions distributed over the ratios provided by each nangam
                        # region divided by 1000 for units
                        try:
                            Ar.pip_flow[mex_pipe_region_temp][nangam_region][index + Ar.years[0] - year_shift] = \
                                float(element) * Ar.mex_to_usa_dict[mex_pipe_region_temp][nangam_region] / 1000
                        except ValueError:
                            continue
        if mex_pipe_region_temp != '' and row[0] == Ar.imports:
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    for nangam_region in Ar.nangam_regions_acronyms:
                        # Set pip_flow with pipe flow data for each mexican region, nangam region, and year as the total
                        # imports to Mexican regions distributed over the ratios provided by each nangam
                        # region divided by 1000 for units
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
# Pipeline flow from the United States to Canada modeled off flow to each Canadian region being proportional to capacity
# to each Canadian region. Total pipeline flow/exports are read from Natural_Gas_Imports_and_Exports.csv
def pip_flow_3():
    f_can_pip_flow = open(Fx.include('Natural_Gas_Imports_and_Exports.csv'), 'r')
    file_reader = csv.reader(f_can_pip_flow, delimiter=',')
    year_shift = 0
    usa_to_can_sum = 0
    for canadian_region in Ar.canadian_regions_acronyms:
        for nangam_region in Ar.nangam_regions_acronyms:
            # Sum total pipe capacity from United States to Canada
            usa_to_can_sum += Ar.pip_cap[nangam_region][canadian_region]
    for row in file_reader:
        if Fx.year_sh(row, ''):
            # Read in correct data based on year
            year_shift = Fx.year_sh(row, '')
        if row[0] == Ar.usa_to_can:
            for index, element in enumerate(row):
                if index + Ar.years[0] - year_shift in Ar.years:
                    for canadian_region in Ar.canadian_regions_acronyms:
                        for nangam_region in Ar.nangam_regions_acronyms:
                            # Set pipe flow from a nangam region to canadian region proportional to the capacity from
                            # the nangam region to canadian region (total exports from us to canada times the ratio of
                            # the capacity between two regions over the capacity between the two countries)
                            Ar.pip_flow[nangam_region][canadian_region][index + Ar.years[0] - year_shift] += \
                                float(element) * 1000/365 * Ar.pip_cap[nangam_region][canadian_region] / usa_to_can_sum
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
    pip_flow_ind = -99999
    for row in file_reader:
        if row[0] == '':
            for index, element in enumerate(row):
                # Found column indices based on keywords found in the row
                if element == Ar.region_from and pip_region_from_ind == -99999:
                    pip_region_from_ind = index
                if element == Ar.region_to and pip_region_to_ind == -99999:
                    pip_region_to_ind = index
                if element == Ar.can_to_can and pip_flow_ind == -99999:
                    pip_flow_ind = index
        try:
            # Add to pipeline flow for region_from -> region_To for each year
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
