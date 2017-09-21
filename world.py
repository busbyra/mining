#!/usr/local/bin/python

import timeout, os, time
from map_with_debugs import Map
from sys import argv
import zerg

TICKS = 100
refresh_delay = 0.0 # number should represent seconds
try:
    if len(argv) > 1 and argv[1].startswith("-refresh"):
        refresh_delay = float(argv.pop(1).split("=")[1])
except:
    pass # Any problem and the refresh delay will remain at 0

overlord = zerg.Overlord(TICKS)

maps = dict()
for n in range(3):
    maps[n] = Map(10, 5)
    if n+1 < len(argv):
        maps[n].load_from_file(argv[n+1])

    overlord.add_map(n, maps[n].summary())

zerg_locations = { n: None for n in overlord.zerg }
zerg_health = { zerg_id: the_zerg.health for zerg_id, the_zerg in overlord.zerg.items() }



print(zerg_locations)

mined = 0

for _ in range(TICKS):
    act = 'NONE'
    try:
        with timeout.within(1000):
            act = overlord.action()
    except timeout.TimeoutError:
        pass

    print(act)
    if act.startswith('DEPLOY'):
        _, z_id, map_id = act.split()
        z_id = int(z_id)
        map_id = int(map_id)

        if zerg_locations[z_id] is None:
            if maps[map_id].add_zerg(overlord.zerg[z_id], zerg_health[z_id]):
                zerg_locations[z_id] = map_id

    elif act.startswith('RETURN'):
        _, z_id = act.split()
        z_id = int(z_id)

        if zerg_locations[z_id] is not None:
            map_id = zerg_locations[z_id]
            extracted, hp = maps[map_id].remove_zerg(z_id)
            if extracted is not None:
                zerg_locations[z_id] = None
                zerg_health[z_id] = hp
                mined += extracted


    for n in maps:
        maps[n].tick()
        print(maps[n])
    time.sleep(refresh_delay)
#    os.system('cls' if os.name == 'nt' else 'clear')

print("Total mined:", mined)
print("Refined Minerals:", overlord.refined_minerals)
