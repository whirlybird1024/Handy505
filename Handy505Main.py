import pygame
#import random
#import colorsys
#import math
#import glob
#import sys
import os.path
from os import path
#import traceback
import csv
from gpiozero import Button

#import operator

# CONFIG #
#SCREEN = (600, 480) #correct ratio for pi
SCREEN = (480, 500)
ALIGN = 0 # "LEFT" "CENTER" "RIGHT"
ROTATE = 1 # 0 1 2 3

FONTSIZE = 24

TEXT_DELAY = 50 #ms
CLOCK_DELAY = 200
FPS = 20
MODE = 2 #RBMENU NEWMENU RBDEX NEWDEX

KEY_BINDINGS = {

    Button(25): "RIGHT",
    Button(24): "DOWN",
    Button(23): "LEFT",
    Button(22): "UP",
    Button(5): "A",
    Button(12): "B",
}

led = LED(4)

##########

from menu import MainMenu
from menu import SoundMenu
from dex import dexMainRBY
from intro import playIntro
from genPkmn import test
from pokeZone import zoneScreen
#from scan import scan
import cfg


##ROOT = os.path.dirname(__file__)

def main():
    pygame.init()
    pygame.mixer.init()
    #pygame.mouse.set_visible(False)

    pygame.display.set_caption('Handy505')

    screen = pygame.display.set_mode(SCREEN)#, pygame.FULLSCREEN)

    #pygame.display.toggle_fullscreen()

    switch = {
        0: dexMainRBY(screen, FONTSIZE),
        1: dexMainRBY(screen, FONTSIZE),
        2: dexMainRBY(screen, FONTSIZE)
    }

    addMon(25, True)

    #TEST
    #test()
    DexHolder = dexHolderInfo()
    holderInfo = DexHolder.getInfo()

    main = switch.get(MODE, None)
    menu = MainMenu(screen,FONTSIZE)
    sMenu = SoundMenu(screen,FONTSIZE)
    intro = playIntro(screen,FONTSIZE)
    pokeZone = zoneScreen(screen,FONTSIZE)
    #scn = scan(screen)
    #dataCleaner() ##cleans csv files of unneeded data
    #imageCleaner() ##adds transparency to list of pics

    running = True
    print("Holder Info: " + holderInfo['intro'])
    if(holderInfo['intro'] == "False"):
        #cfg.CURRENT_MODE = 4
        print("PLAY INTRO")

    if cfg.CURRENT_MODE == 0: menu.dispMenu()
    elif cfg.CURRENT_MODE == 1: main.dexRBYRUN()
    elif cfg.CURRENT_MODE == 3: sMenu.dispMenu()
    elif cfg.CURRENT_MODE == 4: intro.play()
    elif cfg.CURRENT_MODE == 5: pokeZone.dispZone()
        
    screen.blit(pygame.transform.rotate(screen, 90),(0,0))        
    while running:
        for event in pygame.event.get():
            ##print event
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                TIMER = 0
                pressed = True
                ##print event.key 

                for key, val in KEY_BINDINGS.items():
                    if event.key == key:
                        ##print event.key
                        action = val
                        inputManager(main, menu, sMenu, intro, action, screen,pokeZone)
        #if cfg.CURRENT_MODE == 0: menu.dispMenu()
        #elif cfg.CURRENT_MODE == 1: main.dexRBYRUN()
        #elif cfg.CURRENT_MODE == 3: sMenu.dispMenu()
                        
        #if cfg.CURRENT_MODE == 2: scn.scanning()
                        
        ##print "current mode " + str(cfg.CURRENT_MODE)
        #GPIO
                        
        Button(25).when_pressed = inputManager(main, menu, sMenu, intro, "RIGHT", screen,pokeZone)
        Button(24).when_pressed = inputManager(main, menu, sMenu, intro, "DOWN", screen,pokeZone)
        Button(23).when_pressed = inputManager(main, menu, sMenu, intro, "LEFT", screen,pokeZone)
        Button(22).when_pressed = inputManager(main, menu, sMenu, intro, "UP", screen,pokeZone)
        Button(5).when_pressed = inputManager(main, menu, sMenu, intro, "A", screen,pokeZone)
        Button(12).when_pressed = inputManager(main, menu, sMenu, intro, "B", screen,pokeZone) 
                
        led.on()
        pygame.display.flip()

    #gameLoop(main)

    


def inputManager(main, menu, sMenu, intro, action, screen,pokeZone): #scn,
    #input methods
    if cfg.CURRENT_MODE == 0: menu.inputHandler(action)
    elif cfg.CURRENT_MODE == 1: main.inputHandler(action)
    #elif cfg.CURRENT_MODE == 2: scn.inputHandler(action)
    elif cfg.CURRENT_MODE == 3: sMenu.inputHandler(action)
    elif cfg.CURRENT_MODE == 4: intro.inputHandler(action)
    elif cfg.CURRENT_MODE == 5: pokeZone.inputHandler(action)

    #display methods
    if cfg.CURRENT_MODE == 0: menu.dispMenu()
    elif cfg.CURRENT_MODE == 1: main.dexRBYRUN()
    #elif cfg.CURRENT_MODE == 2: scn.scanning()
    elif cfg.CURRENT_MODE == 3: sMenu.dispMenu()
    elif cfg.CURRENT_MODE == 4: intro.play()
    elif cfg.CURRENT_MODE == 5: pokeZone.dispZone()

    #make sure to uncomment for screen flipping
    #screen.blit(pygame.transform.rotate(screen, 90),(0,0))

def addMon(num, caught):
    lines = {}
    
    with open('csv/dexOwnerList.csv') as csvfile:
        ownData = csv.DictReader(csvfile)
        for row in ownData:
            for column, value in row.items():
                lines.setdefault(column, []).append(value)

    holder = {}
    with open('csv/dexHolder.csv') as csvfile:
        holderData = csv.DictReader(csvfile)
        for row in holderData:
            holder = row

    ##print lines['caught'][num-1]
    if(caught and lines['caught'][num-1] == '0'):
            #print "caught!"
            lines['caught'][num-1] = 1
            
            holder['Own'] = (int(holder['Own']) + 1)
            holder['caught'] = (int(holder['caught']) + 1)

            if(lines['seen'][num-1] == '0'):
                #print 'seen!'
                lines['seen'][num-1] = 1
                holder['seen'] = (int(holder['seen']) + 1)
            #print holder['Own']
            
    elif(not caught and lines['seen'][num-1] == '0'):
            lines['seen'][num-1] = 1
            holder['seen'] = (int(holder['seen']) + 1)
    #print holder['name']
    headers = ['name','class','intro','seen','caught','Own']        
    with open('csv/dexHolder.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerow(holder)

    headers = ['species_id','name','pokedex_number','seen','caught']
    with open('csv/dexOwnerList.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for data in lines['species_id']:
            ##print lines
            ##print lines[data]
            ##print data
            temp = {}
            i=0
            while i<len(headers):
                ##print data[i]
                temp[headers[i]] = lines[headers[i]][int(data)-1]
                ##print headers[i]
                ##print temp[headers[i]]
                i+=1
            ##print temp
            writer.writerow(temp)
    
    #dexMainRBY(screen, FONTSIZE)


class dexHolderInfo():
    def __init__(self):
        self.holder = {}
        with open('csv/dexHolder.csv') as csvfile:
            self.ownData = csv.DictReader(csvfile)
            for row in self.ownData:
                self.holder = row
    def getInfo(self):
        return self.holder

#turns white(or other colors) to transparency
class imageCleaner():
    def __init__(self):
        for i in range(1,152):
            #print "scrubbing " + str(i)+".png"
            image = pygame.image.load("pics/generation-1/"+str(i)+".png").convert_alpha()
            for x in range(image.get_width()):
                for y in range(image.get_height()):
                    if image.get_at((x, y)) == (255, 255, 255, 255):
                        image.set_at((x, y), (255, 255, 255, 0))
            ##print str(x)
            pygame.image.save(image, "pics/generation-1/Transparent/"+str(i)+".png")

#scrubs useless data and adds data to csv files
class dataCleaner():
    def __init__(self):
        self.lines = {}
        
        with open('csv/pokemon_moves.csv') as csvfile:
            self.ownData = csv.DictReader(csvfile)
            for row in self.ownData:
                for column, value in row.items():
                    self.lines.setdefault(column, []).append(value)
                    
        #for i in range (0,len(self.lines['pokedex_id'])):
        i=0
        while i<len(self.lines['version_group_id']):
            ##print i
            vers =  int(self.lines['version_group_id'][i])
            if(vers != 1):
                #print "delete line: " + str(self.lines['version_group_id'][i])
                del self.lines['pokemon_id'][i]
            else: i+=1

        headers = ['species_id','name','pokedex_number','seen','caught']
        
        with open('csv/pokemon_moves.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            for data in self.lines:
                temp = {}
                i=0
                while i<len(headers):
                    temp[headers[i]] = data[i]
                    i+=1
                #print temp
                writer.writerow(temp)

if __name__=="__main__":
    main()
