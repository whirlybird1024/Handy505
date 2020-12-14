# -*- coding: cp1252 -*-
import pygame
#import random
import csv
import os.path
from os import path

import cfg

topEntry = 0 #entry at the top of the list
position = 0
scr = 0 #0=menu 1=entry 2=dexter
caught = 0 #0=unseen 1=seen 2=caught
dexSpeak = False #is dexter speaking
pokeList = 0 #0=norm 1=seen 2=caught 3=Type 4=Beta
listNum = 2 #total number of above lists that are complete
totalData = 151
numList = [0,0,0,0,0,0,0]
totalSeen = 0
totalCaught = 0
timesDataRead = 0

class dexMainRBY():
    def __init__(self, screen, FONTSIZE):
        self.font = pygame.font.Font("PKMNRBYGSC.ttf", FONTSIZE)
        self.data = DataRead(self.font, screen)
        self.menu = RenderMenu(self.font, screen, self.data)
        self.entry = RenderEntry(self.font, screen, self.data)
        self.screen = screen
        self.dexter = dexterInfo(self.font, screen, self.data)
        global topEntry
        topEntry = self.data.getTopEntry()
    #buffer = pygame.Surface((256, 256))
    def dexRBYRUN(self):
        ##print entry
        menu = self.menu
        data = self.data
        screen = self.screen
        dexter = self.dexter
        entrySCR = self.entry
        global dexSpeak
        
        #Bulba = pygame.image.load("pics/sugimori/1.png")
        #Bulba = pygame.transform.scale(Bulba, (350,350))
        #screen.blit(Bulba, (50,50))
        if(scr == 0):
            screen.fill((248,232,248))
            if(pokeList == 0):
                ##print "DexList"
                menu.rbyDexMenu()
                menu.populateListRBY(topEntry)
            elif(pokeList == 1):
                ##print "SeenList"
                menu.rbyDexMenu()
                menu.populateListSeen(topEntry)
            elif(pokeList == 2):
                ##print "caughtList"
                menu.rbyDexMenu()
                menu.populateListCaught(topEntry)
            menu.Arrow()
        elif(scr == 1):
            ##print entry
            screen.fill((248,232,248))#255,255,255
            entrySCR.rbyEntry()
            if(caught == 1):
                entrySCR.seenEntryData()
            elif(caught == 2):
                entrySCR.caughtEntryData()
        elif(scr == 2 and not dexSpeak):
            screen.fill((248,232,248))#255,255,255
            dexter.dexter()
            dexSpeak = True

    #all main classes have an inputHandler so input collection can be uniform.
    #it sends input where it needs to go depending on the mode
    def inputHandler(self, action):
        if(scr == 0):
            self.menu.menuInputRBY(action)
        elif(scr == 1):
            self.entry.entryInputRBY(action)
        elif(scr == 2):
            self.dexter.dexterInputRBY(action)
        

    

class DataRead():
    def __init__(self, font, screen):
        self.font = font
        self.screen = screen
        self.lines = list()
        self.holder = {}
        self.species = list()
        self.flavor = list()
        self.htWt = list()
        global totalData
        global totalSeen
        global totalCaught
        with open('csv/dexOwnerList.csv') as csvfile:
            self.ownData = csv.DictReader(csvfile)
            for row in self.ownData:
                ##print row
                if(row['seen'] == '1'):
                    totalSeen += 1
                    ##print totalSeen
                if(row['caught'] == '1'):
                    totalCaught += 1
                    ##print totalCaught
                self.lines.append(row)

        with open('csv/dexHolder.csv') as csvfile:
            self.ownData = csv.DictReader(csvfile)
            for row in self.ownData:
                self.holder = row

        with open('csv/pokemon_species_names.csv') as csvfile:
            self.ownData = csv.DictReader(csvfile)
            for row in self.ownData:
                self.species.append(row)
                
        with open('csv/pokemon_species_flavor_text.csv') as csvfile:
            self.ownData = csv.DictReader(csvfile)
            for row in self.ownData:
                self.flavor.append(row)

        with open('csv/pokemon.csv') as csvfile:
            self.ownData = csv.DictReader(csvfile)
            for row in self.ownData:
                self.htWt.append(row)


    def getEntry(self, num):
        totalData = len(self.lines)
        ##print "Data Length: "  + str(totalData)
        return self.lines[num]

    def getSpecies(self,num):
        return self.species[num]

    def getFlavor(self,num):
        return self.flavor[num]

    def getHtWt(self,num):
        return self.htWt[num]

    def getUserInfo(self):
        return self.holder
    
    def getTopEntry(self):
        iNum = 0
        with open('csv/dexOwnerList.csv') as csvfile:
            self.ownData = csv.DictReader(csvfile)
            for row in self.ownData:
                    ##print row
                if(row['seen'] == '1'):
                      return iNum
                else:
                    iNum += 1
        

    #def getSeen(self):
    def reloadData(self):
        self.font = font
        self.screen = screen
        self.lines = list()
        self.holder = {}
        self.species = list()
        self.flavor = list()
        self.htWt = list()
        global totalData
        global totalSeen
        global totalCaught
        with open('csv/dexOwnerList.csv') as csvfile:
            self.ownData = csv.DictReader(csvfile)
            for row in self.ownData:
                ##print row
                if(row['seen'] == '1'):
                    totalSeen += 1
                    ##print totalSeen
                if(row['caught'] == '1'):
                    totalCaught += 1
                    ##print totalCaught
                self.lines.append(row)

        with open('csv/dexHolder.csv') as csvfile:
            self.ownData = csv.DictReader(csvfile)
            for row in self.ownData:
                self.holder = row

        with open('csv/pokemon_species_names.csv') as csvfile:
            self.ownData = csv.DictReader(csvfile)
            for row in self.ownData:
                self.species.append(row)
                
        with open('csv/pokemon_species_flavor_text.csv') as csvfile:
            self.ownData = csv.DictReader(csvfile)
            for row in self.ownData:
                self.flavor.append(row)

        with open('csv/pokemon.csv') as csvfile:
            self.ownData = csv.DictReader(csvfile)
            for row in self.ownData:
                self.htWt.append(row)
        
        

class RenderMenu():
    
    def __init__(self, font, screen,data):
        self.font = font
        self.screen = screen
        self.data = data
        self.subPosition = 0
        self.menu = True #true=main false=sub
        self.entry = False #true=entry false=menu
        
        
    def rbyDexMenu(self):
        font = self.font
        screen = self.screen
        data = self.data

        if(pokeList == 0):
            cont = font.render("CONTENTS", True, (0, 0, 0))
            screen.blit(cont, (20,15))
        elif(pokeList == 1):
            cont = font.render("SEEN PKMN", True, (0, 0, 0))
            screen.blit(cont, (20,15))
        elif(pokeList == 2):
            cont = font.render("CAUGHT PKMN", True, (0, 0, 0))
            screen.blit(cont, (20,15))
        
        seen = font.render("SEEN", True, (0, 0, 0))
        screen.blit(seen, (370,45))
        own = font.render("OWN", True, (0, 0, 0))
        screen.blit(own, (370,130))

        #LOWER MENU
        dat = font.render("INFO", True, (0, 0, 0))
        screen.blit(dat, (380,275))
        cry = font.render("DATA", True, (0, 0, 0))
        screen.blit(cry, (380,325))
        area = font.render("CRY", True, (0, 0, 0))
        screen.blit(area, (380,375))
        send = font.render("AREA", True, (0, 0, 0))
        screen.blit(send, (380,425))

        #FRAME
        frame = pygame.image.load("pics/menu/menuRBY.png")
        screen.blit(frame, (0,0))

        #SEEN OWN DATA
        seenNum = font.render(data.getUserInfo()['seen'], True, (0, 0, 0))
        screen.blit(seenNum, (420,65))
        ownNum = font.render(data.getUserInfo()['caught'], True, (0, 0, 0))
        screen.blit(ownNum, (420,150))


    def populateListRBY(self, topEntry):
        font = self.font
        screen = self.screen
        data = self.data
        for i in range (0,7):
            entry = topEntry + i
            num = font.render("{0}".format(format((entry+1), '03')), True, (0, 0, 0))
            screen.blit(num, (20,(40+(i*60))))
            dat = data.getEntry(entry)
            if(dat['seen'] == '1'):
                txt = font.render(dat['name'].upper(), True, (0, 0, 0))
            else:
                txt = font.render('----------', True, (0, 0, 0))
            screen.blit(txt, (90,(70+(i*60))))
            if(dat['caught'] == '1'):
                ball = pygame.image.load("pics/menu/pokeballIcon.png")
                ball = pygame.transform.scale(ball, (25,25))
                screen.blit(ball, (62,(70+(i*60))))

            ##print "i: " + str(i)
            numList[i] = entry

    def populateListSeen(self, topEntry):
        font = self.font
        screen = self.screen
        data = self.data
        top = topEntry
        i = 0
        while(i<7):
            entry = top + i
            
            dat = data.getEntry(entry)
            if(dat['seen'] == '1'):
                num = font.render("{0}".format(format((entry+1), '03')), True, (0, 0, 0))
                screen.blit(num, (20,(40+(i*60))))
                txt = font.render(dat['name'].upper(), True, (0, 0, 0))
                screen.blit(txt, (90,(70+(i*60))))
                numList[i] = entry
                if(dat['caught'] == '1'):
                    ball = pygame.image.load("pics/menu/pokeballIcon.png")
                    ball = pygame.transform.scale(ball, (25,25))
                    screen.blit(ball, (62,(70+(i*60))))
                i+=1
            else:
                top += 1
            if(entry >= totalData - 1):
                i = 7
                ##print "data length: " + str(totalData)
            ##print "i: " + str(i)
            #numList[i] = entry

    def populateListCaught(self, topEntry):
        font = self.font
        screen = self.screen
        data = self.data
        top = topEntry
        i = 0
        while(i<7):
            entry = top + i
            
            dat = data.getEntry(entry)
            if(dat['caught'] == '1'):
                num = font.render("{0}".format(format((entry+1), '03')), True, (0, 0, 0))
                screen.blit(num, (20,(40+(i*60))))
                txt = font.render(dat['name'].upper(), True, (0, 0, 0))
                screen.blit(txt, (90,(70+(i*60))))
                numList[i] = entry
                if(dat['caught'] == '1'):
                    ball = pygame.image.load("pics/menu/pokeballIcon.png")
                    ball = pygame.transform.scale(ball, (25,25))
                    screen.blit(ball, (62,(70+(i*60))))
                i+=1
            else:
                top += 1
            if(entry >= totalData - 1):
                i = 7

    def Arrow(self):
        main = self.menu
        screen = self.screen
        pos = position
        sub = self.subPosition
        #mainArrow
        if(main):
            arrow = pygame.image.load("pics/menu/activeArrowRBY.png")
        else:
            arrow = pygame.image.load("pics/menu/inactiveArrowRBY.png")
        arrow = pygame.transform.scale(arrow, (20,20))
        screen.blit(arrow, (0,70 + (60 * pos)))

        #subArrow
        if(main):
            subarrow = pygame.image.load("pics/menu/inactiveArrowRBY.png")
        else:
            subarrow = pygame.image.load("pics/menu/activeArrowRBY.png")
        subarrow = pygame.transform.scale(subarrow, (20,20))
        screen.blit(subarrow, (360,278 + (50 * sub)))

    def menuInputRBY(self, action):
        menu = self.menu
        data = self.data
        global topEntry
        global position
        global scr
        global caught
        global pokeList
        global totalData
        if(action == "UP"):
            if(menu):
                if(position > 0):
                    position -= 1
                else:
                    if(topEntry >0):
                        topEntry -= 1
            else:
                if(self.subPosition > 0):
                    self.subPosition -= 1
        if(action == "DOWN"):
            if(menu):
                if(position < 6):
                    position += 1
                else:
                    if(topEntry < 151):
                        topEntry += 1
            else:
                if(self.subPosition < 3):
                    self.subPosition += 1
        if(action == "A"):
            if(menu): self.menu = False
            else:
                if(self.subPosition == 0):
                    dat = data.getEntry(numList[position])
                    if(dat['seen'] == '1'):
                        caught = 1
                        scr = 2
                        
                if(self.subPosition == 1):
                    dat = data.getEntry(numList[position])
                    if(dat['caught'] == '1'):
                        caught = 2
                        scr = 1
                    elif(dat['seen'] == '1'):
                        caught = 1
                        scr = 1
                    elif(dat['seen'] == '0'):
                        caught = 0
                    ##print caught
                elif(self.subPosition == 2):
                    dat = data.getEntry(numList[position])
                    if(dat['caught'] == '1'):
                        soundFile = 'sound/criesRBY/'+str(format(int(dat['species_id']), '03'))+".wav"
                        ##print ("Update")
                        ##print ("File exists:"+str(path.exists(soundFile)))
                        if(path.exists(soundFile)):
                            pygame.mixer.music.load(soundFile)
                            pygame.mixer.music.set_volume(cfg.VOLUME)
                            ##print cry
                            pygame.mixer.music.play()
        if(action == "B"):
            if(menu == False):
                if(scr == 0):
                    self.menu = True
                else: scr = 0
            else: cfg.CURRENT_MODE = 0

        if(action == "RIGHT"):
            #print "changeRight, PokeList: " + str(pokeList)
            if(pokeList < listNum):
                pokeList += 1
            else:
                pokeList = 0

        if(action == "LEFT"):
            #print "changeLeft"
            if(pokeList > 0):
                pokeList -= 1
            else:
                pokeList = listNum
                

class dexterInfo():
    def __init__(self, font, screen,data):
        self.font = font
        self.screen = screen
        self.data = data

    def dexter(self):
        font = self.font
        screen = self.screen
        data = self.data

        num = numList[position]

        pic = pygame.image.load("pics/sugimori/"+str(num+1)+".png")
        pic = pygame.transform.scale(pic, (440,440))

        screen.blit(pic, (20,20))

        dat = data.getEntry(num)

        soundFile = 'sound/dexterEntries/'+dat['species_id']+".wav"
        
        if(path.exists(soundFile)):
            pygame.mixer.music.load(soundFile)
            pygame.mixer.music.set_volume(cfg.VOLUME)
            #print soundFile
            ##print cry
            pygame.mixer.music.play()

    def dexterInputRBY(self, action):
        data = self.data
        global scr
        global dexSpeak
        
        if(action == "A"):
            #print "dexter cancel A"
            pygame.mixer.music.stop()
            dexSpeak = False
            scr = 0
        if(action == 'B'):
            #print "dexter B"
            dexSpeak = False
            pygame.mixer.music.stop()
            scr = 0

class RenderEntry():
    def __init__(self, font, screen,data):
        self.font = font
        self.screen = screen
        self.data = data
        self.page = True #t=pg1 f=pg2

        self.entryFont = pygame.font.Font("PKMNRBYGSC.ttf", 30)
        
    def rbyEntry(self):
        font = self.font
        screen = self.screen
        data = self.data
        
        ht = font.render("HT", True, (0, 0, 0))
        screen.blit(ht, (220,150))
        wt = font.render("WT", True, (0, 0, 0))
        screen.blit(wt, (220,210))

        #FRAME
        frame = pygame.image.load("pics/menu/entryRBY.png")
        screen.blit(frame, (0,0))

    def caughtEntryData(self):
        font = self.font
        screen = self.screen
        data = self.data
        num = numList[position]

        ##data
        dat = data.getEntry(num)
        spec = data.getSpecies(num)
        flv = data.getFlavor(num)
        htWt = data.getHtWt(num)

        #Sprite
        sprite = pygame.image.load("pics/generation-1/Transparent/"+str(num+1)+".png")
        sprite = pygame.transform.scale(sprite, (130,130))
        screen.blit(sprite, (50,80))

        #Dex Number
        dexNum = font.render("No. "+"{0}".format(format((num+1), '03')), True, (0, 0, 0))
        screen.blit(dexNum, (50,(210)))

        #Height and Weight
        height = float(htWt['height'])/10
        format(height, '.1f')
        ht = font.render(str(height) + "  m", True, (0, 0, 0))
        screen.blit(ht, (320,150))
        weight = float(htWt['weight'])/10
        wt = font.render(str(weight) + "  kg", True, (0, 0, 0))
        screen.blit(wt, (320,210))

        #Name info
        name = font.render(dat['name'].upper(), True, (0, 0, 0))
        screen.blit(name, (220,30))
        genus = str(spec['genus'])
        genus = genus.replace(' Pokémon', '')
        species = font.render(genus.upper(), True, (0, 0, 0))
        screen.blit(species, (220,90))

        #flavor
        ##print flv['flavor_text']
        flavor = flv['flavor_text']
        flavor = flavor.splitlines()
        ##print flavor
        i = 0
        while (i<3):
            ##print(self.page)
            if(self.page):
                flvText = self.entryFont.render(flavor[i], True, (0, 0, 0))
                screen.blit(flvText, (30,280 + (i*70)))
            else:
                flvText = self.entryFont.render(flavor[i+3], True, (0, 0, 0))
                screen.blit(flvText, (30,280 + (i*70)))
            if(i<2):
                i+=1
            else:
                break


    def seenEntryData(self):
        font = self.font
        screen = self.screen
        data = self.data
        num = numList[position]

        ##data
        dat = data.getEntry(num)
        spec = data.getSpecies(num)
        flv = data.getFlavor(num)
        htWt = data.getHtWt(num)

        #Sprite
        sprite = pygame.image.load("pics/generation-1/Transparent/"+str(num+1)+".png")
        sprite = pygame.transform.scale(sprite, (130,130))
        for x in range(sprite.get_width()):
            for y in range(sprite.get_height()):
                if sprite.get_at((x, y)) != (255, 255, 255, 0):
                    sprite.set_at((x, y), (0, 0, 0, 255))
        #sprite.fill((0,0,0,0), None, pygame.BLEND_RGBA_ADD)
        screen.blit(sprite, (50,80))

        #Dex Number
        dexNum = font.render("No. "+"{0}".format(format((num+1), '03')), True, (0, 0, 0))
        screen.blit(dexNum, (50,(210)))

        #Height and Weight
        ht = font.render("???  m", True, (0, 0, 0))
        screen.blit(ht, (320,150))
        wt = font.render("???  kg", True, (0, 0, 0))
        screen.blit(wt, (320,210))

        #Name info
        name = font.render(dat['name'].upper(), True, (0, 0, 0))
        screen.blit(name, (220,30))
        species = font.render("??????", True, (0, 0, 0))
        screen.blit(species, (220,90))

    def entryInputRBY(self, action):
        data = self.data
        global scr
        if(action == "A"):
            self.page = not self.page
        if(action == 'B'):
            #print "cancel"
            self.page = True
            scr = 0
