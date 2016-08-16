import logging

from LoLVRSpectate.memorpy.MemWorker import MemWorker


class LeagueOfLegends(object):
    def __init__(self):
        self.mw = MemWorker(b"League of Legends")

        cam_base_address = self._cam_base_addr

        self._y = self.mw.Address(int(cam_base_address + 12))
        self._x = self.mw.Address(int(cam_base_address + 20))
        self._z = self.mw.Address(int(cam_base_address + 16))
        self._pitch = self.mw.Address(int(cam_base_address + 64))
        self._yaw = self.mw.Address(int(cam_base_address + 60))
        self._fov = self.mw.Address(int(cam_base_address + 340))
        self._fps_toggle = self.mw.Address(int(cam_base_address + 616))

        self._clip_distance = self.mw.Address(self._base_addr + int("1195150", base=16))

        self._minion_hp_bar = self.mw.Address(int(cam_base_address + 92))

    @property
    def _base_addr(self):
        return self.mw.process.list_modules()[0].modBaseAddr

    @property
    def _cam_base_addr(self):
        # HOW TO: Find base addr
        # 1) Move screen to lowest y coord
        # 2) Scan for float = 520
        # 3) Move screen to highest y coord
        # 4) Scan for float = 14765
        # 5) Select the address that will updated the camera pos when changed
        # 6) Right click this address and click "find out what accesses this address"
        # 7) Select an element and press more information
        # 8) Copy the value which is listed at the end of the string "The value of the pointer needed to find this ..."
        # 9) Search for this this value as an 8-bit hex value
        # 10) Now search for the first address found
        # 11) You should now have found a "green" address, select this and double click the address
        # 12) You should now be able to see a string similar to "League of Legends.exe"+13D4280 <-- base addr

        addr = self._base_addr + int("13D4280", base=16)
        addr_1 = self.mw.Address(addr)
        logging.debug("Base address: " + str(addr))
        addr_2 = self.mw.Address(addr_1.read())
        return addr_2.read()

    @property
    def y(self):
        return self._y.read(type="float")

    @y.setter
    def y(self, val):
        self._y.write(val, type="float")

    @property
    def x(self):
        return self._x.read(type="float")

    @x.setter
    def x(self, val):
        self._x.write(val, type="float")

    @property
    def z(self):
        return self._z.read(type="float")

    @z.setter
    def z(self, val):
        self._z.write(val, type="float")

    @property
    def pitch(self):
        return self._pitch.read(type="float")

    @pitch.setter
    def pitch(self, val):
        self._pitch.write(val, type="float")

    @property
    def yaw(self):
        return self._yaw.read(type="float")

    @yaw.setter
    def yaw(self, val):
        self._yaw.write(val, type="float")

    @property
    def clip_distance(self):
        return self._clip_distance.read(type="float")

    @clip_distance.setter
    def clip_distance(self, val):
        self._clip_distance.write(val, type="float")

    @property
    def fps(self):
        return bool(self._fps_toggle.read(type="int"))

    @fps.setter
    def fps(self, val):
        self._fps_toggle.write(int(val), type="int")

    @property
    def fov(self):
        return self._fov.read(type="float")

    @fov.setter
    def fov(self, val):
        self._fov.write(val, type="float")

    @property
    def minion_hp_bar(self):
        return bool(self._minion_hp_bar.read(type="int"))

    @minion_hp_bar.setter
    def minion_hp_bar(self, val):
        if val:
            self._minion_hp_bar.write(0, type="int")
        else:
            self._minion_hp_bar.write(3, type="int")
