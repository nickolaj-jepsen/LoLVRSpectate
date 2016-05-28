import openvr
import time
import math
from datetime import datetime
from LeagueOfLegends import LeagueOfLegends
from OpenVR import OpenVR, position_distance, position_average, Position, position_rotation

lol = LeagueOfLegends()
lol.fps = True
lol.minion_hp_bar = False
lol.clip_distance = 30000
lol.fov = 100

vr = OpenVR()

x_offset = -3000
y_offset = 7382.5
z_offset = 5000
yaw_offset = 0
previous_control_pos = None
scale = z_offset

counter = 0
timer = datetime.now()


def offset(previous, current, update_z=False):
    global x_offset
    global y_offset
    global z_offset
    global yaw_offset
    global scale

    theta = math.radians(-yaw_offset)
    cs = math.cos(theta)
    sn = math.sin(theta)
    if update_z:
        z_offset += (previous.z - current.z) * scale * 2

    x = (previous.x - current.x) * scale * 4
    y = (previous.y - current.y) * scale * 4

    x_offset += x*cs-y*sn
    y_offset += x*sn+y*cs

while True:
    scale = z_offset

    controller = vr.controllers()
    btns = [x.buttons() for x in controller]
    controller_pos = [x.position() for x in controller]

    if len(controller) == 2:
        if btns[0].trigger_button and btns[1].trigger_button:
            if previous_control_pos is None or isinstance(previous_control_pos, Position):
                previous_control_pos = controller_pos
            else:
                previous_distance = position_distance(previous_control_pos[0], previous_control_pos[1])
                distance = position_distance(controller_pos[0], controller_pos[1])

                previous_average = position_average(previous_control_pos[0], previous_control_pos[1])
                average = position_average(controller_pos[0], controller_pos[1])

                previous_rotation = (position_rotation(previous_control_pos[0], previous_control_pos[1]))
                rotation = (position_rotation(controller_pos[0], controller_pos[1]))

                yaw_offset += previous_rotation - rotation

                offset(previous_average, average)
                z_offset += (previous_distance - distance) * scale * 2

                previous_control_pos = controller_pos

        elif btns[0].trigger_button or btns[1].trigger_button:
            current_trigger = int(btns[1].trigger_button)

            if previous_control_pos is None:
                previous_control_pos = controller_pos
            else:
                print(previous_control_pos, controller_pos)
                offset(previous_control_pos[current_trigger], controller_pos[current_trigger])
                previous_control_pos = controller_pos
        else:
            previous_control_pos = None
    elif len(controller) == 1:
        if btns[0].trigger_button:
            if previous_control_pos is None or isinstance(previous_control_pos, list):
                previous_control_pos = controller_pos[0]
            else:
                offset(previous_control_pos, controller_pos[0], update_z=True)
                previous_control_pos = controller_pos[0]
        else:
            previous_control_pos = None

    pos = vr.hmd.position()

    lol.yaw = pos.yaw + yaw_offset
    lol.pitch = pos.pitch*-1
    lol.x = (pos.x*scale) + x_offset
    lol.y = (pos.y*scale) + y_offset
    lol.z = (pos.z*scale) + z_offset

    if timer.second < datetime.now().second:
        timer = datetime.now()
        print("tracking_fps: {0:03d}, controllers: {1:01d}".format(counter, len(controller)))
        counter = 0
    else:
        counter += 1

    time.sleep(0.005)

openvr.shutdown()
