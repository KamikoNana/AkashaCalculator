## This file contains GHG data imported from the excel file

## Please ensure the data provided in the excel file is correct

project_phases = {'CONSTRUCTION': {'phase': 'CONSTRUCTION', 'years': 15}, 'OPERATION': {'phase': 'OPERATION', 'years': 50}}

energy = {'network': {'phase': 'CONSTRUCTION', 'type': 'CONSUMED', 'source': 'network', 'quantity': 150, 'ef': 10}, 'hydropower': {'phase': 'OPERATION', 'type': 'PRODUCED', 'source': 'hydropower', 'quantity': 50, 'ef': 3}}

vehicles = {'truck_diesel': {'phase': 'CONSTRUCTION', 'type': 'ROAD', 'vehicle_fuel': 'truck_diesel', 'distance': 500, 'n_vehicles': 9, 'co2_emissions': 16, 'ch4_emissions': 13, 'ch4_cf': 5, 'n2o_emissions': 8, 'n2o_cf': 25}, 'aircraft_diesel': {'phase': 'OPERATION', 'type': 'AIR', 'vehicle_fuel': 'aircraft_diesel', 'distance': 400, 'n_vehicles': 8, 'co2_emissions': 10, 'ch4_emissions': 9, 'ch4_cf': 5, 'n2o_emissions': 5, 'n2o_cf': 25}}

fixed_combustion = {'building_heater': {'phase': 'OPERATION', 'enginery_fueltype': 'building_heater', 'quantity': 500, 'n_machines': 6, 'ef': 16}}

mobile_combustion = {'motoserra': {'phase': 'CONSTRUCTION', 'enginery_fueltype': 'motoserra', 'quantity': 50, 'n_machines': 4, 'co2_emissions': 16, 'ch4_emissions': 13, 'ch4_cf': 5, 'n2o_emissions': 8, 'n2o_cf': 25}}

materials_prod = {'acids': {'phase': 'OPERATION', 'material': 'acids', 'process': 'idk', 'quantity': 500, 'ef': 24}}

materials_use = {'cement': {'phase': 'CONSTRUCTION', 'material': 'cement', 'quantity': 100000, 'ef': 29}}

soil_use = {'olive_camp': {'change': 'olive_camp', 'area': 28, 'previous soil use': 'olives', 'previous sequestration factor': 40, 'new soil use': 'short_grass', 'new sequestration factor': 10}}

waste_treatm = {'station_water_treatment': {'phase': 'OPERATION', 'treatment': 'station_water_treatment', 'stream': 'WATER', 'quantity': 600, 'co2_emissions': 16, 'ch4_emissions': 13, 'ch4_cf': 5, 'n2o_emissions': 8, 'n2o_cf': 25}}

