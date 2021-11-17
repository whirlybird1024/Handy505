# -*- coding: cp1252 -*-
import pygame
import random
import csv
import os.path
from os import path
import subprocess
from sprite_strip_anim import SpriteStripAnim

from random import seed
from random import randint
seed(1)

import numpy as np

import cfg
import spritesheet

SCREEN = (480, 480)

#  0
#3   1
#  2

ORIENT = 2
LOCATE = (150, 150)
MAINSCREEN = True

MON = "eevee"
NUM = 133
CELLX = 30 #Sprite sheet cell X size
CELLY = 32 #Sprite sheet cell Y size
SPRX = 0 #Sprite sheet Column
SPRY = 2 #Sprite sheet Row

ZONEX = 23
ZONEY = 23

LOCATION = [10,10]

MAP = 0

ITER = 0
COUNT = 0

MOVING = False

IMGMODE = False

class zoneScreen():
    def __init__(self, screen,FONTSIZE):
        self.screen = screen
        self.font = pygame.font.Font("PKMNRBYGSC.ttf", FONTSIZE)
        self.data = DataRead()
        self.behave = MonBehavior()

    def timer(self):
        global ITER
        global COUNT

        COUNT += 1
        if(COUNT >= 100):
            COUNT = 0
            ITER += 1
            self.timerEvents()
            #print("Current Iter: " + str(ITER))
            if(ITER >= 10):
                ITER = 0

        #self.timerEvents()

    def timerEvents(self):
        behave = self.behave
        screen = self.screen
        #print("Moving:" + str(MOVING))
        if MOVING:
            behave.moving()
            self.dispZone()
            screen.blit(pygame.transform.rotate(screen, 90),(0,0))

    def dispZone(self):
        font = self.font
        screen = self.screen
        data = self.data
        behave = self.behave
        
        zoneBG = pygame.image.load("pics/zone/pokezone.png")
        zoneBG = pygame.transform.scale(zoneBG, SCREEN)
        screen.fill((248,232,248))
        screen.blit(zoneBG, (0,0))

        NAME = data.getName()
        CLASS = data.getClass()

        PokeSheet = spritesheet.spritesheet("pics/zone/" + MON + ".png")
        PokeSprite = PokeSheet.image_at((SPRX * CELLX, SPRY * CELLY, CELLX, CELLY),colorkey=(255, 255, 255))
        PokeSprite = pygame.transform.scale(PokeSprite, (ZONEX*2,ZONEY*2))
        screen.blit(PokeSprite, (LOCATION[0]*ZONEX,LOCATION[1]*ZONEY))

        if(IMGMODE == True):
            imgScreen = pygame.image.load("pics/zone/" + MON + "Face.png")
            imgScreen = pygame.transform.scale(imgScreen, (154,154))
            screen.blit(imgScreen, (160,160))
            print("face")

            
            if(pygame.mouse.get_pressed() == (1, 0, 0)):
                print("pet")
                imgScreen = pygame.image.load("pics/zone/" + MON + "Pet.png")
                imgScreen = pygame.transform.scale(imgScreen, (154,154))
                screen.blit(imgScreen, (160,160))
                soundFile = 'sound/criesRBY/'+str(NUM)+".wav"
                screen.blit(pygame.transform.rotate(screen, 90),(0,0))
                if(path.exists(soundFile)):
                    pygame.mixer.music.load(soundFile)
                    pygame.mixer.music.set_volume(cfg.VOLUME)
                    pygame.mixer.music.play()


        #if(MOVING):
        
        #PokeSprite = pygame.image.load("pics/zone/" + MON + ".png")
        #PokeSprite = pygame.transform.scale(PokeSprite, (24,24))
        #screen.blit(PokeSprite, (114,50))
        #screen.blit(pygame.transform.rotate(screen, 90),(0,0))

        
    def inputHandler(self, action):
        global MENUPOS
        global OPTIONS
        global SCAN
        global IMGMODE
        behave = self.behave
        if(action == "A" and IMGMODE == False):      
            IMGMODE = True
                    
        if(action == "B" and IMGMODE == False):
            cfg.CURRENT_MODE = 0
        elif(action == "B" and IMGMODE == True):
            IMGMODE = False
        if(action == "UP"):
            behave.movement(0)
        if(action == "DOWN"):
            behave.movement(2)
        if(action == "LEFT"):
            behave.movement(3)
        if(action == "RIGHT"):
            behave.movement(1)


class MonBehavior():
    def __init__(self):
        global NAME
        global CLASS

    def movement(self,d):
        global ORIENT
        global MOVING
        global SPRX
        global SPRY

        checkMap = self.checkMap 
        
        #direct = random.randint(0,3)
        direct = d

        print("randirection: " + str(direct))

        if(direct == 0):
            SPRX = 0
            SPRY = 0
            if(checkMap(LOCATION[0],LOCATION[1]-1) == 0):
                ORIENT =  direct
                MOVING = True
            else: print("dangerZone")
        elif(direct == 1):
            SPRX = 1
            SPRY = 2
            if(checkMap(LOCATION[0]+1,LOCATION[1]) == 0):
                ORIENT =  direct
                MOVING = True
            else: print("dangerZone")
        elif(direct == 2):
            SPRX = 0
            SPRY = 2
            if(checkMap(LOCATION[0],LOCATION[1]+1) == 0):
                ORIENT =  direct
                MOVING = True
            else: print("dangerZone")
        elif(direct == 3):
            SPRX = 1
            SPRY = 0
            if(checkMap(LOCATION[0]-1,LOCATION[1]) == 0):
                ORIENT =  direct
                MOVING = True
            else: print("dangerZone")
        
        #ORIENT =  direct
        #MOVING = True
        
        #roll rng for direction, check on chart, if ok then move
        #moving()

    def moving(self):
        global LOCATION
        global MOVING
        
        if(ORIENT == 0):
            
            LOCATION[1] = LOCATION[1] - 0.1
            #LOCATION[1] = LOCATION[1] - (1/(COUNT/1000))
            LOCATION[1] = "%.1f" % LOCATION[1]
            LOCATION[1] = float(LOCATION[1])
            if(LOCATION[1] == int(LOCATION[1])):
                MOVING = False
            #LOCATION[1] = LOCATION[1] - (1/(COUNT/1000))
        if(ORIENT == 2):
            LOCATION[1] += .1
            LOCATION[1] = "%.1f" % LOCATION[1]
            LOCATION[1] = float(LOCATION[1])
            
            if(LOCATION[1].is_integer()):
                MOVING = False

        if(ORIENT == 1):
            LOCATION[0] += .1
            LOCATION[0] = "%.1f" % LOCATION[0]
            LOCATION[0] = float(LOCATION[0])
            
            if(LOCATION[0].is_integer()):
                MOVING = False

        if(ORIENT == 3):
            LOCATION[0] -= .1
            LOCATION[0] = "%.1f" % LOCATION[0]
            LOCATION[0] = float(LOCATION[0])
            
            if(LOCATION[0].is_integer()):
                MOVING = False

    def checkMap(self,x,y):
        global LOCATION
        global MAP

        intX = int(y)
        intY = int(x)
        
        print("X: " + str(intX))
        print("Y: " + str(intY))

        print(MAP[intX][intY])
        return MAP[intX][intY]

class DataRead():
    def __init__(self):
        global NAME
        global CLASS

        global MAP
        
        with open('csv/dexHolder.csv') as csvfile:
            self.ownData = csv.DictReader(csvfile)
            for row in self.ownData:
                self.holder = row

        mapData = open('csv/maps/eeveeZone.csv')
        MAP = np.loadtxt(mapData, delimiter=",")
        print(MAP)

    def getName(self):
        return self.holder['name']
    def getClass(self):
        return str(self.holder['class']) + ".png"
            


            
