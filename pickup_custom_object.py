#!/usr/bin/env python3

# Copyright (c) 2017 Anki, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''This example demonstrates how you can define custom objects.

The example defines several custom objects (2 cubes, a wall and a box). When
Cozmo sees the markers for those objects he will report that he observed an
object of that size and shape there.

You can adjust the markers, marker sizes, and object sizes to fit whatever
object you have and the exact size of the markers that you print out.
'''

import time

import cozmo
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes, ObservableElement, ObservableObject
from cozmo.util import Pose
import sys
print(sys.path)



def lookForCubes(robot, timeout, head_height):
    robot.set_lift_height(height = 0, accel = 6, max_speed = 500, duration = 1, in_parallel = False, num_retries = 3).wait_for_completed()
    start_time = time.time()
    if head_height == 0:
        robot.set_head_angle(cozmo.util.Angle(degrees = 0)).wait_for_completed()
    elif head_height == 1:
        robot.set_head_angle(cozmo.util.Angle(degrees = 22.25)).wait_for_completed()
    elif head_height == 2:
        robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
    while (time.time() - start_time < timeout):
        action = robot.turn_in_place(cozmo.util.Angle(degrees = 20), in_parallel = False, num_retries = 0, speed =cozmo.util.radians(25),accel = None, angle_tolerance = None, is_absolute = False).wait_for_completed()
        cubes = robot.world.wait_until_observe_num_objects(num=1, object_type=CustomObject, timeout=3)
        if len(cubes) > 0:
            print('lencube:',len(cubes));
            #action.wait_for_completed()
            return cubes
    return []
        
def pickupCube(robot, cube_location):
    robot.set_lift_height(height = 0, accel = 6, max_speed = 500, duration = 1, in_parallel = False, num_retries = 3).wait_for_completed()
    robot.go_to_pose(cube_location,relative_to_robot=False).wait_for_completed()
    robot.drive_wheels(-50,-50)
    time.sleep(3)
    robot.go_to_pose(cube_location,relative_to_robot=False).wait_for_completed()

    robot.drive_wheels(0, 0)
    robot.set_lift_height(height = 1, accel = 6, max_speed = 500, duration = 1, in_parallel = False, num_retries = 3).wait_for_completed()
    robot.drive_wheels(-25, -25)
    time.sleep(2)
    robot.drive_wheels(0, 0)

    
    


def handle_object_appeared(evt, **kw):
    # This will be called whenever an EvtObjectAppeared is dispatched -
    # whenever an Object comes into view.
    if isinstance(evt.obj, CustomObject):
        print("Cozmo started seeing a %s" % str(evt.obj.object_type))


def handle_object_disappeared(evt, **kw):
    # This will be called whenever an EvtObjectDisappeared is dispatched -
    # whenever an Object goes out of view.
    if isinstance(evt.obj, CustomObject):
        print("Cozmo stopped seeing a %s" % str(evt.obj.object_type))

def pickupObject(robot):
    robot.drive_wheels(100,100)
    time.sleep(2.5)
    robot.drive_wheels(0,0)
    robot.set_lift_height(height = 1, accel = 6, max_speed = 500, duration = 1, in_parallel = False, num_retries = 3).wait_for_completed()
    robot.drive_wheels(-50,-50)
    time.sleep(3)
    robot.drive_wheels(0,0)
    cubes = robot.world.wait_until_observe_num_objects(num=1, object_type=CustomObject, timeout=3)
    if len(cubes) == 0:
        return
    else:
        robot.set_lift_height(height = 0, accel = 6, max_speed = 500, duration = 1, in_parallel = False, num_retries = 3).wait_for_completed()
        robot.go_to_pose(cubes[0].pose,relative_to_robot=False).wait_for_completed()
        pickupObject(robot)

        

def custom_objects(robot: cozmo.robot.Robot):
    # Add event handlers for whenever Cozmo sees a new object
    robot.add_event_handler(cozmo.objects.EvtObjectAppeared, handle_object_appeared)
    robot.add_event_handler(cozmo.objects.EvtObjectDisappeared, handle_object_disappeared)





    custom_box = robot.world.define_custom_box(custom_object_type=cozmo.objects.CustomObjectTypes.CustomType00, \
                                                       marker_front=cozmo.objects.CustomObjectMarkers.Circles2, \
                                                       marker_back=cozmo.objects.CustomObjectMarkers.Circles3, \
                                                       marker_top=cozmo.objects.CustomObjectMarkers.Circles4, \
                                                       marker_bottom=cozmo.objects.CustomObjectMarkers.Circles5, \
                                                       marker_left=cozmo.objects.CustomObjectMarkers.Diamonds2, \
                                                       marker_right=cozmo.objects.CustomObjectMarkers.Diamonds3, \
                                                       depth_mm=60, \
                                                       width_mm=60, \
                                                       height_mm=45, \
                                                       marker_width_mm=24.892, \
                                                       marker_height_mm=24.892, \
                                                       is_unique=True)

    if (custom_box is not None):
        print("All objects defined successfully!")
    else:
        print("One or more object definitions failed!")
        return

    print("Show the above markers to Cozmo and you will see the related objects "
          "annotated in Cozmo's view window, you will also see print messages "
          "everytime a custom object enters or exits Cozmo's view.")

    print("Press CTRL-C to quit")


    cubes = lookForCubes(robot, 45, 0)
    old_pose = robot.pose
    print("looking for cubes!") 
    if len(cubes) == 1:
        print("found object")
        robot.set_lift_height(height = 0, accel = 6, max_speed = 500, duration = 1, in_parallel = False, num_retries = 3).wait_for_completed()
        robot.go_to_pose(cubes[0].pose,relative_to_robot=False).wait_for_completed()
        pickupObject(robot)
        robot.drive_wheels(-50,-50)
        time.sleep(3)
        robot.drive_wheels(0,0)
        robot.go_to_pose(old_pose,relative_to_robot=False).wait_for_completed()
        robot.set_lift_height(height = 0, accel = 6, max_speed = 500, duration = 1, in_parallel = False, num_retries = 3).wait_for_completed()
    else:
        print("Cannot locate custom box")


    while True:
        time.sleep(0.1)


cozmo.run_program(custom_objects)
