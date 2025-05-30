'''
This file contains all necessary elements to run the code, create a usable database and all outputs
More information can be found in the Akasha Guidebook avaliable in the GitHub repository
'''

import pandas
import matplotlib.pyplot as plt
from itertools import zip_longest
import json
import os
import sys

from Entity.Combustion.fixed_comb_entity import FixedCombustion
from Entity.Combustion.mobile_comb_entity import MobileCombustion
from Entity.Energy.energy_entity import Energy, EnergyType
from Entity.Materials.materials_production_entity import MaterialsProduction
from Entity.Materials.materials_use_entity import MaterialsUse
from Entity.ProjectPhases.project_phases_entity import ProjectPhases, Phase
from Entity.SoilUseChange.soil_use_change_entity import SoilUseChange
from Entity.Vehicles.vehicles_entity import Vehicles, VehiclesType
from Entity.WasteTreatm.waste_treatm_entity import WasteTreatment

from Services.ProjectPhases.project_phases_service import ProjectPhasesService
from Services.Energy.energy_calc_service import EnergyCalculations
from Services.Combustion.fixed_comb_calc_service import FixedCombustionCalculations
from Services.Combustion.mobile_comb_calc_service import MobileCombustionCalculations
from Services.Materials.materials_production_calc_service import MaterialsProductionCalculations
from Services.Materials.materials_use_calc_service import MaterialsUseCalculations
from Services.SoilUseChange.soil_use_change_calc_service import SoilUseChangeCalculations
from Services.Vehicles.vehicles_calc_service import VehiclesCalculations
from Services.WasteTreatm.waste_treatm_calc_service import WasteTreatmentCalculations

'''
1. Transition between excel and .json format databse
- Creates new dictionaries for each emissions category
- Transposes the information for each element from the excel to a dictionary
- Creates the complete database with dictionaries (emissions catgory) of disctionaries (each element in that category)
'''

project_phases = {}
energy = {}
vehicles = {}
fixed_combustion = {}
mobile_combustion = {}
materials_prod = {}
materials_use = {}
soil_use_change = {}
waste_treatm = {}

def create_objects(xls, file_path):
    ''' 
    Get each element from the excel file and transposes into usable variables
    '''
    sheet_data = pandas.read_excel(file_path, sheet_name="PROJECT_PHASES")
    for index, row in sheet_data.iterrows():
        phase = row['project_phase']
        years = row['duration']
        
        object = ProjectPhases(phase, years)
        project_phases[phase] = object.to_dict()
    
    sheet_data = pandas.read_excel(file_path, sheet_name="ENERGY")
    for index, row in sheet_data.iloc[1:].iterrows():
        
        phase = row['project_phase']
        type = row['type']
        source = row['source']
        quantity = row['quantity']
        ef = row['emission_factor']
        
        object = Energy(phase, type, source, quantity, ef)
        energy[source] = object.to_dict()
        
    sheet_data = pandas.read_excel(file_path, sheet_name="VEHICLES")
    for index, row in sheet_data.iloc[1:].iterrows():
        phase = row['project_phase']
        type = row['type']
        vehicle = row['vehicle_fueltype']
        km = row['distance']
        n = row['n_vehicles']
        co2_emissions = row['co2_emissions']
        ch4_emissions = row['ch4_emissions']
        ch4_cf = row['ch4_corrfactor']
        n2o_emissions = row['n2o_emissions']
        n2o_cf = row['n2o_corrfactor']
        
        object = Vehicles(phase, type, vehicle, km, n, co2_emissions, \
            ch4_emissions, ch4_cf, n2o_emissions, n2o_cf)
        vehicles[vehicle] = object.to_dict()
        
    sheet_data = pandas.read_excel(file_path, sheet_name="FIXED_COMBUSTION")
    for index, row in sheet_data.iloc[1:].iterrows():
        phase = row['project_phase']
        enginery_fueltype = row['enginery_fueltype']
        quantity = row['quantity']
        n = row['n_machines']
        ef = row['emission_factor']
        
        object = FixedCombustion(phase, enginery_fueltype, quantity, n, ef)
        fixed_combustion[enginery_fueltype] = object.to_dict()
    
    sheet_data = pandas.read_excel(file_path, sheet_name="MOBILE_COMBUSTION")
    for index, row in sheet_data.iloc[1:].iterrows():
        phase = row['project_phase']
        enginery_fueltype = row['enginery_fueltype']
        quantity = row['quantity']
        n = row['n_machines']
        co2_emissions = row['co2_emissions']
        ch4_emissions = row['ch4_emissions']
        ch4_cf = row['ch4_corrfactor']
        n2o_emissions = row['n2o_emissions']
        n2o_cf = row['n2o_corrfactor']
        
        object = MobileCombustion(phase, enginery_fueltype, quantity, n,\
                    co2_emissions, ch4_emissions, ch4_cf, n2o_emissions, n2o_cf)
        mobile_combustion[enginery_fueltype] = object.to_dict()
        
    sheet_data = pandas.read_excel(file_path, sheet_name="MATERIALS_PRODUCTION")
    for index, row in sheet_data.iloc[1:].iterrows():
        phase = row['project_phase']
        material = row['material']
        process = row['process']
        quantity = row['quantity']
        ef = row['emission_factor']
        
        object = MaterialsProduction(phase, material, process, quantity, ef)
        materials_prod[material] = object.to_dict()
    
    sheet_data = pandas.read_excel(file_path, sheet_name="MATERIALS_USE")
    for index, row in sheet_data.iloc[1:].iterrows():
        phase = row['project_phase']
        material = row['material']
        quantity = row['quantity']
        ef = row['emission_factor']
        
        object = MaterialsUse(phase, material, quantity, ef)
        materials_use[material] = object.to_dict()

    sheet_data = pandas.read_excel(file_path, sheet_name="SOIL_USE_CHANGE")
    for index, row in sheet_data.iloc[1:].iterrows(): 
        change = row['change']
        area = row['area']
        previous_soiluse = row['prev_soil_use']
        new_soiluse = row['new_soil_use']
        prev_seqfactor = row['prev_seq_factor']
        new_seqfactor = row['new_seq_factor']
        
        object = SoilUseChange(change, area, previous_soiluse, prev_seqfactor, \
                    new_soiluse, new_seqfactor)
        soil_use_change[change] = object.to_dict()
        
    sheet_data = pandas.read_excel(file_path, sheet_name="WASTE_TREATMENT")
    for index, row in sheet_data.iloc[1:].iterrows():
        phase = row['project_phase']
        treatment = row['treatment']
        stream = row['stream']
        quantity = row['quantity']
        co2_emissions = row['co2_emissions']
        ch4_emissions = row['ch4_emissions']
        ch4_cf = row['ch4_corrfactor']
        n2o_emissions = row['n2o_emissions']
        n2o_cf = row['n2o_corrfactor']
        
        object = WasteTreatment(phase, treatment, stream, quantity, co2_emissions,\
                    ch4_emissions, ch4_cf, n2o_emissions, n2o_cf)
        waste_treatm[treatment] = object.to_dict()

      
def create_database():
    '''
    Creates a JSON file with the emission data.
    '''
    data = {
        "project_phases": project_phases,
        "energy": energy,
        "vehicles": vehicles,
        "fixed_combustion": fixed_combustion,
        "mobile_combustion": mobile_combustion,
        "materials_prod": materials_prod,
        "materials_use": materials_use,
        "soil_use_change": soil_use_change,
        "waste_treatm": waste_treatm
    }

    with open('ghg_database.json', 'w') as f:        
        json.dump(data, f, indent=4)

def get_base_path():
    if getattr(sys, 'frozen', False):  # If running as .exe
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))  # If running as .py

json_path = os.path.join(get_base_path(), 'ghg_database.json')
json_path = os.path.abspath(json_path)  # Normalize the full path

def init_calculations_services():
    global energy_calculations
    energy_calculations = EnergyCalculations(json_path)
    global vehicles_calculations
    vehicles_calculations = VehiclesCalculations(json_path)
    global fixed_combustion_calculations
    fixed_combustion_calculations = FixedCombustionCalculations(json_path)
    global mobile_combustion_calculations
    mobile_combustion_calculations = MobileCombustionCalculations(json_path)
    global materials_production_calculations
    materials_production_calculations = MaterialsProductionCalculations(json_path)
    global materials_use_calculations
    materials_use_calculations = MaterialsUseCalculations(json_path)
    global soil_use_change_calculations
    soil_use_change_calculations = SoilUseChangeCalculations(json_path)
    global waste_treatment_calculations
    waste_treatment_calculations = WasteTreatmentCalculations(json_path)
    

'''
2. Functions to sum all values from all categories
'''


def sum_all_num():
    '''
    Sums all categories emissions, resulting the total emissions of the project (numeric)
    '''
    energy = energy_calculations.total_emissions_energy()[0]
    vehicles = vehicles_calculations.total_emissions_vehicles_all()[0]
    fixed_machinery = fixed_combustion_calculations.total_emissions_fixedcomb()[0]
    mobile_machinery = mobile_combustion_calculations.total_emissions_mobilecomb()[0]
    materials_production = materials_production_calculations.total_emissions_materialsprod()[0]
    materials_use = materials_use_calculations.total_emissions_materialsuse()[0]
    soil = soil_use_change_calculations.total_emissions_soilusechange()[0]
    waste = waste_treatment_calculations.total_emissions_waste_all()[0]
    
    if soil > 0:
        total = energy + vehicles + fixed_machinery + mobile_machinery + materials_production + materials_use\
             + waste
    elif soil < 0:
        total = energy + vehicles + fixed_machinery + mobile_machinery + materials_production + materials_use\
             + soil + waste
    
    return total

def sum_all_list():
    '''
    Sums all categories emissions, resulting the total commulative value for each year in the project horizon (list)
    '''
    energy = energy_calculations.total_emissions_peryear_energy()
    vehicles = vehicles_calculations.total_emissions_peryear_vehicles_all()
    fixed_machinery = fixed_combustion_calculations.total_emissions_peryear_fixedcomb()
    mobile_machinery = mobile_combustion_calculations.total_emissions_peryear_mobilecomb()
    materials_production = materials_production_calculations.total_emissions_peryear_materialsprod()
    waste = waste_treatment_calculations.total_emissions_peryear_waste_all()
    
    total = [sum(values) for values in zip_longest(
            energy, vehicles, fixed_machinery, mobile_machinery, materials_production, waste, fillvalue=0)]
    
    return total

'''
3. Graphic displayes - elaborates all plots for output display
'''
 
def plot_total_peryear():
    years = list(range(1, len(sum_all_list()) + 1))
    emissions = sum_all_list()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('Total Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tonCO2eq)')
    ax.grid(True)
    
    return fig
    
def plot_energy_peryear():
    years = list(range(1, len(energy_calculations.total_emissions_peryear_energy()) + 1))
    emissions = energy_calculations.total_emissions_peryear_energy()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('Energy - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tonCO2eq)')
    ax.grid(True)
    
    return fig

def plot_vehicles_all_peryear():
    years = list(range(1, len(vehicles_calculations.total_emissions_peryear_vehicles_all()) + 1))
    emissions = vehicles_calculations.total_emissions_peryear_vehicles_all()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('All Vehicles - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tonCO2eq)')
    ax.grid(True)
    
    return fig
    
def plot_vehicles_road_peryear():
    years = list(range(1, len(vehicles_calculations.total_emissions_peryear_vehicles_type("ROAD")) + 1))
    emissions = vehicles_calculations.total_emissions_peryear_vehicles_type("ROAD")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('ROAD Vehicles - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tonCO2eq)')
    ax.grid(True)
    
    return fig
    
def plot_vehicles_train_peryear():
    years = list(range(1, len(vehicles_calculations.total_emissions_peryear_vehicles_type("TRAIN")) + 1))
    emissions = vehicles_calculations.total_emissions_peryear_vehicles_type("TRAIN")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('TRAIN Vehicles - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tonCO2eq)')
    ax.grid(True)
    
    return fig
    
def plot_vehicles_ship_peryear():
    years = list(range(1, len(vehicles_calculations.total_emissions_peryear_vehicles_type("SHIP")) + 1))
    emissions = vehicles_calculations.total_emissions_peryear_vehicles_type("SHIP")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('SHIP Vehicles - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tonCO2eq)')
    ax.grid(True)
    
    return fig
    
def plot_vehicles_air_peryear():
    years = list(range(1, len(vehicles_calculations.total_emissions_peryear_vehicles_type("AIR")) + 1))
    emissions = vehicles_calculations.total_emissions_peryear_vehicles_type("AIR")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('AIR Vehicles - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tonCO2eq)')
    ax.grid(True)
    
    return fig

def plot_fixedcomb_peryear():
    years = list(range(1, len(fixed_combustion_calculations.total_emissions_peryear_fixedcomb()) + 1))
    emissions = fixed_combustion_calculations.total_emissions_peryear_fixedcomb()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('Fixed Combustion - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tonCO2eq)')
    ax.grid(True)
    
    return fig

def plot_mobilecomb_peryear():
    years = list(range(1, len(mobile_combustion_calculations.total_emissions_peryear_mobilecomb()) + 1))
    emissions = mobile_combustion_calculations.total_emissions_peryear_mobilecomb()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('Mobile Combustion - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tonCO2eq)')
    ax.grid(True)
    
    return fig

def plot_materialsprod_peryear():
    years = list(range(1, len(materials_production_calculations.total_emissions_peryear_materialsprod()) + 1))
    emissions = materials_production_calculations.total_emissions_peryear_materialsprod()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('Materials Production - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tonCO2eq)')
    ax.grid(True)
    
    return fig
    
## materials used do not have a plot because it's measured in total quantities

## soil use change do not have a plot because it's measured in a form of total balance
    
def plot_waste_all_peryear():
    years = list(range(1, len(waste_treatment_calculations.total_emissions_peryear_waste_all()) + 1))
    emissions = waste_treatment_calculations.total_emissions_peryear_waste_all()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('All Waste Treatments - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tonCO2eq)')
    ax.grid(True)
    
    return fig
    
def plot_waste_solids_peryear():
    years = list(range(1, len(waste_treatment_calculations.total_emissions_peryear_waste_type("WATER")) + 1))
    emissions = waste_treatment_calculations.total_emissions_peryear_waste_type("WATER")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('WATER Treatment - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tonCO2eq)')
    ax.grid(True)
    
    return fig

def plot_waste_water_peryear():
    years = list(range(1, len(waste_treatment_calculations.total_emissions_peryear_waste_type("SOLID")) + 1))
    emissions = waste_treatment_calculations.total_emissions_peryear_waste_type("SOLID")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('SOLID Treatment - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tonCO2eq)')
    ax.grid(True)
    
    return fig

def plot_waste_gas_peryear():
    years = list(range(1, len(waste_treatment_calculations.total_emissions_peryear_waste_type("GAS")) + 1))
    emissions = waste_treatment_calculations.total_emissions_peryear_waste_type("GAS")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('GAS Treatment - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tonCO2eq)')
    ax.grid(True)
    
    return fig

'''
4. Numeric plots - Elaborates all numeric outputs for display
'''

def show_total():
    all = sum_all_num()
    
    show = (
        "Total GHG Emissions: \n"
        f"{all} tonCO2eq"
    )
    
    return show
    
def show_energy():
    all = energy_calculations.total_emissions_energy()[0]
    balance = energy_calculations.GHG_emissions_saved_energy()[0]
    
    show = (
        "ENERGY GHG Emissions \n"
        f"Energy Emissions: {all} tonCO2eq \n"
        f"Energy Emissions Balance: {balance} tonCO2eq \n"
    )
    
    return show

    
def show_vehicles():
    all = vehicles_calculations.total_emissions_vehicles_all()[0]
    road = vehicles_calculations.total_emissions_vehicles_type("ROAD")[0]
    train = vehicles_calculations.total_emissions_vehicles_type("AIR")[0]
    ship = vehicles_calculations.total_emissions_vehicles_type("TRAIN")[0]
    air = vehicles_calculations.total_emissions_vehicles_type("SHIP")[0]
    
    show = (
        "VEHICLES GHG Emissions \n"
        f"All Vehicles Emissions: {all} tonCO2eq \n"
        f"- Road Vehicles Emissions: {road} tonCO2eq \n"
        f"- Train Vehicles Emissions: {train} tonCO2eq \n"
        f"- Ship Vehicles Emissions: {ship} tonCO2eq \n"
        f"- Air Vehicles Emissions: {air} tonCO2eq \n"
    )
    
    return show

def show_combustionmachinery():
    all = fixed_combustion_calculations.total_emissions_fixedcomb()[0] + mobile_combustion_calculations.total_emissions_mobilecomb()[0]
    fixed = fixed_combustion_calculations.total_emissions_fixedcomb()[0]
    mobile = mobile_combustion_calculations.total_emissions_mobilecomb()[0]
    
    show = (
        "COMBUSTION MACHINERY GHG Emissions \n"
        f"All Combustion Machinery Emissions: {all} tonCO2eq \n"
        f"- Fixed Combustion Machinery Emissions: {fixed} tonCO2eq \n"
        f"- Mobile Combustion Machinery Emissions: {mobile} tonCO2eq \n"
    )
    
    return show

def show_materials():
    used = materials_use_calculations.total_emissions_materialsuse()[0]
    produced = materials_production_calculations.total_emissions_materialsprod()[0]
    
    show= (
        "MATERIALS GHG Emissions \n"
        f"- Emissions for Materials Used: {used} tonCO2eq \n"
        f"- Emissions for Materials Production: {produced} tonCO2eq \n"
    )

    return show

def show_soilusechange():
    all = soil_use_change_calculations.total_emissions_soilusechange()[0]
    
    show = (
        "SOIL USE CHANGE GHG Emissions \n"
        f"Soil Use Change Impact: {all} tonCO2eq \n"
    )
    
    return show

def show_wastetreatment():
    all = waste_treatment_calculations.total_emissions_waste_all()[0]
    water = waste_treatment_calculations.total_emissions_waste_type('WATER')[0]
    solid = waste_treatment_calculations.total_emissions_peryear_waste_type('SOLID')[0]
    gas = waste_treatment_calculations.total_emissions_waste_type('GAS')[0]
    
    show = (
        "All WASTE TREATMENT GHG Emissions \n"
        f"All Waste Treatment Emissions: {all} tonCO2eq \n"
        f"- Wastewater Treatment Emissions: {water} tonCO2eq \n"
        f"- Solid waste Treatment Emissions: {solid} tonCO2eq \n"
        f"- Gas stream Treatment Emissions: {gas} tonCO2eq \n"
    )
    
    return show