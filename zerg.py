#!/usr/bin/env python3
"""
DOCSTRING HERE
"""
from collections import defaultdict
from random import randint, choice

class Zerg:
    pass

class Drone:
    def __init__(self):
        self.health = 40 
        self.moves = 1
        self.capacity = 10
        self.location = dict()
        self.xy = tuple()
        self.mined = 0
        self.step = 0
        self.getme = False
        self.home = tuple()
    
    def steps(self):
        return self.step
    
    def action(self, context):
        # Push this off to a map class or something
        self.location[tuple((context.x, context.y-1))] = vars(context)['south']
        self.location[tuple((context.x, context.y+1))] = vars(context)['north']
        self.location[tuple((context.x+1, context.y))] = vars(context)['east']
        self.location[tuple((context.x-1, context.y))] = vars(context)['west']
        self.xy = (tuple((context.x, context.y)))
        map_keys = list(self.location)
        minx = min(map_keys)[0]
        maxx = max(map_keys)[0]
        miny = min(map_keys, key=lambda atuple:atuple[1])[1]
        maxy = max(map_keys, key=lambda atuple:atuple[1])[1]
        for x in range(minx, maxx + 1):
            for y in range(miny, maxy + 1):
                print(self.location.get(tuple((x,y)),"@"), end="")
            print()

        for k, v in self.location.items():
            if v == '_':
                self.home = k
        if self.mined == 10:
            self.getme = True
            for k,v in context.__dict__.items():
                if v == '_':
                    return k.upper()
                else:
                    if self.xy == self.home:
                        print("HOME")
                        return 'CENTER'
                    new = randint(0, 3)
                    if new == 0:
                        self.step += 1
                        return 'NORTH'
                    elif new == 1:
                        self.step += 1
                        return 'SOUTH'
                    elif new == 2:
                        self.step += 1
                        return 'EAST'
                    elif new == 3:
                        self.step += 1
                        return 'WEST'
                    else:
                        return 'CENTER'
        else:
            for k,v in context.__dict__.items():
                if v == '*':
                    check = k.upper()
                    self.mined += 1
                    return check
            new = randint(0, 3)
            if new == 0:
                if self.location[tuple((context.x, context.y + 1))] != '#':
                    if self.location[tuple((context.x, context.y + 1))] != '~':
                        return 'NORTH'
                else:
                    new = randint(0,3)
            elif new == 1:
                if self.location[tuple((context.x, context.y - 1))] != '#':
                    if self.location[tuple((context.x, context.y - 1))] != '~':
                        return 'SOUTH'
                else:
                    new = randint(0,3)
            elif new == 2:
                if self.location[tuple((context.x + 1, context.y))] != '#':
                    if self.location[tuple((context.x + 1, context.y))] != '~':
                        return 'EAST'
                else:
                    new = randint(0,3)
            elif new == 3:
                if self.location[tuple((context.x - 1, context.y))] != '#':
                    if self.location[tuple((context.x - 1, context.y))] != '~':
                        return 'WEST'
                else:
                    new = randint(0,3)
            else:
                return check

    def get_init_cost(self):
        pass
        # 10 health = 1 mineral
        # 5 capacity = 1 mineral
        # 1 move = 3 minerals

class Miner(Drone):
    def __init__(self):
        self.health = 10
        self.moves = 1
        self.capacity = 25
        self.location = dict()
        self.xy = tuple()
        self.mined = 0
        self.step = 0
        self.getme = False
        self.home = tuple()


class Scout(Drone):
    pass


class Overlord(Zerg):
    def __init__(self, ticks, refined_minerals):
        self.maps = {}
        self.zerg = {}
        self.deployedzerg = {}
        self.refined_minerals = refined_minerals
        self.ticks = ticks
        checks = self.maps
        self.dashboard = Dashboard.update

        for _ in range(6):
            z = Miner()
            self.zerg[id(z)] = z
            # Change this to adjust based on the actual cost
            self.refined_minerals -= 9

    def add_map(self, map_id, summary):
        self.maps[map_id] = summary
    
    def action(self):
        if self.ticks < 10:
            return 'RETURN {}'.format(choice(list(self.zerg.keys())))
        act = randint(0, 3)
        self.ticks -= 1
        for i in self.zerg.keys():
            if self.zerg[i].getme == True:
                return 'RETURN {}'.format(choice(list(self.zerg.keys())))    
        if act == 0:
            return 'RETURN {}'.format(choice(list(self.zerg.keys())))
        elif act == 1 or act == 2:
            check = choice(list(self.zerg.keys()))
            return 'DEPLOY {} {}'.format(choice(list(self.zerg.keys())),
                    choice(list(self.maps.keys())))
        else:
            return 'NONE'


class Dashboard():
    """This is a Dashboard template that I did not flesh out.
    """
    def __init__(self):
        pass

    def update():
        return "No Dashboard for you!"
