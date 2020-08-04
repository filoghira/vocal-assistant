from phue import Bridge
from hueLights_const import *
import time


def access_lights(bridge_ip):
    b = Bridge(bridge_ip)
    light_names_list = b.get_light_objects('name')
    return light_names_list


def film_lights():
    lights = access_lights(bridge_ip_address)
    for light in lights:
        lights[light].on = True
        lights[light].hue = 7000
        lights[light].saturation = 100


def danger_mode():
    lights = access_lights(bridge_ip_address)
    while True:
        time.sleep(1)
        for light in lights:
            lights[light].on = True
            lights[light].hue = 180
            lights[light].saturation = 100
        time.sleep(1)
        for light in lights:
            lights[light].on = True
            lights[light].hue = 7000
            lights[light].saturation = 100
