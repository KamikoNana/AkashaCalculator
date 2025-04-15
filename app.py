import pandas
import matplotlib.pyplot as plt

from Entity.Combustion.fixed_comb_entity import FixedCombustion
from Entity.Combustion.mobile_comb_entity import MobileCombustion
from Entity.Energy.energy_entity import Energy
from Entity.Materials.materials_production_entity import MaterialsProduction
from Entity.Materials.materials_use_entity import MaterialsUse
from Entity.ProjectPhases.project_phases_entity import ProjectPhases
from Entity.SoilUseChange.soil_use_change_entity import SoilUseChange
from Entity.Vehicles.vehicles_entity import Vehicles
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

file_path = "database.xlsx"
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
        source = row['name']
        quantity = row['quantity']
        ef = row['emission_factor']
        
        object = Energy(phase, type, source, quantity, ef)
        energy[source] = object.to_dict()
        
    sheet_data = pandas.read_excel(file_path, sheet_name="VEHICLES")
    for index, row in sheet_data.iloc[1:].iterrows():
        phase = row['project_phase']
        type = row['type']
        name = row['name']
        km = row['distance']
        n = row['n_vehicles']
        co2_emissions = row['co2_emissions']
        ch4_emissions = row['ch4_emissions']
        ch4_cf = row['ch4_corrfactor']
        n2o_emissions = row['n2o_emissions']
        n2o_cf = row['n2o_corrfactor']
        
        object = Vehicles(phase, type, name, km, n, co2_emissions, \
            ch4_emissions, ch4_cf, n2o_emissions, n2o_cf)
        vehicles[name] = object.to_dict()
        
    sheet_data = pandas.read_excel(file_path, sheet_name="FIXED_COMBUSTION")
    for index, row in sheet_data.iloc[1:].iterrows():
        phase = row['project_phase']
        enginery_fueltype = row['name']
        quantity = row['quantity']
        n = row['n_machines']
        ef = row['emission_factor']
        
        object = FixedCombustion(phase, enginery_fueltype, quantity, n, ef)
        fixed_combustion[enginery_fueltype] = object.to_dict()
    
    sheet_data = pandas.read_excel(file_path, sheet_name="MOBILE_COMBUSTION")
    for index, row in sheet_data.iloc[1:].iterrows():
        phase = row['project_phase']
        enginery_fueltype = row['name']
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
        material = row['name']
        quantity = row['quantity']
        ef = row['emission_factor']
        
        object = MaterialsUse(phase, material, quantity, ef)
        materials_use[material] = object.to_dict()

    sheet_data = pandas.read_excel(file_path, sheet_name="SOIL_USE_CHANGE")
    for index, row in sheet_data.iloc[1:].iterrows(): 
        change = row['name']
        area = row['area']
        previous_soiluse = row['prev_soil_use']
        new_soiluse = row['new_soil_use']
        prev_seqfactor = row['prev_seq_factor']
        new_seqfactor = row['new_seq_factor']
        
        object = SoilUseChange(change, area, previous_soiluse, prev_seqfactor, \
                    new_soiluse, new_seqfactor)
        soil_use_change[name] = object.to_dict()
        
    sheet_data = pandas.read_excel(file_path, sheet_name="WASTE_TREATMENT")
    for index, row in sheet_data.iloc[1:].iterrows():
        phase = row['project_phase']
        treatment = row['name']
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
 #bellow about the plots and prepare data to be displayed
 
def plot_energy_peryear():
    years = list(range(1, len(EnergyCalculations.total_emissions_peryear_energy()) + 1))

    plt.figure(figsize=(10, 6))
    plt.plot(years, EnergyCalculations.total_emissions_peryear_energy(), marker='o', linestyle='-', color='g')

    plt.title('Energy - Cumulative Emissions Over Time')
    plt.xlabel('Year')
    plt.ylabel('Cumulative Emissions (tons of CO2e)')
    plt.grid(True)
    plt.show()

def plot_fixedcomb_peryear():
    years = list(range(1, len(FixedCombustionCalculations.total_emissions_peryear_fixedcomb()) + 1))

    plt.figure(figsize=(10, 6))
    plt.plot(years, FixedCombustionCalculations.total_emissions_peryear_fixedcomb(), marker='o', linestyle='-', color='g')

    plt.title('Fixed Combustion - Cumulative Emissions Over Time')
    plt.xlabel('Year')
    plt.ylabel('Cumulative Emissions (tons of CO2e)')
    plt.grid(True)
    plt.show()

def plot_mobilecomb_peryear():
    years = list(range(1, len(MobileCombustionCalculations.total_emissions_peryear_mobilecomb()) + 1))

    plt.figure(figsize=(10, 6))
    plt.plot(years, MobileCombustionCalculations.total_emissions_peryear_mobilecomb(), marker='o', linestyle='-', color='g')

    plt.title('Mobile Combustion - Cumulative Emissions Over Time')
    plt.xlabel('Year')
    plt.ylabel('Cumulative Emissions (tons of CO2e)')
    plt.grid(True)
    plt.show()

def plot_materialsprod_peryear():
    years = list(range(1, len(MaterialsProductionCalculations.total_emissions_peryear_materialsprod()) + 1))

    plt.figure(figsize=(10, 6))
    plt.plot(years, MaterialsProductionCalculations.total_emissions_peryear_materialsprod(), marker='o', linestyle='-', color='g')

    plt.title('Materials Production - Cumulative Emissions Over Time')
    plt.xlabel('Year')
    plt.ylabel('Cumulative Emissions (tons of CO2e)')
    plt.grid(True)
    plt.show()
    
## materials used do not have a plot because its measured in total quantities and not by time

## soil use change do not have a plot because its measured in a form of balance

def plot_vehicles_all_peryear():
    years = list(range(1, len(VehiclesCalculations.total_emissions_peryear_vehicles_all()) + 1))

    plt.figure(figsize=(10, 6))
    plt.plot(years, VehiclesCalculations.total_emissions_peryear_vehicles_all(), marker='o', linestyle='-', color='g')

    plt.title('All Vehicles - Cumulative Emissions Over Time')
    plt.xlabel('Year')
    plt.ylabel('Cumulative Emissions (tons of CO2e)')
    plt.grid(True)
    plt.show()
    
def plot_vehicles_road_peryear():
    years = list(range(1, len(VehiclesCalculations.total_emissions_peryear_vehicles_type("ROAD")) + 1))

    plt.figure(figsize=(10, 6))
    plt.plot(years, VehiclesCalculations.total_emissions_peryear_vehicles_type("ROAD"), marker='o', linestyle='-', color='g')

    plt.title('ROAD Vehicles - Cumulative Emissions Over Time')
    plt.xlabel('Year')
    plt.ylabel('Cumulative Emissions (tons of CO2e)')
    plt.grid(True)
    plt.show()
    
def plot_vehicles_train_peryear():
    years = list(range(1, len(VehiclesCalculations.total_emissions_peryear_vehicles_type("TRAIN")) + 1))

    plt.figure(figsize=(10, 6))
    plt.plot(years, VehiclesCalculations.total_emissions_peryear_vehicles_type("TRAIN"), marker='o', linestyle='-', color='g')

    plt.title('TRAIN Vehicles - Cumulative Emissions Over Time')
    plt.xlabel('Year')
    plt.ylabel('Cumulative Emissions (tons of CO2e)')
    plt.grid(True)
    plt.show()
    
def plot_vehicles_ship_peryear():
    years = list(range(1, len(VehiclesCalculations.total_emissions_peryear_vehicles_type("SHIP")) + 1))

    plt.figure(figsize=(10, 6))
    plt.plot(years, VehiclesCalculations.total_emissions_peryear_vehicles_type("SHIP"), marker='o', linestyle='-', color='g')

    plt.title('SHIP Vehicles - Cumulative Emissions Over Time')
    plt.xlabel('Year')
    plt.ylabel('Cumulative Emissions (tons of CO2e)')
    plt.grid(True)
    plt.show()
    
def plot_vehicles_air_peryear():
    years = list(range(1, len(VehiclesCalculations.total_emissions_peryear_vehicles_type("AIR")) + 1))

    plt.figure(figsize=(10, 6))
    plt.plot(years, VehiclesCalculations.total_emissions_peryear_vehicles_type("AIR"), marker='o', linestyle='-', color='g')

    plt.title('AIR Vehicles - Cumulative Emissions Over Time')
    plt.xlabel('Year')
    plt.ylabel('Cumulative Emissions (tons of CO2e)')
    plt.grid(True)
    plt.show()
    
def plot_waste_all_peryear():
    years = list(range(1, len(WasteTreatmentCalculations.total_emissions_peryear_waste_all()) + 1))

    plt.figure(figsize=(10, 6))
    plt.plot(years, WasteTreatmentCalculations.total_emissions_peryear_waste_all(), marker='o', linestyle='-', color='g')

    plt.title('All Waste Treatments - Cumulative Emissions Over Time')
    plt.xlabel('Year')
    plt.ylabel('Cumulative Emissions (tons of CO2e)')
    plt.grid(True)
    plt.show()
    
def plot_waste_solids_peryear():
    years = list(range(1, len(WasteTreatmentCalculations.total_emissions_peryear_waste_type("WATER")) + 1))

    plt.figure(figsize=(10, 6))
    plt.plot(years, WasteTreatmentCalculations.total_emissions_peryear_waste_type("WATER"), marker='o', linestyle='-', color='g')

    plt.title('WATER Treatment - Cumulative Emissions Over Time')
    plt.xlabel('Year')
    plt.ylabel('Cumulative Emissions (tons of CO2e)')
    plt.grid(True)
    plt.show()

def plot_waste_water_peryear():
    years = list(range(1, len(WasteTreatmentCalculations.total_emissions_peryear_waste_type("SOLID")) + 1))

    plt.figure(figsize=(10, 6))
    plt.plot(years, WasteTreatmentCalculations.total_emissions_peryear_waste_type("SOLID"), marker='o', linestyle='-', color='g')

    plt.title('SOLIDS Treatment - Cumulative Emissions Over Time')
    plt.xlabel('Year')
    plt.ylabel('Cumulative Emissions (tons of CO2e)')
    plt.grid(True)
    plt.show()

def plot_waste_gas_peryear():
    years = list(range(1, len(WasteTreatmentCalculations.total_emissions_peryear_waste_type("GAS")) + 1))

    plt.figure(figsize=(10, 6))
    plt.plot(years, WasteTreatmentCalculations.total_emissions_peryear_waste_type("GAS"), marker='o', linestyle='-', color='g')

    plt.title('GAS stream Treatment - Cumulative Emissions Over Time')
    plt.xlabel('Year')
    plt.ylabel('Cumulative Emissions (tons of CO2e)')
    plt.grid(True)
    plt.show()

#above are defined the plots
##
#bellow is presented the number data

def sum_all():
    energy = EnergyCalculations.total_emissions_energy()[0]
    vehicles = VehiclesCalculations.total_emissions_vehicles_all()[0]
    
    total = energy + vehicles
    
    return total

def show_total():
    print('Total Emissions (units)')
    print(sum_all())
    
def show_energy():
    print('Emissions Source: ENERGY')
    print('Energy Emissions (units)')
    print(EnergyCalculations.total_emissions_energy()[0])
    print('Energy Emissions Balance')
    print(EnergyCalculations.GHG_emissions_saved_energy()[0])
    
def show_vehicles():
    print('Emissions Source: VEHICLES')
    print('All Vehicles Emissions (unites)')
    print(VehiclesCalculations.total_emissions_vehicles_all()[0])
    print('Road Vehicles (units)')
    print(VehiclesCalculations.total_emissions_vehicles_type("ROAD")[0])
    print('Aircraft Vehicles (units)')
    print(VehiclesCalculations.total_emissions_vehicles_type("AIR")[0])
    print('Railway Vehicles (units)')
    print(VehiclesCalculations.total_emissions_vehicles_type("TRAIN")[0])
    print('Shipment Vehicles (units)')
    print(VehiclesCalculations.total_emissions_vehicles_type("SHIP")[0])

def show_combustionmachinery():
    print("Emissions Source: COMBUSTION MACHINERY")
    print("- Fixed Combustion Machinery")
    print(FixedCombustionCalculations.total_emissions_fixedcomb)
    print("- Mobile Combustion Machinery")
    print(MobileCombustionCalculations.total_emissions_mobilecomb)

def show_materials():
    print('Emissions Source: MATERIALS')
    print('Matrials Used (Units)')
    print(MaterialsUseCalculations.total_emissions_materialsuse()[0])
    print('Materials Produced (Units)')
    print(MaterialsProductionCalculations.total_emissions_materialsprod()[0])

def show_soilusechange():
    print('Emissions Source: SOIL USE CHANGE')
    print('Soil Use Change Impact (Units)')
    print(SoilUseChangeCalculations.total_emissions_soilusechange()[0])

def show_wastetreatment():
    print('Emissions Source: WASTE TREATMENT')
    print('All waste treatment (Units)')
    print(WasteTreatmentCalculations.total_emissions_waste_all()[0])
    print('Solid waste treatment (Units)')
    print(WasteTreatmentCalculations.total_emissions_peryear_waste_type('SOLID')[0])
    print('Wastewater treatment (Units)')
    print(WasteTreatmentCalculations.total_emissions_waste_type('WATER')[0])
    print('Gas stream treatment (Units)')
    print(WasteTreatmentCalculations.total_emissions_waste_type('GAS')[0])