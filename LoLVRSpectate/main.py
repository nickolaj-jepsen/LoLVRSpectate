import sys
import time

from PySide.QtCore import *
from PySide.QtGui import *

from LoLVRSpectate.Spectate import VRSpectate
from LoLVRSpectate.memorpy import Process
from LoLVRSpectate.memorpy.Process import ProcessException
from LoLVRSpectate.ui.main_dialog import Ui_MainDialog


class SpectateThread(QThread):
    error = Signal(str)

    def __init__(self):
        super(SpectateThread, self).__init__()
        self.spectate = None

    def run(self, *args, **kwargs):
        try:
            self.spectate = VRSpectate()
            self.spectate.run()
        except ProcessException as e:
            if "get pid from name" in str(e):
                self.error.emit("LoL client was not found")
            elif "ReadProcessMemory" in str(e):
                self.error.emit("Either the LoL client or this program is outdated")
            else:
                self.error.emit(str(e))


class ProcessWatcher(QThread):
    running = Signal(bool)

    def __init__(self, process_name):
        super(ProcessWatcher, self).__init__()
        self.process_name = process_name

    def run(self):
        while True:
            process = Process()
            if not process.process_from_name(self.process_name):
                self.running.emit(False)
            else:
                self.running.emit(True)
            time.sleep(2)


class MainDialog(QDialog, Ui_MainDialog):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)

        self.spectate = None
        self.setupUi(self)

        self.lol_watcher = ProcessWatcher(b"League of Legends")
        self.lol_watcher.running.connect(self.lol_watcher_update, Qt.QueuedConnection)
        self.lol_watcher.start()

        self.vorpx_watcher = ProcessWatcher(b"vorpControl")
        self.vorpx_watcher.running.connect(self.vorpx_watcher_update, Qt.QueuedConnection)
        self.vorpx_watcher.start()

        self.pushButtonStart.clicked.connect(self.start_spectate)

    def start_spectate(self):
        if self.spectate is None:
            self.spectate = SpectateThread()
            self.spectate.error.connect(self.spectate_error, Qt.QueuedConnection)
        self.spectate.start()

    def stop_spectate(self):
        if self.spectate is not None:
            self.spectate.terminate()

    def spectate_error(self, error):
        error_box = QMessageBox(self)
        error_box.setIcon(QMessageBox.Critical)
        error_box.setText(error)
        error_box.show()
        self.stop_spectate()

    @Slot(bool)
    def lol_watcher_update(self, running):
        if running:
            self.labelLoLRunning.setText("Running")
            self.labelLoLRunning.setStyleSheet("color: rgb(0, 135, 0)")
        else:
            self.labelLoLRunning.setText("Not Running")
            self.labelLoLRunning.setStyleSheet("color: rgb(255, 0, 0)")

    @Slot(bool)
    def vorpx_watcher_update(self, running):
        if running:
            self.labelVorpXRunning.setText("Running")
            self.labelVorpXRunning.setStyleSheet("color: rgb(0, 135, 0)")
        else:
            self.labelVorpXRunning.setText("Not Running")
            self.labelVorpXRunning.setStyleSheet("color: rgb(255, 0, 0)")


def start_app():
    app = QApplication(sys.argv)
    tray_icon = MainDialog()
    tray_icon.show()
    app.exec_()
