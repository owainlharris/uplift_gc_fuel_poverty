"""
fuel_poverty_census_analysis.py

This script is designed to plot England 2021 Census data alongisde fuel poverty data, looking for correlations between the two. 

Created by Owain Harris  20-6-23
"""

#Import Libraries
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt 
import seaborn as sns 

# Import and Clean Central Heating Data from UK Census 
central_heating = pd.read_csv('central_heating_uk_2021_census.csv')
central_heating = central_heating.rename(columns={'Lower tier local authorities Code':'Area Code', 'Lower tier local authorities':'Name', 'Type of central heating in household (13 categories) Code':'Heating Type Code', 'Type of central heating in household (13 categories)':'Central Heating Type'}).drop(['Heating Type Code'], axis=1)
central_heating['Household No.s'] = central_heating['Observation'].groupby(central_heating['Area Code']).transform('sum')
central_heating['Observation (%)'] = central_heating['Observation'] / central_heating['Household No.s'] * 100

# Import and Clean Fuel Poverty Data
fuel_poverty = pd.read_excel('sub_regional_fuel_poverty_2021.xlsx', sheet_name='Table 2', skiprows=2) # create column of all local authorities
fuel_poverty = fuel_poverty.rename(columns={'Area Codes [Note 4]':'Area Code', 'Number of households':'Household No.s Census', 'Number of households in fuel poverty':'In Fuel Poverty', 'Proportion of households fuel poor (%)':'Households in Fuel Poverty (%)'}).drop(['Unnamed: 2', 'Unnamed: 3'], axis=1)

# Merge Data Sets
heating_and_poverty = pd.merge(central_heating, fuel_poverty, on='Area Code')

# Plot Fuel Poverty for All Central Heating Types
custom_palette = sns.color_palette("tab20", 13)
sns.relplot(data = heating_and_poverty, x='Observation (%)', y='Households in Fuel Poverty (%)', hue='Central Heating Type', palette=custom_palette, legend='full')
# plt.savefig('all_central_heating_vs_fuel_poverty.png', dpi=500)
plt.show()

# Plot Fuel Poverty for Gas Only Central Heating
heating_and_poverty_gas = heating_and_poverty[heating_and_poverty['Central Heating Type'] == 'Mains gas only']
print(heating_and_poverty_gas)
heating_and_poverty_gas = heating_and_poverty_gas.rename(columns={'Observation (%)':'Households with Gas Central Heating (%)'})
heating_and_poverty_gas.plot(x='Households with Gas Central Heating (%)', y='Households in Fuel Poverty (%)', kind='scatter', color ='blue')
plt.title('Gas Central Heating Only vs Fuel Poverty in England 2021')
plt.savefig('gas_central_heating_vs_fuel_poverty.png', dpi=500)
plt.show()

# Import Tenure Census Data
tenure = pd.read_csv('tenure_census_2021.csv')
tenure = tenure.rename({'Lower tier local authorities Code':'Area Code', 'Lower tier local authorities':'Name', 'Tenure of household (7 categories) Code':'Tenure Code', 'Tenure of household (7 categories)':'Tenure'}, axis=1).drop(['Tenure Code'], axis=1)
tenure['Household No.s'] = tenure['Observation'].groupby(tenure['Area Code']).transform('sum')
tenure['Observation (%)'] = tenure['Observation'] / tenure['Household No.s'] * 100
print(tenure)

# Merge Tenure Data with Fuel Poverty Data
tenure_and_poverty = pd.merge(tenure, fuel_poverty, on='Area Code')

# Plot Fuel Poverty for All Tenure Types
sns.relplot(data = tenure_and_poverty, x='Observation (%)', y='Households in Fuel Poverty (%)', hue='Tenure', palette='tab10', legend='full')
plt.savefig('all_tenure_vs_fuel_poverty.png', dpi=500)
plt.show()

# Import Accomoation Type Census Data
accommodation_type = pd.read_csv('accomodation_type_census_2021.csv')
accommodation_type = accommodation_type.rename({'Lower tier local authorities Code':'Area Code', 'Lower tier local authorities':'Name', 'Accommodation type (5 categories) Code':'Accommodation Type Code', 'Accommodation type (5 categories)':'Accommodation Type'}, axis=1)
accommodation_type['Household No.s'] = accommodation_type['Observation'].groupby(accommodation_type['Area Code']).transform('sum')
accommodation_type['Observation (%)'] = accommodation_type['Observation'] / accommodation_type['Household No.s'] * 100

# Merge Accomodation Type Data with Fuel Poverty Data
accommodation_type_and_poverty = pd.merge(accommodation_type, fuel_poverty, on='Area Code')

# Plot Fuel Poverty for All Accomodation Types
sns.relplot(data = accommodation_type_and_poverty, x='Observation (%)', y='Households in Fuel Poverty (%)', hue='Accommodation Type', palette='tab10', legend='full')
plt.savefig('all_accommodation_type_vs_fuel_poverty.png', dpi=500)
plt.show()

# Import Household Deprivation Census Data
deprivation = pd.read_csv('household_deprivation_census_2021.csv')
deprivation = deprivation.rename({'Lower tier local authorities Code':'Area Code', 'Lower tier local authorities':'Name', 'Household deprivation (6 categories) Code':'Deprivation Code', 'Household deprivation (6 categories)':'Deprivation'}, axis=1)
deprivation['Household No.s'] = deprivation['Observation'].groupby(deprivation['Area Code']).transform('sum')
deprivation['Observation (%)'] = deprivation['Observation'] / deprivation['Household No.s'] * 100

# Merge Deprivation Data with Fuel Poverty Data
deprivation_and_poverty = pd.merge(deprivation, fuel_poverty, on='Area Code')

# Plot Fuel Poverty for All Deprivation Types
sns.relplot(data = deprivation_and_poverty, x='Observation (%)', y='Households in Fuel Poverty (%)', hue='Deprivation', palette='tab10', legend='full')
plt.savefig('all_deprivation_vs_fuel_poverty.png', dpi=500)
plt.show()

# Plot Not-Deprived vs Fuel Poverty - colour code by regions 
deprivation_and_poverty_not_deprived = deprivation_and_poverty[deprivation_and_poverty['Deprivation'] == 'Household is not deprived in any dimension']
deprivation_and_poverty_not_deprived.plot(x='Observation (%)', y='Households in Fuel Poverty (%)', kind='scatter', color ='red')
plt.title('Deprivation vs Fuel Poverty in England 2021')
plt.savefig('deprivation_vs_fuel_poverty.png', dpi=500)
plt.show()