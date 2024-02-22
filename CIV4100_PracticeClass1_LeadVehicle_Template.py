#!/usr/bin/env python

import glob
import os
import sys
import random
import time
import argparse
import math
import carla


try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

X = -2.1
Y = 120
Z = 0.2

PITCH = 0
YAW = 90
ROLL = 0

TRIGGER_DIST = 25
VEHICLE_MODEL = 'vehicle.toyota.prius'

# set up spectator camera
SPEC_CAM_X = 25
SPEC_CAM_Y = 120
SPEC_CAM_Z = 120
SPEC_CAM_PITCH = -90
SPEC_CAM_YAW = 0
SPEC_CAM_ROLL = 0

SPAWNED_VEHICLE_ROLENAME = 'stationary_vehicle'

LEAD_VEHICLE_VELOCITY = 3


#########################################################################################################
def main(args):
    try:
        client = carla.Client('localhost', 2000)  # create client to connect to simulator
        client.set_timeout(10.0)
        world = client.load_world('Town01')

        print('Sucessfully connected and retrieved carla world.')

        # set spectator camera to a birds view of testing area
        # get the spectator actor which is a spectator that controls camera view
        # in simulation window (window that appears when you start carla)
        spectator = world.get_spectator()
        spectator.set_transform(carla.Transform(carla.Location(SPEC_CAM_X, SPEC_CAM_Y, SPEC_CAM_Z),
                                                carla.Rotation(SPEC_CAM_PITCH, SPEC_CAM_YAW, SPEC_CAM_ROLL)))

        world.set_weather(carla.WeatherParameters())  # set default weather

        # get blueprint library which is used for creating actors
        blueprint_library = world.get_blueprint_library()

        # select a blueprint for our lead vehicle
        lead_vehicle_bp = next(bp for bp in blueprint_library if bp.id == VEHICLE_MODEL)

        # set lead vehicle role_name attribute to reflect lead_vehicle so that
        # it's easily distinguishable in debugging
        lead_vehicle_bp.set_attribute('role_name', SPAWNED_VEHICLE_ROLENAME)

        # FILL IN X, Y, Z and PITCH, YAW, ROLL to Location() and Rotation()
        spawn_loc = carla.Location()
        rotation = carla.Rotation()
        transform = carla.Transform(spawn_loc, rotation)

        # spawn the vehicle
        lead_vehicle = world.spawn_actor(lead_vehicle_bp, transform)
    
        time.sleep(5)
        # set the direction and speed of movement set_target_velocity()
        lead_vehicle.set_target_velocity()  # set target velocity for lead vehicle

        time.sleep(20)
        lead_vehicle.set_target_velocity(carla.Vector3D(0, 0, 0))  # set target velocity for lead vehicle
        time.sleep(20)
         # set target velocity for lead vehicle
        lead_vehicle.destroy()

    finally:
        print("Finished Executing Test Case!")


if __name__ == '__main__':
    description = "Carla-Autoware Manual Test Case - Stationary Vehicle"

    parser = argparse.ArgumentParser(description=description)

    # parser.add_argument('--target-velocity',  type=int, help='')

    args = parser.parse_args()

    main(args)
