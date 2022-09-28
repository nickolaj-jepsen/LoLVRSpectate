import math

import openvr

from LoLVRSpectate.utils import MWT


class UnsupportedAmountOfControllersError(Exception):
    pass


def position_distance(first, second):
    """
    Calculate the distance between two positions

    :param first: The first position
    :type first: Position
    :param second: The second position
    :type second: Position

    :return: The distance between the positions in meters
    :rtype: float
    """
    x = first.x - second.x
    y = first.y - second.y
    z = first.z - second.z
    return math.sqrt(x**2 + y**2 + z**2)


def position_rotation(first, second):
    """
    Calculate the relative rotation between two points

    :param first: The first position
    :type first: Position
    :param second: The second position
    :type second: Position

    :return: The relative rotation in degrees
    :rtype: float
    """
    x = first.x - second.x
    y = first.y - second.y
    return math.degrees(math.atan2(x, y))


def position_average(first, second):
    """
    Calculate the average position of two points

    :param first: The first position
    :type first: Position
    :param second: The second position
    :type second: Position

    :return: The average position of two points
    :rtype: Position
    """

    x = (first.x + second.x) / 2
    y = (first.y + second.y) / 2
    z = (first.z + second.z) / 2
    roll = (first.roll + second.roll) / 2
    yaw = (first.yaw + second.yaw) / 2
    pitch = (first.pitch + second.pitch) / 2
    return Position(x, y, z, roll, yaw, pitch)


class Position(object):
    def __init__(self, x, y, z, roll, yaw, pitch):
        """
        A representation of a point in a coordinate system

        :param x: float
        :param y: float
        :param z: float
        :param roll: float
        :param yaw: float
        :param pitch: float
        """
        self.x = x
        self.y = y
        self.z = z
        self.roll = roll
        self.yaw = yaw
        self.pitch = pitch

    @classmethod
    def from_matrix(cls, matrix):
        """
        Create a Position object from a matrix provided from the openvr sdk

        :param matrix: A rotation matrix provided by the openvr sdk
        :type matrix: list
        """
        x = matrix[2][3]
        y = -matrix[0][3]
        z = matrix[1][3]
        roll = math.atan2(matrix[1][1], matrix[1][0]) - (math.pi/2)
        yaw = math.degrees(math.atan2(matrix[0][2], matrix[2][2]))+180
        pitch = math.degrees(math.atan2(matrix[1][2], math.sqrt(matrix[1][1]**2 + matrix[1][0]**2)))
        return cls(x, y, z, roll, yaw, pitch)


class Buttons(object):
    def __init__(self, value):
        """
        A representation of the buttons of a Vive controller

        :param value: An integer provided by the openvr sdk
        """

        self.value = value
        self.trigger = value.rAxis[1]
        self.touchpad = value.rAxis[0]

        pressed_value = self.value.ulButtonPressed

        if pressed_value >= 8589934592:
            self.trigger_button = True
            pressed_value -= 8589934592
        else:
            self.trigger_button = False

        if pressed_value >= 4294967296:
            self.touchpad_button = True
            pressed_value -= 4294967296
        else:
            self.touchpad_button = False

        if pressed_value >= 4:
            self.grip_button = True
            pressed_value -= 4
        else:
            self.grip_button = False

        self.menu_button = pressed_value >= 2

    def __getitem__(self, item):
        """
        An attribute for finding the value of a button by string

        :param item: name of the button
        :type item: str
        :return: value of the button
        :rtype: bool
        """
        if item == "trigger":
            return self.trigger_button
        if item == "touchpad":
            return self.touchpad_button
        if item == "grip":
            return self.grip_button
        if item == "menu":
            return self.menu_button


class TrackedDevice(object):
    def __init__(self, vr=None):
        """
        A base object for all tracked openvr elements

        :param vr: An already initialised version of openvr, else create a new
        :type vr: openvr.IVRSystem
        """

        self.openvr = openvr.init(openvr.VRApplication_Utility) if vr is None else vr

    def position(self):
        """
        Get the position of the tracked device

        :return: the position of the tracked device
        :rtype: Position
        """
        poses = self.openvr.getDeviceToAbsoluteTrackingPose(
            openvr.TrackingUniverseStanding,
            0,
            openvr.k_unMaxTrackedDeviceCount
        )
        return Position.from_matrix(poses[self.device_id].mDeviceToAbsoluteTracking)


class HMD(TrackedDevice):
    def __init__(self, *args, **kwargs):
        """
        A representation of the  Head Mounted Display
        """
        super(HMD, self).__init__(*args, **kwargs)
        self.device_id = openvr.k_unTrackedDeviceIndex_Hmd


class Controller(TrackedDevice):
    def __init__(self, device_id, *args, **kwargs):
        """
        A representation of the Vive Controller

        :param device_id: the controller id
        :type device_id: int
        """
        self.device_id = device_id
        super(Controller, self).__init__(*args, **kwargs)

    def buttons(self):
        """
        Get the state of the controllers buttons

        :return: the state of the controllers buttons
        :rtype: Buttons
        """
        resp = self.openvr.getControllerState(self.device_id)
        if resp[0] != 1:
            raise ConnectionError
        return Buttons(resp[1])


class ControllersFrame(object):
    def __init__(self, controllers):
        """
        A static representation of the controllers at the point of time the objects creation

        :param controllers: list of controllers
        :type controllers: list
        """
        self.controllers_pos = [x.position() for x in controllers]
        self.buttons = [x.buttons() for x in controllers]
        self._len = len(self.controllers_pos)

    def __len__(self):
        return self._len

    def position(self, controller_id="all"):
        """
        Get the positional value of the controllers

        :param controller_id: either a integer representing which controller
        to use or "all" for the average of all controllers
        :type controller_id: int or str
        :return: the position of the selected controller(s)
        :rtype: Position
        """
        # Specify what controller_id you want pos from
        if controller_id == "all":
            if len(self) == 1:
                return self.controllers_pos[0]
            elif len(self) == 2:
                return position_average(self.controllers_pos[0], self.controllers_pos[1])
            else:
                raise UnsupportedAmountOfControllersError()
        elif type(controller_id) == int:
            return self.controllers_pos[controller_id]
        else:
            raise TypeError("controller_id needs to be an integer")

    @property
    def relative_rotation(self):
        """
        Get the relative rotation if the frame contains two controllers

        :return: The relative rotation in degrees
        :rtype: float
        """
        if len(self) == 2:
            return position_rotation(self.controllers_pos[0], self.controllers_pos[1])
        else:
            raise UnsupportedAmountOfControllersError()

    @property
    def relative_distance(self):
        """
        Get the distance between the controllers

        :return: The distance between the controllers in m
        :rtype: float
        """
        if len(self) == 2:
            return position_distance(self.controllers_pos[0], self.controllers_pos[1])
        else:
            raise UnsupportedAmountOfControllersError()

    def button_pressed(self, name):
        """
        Get that state of the controllers button by name

        :param name: name of the button to check
        :return: a list containing a boolean for each controller
        :rtype: list
        """
        return [x[name] for x in self.buttons]


class OpenVR(object):
    def __init__(self):
        """
        A representation of the openvr sdk
        """

        self.openvr = openvr.init(openvr.VRApplication_Overlay)
        self.hmd = HMD(vr=self.openvr)

    @MWT(timeout=1)
    def controllers(self):
        """
        Search for active controllers

        :return: list of active controllers
        :rtype: list
        """
        return [
            Controller(x)
            for x in range(openvr.k_unMaxTrackedDeviceCount)
            if self.openvr.getTrackedDeviceClass(x) == 2
            and self.openvr.getControllerState(x)[0] != 0
        ]

    def controller_frame(self):
        """
        Get a controller frame of the active controllers

        :return: the current controller frame
        :rtype: ControllersFrame
        """
        return ControllersFrame(self.controllers())
