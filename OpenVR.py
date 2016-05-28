import openvr
import math
import functools

from utils import MWT


def position_distance(first, second):
    x = first.x - second.x
    y = first.y - second.y
    z = first.z - second.z
    return math.sqrt(x**2 + y**2 + z**2)


def position_rotation(first, second):
    x = first.x - second.x
    y = first.y - second.y
    return math.degrees(math.atan2(x, y))


def position_average(first, second):
    x = (first.x + second.x) / 2
    y = (first.y + second.y) / 2
    z = (first.z + second.z) / 2
    roll = (first.roll + second.roll) / 2
    yaw = (first.yaw + second.yaw) / 2
    pitch = (first.pitch + second.pitch) / 2
    return Position(x, y, z, roll, yaw, pitch)


class Position(object):
    def __init__(self, x, y, z, roll, yaw, pitch):
        self.x = x
        self.y = y
        self.z = z
        self.roll = roll
        self.yaw = yaw
        self.pitch = pitch

    @classmethod
    def from_matrix(cls, matrix):
        x = matrix[2][3]
        y = -matrix[0][3]
        z = matrix[1][3]
        roll = math.atan2(matrix[1][1], matrix[1][0]) - (math.pi/2)
        yaw = math.degrees(math.atan2(matrix[0][2], matrix[2][2]))+180
        pitch = math.degrees(math.atan2(matrix[1][2], math.sqrt(matrix[1][1]**2 + matrix[1][0]**2)))
        return cls(x, y, z, roll, yaw, pitch)


class Buttons(object):
    def __init__(self, value):
        self.value = value
        self.trigger = value.rAxis[1]
        self.touchpad = value.rAxis[0]

        pressed_value = self.value.ulButtonPressed

        if pressed_value - 8589934592 >= 0:
            self.trigger_button = True
            pressed_value -= 8589934592
        else:
            self.trigger_button = False

        if pressed_value - 4294967296 >= 0:
            self.touchpad_button = True
            pressed_value -= 4294967296
        else:
            self.touchpad_button = False

        if pressed_value - 4 >= 0:
            self.grip_button = True
            pressed_value -= 4
        else:
            self.grip_button = False

        if pressed_value - 2 >= 0:
            self.menu_button = True
        else:
            self.menu_button = False


class TrackedDevice(object):
    def __init__(self, vr=None):
        if vr is None:
            self.openvr = openvr.init(openvr.VRApplication_Utility)
        else:
            self.openvr = vr

    def position(self):
        poses = self.openvr.getDeviceToAbsoluteTrackingPose(
            openvr.TrackingUniverseStanding,
            0,
            openvr.k_unMaxTrackedDeviceCount
        )
        return Position.from_matrix(poses[self.device_id].mDeviceToAbsoluteTracking)


class HMD(TrackedDevice):
    def __init__(self, *args, **kwargs):
        super(HMD, self).__init__(*args, **kwargs)
        self.device_id = openvr.k_unTrackedDeviceIndex_Hmd


class Controller(TrackedDevice):
    def __init__(self, device_id, *args, **kwargs):
        self.device_id = device_id
        super(Controller, self).__init__(*args, **kwargs)

    def buttons(self):
        resp = self.openvr.getControllerState(self.device_id)
        if resp[0] != 1:
            raise ConnectionError
        return Buttons(resp[1])


class OpenVR(object):
    def __init__(self):
        self.openvr = openvr.init(openvr.VRApplication_Overlay)
        self.hmd = HMD(vr=self.openvr)

    @MWT(timeout=1)
    def controllers(self):
        val = []
        for x in range(0, openvr.k_unMaxTrackedDeviceCount):
            if self.openvr.getTrackedDeviceClass(x) == 2 and self.openvr.getControllerState(x)[0] != 0:
                val.append(Controller(x))
        return val

if __name__ == "__main__":
    import time
    vr = OpenVR()
    while True:
        btns = vr.controllers[0].buttons()
        print(btns.trigger_button, btns.touchpad_button, btns.grip_button, btns.menu_button)
        time.sleep(0.5)