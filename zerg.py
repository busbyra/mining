#!/usr/bin/env python3
"""
This is the biomass that the Zerg come from.  When the hive is ready to deploy
their Zerg somewhere on a planet, they reference this module for basic
Overlord and Drone processes.

Further analysis is needed to determine how they deploy their more combat
oriented units.
"""
from collections import defaultdict
from random import randint, choice

class Zerg:
    """ This is the basic parent class that all Zerg come from.  This should
    have been where a lot of the default information was stored about every
    Zerg.
    """
    pass

class Drone(Zerg):
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
        """Returns the total steps used from the Zergs."""
        return self.step
    
    def action(self, context):
        """
        This runs through and updates a personal map for each Zerg.
        This provides simple logic to try and keep them alive as they explore
        the map and mine minerals.
        """
        # This needs to be pushed out to the Overlord
        self.location[tuple((context.x, context.y-1))] = vars(context)['south']
        self.location[tuple((context.x, context.y+1))] = vars(context)['north']
        self.location[tuple((context.x+1, context.y))] = vars(context)['east']
        self.location[tuple((context.x-1, context.y))] = vars(context)['west']
        self.xy = (tuple((context.x, context.y)))
        #I got the following from following Dave's example
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
                if self.location[tuple((context.x, context.y + 1))] != '#'\
                and self.location[tuple((context.x, context.y + 1))] != '~':
                        return 'NORTH'
                else:
                    new = randint(0,3)
            elif new == 1:
                if self.location[tuple((context.x, context.y - 1))] != '#'\
                and self.location[tuple((context.x, context.y - 1))] != '~':
                        return 'SOUTH'
                else:
                    new = randint(0,3)
            elif new == 2:
                if self.location[tuple((context.x + 1, context.y))] != '#'\
                and self.location[tuple((context.x + 1, context.y))] != '~':
                        return 'EAST'
                else:
                    new = randint(0,3)
            elif new == 3:
                if self.location[tuple((context.x - 1, context.y))] != '#'\
                and self.location[tuple((context.x - 1, context.y))] != '~':
                        return 'WEST'
                else:
                    new = randint(0,3)
            else:
                return check

    def get_init_cost(self):
        """ This should determined how many minerals it takes to initialize a
        drone.
        """
        pass

class Miner(Drone):
    """Miner subclass of drone.
    """
    def __init__(self):
        """These stats should have been registered from the Drone or Zerg
        classes.
        """
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
    """Scout subclass of drone.
    This drone was deemed not worthy due to movement costs.
    """
    pass


class Overlord(Zerg):
    """The Overlord class is used to control the drones and visualize the map
    in order to determine whether the map is worth mining.
    """
    
    def __init__(self, ticks, refined_minerals):
        """ This holds all of the needed information for a given Overlord.
        """
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
        """This adds a map to the map dictionary list, to include a summary
        to indicate the density of minerals in the area.
        """
        self.maps[map_id] = summary
    
    def action(self):
        """The actions the Overlord takes. RETURN and DEPLOY are randomized
        at this time.
        """
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
        """ This should have updated the Overlord of the map location for the
        Zerg.
        """
        return "No Dashboard for you!"
