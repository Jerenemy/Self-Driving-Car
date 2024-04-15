import pygame as pg 
pg.init()
from sys import exit
import math
import random

#******************************************************* 3 AREAS OF FOCUS *******************************************************
#1 Flow Control
"""
Using main while loop. Use while and for loops within methods
"""
#2 Packages
"""
Importing pygame and using pygame built-in functions to display screen and objects, draw shapes, detect key-presses
"""
#3 Object-Oriented
"""
Define multiple classes, use methods, inheritence
"""

#******************************************************* CONSTANTS *******************************************************

#SCREEN
WIDTH, HEIGHT = 1200, 800
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))      

#COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
PURPLE = ( 211, 3, 252)
YELLOW = (255, 241, 0)

RECT_W = 100 #width of obstacle-hit-detecting rects

#rects to display in corner whenever vehicle hits obstacle and coords appended to list of coords to avoid
car_rect = (0, 0, RECT_W, RECT_W)
car_rect1 = (WIDTH - RECT_W, 0, RECT_W, RECT_W)
car_rect2 = (WIDTH - RECT_W, HEIGHT - RECT_W, RECT_W, RECT_W)
car_rect3 = (0, HEIGHT - RECT_W, RECT_W, RECT_W)

#******************************************************* CLASSES *******************************************************

class Display:
    def __init__(self):
        self.obst = 0
        self.obst_coords = 0
        self.color = BLACK
        self.caption = "Car" 
        
    def window_display(self): 
        """
        sig: NoneType --> NoneType
        method to display window using pg
        """
        #display window using pg
        SCREEN.fill(self.color)
        pg.display.set_caption(self.caption)

class Vehicle:
    def __init__(self, x_coord, y_coord, color): 
        self.x_coord = x_coord
        self.y_coord = y_coord
        
        self.size = 50
        
        self.color = color
        self.speed = 10
        self.width = 5
        
        self.last_randomnum = 0
        
    def disp(self):
        """
        sig: NoneType --> NoneType
        displays vehicle as geometric shapes: a rect and two circles to suggest a car
        """
        #define coordinates for car
        top_right = (self.x_coord - self.size/2, self.y_coord)
        bottom_left = (self.size, self.size/2)
        center_wheel1 = self.x_coord - self.size/4, self.y_coord + self.size/2
        center_wheel2 = self.x_coord + self.size/4, self.y_coord + self.size/2
        radius_wheel = 10
        pg.draw.rect(SCREEN, self.color, (top_right, bottom_left), self.width)
        pg.draw.circle(SCREEN, self.color, center_wheel1, radius_wheel, self.width)
        pg.draw.circle(SCREEN, self.color, center_wheel2, radius_wheel, self.width)

    def generate_random_move(self, detected_obstacle):
        """
        sig: bool --> dict{str:bool}
        pass hit_obstacles method
        generates and returns a dict of random direction for vehicle to move in (either up, down, left, or right, each associated with a bool in a dict). If vehicle attempts to move through a point where an obstacle was detected, vehicle will move in the opposite direction instead as to not hit the obstacle.
        """
        move_frequency = 5 #must be > 5 to move in all directions, increase value to make vehicle move less frequently
        if detected_obstacle == False:
            #random number picked if no obstacle to avoid
            randomnum = random.randrange(1, move_frequency, 1)
            self.last_randomnum = randomnum
        else:
            #if obstacle detected, random number changed to cause spaceship to move in opposite direction and avoid obstacle
            if self.last_randomnum != 0: #account for first move
                if self.last_randomnum == 1 or self.last_randomnum == 3: #LEFT changed to RIGHT, UP changed to DOWN
                    randomnum = self.last_randomnum + 1
                else: #RIGHT changed to LEFT, DOWN changed to UP
                    randomnum = self.last_randomnum - 1
            else: #if first move, then just pick another random move
                randomnum = random.randrange(1, move_frequency, 1)
          
        randomdir = {"LEFT":False, "RIGHT":False, "UP":False, "DOWN":False} #dict to associate move direction with bool
        
        #direction vehicle moves based on randomnum, bool in dict associated with direction changed to True
        if randomnum == 1:
            randomdir["LEFT"] = True
        if randomnum == 2:
            randomdir["RIGHT"] = True
        if randomnum == 3:
            randomdir["UP"] = True
        if randomnum == 4:
            randomdir["DOWN"] = True
        
        #TO DO: make probability lower when hitting ostacles
        
        return randomdir #return dict
    
    def move_with_dict(self, random_move):
        """
        sig: dict{str:bool} --> none
        passes generate_random_move method
        iterates through dict of moves until finds a value of True, then changes the x/y coords of the vehicle accordingly
        """
        
        i = 0
        #create list of dicts, changing key to = the coordinate change value 
        move_list = [{-self.speed:random_move["LEFT"], self.speed:random_move["RIGHT"]}, {-self.speed:random_move["UP"], self.speed:random_move["DOWN"]}]
        #while loop to iterate through list (need i to know to change x or y coord)
        while i < len(move_list):   
            #for loop inside while loop: if value is True, add key to x/y coord
            for key in move_list[i]:
                if move_list[i][key] == True:
                    if i == 0:
                        self.x_coord += key
                    elif i == 1:
                        self.y_coord += key
            i += 1    
        
    def check_distance(self, obstacle_list):   
        """
        sig: list[Obstacle] --> bool
        checks distance between vehicle and each obstacle in list, returns True if vehicle hits obstacle
        """
        for obstacle in obstacle_list:   
            d = math.sqrt(((obstacle.x_coord - self.x_coord) ** 2) + ((obstacle.y_coord - self.y_coord) ** 2) )
            if d < obstacle.size + self.size:
                return True
            #TO DO: sort obstacle list
        return False

    def relocate_off_screen(self):
        """
        sig: NoneType --> NoneType
        relocates vehicle to opposite side of screen if it goes off the screen
        """
        if self.x_coord < 0:
            self.x_coord += WIDTH
        if self.x_coord > WIDTH:
            self.x_coord -= WIDTH
        if self.y_coord < 0:
            self.y_coord += HEIGHT
        if self.y_coord > HEIGHT:
            self.y_coord -= HEIGHT
    
    def hit_obstacles(self, detected_obstacle_coords_list):
        """
        sig: list[list[int]] --> bool
        pass detected_obstacle_coords list, same list as passed in initiate_vehicle function
        returns True if vehicle coords equals set of coords in detected_obstacle_coords list, otherwise returns False
        """
        for coords in detected_obstacle_coords_list:
            if self.x_coord - self.speed <= coords[0] <= self.x_coord + self.speed and self.y_coord - self.speed <= coords[1] <= self.y_coord + self.speed:
                return True
            #figure out a way to get the car to move in the opposite direction of the obstacle when it hits, now it just moves in the opposite direction that the random generator suggests
        return False
    #when it hits the obstacle, the NEXT MOVE SHOULD BE THE OPPOSITE MOVE THAT JUST OCCURRED
    
    def force_relocate(self):
        """
        sig: NoneType --> NoneType
        moves all vehicles to mouse cursor when clicked
        """
        if True in pg.mouse.get_pressed():
            #pg.mouse.get_pos()
            self.x_coord = pg.mouse.get_pos()[0]
            self.y_coord = pg.mouse.get_pos()[1]
        
class Obstacle:
    def __init__(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.size = 10
        self.width = 5
        self.color = RED
        self.i = 0
        self.obst_amount = 5
    
    def disp(self):
        """
        sig: NoneType --> NoneType
        displays obstacle as a circle
        """
        #improve to taste
        pg.draw.circle(SCREEN, self.color, (self.x_coord, self.y_coord), self.size, self.width)
    
    def generate_random(self):
        """
        sig: NoneType --> NoneType
        changes set attributes of obstacles to be randomly generated within given ranges
        """
        
        #random_num = random.randrange(1, 5, 1)
        random_size = random.randrange(20,100,20)
        self.color = BLACK
        self.x_coord = random.randrange(1, WIDTH, 1)
        self.y_coord = random.randrange(1, HEIGHT, 1)
        self.size = random_size
        #can change this to just generate from one thing every time, unless want more specific parameters, such as different colors/shapes. Currently is redundant to have 4 options that generate with the same random parameters
        """if random_num == 1: 
            self.color = BLUE
            self.x_coord = random.randrange(1, WIDTH, 1)
            self.y_coord = random.randrange(1, HEIGHT, 1)
            self.size = random_size
        if random_num == 2: 
            self.color = BLUE
            self.x_coord = random.randrange(1, WIDTH, 1)
            self.y_coord = random.randrange(1, HEIGHT, 1)
            self.size = random_size
        if random_num == 3: 
            self.color = BLUE
            self.x_coord = random.randrange(1, WIDTH, 1)
            self.y_coord = random.randrange(1, HEIGHT, 1)
            self.size = random_size
        if random_num == 4: 
            self.color = BLUE
            self.x_coord = random.randrange(1, WIDTH, 1)
            self.y_coord = random.randrange(1, HEIGHT, 1)
            self.size = random_size
        """
            
class ObstacleList(list):
    
    def display_obstacles(self, obstacle):
        """
        sig: Obstacle --> NoneType
        displays each obstacle in ObstacleList object list
        """
        for obstacle in self:
            obstacle.disp()

class Point:
    def __init__(self, coords, color):
        self.coords = coords
        self.color = color
    def disp(self):
        pg.draw.circle(SCREEN, self.color, coords, 3, 0)
    def generate(self):
        self.coords = self.coords
        self.color = self.color

class PointList(list):
    def display_points(self):
        for point in self:
            point.disp()
        

def initiate_vehicle(vehicle, rect_color, rect_dimensions, detected_obstacle_coords_list):
    """
    sig: Vehicle, tuple(int), tuple(int), list[list[int]] --> NoneType
    the first tuple must be the RGB values of a color having len(2) with each int 0<=int<=255, the second tuple must be dimensions of a rect with len(3) and the first two ints the coords of the top left corner of the rect and the second two the length and width of the rect
    initiates the vehicles with given attributes of rect that displays when vehicle hits an obstacle, and a list of coords of detected obstacles for the vehicle to avoid (all vehicles may use the same list of obstacle coords)
    """
    vehicle.disp()
    vehicle.move_with_dict(vehicle.generate_random_move(vehicle.hit_obstacles(detected_obstacle_coords_list)))
    vehicle.relocate_off_screen()
    vehicle.force_relocate()
    
    if vehicle.check_distance(obst_collection) == True:
        pg.draw.rect(SCREEN, rect_color, rect_dimensions)
        detected_obstacle_coords_list.append([vehicle.x_coord, vehicle.y_coord])
        
#******************************************************* VARIABLES *******************************************************

obst_i = 0 #index in loop that displays obstacles
obst_amount = 20 #amount of obstacles displayed (actually a constant, but assiciated with variable obst_i)

detected_obstacle_coords = [] #list of detected obstacle coords to avoid

run = True #main bool

#******************************************************* OBJECTS *******************************************************

car = Vehicle(100, 100, RED)
car1 = Vehicle(100, HEIGHT - 100, YELLOW)
car2 = Vehicle(WIDTH - 100, HEIGHT - 100, GREEN)
car3 = Vehicle(WIDTH - 100, 100, PURPLE)
dsp = Display()
obst_collection = ObstacleList()
pt_collection = PointList()
#******************************************************* MAIN LOOP *******************************************************

while run: #main while loop
    kp = pg.key.get_pressed() #define variable for to get key_pressed bools
    clock = pg.time.Clock() #define variable for clock
    FPS = 60 #define frames per second that the game will run at (capped at speed code can run)
    clock.tick(FPS) #initiate game speed
    
    #quit game
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
          
    dsp.window_display() #display the game window
    
    
    
    #generate the amount of random obstacles determined by obst_amoumnt variable
    while obst_i < obst_amount:
        obst = Obstacle(100, 50)
        obst.generate_random()
        obst_collection.append(obst)
        obst_i += 1
    obst_collection.display_obstacles(obst)

    for coords in detected_obstacle_coords:
        pt = Point(coords, BLUE)
        pt.disp()
        pt_collection.append(pt)
    pt_collection.display_points()
        
    
    #initiate vehicles with corresponding obstacle-hit-detecting rects
    initiate_vehicle(car, RED, car_rect, detected_obstacle_coords)
    initiate_vehicle(car1, YELLOW, car_rect1, detected_obstacle_coords)
    initiate_vehicle(car2, GREEN, car_rect2, detected_obstacle_coords)
    initiate_vehicle(car3, PURPLE, car_rect3, detected_obstacle_coords)          
       
    pg.display.update() #update the display each frame
    
    if kp[pg.K_b]:
        breakpoint() #breakpoint in game when press B
        
pg.quit()