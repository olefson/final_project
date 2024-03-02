import pygame
import pygwidgets
from classes import *
from abc import ABC, abstractclassmethod

# Create Display Window
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
timer = pygame.time.Clock() # Timer for FPS
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 1000) # 1 second timer
font = pygame.font.Font(None, 36)

# Game States
main_menu = "main"
results_menu = "results"
station_management_menu = "station_management"
menu_state = "main"

# Classes
# Abstract Button Class
class Button(ABC):
    def __init__(self, window, loc, **kwargs):
        self.window = window
        self.loc = loc
        self.kwargs = kwargs
        self.is_hovered = False
        self.is_clicked = False
    
    # ABSTRACT METHODS
    @abstractmethod
    def draw(self):
        pass
    
    @abstractmethod
    def handleEvent(self, event):
        pass

# TextButton Subclas, POLYMORPHISM
class TextButton(Button):
    def __init__(self, window, loc, text, **kwargs):
        super().__init__(window, loc, **kwargs)
        self.text = text
        self.width = kwargs.get('width', None)
        self.height = kwargs.get('height', 40)
        self.textColor = kwargs.get('textColor', (0, 0, 0))
        self.upColor = kwargs.get('upColor', (170, 170, 170))
        self.overColor = kwargs.get('overColor', (210, 210, 210))
        self.downColor = kwargs.get('downColor', (140, 140, 140))
        self.fontName = kwargs.get('fontName', None)
        self.fontSize = kwargs.get('fontSize', 20)
        self.soundOnClick = kwargs.get('soundOnClick', None)
        self.enterToActivate = kwargs.get('enterToActivate', False)
        self.callBack = kwargs.get('callBack', None)
        self.nickname = kwargs.get('nickname', None)
        self.activationKeysList = kwargs.get('activationKeysList', None)
        self.rect = pygame.Rect(loc[0], loc[1], self.width, self.height)
    
    def is_over(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def is_down(self):
        return pygame.mouse.get_pressed()[0] and self.is_over()
    
    
    def draw(self):
        if self.is_down():
            color = self.upColor
        elif self.is_over():
            color = self.overColor
        else:
            color = self.upColor
            
        pygame.draw.rect(self.window, color, self.rect)
        # Draw text on button
        text_surface = font.render(self.text, True, self.textColor)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.window.blit(text_surface, text_rect)
    
    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_clicked = False
            if self.rect.collidepoint(event.pos):
                # Execute the callback function if it exists
                if self.kwargs.get('callBack'):
                    self.kwargs['callBack']()
# Helper Fucncitons

# Trackers
hours = 0 # Keeps track of Seconds-to-Hours in timer
daily_profit = "" # Keeps track of daily profit
weekly_profit = "0" # Keeps track of weekly profit
total_cars_charged_daily = "" # Keeps track of total cars charged daily
total_cars_charged_weekly = "" # Keeps track of total cars charged weekly
cars_not_charged_community_1 = "" # Keeps track of cars not charged in community 1
cars_not_charged_community_2 = "" # Keeps track of cars not charged in community 2
cars_not_charged_community_3 = "" # Keeps track of cars not charged in community 3
Suggested_Community = "" # Keeps track of suggested community

# Text
holder = ""

# Result page text (to update)
cost = pygwidgets.DisplayText(window, (100, 50), "Cost:" + holder + "$")
Total_EV_Charged_Daily = pygwidgets.DisplayText(window, (100, 100), "Total EVs Charged Daily: " + total_cars_charged_daily)
Total_EV_Charged_Weekly = pygwidgets.DisplayText(window, (100, 150), "Total EVs Charged Weekly: " + total_cars_charged_weekly)
Total_Vehicles_Not_Charged_Comunity_1 = pygwidgets.DisplayText(window, (100, 200), "Total Vehicles Not Charged Community 1: " + cars_not_charged_community_1)
Total_Vehicles_Not_Charged_Comunity_2 = pygwidgets.DisplayText(window, (100, 250), "Total Vehicles Not Charged Community 2: " + cars_not_charged_community_2)
Total_Vehicles_Not_Charged_Comunity_3 = pygwidgets.DisplayText(window, (100, 300), "Total Vehicles Not Charged Community 3: " + cars_not_charged_community_3)
Total_Cost_EV_Day = pygwidgets.DisplayText(window, (100, 350), "Total Cost of EVs Charged Daily: " + daily_profit)
Suggested_Communities = pygwidgets.DisplayText(window, (100, 400), "Suggested Community: " + Suggested_Community)
# Input Text

# Buttons
exit_button = TextButton(window, (290, 450), "Exit", width=200, height=50, callBack=pygame.quit) #use of abstract button class
add_station_button = pygwidgets.TextButton(window, (290, 300), "Add Station", width=200, height=50, fontSize=36)
back_button = pygwidgets.TextButton(window, (290, 450), "Back", width=200, height=50, fontSize=36)
submit_station_button= pygwidgets.TextButton(window, (290, 300), "Submit Station", width=200, height=50, fontSize=36)

# radio buttons
community_1_button = pygwidgets.TextRadioButton(window, (100, 100), group="communities", text="Community 1", value=False)
community_2_button = pygwidgets.TextRadioButton(window, (100, 150), group="communities", text="Community 2", value=False)
community_3_button = pygwidgets.TextRadioButton(window, (100, 200), group="communities", text="Community 3", value=False)
Level2_Charge_Station_Button = pygwidgets.TextRadioButton(window, (300, 125), group="stations", text="Level 2 Station", value=False)
Level3_Charge_Station_Button = pygwidgets.TextRadioButton(window, (300, 175), group="stations", text="Level 3 Station", value=False)
# Elements


# Game Loop
run = True

while run:
    window.fill((255, 255, 255))
    timer.tick(60)  # Control the frame rate
    

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == TIMER_EVENT:
            hours += 1
            CommunityList.charge_vehicles()
            print(hours)
        
        # Days
        if hours == 5:
            daily_profit = str(CommunityList.calculate_total_charge_cost())
            total_cars_charged_daily = str(CommunityList.calculate_total_fully_charged_cars())
            
        # Weeks
        if hours == 10:
            weekly_profit = str(CommunityList.calculate_total_charge_cost())
            total_cars_charged_weekly = str(CommunityList.calculate_total_fully_charged_cars())
            cars_not_charged_community_1 = str(CommunityList.communities[0].get_total_vehicles_not_charged())
            cars_not_charged_community_2 = str(CommunityList.communities[1].get_total_vehicles_not_charged())
            cars_not_charged_community_3 = str(CommunityList.communities[2].get_total_vehicles_not_charged())
            Suggested_Community = CommunityList.find_best_community()
            holder = str(CommunityList.calculate_cost())
            CommunityList.reset_cost()
            cost.setValue("Cost of stations: " + "$" + holder)
            
            # Update info
            Total_Cost_EV_Day.setValue("Total Cost of EVs Charged Daily: " + daily_profit)
            Total_EV_Charged_Daily.setValue("Total EVs Charged Daily: " + total_cars_charged_daily)
            Total_EV_Charged_Weekly.setValue("Total EVs Charged Weekly: " + total_cars_charged_weekly)
            Total_Vehicles_Not_Charged_Comunity_1.setValue("Total Vehicles Not Charged Community 1: " + cars_not_charged_community_1)
            Total_Vehicles_Not_Charged_Comunity_2.setValue("Total Vehicles Not Charged Community 2: " + cars_not_charged_community_2)
            Total_Vehicles_Not_Charged_Comunity_3.setValue("Total Vehicles Not Charged Community 3: " + cars_not_charged_community_3)
            Suggested_Communities.setValue("Suggested Community: " + Suggested_Community)
            # Automatically navigate to results menu
            menu_state = results_menu
            
            
        # Handle events for the main menu
        elif menu_state == main_menu:
            if exit_button.handleEvent(event):
                run = False
            elif add_station_button.handleEvent(event):
                menu_state = station_management_menu
        # Handle events for the station management menu
        elif menu_state == station_management_menu:
            if back_button.handleEvent(event):
                menu_state = main_menu
            if community_1_button.handleEvent(event):
                print("Community 1 selected")
            if community_2_button.handleEvent(event):
                print("Community 2 selected")
            if community_3_button.handleEvent(event):
                print("Community 3 selected")
            if Level2_Charge_Station_Button.handleEvent(event):
                print("Level 2 Station selected")
            if Level3_Charge_Station_Button.handleEvent(event):
                print("Level 3 Station selected")
            if submit_station_button.handleEvent(event):
                if community_1_button.getValue():
                    if Level2_Charge_Station_Button.getValue():
                        CommunityList.communities[0].add_station(Level2_Charge_Station())
                        print("Lvl 2 station submitted for community 1")
                    elif Level3_Charge_Station_Button.getValue():
                        CommunityList.communities[0].add_station(Level3_Charge_Station())
                        print("Lvl 3 station submitted for community 1")
                elif community_2_button.getValue():
                    if Level2_Charge_Station_Button.getValue():
                        CommunityList.communities[1].add_station(Level2_Charge_Station())
                        print("Lvl 2 station submitted for community 2")
                    elif Level3_Charge_Station_Button.getValue():
                        CommunityList.communities[1].add_station(Level3_Charge_Station())
                        print("Lvl 3 station submitted for community 2")
                elif community_3_button.getValue():
                    if Level2_Charge_Station_Button.getValue():
                        CommunityList.communities[2].add_station(Level2_Charge_Station())
                        print("Lvl 2 station submitted for community 3")
                    elif Level3_Charge_Station_Button.getValue():
                        CommunityList.communities[2].add_station(Level3_Charge_Station())
                        print("Lvl 3 station submitted for community 3")
                else:
                    print("Invalid Selection")
                menu_state = main_menu
        # Handle events for the results menu
        elif menu_state == results_menu:
            if back_button.handleEvent(event):
                menu_state = main_menu

    # Draw the current menu state
    if menu_state == main_menu:
        # Draw elements for the main menu
        add_station_button.draw()
        exit_button.draw()
    elif menu_state == station_management_menu:
        # Draw elements for the station management menu
        back_button.draw()
        community_1_button.draw()
        community_2_button.draw()
        community_3_button.draw()
        Level2_Charge_Station_Button.draw()
        Level3_Charge_Station_Button.draw()
        submit_station_button.draw()
    elif menu_state == results_menu:
        # Draw elements for the results menu
        back_button.draw()
        cost.draw()
        Total_EV_Charged_Daily.draw()
        Total_EV_Charged_Weekly.draw()
        Total_Vehicles_Not_Charged_Comunity_1.draw()
        Total_Vehicles_Not_Charged_Comunity_2.draw()
        Total_Vehicles_Not_Charged_Comunity_3.draw()
        Total_Cost_EV_Day.draw()
        Suggested_Communities.draw()

    pygame.display.update()