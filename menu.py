# -*- coding: cp1252 -*-
import pygame
#import random
import csv
import os.path
from os import path
import subprocess

from random import seed
from random import randint
seed(1)

import cfg
SCREEN = (480, 480)
MENUPOS = 0
OPTIONS = False
SCAN = False
MenuPos = {
        0: (33,360),  ## 0  2
        1: (33,400),  ## 1  3
        2: (255,360),
        3: (255,400)
    }
NAME = ""
CLASS = ""

class MainMenu():
    def __init__(self, screen,FONTSIZE):
        self.screen = screen
        self.font = pygame.font.Font("PKMNRBYGSC.ttf", FONTSIZE)
        self.data = DataRead()

    def dispMenu(self):
        font = self.font
        screen = self.screen
        data = self.data
        
        menuBG = pygame.image.load("pics/menu/mainMenu.png")
        menuBG = pygame.transform.scale(menuBG, SCREEN)
        screen.fill((248,232,248))
        screen.blit(menuBG, (0,0))

        NAME = data.getName()
        CLASS = data.getClass()

        TrainerSprite = pygame.image.load("pics/trainer/" + CLASS)
        TrainerSprite = pygame.transform.scale(TrainerSprite, (252,252))
        screen.blit(TrainerSprite, (114,50))
        
        #menu text
        if(OPTIONS == False and SCAN == False):
            dex = font.render("POKEDEX", True, (0, 0, 0))
            screen.blit(dex, (60,360))
            scan = font.render("SCAN", True, (0, 0, 0))
            screen.blit(scan, (60,400))

            dex = font.render(NAME, True, (0, 0, 0))
            screen.blit(dex, (282,360))
            scan = font.render("OPTIONS", True, (0, 0, 0))
            screen.blit(scan, (282,400))
        elif(OPTIONS):
            dex = font.render("WI-FI", True, (0, 0, 0))
            screen.blit(dex, (60,360))
            scan = font.render("VOLUME", True, (0, 0, 0))
            screen.blit(scan, (60,400))

            dex = font.render("UPDATE", True, (0, 0, 0))
            screen.blit(dex, (282,360))
            scan = font.render("ABOUT", True, (0, 0, 0))
            screen.blit(scan, (285,400))
        elif(SCAN):
            scnMes = font.render("Coming soon! ...Hopefully", True, (0, 0, 0))
            screen.blit(scnMes, (45,230))
            

        ball = pygame.image.load("pics/menu/pokeballIcon.png")
        ball = pygame.transform.scale(ball, (25,25))
        screen.blit(ball, MenuPos.get(MENUPOS, None))

        
    def inputHandler(self, action):
        global MENUPOS
        global OPTIONS
        if(action == "A"):      
            if(OPTIONS == False and SCAN == false):
                if(MENUPOS == 0):
                    print("changing mode: Dex")
                    cfg.CURRENT_MODE = 1
                if(MENUPOS == 1):
                    print("changing mode: Scan")
                    #cfg.CURRENT_MODE = 2
                    SCAN = True
                if(MENUPOS == 3):
                    OPTIONS = True
                    MENUPOS = 0
            elif(OPTIONS):
                if(MENUPOS == 0):
                    subprocess.call('sudo wifi-connect', shell=True)
                if(MENUPOS == 2):
                    subprocess.call('git pull origin main', shell=True)
                if(MENUPOS == 1):
                    #print "changing mode"
                    cfg.CURRENT_MODE = 3
                if(MENUPOS == 3):
                    soundFile = 'sound/dexterEntries/Dexter.wav'
                    pygame.mixer.music.load(soundFile)
                    pygame.mixer.music.set_volume(cfg.VOLUME)
                    pygame.mixer.music.play()
            elif(SCAN):
                SCAN = False
                    
        if(action == "B" and OPTIONS == True):
            OPTIONS = False
            MENUPOS = 0
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

class Intro():
    def __init__(self):
        global NAME
        global CLASS

    def runIntro(self):
        global NAME

    def getData(self):
        with open('csv/intro.csv') as csvfile:
            self.introScript = csv.DictReader(csvfile)
            for row in self.introScript:
                self.script = row

class SoundMenu():
    def __init__(self, screen,FONTSIZE):
        self.screen = screen
        self.font = pygame.font.Font("PKMNRBYGSC.ttf", FONTSIZE)
        self.data = DataRead()

    def dispMenu(self):
        font = self.font
        screen = self.screen
        data = self.data
        
        menuBG = pygame.image.load("pics/menu/mainMenu.png")
        menuBG = pygame.transform.scale(menuBG, SCREEN)
        screen.fill((248,232,248))
        screen.blit(menuBG, (0,0))

        # Background Rect
        color1 = (74,74,74)
        pygame.draw.rect(screen, color1, pygame.Rect(45, 120, 385, 60))
  
        # Sound Rectangle
        if(cfg.VOLUME != 0):
            color2 = (0,0,0) 
            pygame.draw.rect(screen, color2, pygame.Rect(45, 120, 385 * cfg.VOLUME, 60))

        arrows = font.render("LEFT -VOLUME- RIGHT", True, (0, 0, 0))
        screen.blit(arrows, (45,230))

        aButton = font.render("A - TEST VOLUME", True, (0, 0, 0))
        screen.blit(aButton, (45,360))
        bButton = font.render("B - RETURN TO MENU", True, (0, 0, 0))
        screen.blit(bButton, (45,400))

    def inputHandler(self, action):
        global MENUPOS
        global OPTIONS
        if(action == "A"):
            rando = randint(1, 150)
            soundFile = 'sound/criesRBY/'+str(format(rando, '03'))+'.wav'
            pygame.mixer.music.load(soundFile)
            pygame.mixer.music.set_volume(cfg.VOLUME)
            pygame.mixer.music.play()
                    
        if(action == "B"):
            cfg.CURRENT_MODE = 0
            
        if(action == "LEFT" and cfg.VOLUME > 0.0):
            cfg.VOLUME -= 0.2
        if(action == "RIGHT" and cfg.VOLUME < 1.0):
            cfg.VOLUME += 0.2
        

class DataRead():
    def __init__(self):
        global NAME
        global CLASS
        
        with open('csv/dexHolder.csv') as csvfile:
            self.ownData = csv.DictReader(csvfile)
            for row in self.ownData:
                self.holder = row

    def getName(self):
        return self.holder['name']
    def getClass(self):
        return str(self.holder['class']) + ".png"
            


            
