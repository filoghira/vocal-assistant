from phue import Bridge
import time

#Bridge ip address
bridge_ip_address = '192.168.1.9'

def access_lights():
    #Get bridge object
    b = Bridge(bridge_ip_address)
    #Get lights list
    light_list = b.get_light_objects('id')

    return light_list

def turn_on_room(room):
    #Get bridge object
    b = Bridge(bridge_ip_address)
    #Get rooms lights
    room_lights = b.get_group(room, 'lights')

    #Initialize index
    c=0
    #Run through lights
    for light in room_lights:
        #Convert each element to integer
        room_lights[c] = int(room_lights[c])
        if light[0] == light[-1]:
            c += 1

    #Get all lights
    lights = access_lights()

    #Turn on each light in the room
    for light in lights:
        if light in room_lights:
            lights[light].on = True
            lights[light].brightness = 255