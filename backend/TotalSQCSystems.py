from tables import *
import redis
import json
print("in totalSQC")

cache = redis.Redis()
session = Session()
res = {}
zones = session.query(Zone)
for zone in zones:
    temp = {zone.name: {}}
    print("in zone")
    if zone.State != []:
        for state in zone.State:
            print("in state")
            temp[zone.name].update({state.name: {}})
            if state.City != []:
                for city in state.City:
                    print("in city")
                    temp[zone.name][state.name].update({city.name: {}})
                    if city.Store != []:
                        for store in city.Store:
                            temp[zone.name][state.name][city.name].update({store.name: []})
                            if store.Machine != []:
                                machines = []
                                for machine in store.Machine:
                                    machines.append(machine.id)
                                    temp[zone.name][state.name][city.name].update({store.name: machines})
    res.update(temp)

cache.set("Dash-SQC-Stations-Map", json.dumps(res))

session.close()
