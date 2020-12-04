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

#import operator

# CONFIG #
SCREEN = (480, 480)
ALIGN = 0 # "LEFT" "CENTER" "RIGHT"
ROTATE = 1 # 0 1 2 3

FONTSIZE = 24

TEXT_DELAY = 50 #ms
CLOCK_DELAY = 200
FPS = 20
MODE = 2 #RBMENU NEWMENU RBDEX NEWDEX

KEY_BINDINGS = {

    pygame.K_RIGHT: "RIGHT",
    pygame.K_DOWN: "DOWN",
    pygame.K_LEFT: "LEFT",
    pygame.K_UP: "UP",
    pygame.K_SPACE: "A",
    pygame.K_LCTRL: "B",
    pygame.K_x: "R",
    pygame.K_z: "L",

    pygame.K_q: "QUIT",
    pygame.K_ESCAPE: "QUIT",

    pygame.K_1: "ROTATE",
    pygame.K_2: "ALIGN",

    pygame.K_b: "BLACKLIST",
    pygame.K_w: "WHITELIST",
}

##########

from menu import MainMenu
from menu import SoundMenu
from dex import dexMainRBY
from genPkmn import test
import cfg


##ROOT = os.path.dirname(__file__)

def main():
    pygame.init()
    pygame.mixer.init()
    #pygame.mouse.set_visible(False)

    pygame.display.set_caption('Handy505')

    screen = pygame.display.set_mode(SCREEN)

    switch = {
        0: dexMainRBY(screen, FONTSIZE),
        1: dexMainRBY(screen, FONTSIZE),
        2: dexMainRBY(screen, FONTSIZE)
    }

    #TEST
    #test()

    main = switch.get(MODE, None)
    menu = MainMenu(screen,FONTSIZE)
    sMenu = SoundMenu(screen,FONTSIZE)
    #dataCleaner() ##cleans csv files of unneeded data
    #imageCleaner() ##adds transparency to list of pics

    running = True

    if cfg.CURRENT_MODE == 0: menu.dispMenu()
    elif cfg.CURRENT_MODE == 1: main.dexRBYRUN()
    elif cfg.CURRENT_MODE == 3: sMenu.dispMenu()
        
                    
    while running:
        for event in pygame.event.get():
            #print event
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                TIMER = 0
                pressed = True
                #print event.key 

                for key, val in KEY_BINDINGS.iteritems():
                    if event.key == key:
                        #print event.key
                        action = val
                        inputManager(main, menu, sMenu, action)
        #if cfg.CURRENT_MODE == 0: menu.dispMenu()
        #elif cfg.CURRENT_MODE == 1: main.dexRBYRUN()
        #elif cfg.CURRENT_MODE == 3: sMenu.dispMenu()
        #print "current mode " + str(cfg.CURRENT_MODE)
        pygame.display.flip()

    #gameLoop(main)

    
def gameLoop(main, menu):
    running = True
        
                    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if event.type == pygame.KEYDOWN:
            TIMER = 0
            pressed = True
            #print event.key 

            for key, val in KEY_BINDINGS.iteritems():
                if event.key == key:
                    #print event.key
                    action = val
                    inputManager(main, menu, action)
        main.dexRBYRUN()
        #print "running"
        pygame.display.flip()

def inputManager(main, menu, sMenu, action):
    if cfg.CURRENT_MODE == 0: menu.inputHandler(action)
    elif cfg.CURRENT_MODE == 1: main.inputHandler(action)
    elif cfg.CURRENT_MODE == 3: sMenu.inputHandler(action)

    if cfg.CURRENT_MODE == 0: menu.dispMenu()
    elif cfg.CURRENT_MODE == 1: main.dexRBYRUN()
    elif cfg.CURRENT_MODE == 3: sMenu.dispMenu()


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
            print "scrubbing " + str(i)+".png"
            image = pygame.image.load("pics/generation-1/"+str(i)+".png").convert_alpha()
            for x in range(image.get_width()):
                for y in range(image.get_height()):
                    if image.get_at((x, y)) == (255, 255, 255, 255):
                        image.set_at((x, y), (255, 255, 255, 0))
            #print str(x)
            pygame.image.save(image, "pics/generation-1/Transparent/"+str(i)+".png")

#scrubs useless data and adds data to csv files
class dataCleaner():
    def __init__(self):
        self.lines = {}
        
        with open('csv/pokemon_moves.csv') as csvfile:
            self.ownData = csv.DictReader(csvfile)
            for row in self.ownData:
                for column, value in row.iteritems():
                    self.lines.setdefault(column, []).append(value)
                    
        #for i in range (0,len(self.lines['pokedex_id'])):
        i=0
        while i<len(self.lines['version_group_id']):
            #print i
            vers =  int(self.lines['version_group_id'][i])
            if(vers != 1):
                print "delete line: " + str(self.lines['version_group_id'][i])
                del self.lines['pokemon_id'][i]
            else: i+=1
        
        with open('csv/pokemon_moves.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            for data in self.lines:
                temp = {}
                i=0
                while i<len(headers):
                    temp[headers[i]] = data[i]
                    i+=1
                print temp
                writer.writerow(temp)

if __name__=="__main__":
    main()
