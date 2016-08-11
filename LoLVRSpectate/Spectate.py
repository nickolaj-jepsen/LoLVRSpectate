import logging
import math
import time
from datetime import datetime

from LoLVRSpectate.LeagueOfLegends import LeagueOfLegends
from LoLVRSpectate.OpenVR import OpenVR


class VRSpectate(object):
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
        self.prev_controller_frame = self.vr.controller_frame()
        self.scale = self.z_offset

    def _move_offset(self, previous, current, update_z=False):
        theta = math.radians(-self.yaw_offset)
        cs = math.cos(theta)
        sn = math.sin(theta)
        if update_z:
            self.z_offset += (previous.z - current.z) * self.scale * 2

        x = (previous.x - current.x) * self.scale * 4
        y = (previous.y - current.y) * self.scale * 4

        self.x_offset += x*cs-y*sn
        self.y_offset += x*sn+y*cs

    def _next_frame(self):
        self.scale = self.z_offset
        controller_frame = self.vr.controller_frame()

        # Camera movement
        if len(controller_frame) == 2:
            if all(controller_frame.button_pressed("trigger")):
                self.yaw_offset += self.prev_controller_frame.relative_rotation - controller_frame.relative_rotation
                self.z_offset += (self.prev_controller_frame.relative_distance - controller_frame.relative_distance) * self.z_offset * 2
                self._move_offset(self.prev_controller_frame.position(), controller_frame.position())
            elif any(controller_frame.button_pressed("trigger")):
                active_controller = [i for i, x in enumerate(controller_frame.button_pressed("trigger")) if x][0]
                self._move_offset(self.prev_controller_frame.position(active_controller), controller_frame.position(active_controller))
        if len(controller_frame) == 1:
            if any(controller_frame.button_pressed("trigger")):
                self._move_offset(self.prev_controller_frame.position(), controller_frame.position(), update_z=True)

        self.prev_controller_frame = controller_frame

        pos = self.vr.hmd.position()

        self.lol.yaw = pos.yaw + self.yaw_offset
        self.lol.pitch = pos.pitch*-1
        self.lol.x = (pos.x*self.scale) + self.x_offset
        self.lol.y = (pos.y*self.scale) + self.y_offset
        self.lol.z = (pos.z*self.scale) + self.z_offset

    def run(self):
        fps_counter = 0
        fps_timer = datetime.now()

        while True:
            self._next_frame()

            if int(fps_timer.timestamp()) < int(datetime.now().timestamp()):
                fps_timer = datetime.now()
                logging.info("tracking_fps: {0:03d}, controllers: {1:01d}".format(fps_counter,
                                                                                  len(self.prev_controller_frame)))
                fps_counter = 0
            else:
                fps_counter += 1

            time.sleep(0.005)
