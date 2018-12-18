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
Fx.to_csv("End_-_Use_Demand", "End - Use Demand")  # Canadian Consumption
Fx.to_csv("Electricity_Generation", "Electricity Generation")  # Canadian Consumption for Electricity
Fx.to_csv("Primary_Energy_Demand", "Primary Energy Demand")  # Canadian Consumption Price for Electricity
Fx.to_csv("End_-_Use_Prices", "End - Use Prices")  # Canadian Consumption Price for Commercial\
Fx.to_csv("reg_bal_mex", "reg_bal_mex")  # All Statistics for Mexico
Fx.to_csv("EIA-StatetoStateCapacity", "Pipeline State2State Capacity")  # Canadian Pipe Capacity
Fx.to_csv("mex_pip_cap_bcfd", "mex_pip_cap_bcfd")  # Mexico Pipe Capacity
Fx.to_csv("can_pip_cap", "can_pip_cap")  # Canadian Pipe Capacity
print('Converted XLSX to CSV')
# Production Raw Data ##################################################################################################
Us.prod_1()  # Obtain US Production Raw Data
Us.prod_2()  # Obtain US Production Raw Data for Alaska/Hawaii
Us.prod_3()  # Obtain US Production Conversion Matrix from NEMS to NANGAM
Us.prod_4()  # Matrix Multiply NEMS Raw Production Data to NANGAM Production Data
Us.prod_5()  # Aggregate NANGAM Production Data
print('Completed US Production')
Ca.prod_1()  # Obtain CAN Production Raw Data, then Combining Individual Province Data to Region Data
Ca.prod_2()  # Aggregate CAN Production Data
print('Completed CAN Production')
Mx.prod_1()  # Obtain MEX Production Data
Mx.prod_2()  # Aggregate MEX Production Data
print('Completed MEX Production')
Rw.prod_1()  # Obtain ROW Production Data
Rw.prod_2()  # Aggregate ROW Production Data
print('Completed ROW Production')
# Production Price Raw Data ############################################################################################
Us.prod_price_1()  # Obtain US Production Price Raw Data
Us.prod_price_2()  # Calculate US Production Price Value Data from Production Price Raw Data
Us.prod_price_3()  # Matrix Multiply NEMS Price Value Data to NANGAM Final Production Price Data
Us.prod_price_4()  # Aggregate US Production Price Data
print('Completed US Production Price')
Ca.prod_price_1()  # Obtain CAN Production Price Data
Ca.prod_price_2()  # Aggregate CAN Production Price Data
print('Completed CAN Production Price')
Mx.prod_price_1()  # Obtain MEX Production Price Data
Mx.prod_price_2()  # Aggregate MEX Production Price Data
print('Completed MEX Production Price')
# Consumption ##########################################################################################################
Us.cons_1()  # Obtain US Consumption Data
Us.cons_2()  # Obtain US Consumption Data for Alaska/Hawaii
print('Completed US Consumption')
Ca.cons_1()  # Obtain CAN Population Raw Data
Ca.cons_2()  # Obtain CAN Consumption Data
Ca.cons_3()  # Obtain CAN Consumption Data for Electric Power
Ca.cons_4()  # Calculate CAN Consumption Data for Electric Power
Ca.cons_5()  # Aggregate CAN Consumption Data
print('Completed CAN Consumption')
Mx.cons_1()  # Obtain MEX Consumption Data
print('Completed MEX Consumption')
Rw.cons_1()  # Obtain ROW Consumption Data
Rw.cons_2()  # Obtain ROW Consumption Sector Data
# Consumption Prices ###################################################################################################
Us.cons_price_1()  # Obtain US Consumption Price Data
Us.cons_price_2()  # Calculate Alaska/Hawaii Consumption Price Data
print('Completed US Consumption Price')
Ca.cons_price_1()  # Obtain CAN Consumption Price Data
Ca.cons_price_2()  # Aggregate CAN Consumption Price Data
print('Completed CAN Consumption Price')
Mx.cons_price_1()  # Obtain MEX Consumption Price Data
Mx.cons_price_2()  # Aggregate MEX Consumption Price Data
print('Completed MEX Consumption Price')
# Convert Units ########################################################################################################
Us.conversion()  # Convert US Units
Ca.conversion()  # Convert CAN Units
Mx.conversion()  # Convert MEX Units
Rw.conversion()  # Convert ROW Units
print('Completed Unit Conversion')
# Pipe Capacity ########################################################################################################
Pc.pip_cap_1()  # US Pipe Capacity
Pc.pip_cap_2()  # MEX Pipe Capacity
Pc.pip_cap_3()  # CAN Pipe Capacity
Pc.pip_cap_4()  # Remove Intraregional Pipes
print('Completed Pipe Capacity')
# Pipe Flow ############################################################################################################
Pc.pip_flow_1()  # US Pipe Flow from US
Pc.pip_flow_2()  # MEX Pipe Flow to and from US
Pc.pip_flow_3()  # CAN Pipe Flow from US
Pc.pip_flow_4()  # CAN Pipe Flow from CAN
Pc.pip_flow_5()  # Remove Intraregional Pipes
print('Completed Pipe Flow')
# Aggregate Data #######################################################################################################
Fx.aggregate()  # Aggregate All Data
# Print data to excel files ############################################################################################
# ExcelWriter pandas object on an excel file called 'Output.xlsx'
writer = pd.ExcelWriter(Fx.include('Output.xlsx'), engine='xlsxwriter')
# Write all Production Data
Fx.write_all(writer, ['Production', 'BCF/Day', str(Ar.years[0]) + ' to ' + str(Ar.years[-1]), '', '', '', ''],
             Ar.usa_prod, Ar.can_prod, Ar.mex_prod, Ar.row_prod, Ar.prod_stats_acronyms, Ar.years, 'Production')
# Write all Production Price Data
Fx.write_all(writer,
             ['Production Price', '$Million/BCF', str(Ar.years[0]) + ' to ' + str(Ar.years[-1]), '', '', '', ''],
             Ar.usa_prod_price, Ar.can_prod_price, Ar.mex_prod_price, Ar.row_prod_price, Ar.prod_stats_acronyms,
             Ar.years, 'Production Price')
# Write all Consumption Data
Fx.write_all(writer, ['Consumption', 'BCF/Day', str(Ar.years[0]) + ' to ' + str(Ar.years[-1]), '', '', '', ''],
             Ar.usa_cons, Ar.can_cons, Ar.mex_cons, Ar.row_cons, Ar.cons_sectors, Ar.years, 'Consumption')
# Write all Consumption Price Data
Fx.write_all(writer, ['Consumption Price', '$Million/BCF', str(Ar.years[0]) + ' to ' + str(Ar.years[-1]), '', '', '',
                      ''], Ar.usa_cons_price, Ar.can_cons_price, Ar.mex_cons_price, Ar.row_cons_price,
             Ar.cons_sectors, Ar.years, 'Consumption Price')
# Style all four sheets
Fx.style_sheet(writer, ['Production', 'Consumption', 'Production Price', 'Consumption Price'])
Fx.write_cap(writer, ['Pipeline Capacity', 'BCF/Day', str(Ar.years[0]), '', '', '', ''], 'Pipeline Capacity')
Fx.write_flow(writer, ['Pipeline Flow', 'BCF/Day', str(Ar.years[0]) + ' to ' + str(Ar.years[-1]), '', '', '', ''],
              'Pipeline Flow')
writer.save()
print('Completed Writing XLSX')
print('File Opening...')
# Start Up Files #######################################################################################################
file = os.path.join(Fx.include('Output.xlsx'))
os.startfile(file)
