#!/usr/bin/env python3
"""
DOCSTRING HERE
"""
from collections import defaultdict


from random import randint, choice



class Drone:
    def __init__(self):
        self.health = 40 
        self.moves = 1
        self.capacity = 10
        self.location = dict()
        self.xy = tuple()
        self.mined = 0
        self.getme = False
        self.home = tuple()
        self.sets = set()

    def action(self, context):
        self.location[tuple((context.x, context.y-1))] = vars(context)['south']
        self.location[tuple((context.x, context.y+1))] = vars(context)['north']
        self.location[tuple((context.x+1, context.y))] = vars(context)['east']
        self.location[tuple((context.x-1, context.y))] = vars(context)['west']
        self.xy = (tuple((context.x, context.y)))
        self.sets.add(tuple((context.x, context.y)))
        print("Sets:", self.sets)
        print("Location",self.xy)
        for k, v in self.location.items():
            if v == '_':
                self.home = k
        if self.mined == 10:
            self.getme = True
            print("HOME: ",self.home)
            for k,v in context.__dict__.items():
                if v == '_':
                    return k.upper()
                else:
                    if self.xy == self.home:
                        return 'CENTER'
                    new = randint(0, 3)
                    if new == 0:
                        return 'NORTH'
                    elif new == 1:
                        return 'SOUTH'
                    elif new == 2:
                        return 'EAST'
                    elif new == 3:
                        return 'WEST'
                    else:
                        return 'CENTER'
        else:
            for k,v in context.__dict__.items():
                if v == '*':
                    check = k.upper()
                    self.mined += 1
                    print("CHECK", self.mined)
                    return check
            new = randint(0, 3)
            print("Random: ", new)
            if new == 0:
                return 'NORTH'
            elif new == 1:
                return 'SOUTH'
            elif new == 2:
                return 'EAST'
            elif new == 3:
                return 'WEST'
            else:
                return check
        #elif self.mined == 10:
         #   self.getme = True
            # Hunt for home
          #  for k,v in context.__dict__.items():
           #     if v == '_':
            #        return k.upper()


    
    def get_init_cost(self):
        pass
        # 10 health = 1 mineral
        # 5 capacity = 1 mineral
        # 1 move = 3 minerals


class Overlord:
    def __init__(self, total_ticks, refined_minerals=54):
        self.maps = {}
        self.zerg = {}
        self.refined_minerals = refined_minerals
        self.total_ticks = total_ticks
        
        for _ in range(6):
            z = Drone()
            self.zerg[id(z)] = z
            # Change this to adjust based on the actual cost
            self.refined_minerals -= 9

    def add_map(self, map_id, summary):
        self.maps[map_id] = summary

    def action(self):
        act = randint(0, 3)
        self.total_ticks -= 1
        for i in self.zerg.keys():
            if self.zerg[i].getme == True:
                return 'RETURN {}'.format(choice(list(self.zerg.keys())))    
        if self.total_ticks <= 10:
            #for i in self.zerg.keys():
            #    print("Rope", self.zerg[i].getme)
            return 'RETURN {}'.format(choice(list(self.zerg.keys())))
        elif act == 0:
            return 'RETURN {}'.format(choice(list(self.zerg.keys())))
        elif act == 1 or act == 2:
            return 'DEPLOY {} {}'.format(choice(list(self.zerg.keys())),
                    choice(list(self.maps.keys())))
        else:
            return 'NONE'

