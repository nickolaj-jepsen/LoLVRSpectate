import logging

import openvr
import time
import math
from datetime import datetime
from LeagueOfLegends import LeagueOfLegends
from OpenVR import OpenVR, position_distance, position_average, Position, position_rotation


class MainLogic():
    def __init__(self):

        self.lol = LeagueOfLegends()

        self.lol.fps = True
        self.lol.minion_hp_bar = False
        self.lol.clip_distance = 30000
        self.lol.fov = 100

        self.vr = OpenVR()

        self.x_offset = -3000
        self.y_offset = 7382.5
        self.z_offset = 5000
        self.yaw_offset = 0
        self.previous_control_pos = None
        self.scale = self.z_offset

        self.counter = 0
        self.timer = datetime.now()

    def offset(self, previous, current, update_z=False):
        theta = math.radians(-self.yaw_offset)
        cs = math.cos(theta)
        sn = math.sin(theta)
        if update_z:
            self.z_offset += (previous.z - current.z) * self.scale * 2

        x = (previous.x - current.x) * self.scale * 4
        y = (previous.y - current.y) * self.scale * 4

        self.x_offset += x*cs-y*sn
        self.y_offset += x*sn+y*cs

    def run(self):
        while True:
            scale = self.z_offset

            controller = self.vr.controllers()
            btns = [x.buttons() for x in controller]
            controller_pos = [x.position() for x in controller]

            if len(controller) == 2:
                if btns[0].trigger_button and btns[1].trigger_button:
                    if self.previous_control_pos is None or isinstance(self.previous_control_pos, Position):
                        self.previous_control_pos = controller_pos
                    else:
                        previous_distance = position_distance(self.previous_control_pos[0], self.previous_control_pos[1])
                        distance = position_distance(controller_pos[0], controller_pos[1])

                        previous_average = position_average(self.previous_control_pos[0], self.previous_control_pos[1])
                        average = position_average(controller_pos[0], controller_pos[1])

                        previous_rotation = (position_rotation(self.previous_control_pos[0], self.previous_control_pos[1]))
                        rotation = (position_rotation(controller_pos[0], controller_pos[1]))

                        self.yaw_offset += previous_rotation - rotation

                        self.offset(previous_average, average)
                        self.z_offset += (previous_distance - distance) * scale * 2

                        self.previous_control_pos = controller_pos

                elif btns[0].trigger_button or btns[1].trigger_button:
                    current_trigger = int(btns[1].trigger_button)

                    if self.previous_control_pos is None:
                        self.previous_control_pos = controller_pos
                    else:
                        self.offset(self.previous_control_pos[current_trigger], controller_pos[current_trigger])
                        self.previous_control_pos = controller_pos
                else:
                    self.previous_control_pos = None
            elif len(controller) == 1:
                if btns[0].trigger_button:
                    if self.previous_control_pos is None or isinstance(self.previous_control_pos, list):
                        self.previous_control_pos = controller_pos[0]
                    else:
                        self.offset(self.previous_control_pos, controller_pos[0], update_z=True)
                        self.previous_control_pos = controller_pos[0]
                else:
                    self.previous_control_pos = None

            pos = self.vr.hmd.position()

            self.lol.yaw = pos.yaw + self.yaw_offset
            self.lol.pitch = pos.pitch*-1
            self.lol.x = (pos.x*scale) + self.x_offset
            self.lol.y = (pos.y*scale) + self.y_offset
            self.lol.z = (pos.z*scale) + self.z_offset

            if int(self.timer.timestamp()) < int(datetime.now().timestamp()):
                self.timer = datetime.now()
                logging.info("tracking_fps: {0:03d}, controllers: {1:01d}".format(self.counter, len(controller)))
                self.counter = 0
            else:
                self.counter += 1

            time.sleep(0.005)
