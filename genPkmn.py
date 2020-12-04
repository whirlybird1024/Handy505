import pygame
import random
import os.path
from os import path
#import traceback
import csv
import pandas as pd
import math

#import operator

class test():
    def __init__(self):
        self.gen = genWildPkmnByType(36,50,"viridion forest", "")
        

class genWildPkmnByType():
    def __init__(self,typeNum,lvl,area,held):
        self.typeNum = typeNum
        self.lvl = lvl

        self.ID = "test"

        self.util = Utility()

        self.header = {}

        self.hpIV = 0
        self.attackIV = random.randrange(0,15)
        if((self.attackIV % 2) != 2):
            self.hpIV = self.hpIV + 8
        self.defenceIV = random.randrange(0,15)
        if((self.defenceIV % 2) != 2):
            self.hpIV = self.hpIV + 4
        self.spcAttackIV = random.randrange(0,15)
        self.spcDefIV = random.randrange(0,15)
        if((self.spcAttackIV % 2) != 2 or (self.spcDefIV % 2) != 2):
            self.hpIV = self.hpIV + 1
        self.speedIV = random.randrange(0,15)
        if((self.speedIV % 2) != 2):
            self.hpIV = self.hpIV + 2

        self.hp = self.util.HPFormula(self.util.hp,self.hpIV,0,self.lvl)
        self.attack = self.util.HPFormula(self.util.attack,self.attackIV,0,self.lvl)
        self.defence = self.util.HPFormula(self.util.defence,self.defenceIV,0,self.lvl)
        self.spcAttack = self.util.HPFormula(self.util.spcAttack,self.spcAttackIV,0,self.lvl)
        self.spcDef = self.util.HPFormula(self.util.spcDef,self.spcDefIV,0,self.lvl)
        self.speed = self.util.HPFormula(self.util.speed,self.speedIV,0,self.lvl)

        

        name = self.util.getName(self.typeNum)
        types = self.util.getType(self.typeNum)

        gender = random.randrange(1,2)

        moves = self.util.getMoves(self.lvl, self.typeNum)
        ability = getAbility
        nature = random.randrange(1,25)

        self.held = held
        self.area = area
        

        self.rowData = {self.ID, name, self.typeNum, types[0], types[1], gender, moves[0], moves[1], moves[2], moves[3], ability, lvl, self.HP, self.attack, self.defence, self.spcAttack, self.spcDef, self.speed, self.HPIV, self.attackIV, self.defenceIV, self.spcAttackIV, self.spcDefIV, self.speedIV, 0,0,0,0,0,0, nature, self.held, "", self.area}

        self.tmpCsv = pd.read_csv('csv/PCBox/pkmnDefault.csv')
        self.tmpCsv.to_csv('tstPkmn.csv')

        with open('csv/PCBox/pkmnDefault.csv') as csvfile:
            self.headData = csv.DictReader(csvfile)
            for row in self.headData:
                self.header = row
        
        with open('csv/PCBox/tstPkmn.csv', 'a') as csvfile:
            self.pkmnData = csv.DictWriter(csvfile, self.header)
            self.pkmnData.writerow(self.rowData)
                
class Utility():
    def __init__(self):
        self.hp = 0
        self.attack = 0
        self.defence = 0
        self.spcAttack = 0
        self.spcDef = 0
        self.speed = 0
    
    def loadData(self, typeNum):
        with open('csv/pokemon_stats.csv') as csvfile:
            self.statData = csv.DictReader(csvfile)
            for row in self.statData:
                if(row['pokemon_id'] == typeNum):
                    if(row['stat_id'] == 1):
                       self.hp = row['base_stat']
                    if(row['stat_id'] == 2):
                       self.attack = row['base_stat']
                    if(row['stat_id'] == 3):
                       self.defence = row['base_stat']
                    if(row['stat_id'] == 4):
                       self.spcAttack = row['base_stat']
                    if(row['stat_id'] == 5):
                       self.spcDef = row['base_stat']
                    if(row['stat_id'] == 6):
                       self.speed = row['base_stat']
                       
    def HPFormula(self, stat,IV,EV,lvl):
        fullStat = (((((stat+IV)*2+(math.sqrt(EV)/4))*lvl)/100)+lvl+10)
        return fullStat
    
    def statFormula(self, stat,IV,EV,lvl):
        fullStat = (((((stat+IV)*2+(math.sqrt(EV)/4))*lvl)/100)+5)
        return fullStat
    def getMoves(self, lvl, typeNum):
        moves = [0,0,0,0]
        possibleMoves = list()
        
        with open('csv/pokemon_moves.csv') as csvfile:
            moveData = csv.DictReader(csvfile)
            for row in moveData:
                print "CurNum: " + str(row['pokemon_id'])
                #print "TypeNum: " + str(typeNum)
                if(row['pokemon_id'] == typeNum):
                    if(row['pokemon_id'] > typeNum): break
                    print "Mon Found"
                    if(row['pokemon_move_method_id'] == 1 or row['pokemon_move_method_id'] == 2):
                        print "Moves Found"
                        if(row['level'] >= lvl):
                            print "Move Found"
                            print "MoveID" + row['move_id']
                            moveData.append(row['move_id'])

        moveNum = len(moves)
        print "Movenum" + str(moveNum)
        #randNum =
        moveIDs = random.sample(range(0, moveNum), 3)

        moves = [possibleMoves[moveIDs[0]], possibleMoves[moveIDs[1]], possibleMoves[moveIDs[2]], possibleMoves[moveIDs[3]]]
        return moves

    def getType(self, typeNum):
        types = [0,0]

        with open('csv/pokemon_types.csv') as csvfile:
            typeData = csv.DictReader(csvfile)
            for row in typeData:
                if(row['pokemon_id'] == typeNum):
                    if(types[0] == 0):
                        types[0] = row['type_id']
                    else:
                        types[1] = row['type_id']

        return types

    def getName(self, typeNum):
        name = ""

        with open('csv/pokemon.csv') as csvfile:
            nameData = csv.DictReader(csvfile)
            for row in nameData:
                if(row['id'] == typeNum):
                    name = row['identifier']

        return name

    def getAbility(self, typeNum):
        ability = 0
        ableNum = random.range(0,10)
        
        with open('csv/pokemon_types.csv') as csvfile:
            ableData = csv.DictReader(csvfile)
            for row in ableData:
                if(row['pokemon_id'] == typeNum):
                    if(ableNum == 5):
                        if(row['is_hidden'] == 1):
                            ability = row['ability_id']
                else:
                    if(row['is_hidden'] == 0):
                            ability = row['ability_id']

        return ability

        
        
    
