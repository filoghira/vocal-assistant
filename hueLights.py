from phue import Bridge
from exceptions import *

#Bridge ip address
bridge_ip_address = '192.168.1.9'

def access_lights():
    #Get bridge object
    b = Bridge(bridge_ip_address)
    #Get lights list
    light_list = b.get_light_objects('id')

    return light_list

def access_room_lights(group):
    # Get bridge object
    b = Bridge(bridge_ip_address)
    # Get rooms lights
    lights = b.get_group(group, 'lights')

    # Initialize index
    c = 0
    # Run through lights
    for light in lights:
        # Convert each element to integer
        lights[c] = int(lights[c])
        if light[0] == light[-1]:
            c += 1

    return lights

def check_room(room):
    b = Bridge(bridge_ip_address)
    groups = b.get_group()

    check = False

    for group in groups:

        if groups[group]['name'].lower() == room:
            room = groups[group]['name']
            check = True

    if not check:
        raise RoomNotFound(room)

    return check,room

def turn_on_room(room):

    check,room = check_room(room)

    if room:
        room_lights = access_room_lights(room)
        # Get all lights
        lights = access_lights()

        # Turn on each light in the room
        for light in lights:
            if light in room_lights:
                lights[light].on = True

def turn_off_room(room):

    check, room = check_room(room)

    if room:
        room_lights = access_room_lights(room)
        # Get all lights
        lights = access_lights()

        # Turn on each light in the room
        for light in lights:
            if light in room_lights:
                lights[light].on = False