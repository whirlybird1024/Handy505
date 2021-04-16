import pygame
#import random
import csv
import os.path
from os import path
import subprocess

import cfg

PAGE = 0
NAME = ""
CLASS = ""
LENGTH = 0
PG = True

class playIntro():
    def __init__(self, screen,FONTSIZE):
        self.screen = screen
        self.font = pygame.font.Font("PKMNRBYGSC.ttf", FONTSIZE)
        self.data = DataRead()

        global NAME
        NAME = self.data.getName()
        global CLASS
        CLASS = self.data.getClass()

        
        
    def play(self):
        self.screen.fill((248,232,248))
        self.showSprite()
        self.showText()

            

    def inputHandler(self, action):
        global PAGE
        global PG
        if(action == "A"):
            newPage = PAGE - 3
            #print("newPage: " + str(newPage))
            #print("Length: " + str(LENGTH))
            #print("Page: " + str(PAGE))
            if(LENGTH-1 != PAGE):
                if(PG == True):
                    PG = False
                else:
                    PAGE += 1
                    PG = True
            else:
                if(PG == True):
                    PG = False
                else:
                    cfg.CURRENT_MODE = 0

    def showSprite(self):
        screen = self.screen
        dat = self.data

        menuBG = pygame.image.load("pics/menu/mainMenu.png")
        menuBG = pygame.transform.scale(menuBG, (480, 480))
        screen.fill((248,232,248))
        screen.blit(menuBG, (0,0))
        
        img = dat.getIntroImage(PAGE)
        TrainerSprite = pygame.image.load("pics/trainer/" + img)
        TrainerSprite = pygame.transform.scale(TrainerSprite, (252,252))
        screen.blit(TrainerSprite, (114,50))
    def showText(self):
        screen = self.screen
        dat = self.data
        global PG
        page = PG
        
        script = dat.getIntroScript(PAGE)
        script = script.replace("NAME", NAME)
        print script
        script = script.splitlines()
        print script
        i = 0
        while (i<2):
            print(i)
            print(script[i])
            if(page):
                if(i < len(script)):
                    scriptText = self.font.render(script[i], True, (0, 0, 0))
                    screen.blit(scriptText, (40,350 + (i*50)))
            else:
                if(i+2 < len(script)):
                    scriptText = self.font.render(script[i+2], True, (0, 0, 0))
                    screen.blit(scriptText, (40,350 + (i*50)))
            if(i<2):
                i+=1
            else:
                break


class DataRead():
    def __init__(self):
        global NAME
        global CLASS
        global LENGTH

        self.script = list()
        
        with open('csv/dexHolder.csv') as csvfile:
            self.ownData = csv.DictReader(csvfile)
            for row in self.ownData:
                self.holder = row

        with open('csv/intro.csv') as csvfile:
            self.introScript = csv.DictReader(csvfile)
            for row in self.introScript:
                self.script.append(row)
        LENGTH =  len(self.script)
        print(LENGTH)

    def getName(self):
        return self.holder['name']
    def getClass(self):
        return str(self.holder['class']) + ".png"
    def getIntroImage(self,num):
        print("Name: "+NAME)
        ##if(str(self.script[num]['sprite']) is 'NAME'):
        ##    print(NAME)
        ##    return str(NAME) + ".png"
        ##else:
        spriteData = self.script[num]['sprite']
        return eval(spriteData)
    def getIntroScript(self,num):
        return self.script[num]['text']
    
    
    def introDone(self):
        headers = ['name','class','intro','seen','caught','Own']
        
        with open('csv/dexHolder.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            trainerInfo = {'name':self.holder['name'],'class':self.holder['class'],'intro':True,'seen':self.holder['seen'],'caught':self.holder['caught'],'Own':self.holder['Own']}
            writer.writerow(trainerInfo)
            

        
