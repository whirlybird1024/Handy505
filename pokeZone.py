# -*- coding: cp1252 -*-
import pygame
#import random
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

MOVING = False

IMGMODE = False

class zoneScreen():
    def __init__(self, screen,FONTSIZE):
        self.screen = screen
        self.font = pygame.font.Font("PKMNRBYGSC.ttf", FONTSIZE)
        self.data = DataRead()
        self.behave = MonBehavior()

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

            soundFile = 'sound/criesRBY/'+str(NUM)+".wav"
            if(path.exists(soundFile)):
                pygame.mixer.music.load(soundFile)
                pygame.mixer.music.set_volume(cfg.VOLUME)
                pygame.mixer.music.play()
            if(pygame.mouse.get_pressed() == (1, 0, 0)):
                print("pet")
                imgScreen = pygame.image.load("pics/zone/" + MON + "Pet.png")
                imgScreen = pygame.transform.scale(imgScreen, (154,154))
                screen.blit(imgScreen, (160,160))


        #if(MOVING):
        
        #PokeSprite = pygame.image.load("pics/zone/" + MON + ".png")
        #PokeSprite = pygame.transform.scale(PokeSprite, (24,24))
        #screen.blit(PokeSprite, (114,50))

        
    def inputHandler(self, action):
        global MENUPOS
        global OPTIONS
        global SCAN
        global IMGMODE
        if(action == "A" and IMGMODE == False):      
            IMGMODE = True
                    
        if(action == "B" and IMGMODE == False):
            cfg.CURRENT_MODE = 0
        elif(action == "B" and IMGMODE == True):
            IMGMODE = False
        if(action == "UP"):
            if(MENUPOS == 1): MENUPOS = 0
            if(MENUPOS == 3): MENUPOS = 2
        if(action == "DOWN"):
            if(MENUPOS == 0): MENUPOS = 1
            if(MENUPOS == 2): MENUPOS = 3
        if(action == "LEFT"):
            if(MENUPOS == 2): MENUPOS = 0
            if(MENUPOS == 3): MENUPOS = 1
        if(action == "RIGHT"):
            if(MENUPOS == 0): MENUPOS = 2
            if(MENUPOS == 1): MENUPOS = 3


class MonBehavior():
    def __init__(self):
        global NAME
        global CLASS

    def movement(self):
        global ORIENT
        global MOVING
        
        direct = random.randint(0,3)
        if(direct == 0):
            ORIENT =  direct
            MOVING = True
        #roll rng for direction, check on chart, if ok then move

    def moving(self):
        global LOCATION
        
        if(ORIENT == 0):
            LOCATION[1]-=.1
            if(LOCATION[1].is_integer()):
                MOVING = False

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
            


            
