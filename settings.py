# For GUI
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal

# My files
from _settingsForm import Ui_Settings

# Other
import sys
from json import load, dump

settingsPath = "./"
settingsFile = "settings.json"

def loadSettings():
    global settingsFile, settingsPath
    filepath = settingsPath + settingsFile
    with open(filepath, "r", encoding="utf-8") as fil:
        dictToReturn = load(fil)
    return dictToReturn

def dumpSettings(settingsDict):
    global settingsFile, settingsPath
    filepath = settingsPath + settingsFile
    with open(filepath, "w", encoding="utf-8") as fil:
        dump(settingsDict, fil)



class mySettingsWindow(QtWidgets.QMainWindow):
    sigSettingsSaved = pyqtSignal(bool)
    def __init__(self):
        super(mySettingsWindow, self).__init__()
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('img.png'))
        self.setWindowTitle("Cgpa Fantasy: Settings")
        
        # Variables
        self.isChanged = False
        try:
            self.settingsDict = loadSettings()
        except (Exception, OSError) as ex:
            self.errorMessage("Unable to read settings file", str(ex))

        # Set UI initial values
        self.setEnabledSpinBoxWindowHeight()
        self.ui.spinBoxWindowHeight.setValue(self.settingsDict["WinHei"])
        self.ui.radioRememberWinHei.setChecked(self.settingsDict["rememberWinHei"])
        self.ui.radioForceWinHei.setChecked(not (self.settingsDict["rememberWinHei"]) )

        # Dynamic Connections
        self.ui.btnSavePrefs.clicked.connect(self.onSavePrefsClick)

        self.ui.radioForceWinHei.clicked.connect(self.chooseForcedWinHei)
        self.ui.radioRememberWinHei.clicked.connect(self.chooseRememberWinhei)
        self.ui.spinBoxWindowHeight.valueChanged.connect(self.onSBoxCustWinHeiChanged)

        
    # Adopted from: https://stackoverflow.com/questions/45789084/show-messagebox-when-windows-x-close-button-is-pressed
    def closeEvent(self, event): 
        if not self.isChanged:
            event.accept()
        elif self.confirmationMsg("Closing application", "You made changes on settings and did not saved. If you quit now, all changes will be lost. Do you really want to quit?"):
            event.accept()
        else:
            event.ignore()

    def onSavePrefsClick(self):
        try:
            dumpSettings(self.settingsDict)
            self.isChanged = False
            self.sigSettingsSaved.emit(True)
        except (Exception, OSError) as ex:
            self.errorMessage("Unable to save settings to file", str(ex))      

    def setEnabledSpinBoxWindowHeight(self):
        self.ui.spinBoxWindowHeight.setEnabled(not (self.settingsDict["rememberWinHei"]) )

    def chooseForcedWinHei(self):
        self.settingsDict["rememberWinHei"] = 0
        self.setEnabledSpinBoxWindowHeight()
        self.isChanged = True
    
    def chooseRememberWinhei(self):
        self.settingsDict["rememberWinHei"] = 1
        self.setEnabledSpinBoxWindowHeight()
        self.isChanged = True

    def onSBoxCustWinHeiChanged(self):
        self.settingsDict["WinHei"] = self.ui.spinBoxWindowHeight.value()
        self.isChanged = True


    ###############################
    # Message boxes
    ###############################   
    
    def infoMessage(self, title="Info", text="Text text"):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setWindowIcon(QtGui.QIcon('img.png'))
        msg.setText(text)
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet("*{background-color: rgb(70, 70, 70);}\nQLabel{color: white;}\nQPushButton{color: white;}")
        msg.exec_()

    def errorMessage(self, title="Error", text="An error occured"):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setWindowIcon(QtGui.QIcon('img.png'))
        msg.setText(text)
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet("*{background-color: rgb(70, 70, 70);}\nQLabel{color: white;}\nQPushButton{color: white;}")
        msg.exec_()

    def confirmationMsg(self, title="Question", text="Are you sure doing xyz?"):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setWindowIcon(QtGui.QIcon('img.png'))
        msg.setText(text)
        msg.setStyleSheet("*{background-color: rgb(70, 70, 70);}\nQLabel{color: white;}\nQPushButton{color: white;}")
        answer = msg.question(self, title, text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return answer == QMessageBox.Yes


if __name__ == "__main__":
    def app():
        app = QtWidgets.QApplication(sys.argv)
        app.setStyle('Fusion')
        win = mySettingsWindow()
        # app.aboutToQuit.connect(win.onAboutToQuit)
        win.show()
        sys.exit(app.exec_())

    app()