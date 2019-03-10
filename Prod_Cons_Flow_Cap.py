# Prod_Cons calls the CAN_Functions, USA_Functions, and MEX_Functions files to generate csv files, create data
# dictionaries, and write to the excel files

# Note: Alaska Total Consumption Price and Canada Consumption Price have been adjusted to be more accurate
########################################################################################################################
########################################################################################################################
########################################################################################################################
# Import Statements
import os
import USA_Functions as Us
import CAN_Functions as Ca
import MEX_Functions as Mx
import ROW_Functions as Rw
import PIP_CAP_Functions as Pc
import Functions as Fx
import Arrays as Ar
import pandas as pd
# Convert to CSV #######################################################################################################
# Convert all Excel files to CSV files with the xlsx name and sheet name
Fx.to_csv("NEMS_to_NANGAM_ONS", 'Sheet1')  # NEMS to NANGAM Conversion Matrix Onshore
Fx.to_csv("NEMS_to_NANGAM_OFS", 'Sheet1')  # NEMS to NANGAM Conversion Matrix Offshore
Fx.to_csv("Natural_Gas_Production", "Natural Gas Production")  # Consumption Price for Mexico and Canada
Fx.to_csv("reg_bal_mex", "reg_bal_mex")  # All Statistics for Mexico
Fx.to_csv("End_-_Use_Prices_Commercial", "End - Use Prices")  # Canadian Consumption Price for Commercial
Fx.to_csv("End_-_Use_Prices_Industrial", "End - Use Prices")  # Canadian Consumption Price for Industrial
Fx.to_csv("End_-_Use_Prices_Residential", "End - Use Prices")  # Canadian Consumption Price for Residential
Fx.to_csv("EIA-StatetoStateCapacity", "Pipeline State2State Capacity")  # Canadian Pipe Capacity
Fx.to_csv("mex_pip_cap_bcfd", "mex_pip_cap_bcfd")  # Mexico Pipe Capacity
Fx.to_csv("can_pip_cap", "can_pip_cap")  # Canadian Pipe Capacity
Fx.to_csv('EIA-NaturalGasPipelineProjects', 'Natural Gas Pipeline Projects')  # USA Future Pipelines
Fx.to_csv('NG_MOVE_POE2_A_EPG0_ENG_MMCF_A', 'Data 1')  # USA LNG Exports
Fx.to_csv('NG_MOVE_POE1_A_EPG0_IML_MMCF_A', 'Data 1')  # USA LNG Imports
Fx.to_csv('new_output', 'Consumption', '_consumption')  # Month and State Consumption
Fx.to_csv('new_output', 'Production', '_production')  # Month and State Production
for region in Ar.canadian_provinces_full:
    Fx.to_csv("End_-_Use_Demand_" + region, "End - Use Demand")  # Canadian Consumption
    Fx.to_csv("Primary_Energy_Demand_" + region, "Primary Energy Demand")  # Canadian Consumption Price for Electricity
Fx.to_csv('NG_PRI_SUM_A_EPG0_PCS_DMCF_M', 'Data 1')  # USA State Consumption Price
Fx.to_csv('NG_PRI_SUM_A_EPG0_PDV_DMCF_A', 'Data 1')  # USA State Consumption Price
Fx.to_csv('NG_PRI_SUM_A_EPG0_PEU_DMCF_M', 'Data 1')  # USA State Consumption Price
Fx.to_csv('NG_PRI_SUM_A_EPG0_PIN_DMCF_M', 'Data 1')  # USA State Consumption Price
Fx.to_csv('NG_PRI_SUM_A_EPG0_PRS_DMCF_M', 'Data 1')  # USA State Consumption Price
print('Converted XLSX to CSV')
# Production Raw Data ##################################################################################################
Us.prod_1()  # Obtain USA Production Raw Data
Us.prod_2()  # Obtain USA Production Raw Data for Alaska/Hawaii
Us.prod_3()  # Obtain USA Production Conversion Matrix from NEMS to NANGAM
Us.prod_4()  # Matrix Multiply NEMS Raw Production Data to NANGAM Production Data
Us.prod_5()  # Aggregate NANGAM Production Data
Ca.prod_1()  # Obtain CAN Production Raw Data, then Combining Individual Province Data to Region Data
Ca.prod_2()  # Aggregate CAN Production Data
Mx.prod_1()  # Obtain MEX Production Data
Mx.prod_2()  # Aggregate MEX Production Data
Rw.prod_1()  # Obtain ROW Production Data
Rw.prod_2()  # Aggregate ROW Production Data
print('Completed Production')
# Production Price Raw Data ############################################################################################
Us.prod_price_1()  # Obtain USA Production Price Raw Data
Us.prod_price_2()  # Calculate USA Production Price Value Data from Production Price Raw Data
Us.prod_price_3()  # Matrix Multiply NEMS Price Value Data to NANGAM Final Production Price Data
Us.prod_price_4()  # Aggregate USA Production Price Data
Ca.prod_price_1()  # Obtain CAN Production Price Data
Ca.prod_price_2()  # Aggregate CAN Production Price Data
Mx.prod_price_1()  # Obtain MEX Production Price Data
Mx.prod_price_2()  # Aggregate MEX Production Price Data
print('Completed Production Price')
# Consumption ##########################################################################################################
Us.cons_1()  # Obtain USA Consumption Data
Us.cons_2()  # Obtain US AConsumption Data for Alaska/Hawaii
Ca.cons_2()  # Obtain CAN Consumption Data
Ca.cons_3()  # Obtain CAN Consumption Data for Electric Power
Ca.cons_5()  # Aggregate CAN Consumption Data
Mx.cons_1()  # Obtain MEX Consumption Data
Rw.cons_1()  # Obtain ROW Consumption Data
Rw.cons_2()  # Obtain ROW Consumption Sector Data
print('Completed Consumption')
# Consumption Prices ###################################################################################################
Us.cons_price_1()  # Obtain USA Consumption Price Data
Us.cons_price_2()  # Calculate Alaska/Hawaii Consumption Price Data
Ca.cons_price_1()  # Obtain CAN Consumption Price Data
Ca.cons_price_2()  # Aggregate CAN Consumption Price Data
Mx.cons_price_1()  # Obtain MEX Consumption Price Data
Mx.cons_price_2()  # Aggregate MEX Consumption Price Data
print('Completed Consumption Price')
# Convert Units ########################################################################################################
Us.conversion()  # Convert USA Units
Ca.conversion()  # Convert CAN Units
Mx.conversion()  # Convert MEX Units
Rw.conversion()  # Convert ROW Units
print('Completed Unit Conversion')
# Pipe Capacity ########################################################################################################
Pc.pip_cap_1()  # USA -> USA, USA -> CAN, CAN -> USA, USA -> MEX, MEX -> USA Pipe Capacity
Pc.pip_cap_2()  # MEX -> MEX Pipe Capacity
Pc.pip_cap_3()  # CAN -> CAN Pipe Capacity
Pc.pip_cap_4()  # Remove Intraregional Pipes
print('Completed Pipe Capacity')
# Pipe Flow ############################################################################################################
Pc.pip_flow_1()  # USA -> USA, USA -> CAN, CAN -> USA Pipe Flow
Pc.pip_flow_2()  # USA -> MEX, MEX -> USA Pipe Flow
Pc.pip_flow_3()  # USA -> CAN Pipe Flow
Pc.pip_flow_4()  # CAN -> CAN Pipe Flow
Pc.pip_flow_5()  # Remove Intraregional Pipes
Pc.pip_flow_6()  # USA -> CAN, USA -> MEX LNG Pipe Flow
Pc.pip_flow_7()  # USA -> CAN, USA -> MEX LNG Pipe Flow
Pc.pip_flow_8()  # Unit Conversion
print('Completed Pipe Flow')
# Aggregate Data #######################################################################################################
Fx.aggregate()  # Aggregate All Data
# Print data to excel files ############################################################################################
# ExcelWriter pandas object on an excel file called 'Output.xlsx'
writer = pd.ExcelWriter(Fx.include('Yearly Output.xlsx'), engine='xlsxwriter')
# Write all Production Data
Fx.write_all(writer, ['Production', 'BCF/Day', str(Ar.years[0]) + ' to ' + str(Ar.years[-1]), '', '', '', ''],
             Ar.usa_prod, Ar.can_prod, Ar.mex_prod, Ar.row_prod, Ar.prod_stats_acronyms, Ar.years, 'Production',
             'Production')
# Write all Production Price Data
Fx.write_all(writer,
             ['Production Price', '$Million/BCF', str(Ar.years[0]) + ' to ' + str(Ar.years[-1]), '', '', '', ''],
             Ar.usa_prod_price, Ar.can_prod_price, Ar.mex_prod_price, Ar.row_prod_price, Ar.prod_stats_acronyms,
             Ar.years, 'Production Price', 'Production Price')
# Write all Consumption Data
Fx.write_all(writer, ['Consumption', 'BCF/Day', str(Ar.years[0]) + ' to ' + str(Ar.years[-1]), '', '', '', ''],
             Ar.usa_cons, Ar.can_cons, Ar.mex_cons, Ar.row_cons, Ar.cons_sectors, Ar.years, 'Consumption',
             'Consumption')
# Write all Consumption Price Data
Fx.write_all(writer, ['Consumption Price', '$Million/BCF', str(Ar.years[0]) + ' to ' + str(Ar.years[-1]), '', '', '',
                      ''], Ar.usa_cons_price, Ar.can_cons_price, Ar.mex_cons_price, Ar.row_cons_price,
             Ar.cons_sectors, Ar.years, 'Consumption Price', 'Consumption Price')
# Style all four sheets
Fx.style_sheet(writer, ['Production', 'Consumption', 'Production Price', 'Consumption Price'])
Fx.write_cap(writer, ['Pipeline Capacity', 'BCF/Day', str(Ar.years[0]), '', '', '', ''], 'Pipeline Capacity')
Fx.write_flow(writer, ['Pipeline Flow', 'BCF/Day', str(Ar.years[0]) + ' to ' + str(Ar.years[-1]), '', '', '', ''],
              'Pipeline Flow', Ar.pip_flow)
Fx.write_flow(writer, ['LNG Pipeline Flow', 'BCF/Day', str(Ar.years[0]) + ' to ' + str(Ar.years[-1]), '', '', '', ''],
              'LNG Pipeline Flow', Ar.pip_flow_lng)
writer.save()
print('Completed Writing XLSX')
print('File Opening...')
# Start Up Files #######################################################################################################
file = os.path.join(Fx.include('Yearly Output.xlsx'))
os.startfile(file)


########################################################################################################################
########################################################################################################################
# Stuff for Max to Use #################################################################################################
########################################################################################################################
########################################################################################################################
production = dict.fromkeys(Ar.prod_stats_acronyms)
production_price = dict.fromkeys(Ar.prod_stats_acronyms)
consumption = dict.fromkeys(Ar.cons_sectors)
consumption_price = dict.fromkeys(Ar.cons_sectors)
flow = dict.fromkeys(Ar.states_acronyms2)
for region in Ar.states_acronyms2:
    flow[region] = dict.fromkeys(Ar.states_acronyms2)
# print(Ar.usa_prod, Ar.can_prod, Ar.mex_prod, Ar.row_prod)
for prod_stat in Ar.prod_stats_acronyms:
    production[prod_stat] = pd.DataFrame(
        [[Fx.return_dict(Ar.usa_prod, Ar.can_prod, Ar.mex_prod, Ar.row_prod, Ar.prod_stats_acronyms
                         )[prod_stat][region][year] for region in Ar.all_regions_acronyms]
         for year in Ar.years], index=Ar.years,
        columns=Ar.all_regions_acronyms)
    production_price[prod_stat] = pd.DataFrame(
        [[Fx.return_dict(Ar.usa_prod_price, Ar.can_prod_price, Ar.mex_prod_price, Ar.row_prod_price,
                         Ar.prod_stats_acronyms
                         )[prod_stat][region][year] for region in Ar.all_regions_acronyms]
         for year in Ar.years], index=Ar.years,
        columns=Ar.all_regions_acronyms)
for cons_sector in Ar.cons_sectors:
    consumption[cons_sector] = pd.DataFrame(
        [[Fx.return_dict(Ar.usa_cons, Ar.can_cons, Ar.mex_cons, Ar.row_cons, Ar.cons_sectors
                         )[cons_sector][region][year] for region in Ar.all_regions_acronyms]
         for year in Ar.years], index=Ar.years,
        columns=Ar.all_regions_acronyms)
    consumption_price[cons_sector] = pd.DataFrame(
        [[Fx.return_dict(Ar.usa_cons_price, Ar.can_cons_price, Ar.mex_cons_price, Ar.row_cons_price,
                         Ar.cons_sectors
                         )[cons_sector][region][year] for region in Ar.all_regions_acronyms]
         for year in Ar.years], index=Ar.years,
        columns=Ar.all_regions_acronyms)
for region_from in Ar.states_acronyms2:
    for region_to in Ar.states_acronyms2:
        flow[region_from][region_to] = pd.Series(Ar.pip_flow[region_from][region_to])
capacity = pd.DataFrame(Ar.pip_cap)
# print(production, production_price, consumption, consumption_price, flow, capacity)
# Production, Production_Price are Dictionaries with Keys in ['ONS', 'OFS', 'Total'] and values that are time series
# with columns indexed by region acronyms (Ar.all_regions_acronyms)

# Consumption, Consumption_Price are Dictionaries with Keys in ['All Sectors', 'Transportation', 'Residential',
# 'Industrial', 'Electric Power', 'Commercial'] and values that are time series with columns indexed by region acronyms
# (Ar.all_regions_acronyms)

# Flow and LNG Flow are nested dictionaries with first key (Region From) in Ar.all_regions_acronyms and second key
# (Region To) in Ar.all_regions_acronyms and values that are time series

# Capacity is a DataFrame with indices (Region From) and columns (Region To) in Ar.all_regions_acronyms
Fx.monthify_statify()
