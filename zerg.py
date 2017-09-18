#!/usr/bin/env python3
"""
DOCSTRING HERE
"""


from random import randint, choice



class Drone:
    def __init__(self):
        self.health = 40 
        self.moves = 1
        self.capacity = 10
        self.location = list()


    def action(self, context):
        self.location.append((context.x, context.y))
        print("LOC:", self.location)
        print("COORD: {},{}".format(context.x ,context.y))
        print("Zerg ID:",self, "BEEP:", vars(context))
        print("CONTEXT:", context)
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

    
    def get_init_cost(self):
        pass
        # 10 health = 1 mineral
        # 5 capacity = 1 mineral
        # 1 move = 3 minerals


class Overlord:
    def __init__(self, total_ticks, refined_minerals=54):
        self.maps = {}
        self.zerg = {}
        #self.tracker = list()
        self.refined_minerals = refined_minerals

        for _ in range(6):
            z = Drone()
            self.zerg[id(z)] = z
            # Change this to adjust based on the actual cost
            self.refined_minerals -= 9

    def add_map(self, map_id, summary):
        self.maps[map_id] = summary

    def action(self):
        act = randint(0, 3)
        if act == 0:
            return 'RETURN {}'.format(choice(list(self.zerg.keys())))
        elif act == 1 or act ==2:
            return 'DEPLOY {} {}'.format(choice(list(self.zerg.keys())),
                    choice(list(self.maps.keys())))
        else:
            return 'NONE'

o = Overlord(4)

test = o.zerg
for i  in o.zerg.keys():
    print(i, o.zerg[i].health, o.zerg[i].moves, o.zerg[i].capacity)

print(o.maps)

#zerg_locations = { n: None for n in Overlord.zerg }
#print("LOCATIONS: ", zerg_locations)

