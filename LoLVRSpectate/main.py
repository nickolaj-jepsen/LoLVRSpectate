import sys
import time
import pywintypes
import logging

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
            logging.exception(e)
            if "get pid from name" in str(e):
                self.error.emit("LoL client was not found")
            elif "ReadProcessMemory" in str(e):
                self.error.emit("Either the LoL client or this program is outdated")
            else:
                self.error.emit(str(e))
        except pywintypes.error as e:
            logging.exception(e)
            if "SetSecurityInfo" in str(e):
                self.error.emit("Unable to access the League of Legends client, you have to run LoLVRSpectate at the "
                                "same permissions level as the LoL client. \nEX. if the LoL client is running as admin "
                                "LoLVRSpectate also has to run as admin")
        except Exception as e:
            logging.exception(e)
            self.error.emit("Unknown error, please submit a bug report at https://github.com/Fire-Proof/LoLVRSpectate "
                            "(please include the LoLVRSpectate.log file)")


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
        self.spectate_started = False
        self.setupUi(self)

        self.lol_watcher = ProcessWatcher(b"League of Legends")
        self.lol_watcher.running.connect(self.lol_watcher_update, Qt.QueuedConnection)
        self.lol_watcher.start()

        self.vorpx_watcher = ProcessWatcher(b"vorpControl")
        self.vorpx_watcher.running.connect(self.vorpx_watcher_update, Qt.QueuedConnection)
        self.vorpx_watcher.start()

        self.pushButtonStart.clicked.connect(self.toggle_spectate)

    def toggle_spectate(self):
        if self.spectate_started:
            self.pushButtonStart.setText("Start")
            self.stop_spectate()
            self.spectate_started = False
        else:
            self.pushButtonStart.setText("Stop")
            self.start_spectate()
            self.spectate_started = True

    def start_spectate(self):
        if self.spectate is None:
            self.spectate = SpectateThread()
            self.spectate.error.connect(self.spectate_error, Qt.QueuedConnection)
        self.spectate.start()

    def stop_spectate(self):
        if self.spectate is not None:
            if self.spectate.isRunning():
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

    def closeEvent(self, event):
        # Stop Threads before exit
        logging.info("shutting down threads")
        self.stop_spectate()
        self.lol_watcher.terminate()
        self.vorpx_watcher.terminate()
        logging.info("terminating program")
        event.accept()


def start_app():
    app = QApplication(sys.argv)
    tray_icon = MainDialog()
    tray_icon.show()
    app.exec_()
