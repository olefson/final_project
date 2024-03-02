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
        # Calculate cost based on energy used
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
        self.fully_charged = False # Vehicle is not fully charged by default, keeps track to avoid inflated numbers

    def charge(self, station, community):
        # Check if vehicle compatible with station
        if self.fully_charged:
            return False
        if isinstance(self, Level2_EV) and isinstance(station, Level2_Charge_Station):
            energy_needed = min(self.charge_rate, station.capacity)  # Check if station has enough capacity
            if station.has_enough_capacity(energy_needed):
                self.current_charge += energy_needed
                if self.current_charge >= self.capacity:
                    community.add_fully_charged_vehicle()  # Update community's fully charged count
                    community.remove_vehicle(self)  # Remove vehicle from community
                    # print("Vehicle is fully charged")
                return True
        elif isinstance(self, Level3_EV) and isinstance(station, Level3_Charge_Station):
            energy_needed = min(self.charge_rate, station.capacity)  # Check if station has enough capacity
            if station.has_enough_capacity(energy_needed):
                self.current_charge += energy_needed
                if self.current_charge >= self.capacity:
                    community.add_fully_charged_vehicle()  # Update community's fully charged count
                    community.remove_vehicle(self)  # Remove vehicle from community
                    # print("Vehicle is fully charged")
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
        self.fully_charged_count = 0 # Keep track of fully charged vehicles
        self.initial_vehicle_count = 0 # Keep track of initial vehicle count
    
    def get_total_vehicles_not_charged(self):
        total_fully_charged = self.get_fully_charged_count()
        total_not_charged = self.initial_vehicle_count - total_fully_charged
        return total_not_charged
    
    def remove_vehicle(self, vehicle):
        if vehicle in self.vehicles:
            self.vehicles.remove(vehicle)
            
    def get_fully_charged_count(self):
        return self.fully_charged_count
    
    def calculate_charge_cost(self):
        charge_cost_per_kwh = 0.11
        total_cost = 0
        for vehicle in self.vehicles:
            energy_consumed =  vehicle.current_charge / vehicle.capacity
            vehicle_cost = energy_consumed * charge_cost_per_kwh
            total_cost += vehicle_cost
        return total_cost
        
    def add_fully_charged_vehicle(self):
        self.fully_charged_count += 1

    def add_station(self, station):
        self.stations.append(station)

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def random_zero_or_one(self):
            return random.randint(0, 1)

    def generate_random_vehicles(self):
        self.initial_vehicle_count = random.randint(50, 500) # Random number of vehicles
        for i in range(self.initial_vehicle_count):
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
        self.total_charge_cost = 0
        self.total_fully_charged_cars = 0
        
    def find_best_community(self): # Finds community with the least amount of fully charged cars
        best_community = None
        min_fully_charged_count = float('inf')
        
        for community in self.communities:
            fully_charged_count = community.get_fully_charged_count()
            if fully_charged_count < min_fully_charged_count:
                best_community = community
                min_fully_charged_count = fully_charged_count

        if best_community:
            return f"{best_community.name} would benefit from another charging station"
        else:
            return "No community found"
        
    def calculate_total_fully_charged_cars(self):
        self.total_fully_charged_cars = sum(community.get_fully_charged_count() for community in self.communities)
        return self.total_fully_charged_cars
    
    def create_base_communities(self): # Create 3 example communities with random cars
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
    
    def calculate_total_charge_cost(self):
        for community in self.communities:
            self.total_charge_cost += community.calculate_charge_cost()
        return self.total_charge_cost
        
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
                if isinstance(vehicle, Level2_EV):
                    for station in community.stations:
                        if isinstance(station, Level2_Charge_Station):
                            vehicle.charge(station, community)  # Pass community instance as argument
                        else:
                            continue
                if isinstance(vehicle, Level3_EV):
                    for station in community.stations:
                        if isinstance(station, Level3_Charge_Station):
                            vehicle.charge(station, community)  # Pass community instance as argument
                        else:
                            continue
        print("Vehicles charged")
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
