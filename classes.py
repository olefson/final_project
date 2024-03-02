import pygame
import pygwidgets
import random
from abc import ABC, abstractmethod

# ABSTRACT BASE CLASSES...........JUST ADD EM LATER NEED TO FOCUS ON INSTRUCTIONS



class ChargeStation:
    def __init__(self, capacity, cost_per_kwh):
        self.capacity = capacity  # Capacity in kW/day
        self.cost_per_kwh = cost_per_kwh  # Cost per kWh

    def calculate_cost(self, energy_used):
        # calculate cost based on energy used
        return energy_used * self.cost_per_kwh
    
    def has_enough_capacity(self, energy_needed):
        return self.capacity >= energy_needed
    
class Level2_Charge_Station(ChargeStation):
    def __init__(self):
        super().__init__(capacity=600, cost_per_kwh=0.11)  


class Level3_Charge_Station(ChargeStation):
    def __init__(self):
        super().__init__(capacity=1500, cost_per_kwh=0.11)  
        

class ElectricVehicle:
    def __init__(self, capacity, charge_rate, current_charge=0):
        self.capacity = capacity  # Capacity in kWh
        self.charge_rate = charge_rate  # Charge rate in kW
        self.current_charge = current_charge

    def charge(self, station):
        # Check if vehicle compatible with station
        if isinstance(self, Level2_EV) and isinstance(station, Level2_Charge_Station):
            #  calc energy needed
            energy_needed = min(self.charge_rate, station.capacity)
            #  charge vehicle and update remaining capacity of station
            if station.has_enough_capacity(energy_needed):
                self.current_charge += energy_needed
                if self.current_charge >= self.capacity:
                    print("Vehicle is fully charged")
                return True
        elif isinstance(self, Level3_EV) and isinstance(station, Level3_Charge_Station):
            energy_needed = min(self.charge_rate, station.capacity)
            if station.has_enough_capacity(energy_needed):
                self.current_charge += energy_needed
                if self.current_charge >= self.capacity:
                    print("Vehicle is fully charged")
                return True
        else:
            print("Vehicle and station are not compatible")
            return False

    
class Level2_EV(ElectricVehicle):
    def __init__(self, number):
        super().__init__(capacity=40, charge_rate=5, current_charge=0) 
    

            
            
class Level3_EV(ElectricVehicle):
    def __init__(self, number):
        super().__init__(capacity=80, charge_rate=70, current_charge=0)
        

class Community:
    def __init__(self, name):
        self.name = name
        self.stations = []
        self.vehicles = []
        self.revenue = 0
        self.cost = 0

    def add_station(self, station):
        self.stations.append(station)

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def random_zero_or_one(self):
            return random.randint(0, 1)

    def generate_random_vehicles(self):
        for i in range(random.randint(50, 500)):
            if self.random_zero_or_one() == 0:
                self.add_vehicle(Level2_EV(i))
            else:
                self.add_vehicle(Level3_EV(i))
            
    def calculate_cost(self):
        self.cost = 0 # Reset cost to 0
        for station in self.stations:
            if isinstance(station, Level2_Charge_Station):
                self.cost += 1700
            elif isinstance(station, Level3_Charge_Station):
                self.cost += 42000
        return(self.cost)
    
    def calculate_revenue(self):
        for station in self.stations:
            if isinstance(station, Level2_Charge_Station):
                capacity_sold = 600 - station.capacity
                self.revenue += capacity_sold * 0.11
            if isinstance(station, Level3_Charge_Station):
                capacity_sold = 1500 - station.capacity
                self.revenue += capacity_sold * 0.11
        return self.revenue

# Community List class
class CommunityList:
    def __init__(self):
        self.communities = []
        self.total_cost = 0
        self.total_revenue = 0
        
    def create_base_communities(self): # create 3 example communities with random cars
        self.add_community(Community("Community 1"))
        self.communities[0].generate_random_vehicles()
        self.add_community(Community("Community 2"))
        self.communities[1].generate_random_vehicles()
        self.add_community(Community("Community 3"))
        self.communities[2].generate_random_vehicles()
        
    def add_community(self, community):
        community.generate_random_vehicles()
        self.communities.append(community)
    
    def calculate_cost(self):
        self.total_cost = 0
        for community in self.communities:
            self.total_cost += community.calculate_cost()
        return self.total_cost
       
        
    def reset_cost(self):
        self.total_cost = 0
    
    def generate_stations(self): # Randomly generates stations for 3 example communities
        for i in range(0, 5):
            random_number = random.randint(1,3)
            if random_number == 1:
                self.communities[0].add_station(Level2_Charge_Station())
            if random_number == 2:
                self.communities[1].add_station(Level2_Charge_Station())
            if random_number == 3:
                self.communities[2].add_station(Level2_Charge_Station())
        for i in range(0, 7):
            random_number = random.randint(1,3)
            if random_number == 1:
                self.communities[0].add_station(Level3_Charge_Station())
            if random_number == 2:
                self.communities[1].add_station(Level3_Charge_Station())
            if random_number == 3:
                self.communities[2].add_station(Level3_Charge_Station())
    
    def charge_vehicles(self):
        for community in self.communities:
            for vehicle in community.vehicles:
                for station in community.stations:
                    if vehicle.current_charge < vehicle.capacity:
                        vehicle.charge(station)
        return True
    
    def calculate_total_revenue(self):
        for community in self.communities:
            self.total_revenue += community.calculate_revenue()
        return self.total_revenue
        
    
CommunityList = CommunityList()
CommunityList.create_base_communities()
CommunityList.generate_stations()
# print(CommunityList.charge_vehicles())
# print(CommunityList.calculate_total_revenue())
# print(CommunityList.charge_vehicles())
# print(CommunityList.calculate_total_revenue())
# print(CommunityList.charge_vehicles())
# print(CommunityList.calculate_total_revenue())
# print(CommunityList.charge_vehicles())
# print(CommunityList.calculate_total_revenue())
# print(testEV.current_charge)
print(CommunityList.calculate_cost())
print(CommunityList.calculate_cost())
print(CommunityList.calculate_cost())
# testEV.charge(testLevel_2_Station)

# print(testEV.current_charge)
# print(testLevel_2_Station.capacity)
