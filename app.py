import pandas
import matplotlib.pyplot as plt
from itertools import zip_longest

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

project_phases = {}
energy = {}
vehicles = {}
fixed_combustion = {}
mobile_combustion = {}
materials_prod = {}
materials_use = {}
soil_use_change = {}
waste_treatm = {}

file_path = "database_akasha.xlsx"
xls = pandas.ExcelFile(file_path)

def create_objects(xls):
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
    data = {
        "project_phases": project_phases,
        "energy": energy,
        "vehicles": vehicles,
        "fixed_combustion": fixed_combustion,
        "mobile_combustion": mobile_combustion,
        "materials_prod": materials_prod,
        "materials_use": materials_use,
        "soil_use": soil_use_change,
        "waste_treatm": waste_treatm
    }

    with open('ghg_database.py', 'w') as f:
        f.write("## This file contains GHG data imported from the excel file\n\n")
        f.write("## Please ensure the data provided in the excel file is correct\n\n")
        
        for dict_name, dict_data in data.items():
            f.write(f"{dict_name} = {dict_data}\n\n")


create_objects(xls) 
create_database()

 #up is all about the database transition
 ##

#function to sum all emissions
def sum_all_num():
    energy = EnergyCalculations.total_emissions_energy()[0]
    vehicles = VehiclesCalculations.total_emissions_vehicles_all()[0]
    fixed_machinery = FixedCombustionCalculations.total_emissions_fixedcomb()[0]
    mobile_machinery = MobileCombustionCalculations.total_emissions_mobilecomb()[0]
    materials_production = MaterialsProductionCalculations.total_emissions_materialsprod()[0]
    materials_use = MaterialsUseCalculations.total_emissions_materialsuse()[0]
    soil = SoilUseChangeCalculations.total_emissions_soilusechange()[0]
    waste = WasteTreatmentCalculations.total_emissions_waste_all()[0]
    
    total = energy + vehicles + fixed_machinery + mobile_machinery + materials_production + materials_use\
        + soil + waste
    
    return total

def sum_all_list():
    energy = EnergyCalculations.total_emissions_peryear_energy()
    vehicles = VehiclesCalculations.total_emissions_peryear_vehicles_all()
    fixed_machinery = FixedCombustionCalculations.total_emissions_peryear_fixedcomb()
    mobile_machinery = MobileCombustionCalculations.total_emissions_peryear_mobilecomb()
    materials_production = MaterialsProductionCalculations.total_emissions_peryear_materialsprod()
    waste = WasteTreatmentCalculations.total_emissions_peryear_waste_all()
    
    total = [sum(values) for values in zip_longest(
            energy, vehicles, fixed_machinery, mobile_machinery, materials_production, waste, fillvalue=0)]
    
    return total

#bellow about the plots and prepare data to be displayed   
 
def plot_total_peryear():
    years = list(range(1, len(sum_all_list()) + 1))
    emissions = sum_all_list()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('Total Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tons of CO2e)')
    ax.grid(True)
    
    return fig
    
def plot_energy_peryear():
    years = list(range(1, len(EnergyCalculations.total_emissions_peryear_energy()) + 1))
    emissions = EnergyCalculations.total_emissions_peryear_energy()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('Energy - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tons of CO2e)')
    ax.grid(True)
    
    return fig

def plot_fixedcomb_peryear():
    years = list(range(1, len(FixedCombustionCalculations.total_emissions_peryear_fixedcomb()) + 1))
    emissions = FixedCombustionCalculations.total_emissions_peryear_fixedcomb()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('Fixed Combustion - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tons of CO2e)')
    ax.grid(True)
    
    return fig

def plot_mobilecomb_peryear():
    years = list(range(1, len(MobileCombustionCalculations.total_emissions_peryear_mobilecomb()) + 1))
    emissions = MobileCombustionCalculations.total_emissions_peryear_mobilecomb()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('Mobile Combustion - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tons of CO2e)')
    ax.grid(True)
    
    return fig

def plot_materialsprod_peryear():
    years = list(range(1, len(MaterialsProductionCalculations.total_emissions_peryear_materialsprod()) + 1))
    emissions = MaterialsProductionCalculations.total_emissions_peryear_materialsprod()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('Materials Production - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tons of CO2e)')
    ax.grid(True)
    
    return fig
    
## materials used do not have a plot because its measured in total quantities and not by time

## soil use change do not have a plot because its measured in a form of balance

def plot_vehicles_all_peryear():
    years = list(range(1, len(VehiclesCalculations.total_emissions_peryear_vehicles_all()) + 1))
    emissions = VehiclesCalculations.total_emissions_peryear_vehicles_all()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('All Vehicles - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tons of CO2e)')
    ax.grid(True)
    
    return fig
    
def plot_vehicles_road_peryear():
    years = list(range(1, len(VehiclesCalculations.total_emissions_peryear_vehicles_type("ROAD")) + 1))
    emissions = VehiclesCalculations.total_emissions_peryear_vehicles_type("ROAD")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('ROAD Vehicles - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tons of CO2e)')
    ax.grid(True)
    
    return fig
    
def plot_vehicles_train_peryear():
    years = list(range(1, len(VehiclesCalculations.total_emissions_peryear_vehicles_type("TRAIN")) + 1))
    emissions = VehiclesCalculations.total_emissions_peryear_vehicles_type("TRAIN")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('TRAIN Vehicles - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tons of CO2e)')
    ax.grid(True)
    
    return fig
    
def plot_vehicles_ship_peryear():
    years = list(range(1, len(VehiclesCalculations.total_emissions_peryear_vehicles_type("SHIP")) + 1))
    emissions = VehiclesCalculations.total_emissions_peryear_vehicles_type("SHIP")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('SHIP Vehicles - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tons of CO2e)')
    ax.grid(True)
    
    return fig
    
def plot_vehicles_air_peryear():
    years = list(range(1, len(VehiclesCalculations.total_emissions_peryear_vehicles_type("AIR")) + 1))
    emissions = VehiclesCalculations.total_emissions_peryear_vehicles_type("AIR")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('AIR Vehicles - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tons of CO2e)')
    ax.grid(True)
    
    return fig
    
def plot_waste_all_peryear():
    years = list(range(1, len(WasteTreatmentCalculations.total_emissions_peryear_waste_all()) + 1))
    emissions = WasteTreatmentCalculations.total_emissions_peryear_waste_all()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('All Waste Treatments - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tons of CO2e)')
    ax.grid(True)
    
    return fig
    
def plot_waste_solids_peryear():
    years = list(range(1, len(WasteTreatmentCalculations.total_emissions_peryear_waste_type("WATER")) + 1))
    emissions = WasteTreatmentCalculations.total_emissions_peryear_waste_type("WATER")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('WATER Treatment - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tons of CO2e)')
    ax.grid(True)
    
    return fig

def plot_waste_water_peryear():
    years = list(range(1, len(WasteTreatmentCalculations.total_emissions_peryear_waste_type("SOLID")) + 1))
    emissions = WasteTreatmentCalculations.total_emissions_peryear_waste_type("SOLID")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('SOLID Treatment - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tons of CO2e)')
    ax.grid(True)
    
    return fig

def plot_waste_gas_peryear():
    years = list(range(1, len(WasteTreatmentCalculations.total_emissions_peryear_waste_type("GAS")) + 1))
    emissions = WasteTreatmentCalculations.total_emissions_peryear_waste_type("GAS")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, emissions, marker='o', linestyle='-', color='g')

    ax.set_title('GAS Treatment - Cumulative Emissions Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Emissions (tons of CO2e)')
    ax.grid(True)
    
    return fig

#above are defined the plots
##
#bellow is presented the number data

def show_total():
    all = sum_all_num()
    
    show = (
        "Total GHG Emissions: \n"
        f"{all} CO2eq"
    )
    
    return show
    
def show_energy():
    all = EnergyCalculations.total_emissions_energy()[0]
    balance = EnergyCalculations.GHG_emissions_saved_energy()[0]
    
    show = (
        "ENERGY GHG Emissions \n"
        f"Energy Emissions: {all} CO2eq \n"
        f"Energy Emissions Balance: {balance} CO2eq \n"
    )
    
    return show

    
def show_vehicles():
    all = VehiclesCalculations.total_emissions_vehicles_all()[0]
    road = VehiclesCalculations.total_emissions_vehicles_type("ROAD")[0]
    train = VehiclesCalculations.total_emissions_vehicles_type("AIR")[0]
    ship = VehiclesCalculations.total_emissions_vehicles_type("TRAIN")[0]
    air = VehiclesCalculations.total_emissions_vehicles_type("SHIP")[0]
    
    show = (
        "VEHICLES GHG Emissions \n"
        f"All Vehicles Emissions: {all} CO2eq \n"
        f"- Road Vehicles Emissions: {road} CO2eq \n"
        f"- Train Vehicles Emissions: {train} CO2eq \n"
        f"- Ship Vehicles Emissions: {ship} CO2eq \n"
        f"- Air Vehicles Emissions: {air} CO2eq \n"
    )
    
    return show

def show_combustionmachinery():
    all = FixedCombustionCalculations.total_emissions_fixedcomb()[0] + MobileCombustionCalculations.total_emissions_mobilecomb()[0]
    fixed = FixedCombustionCalculations.total_emissions_fixedcomb()[0]
    mobile = MobileCombustionCalculations.total_emissions_mobilecomb()[0]
    
    show = (
        "COMBUSTION MACHINERY GHG Emissions \n"
        f"All Combustion Machinery Emissions: {all} CO2eq \n"
        f"- Fixed Combustion Machinery Emissions: {fixed} CO2eq \n"
        f"- Mobile Combustion Machinery Emissions: {mobile} CO2eq \n"
    )
    
    return show

def show_materials():
    used = MaterialsUseCalculations.total_emissions_materialsuse()[0]
    produced = MaterialsProductionCalculations.total_emissions_materialsprod()[0]
    
    show= (
        "MATERIALS GHG Emissions \n"
        f"- Emissions for Materials Used: {used} CO2eq \n"
        f"- Emissions for Materials Production: {produced} CO2eq \n"
    )

    return show

def show_soilusechange():
    all = SoilUseChangeCalculations.total_emissions_soilusechange()[0]
    
    show = (
        "SOIL USE CHANGE GHG Emissions \n"
        f"Soil Use Change Impact: {all} CO2eq \n"
        "NOTE: If this value is negative, it represents that the soil use change was beneficial and the CO2 capture is higher than before the project implementation \n"
    )
    
    return show

def show_wastetreatment():
    all = WasteTreatmentCalculations.total_emissions_waste_all()[0]
    water = WasteTreatmentCalculations.total_emissions_waste_type('WATER')[0]
    solid = WasteTreatmentCalculations.total_emissions_peryear_waste_type('SOLID')[0]
    gas = WasteTreatmentCalculations.total_emissions_waste_type('GAS')[0]
    
    show = (
        "All WASTE TREATMENT GHG Emissions \n"
        f"All Waste Treatment Emissions: {all} CO2eq \n"
        f"- Wastewater Treatment Emissions: {water} CO2eq \n"
        f"- Solid waste Treatment Emissions: {solid} CO2eq \n"
        f"- Gas stream Treatment Emissions: {gas} CO2eq \n"
    )
    
    return show