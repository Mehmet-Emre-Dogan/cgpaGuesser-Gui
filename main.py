# My files
from _myGui import Ui_MainWindow
from myRow import row
from settings import mySettingsWindow, loadSettings, dumpSettings

# For GUI
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QVBoxLayout, QGroupBox #, QHBoxLayout, QFormLayout, QPushButton, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore 
from PyQt5 import QtGui 
import sys

# Other libraries
import datetime
from json import load, dump
import os
from pkg_resources import parse_version # Sorting function similar enough to natural sort algorithm
from collections import Counter

DEBUG = False
guessPath = "./guesses/"

#####################################
# QSS styles

whiteLabelSheet = "color:white; text-decoration: none; font-weight: normel;"
redLabelSheet = "/*color:red;*/  text-decoration: underline; font-weight: bold;"
# I commented color red because it looked bad. However I won't change variable name

#####################################



class myWindow(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self):
        super(myWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('img.png'))
        self.setWindowTitle("Cgpa Fantasy")

        self.groupBoxRows = QGroupBox("")
        self.layoutForGBR = QVBoxLayout()
        self.groupBoxRows.setStyleSheet("QGroupBox {border: none;}")

        self.initSettings()
        self.addMyRowsToScroll(firstRun=True)

        self.rowArr = []
        self.loadCbox()

        # Variables
        self.isChanged = False

        # Handle dynamic things 
        self.ui.btnAddRow.clicked.connect(self.onAddRowClicked)
        self.ui.btnCalculate.clicked.connect(self.calculateCgpaAutoForced)
        self.ui.btnSaveas.clicked.connect(self.saveAs)
        self.ui.btnSave.clicked.connect(self.save)
        self.ui.btnRefresh.clicked.connect(self.refresh)
        self.ui.btnDelete.clicked.connect(self.delete)
        self.ui.comboBoxGuesses.activated.connect(self.onCBoxActivated)
        self.ui.btnRename.clicked.connect(self.rename)
        self.resized.connect(self.onResize)

        # Menu bar connection: please see sources:
        # https://stackoverflow.com/questions/46082666/pyqt5-toolbar-onclick-function
        # https://zetcode.com/gui/pyqt5/menustoolbars/

        self.ui.menubar.triggered.connect(self.whoGotSelected)


    """Impotant events"""

    # Adopted from: https://stackoverflow.com/questions/45789084/show-messagebox-when-windows-x-close-button-is-pressed
    def closeEvent(self, event): 
        if not self.isChanged:
            event.accept()
        elif self.confirmationMsg("Closing application", "You made changes on current guess and did not saved. If you quit now, all changes will be lost. Do you really want to quit?"):
            event.accept()
        else:
            event.ignore()

    # Copied from: https://stackoverflow.com/questions/43126721/detect-resizing-in-widget-window-resized-signal
    def resizeEvent(self, event):
        self.resized.emit()
        return super(myWindow, self).resizeEvent(event)
    
    
    """Unclassificied functions"""

    # Menu bar selection 
    def whoGotSelected(self, selection):
        txt = selection.text()
        if DEBUG:
            print(f"Selection from menubar: {txt}")
        
        if txt == "See help":
            self.showHelp()
        elif txt == "Settings":
            self.setSettings()


    # See the link below if you want to learn more about launching new window from main window:
    # https://stackoverflow.com/questions/53225320/open-a-new-window-when-the-button-is-clicked-pyqt5/53225726
    def setSettings(self):
        self.settingsWindow = mySettingsWindow()
        self.settingsWindow.show()
        self.settingsWindow.sigSettingsSaved.connect(self.initSettings)

    def initSettings(self):
        self.settingsDict = loadSettings()
        self.resize(self.width(), self.settingsDict["WinHei"])

    def showHelp(self):
        os.system('start https://github.com/Mehmet-Emre-Dogan/cgpaGuesser-Gui/blob/main/README.md')    

    # Do stuff when window is resized.
    def onResize(self):
        winhei = self.height()
        newHeightSA = winhei - 100
        newHeightGB = winhei - 70
        self.ui.scrollArea.setFixedHeight(newHeightSA)
        self.ui.groupBoxCourses.resize(self.ui.groupBoxCourses.width(), newHeightGB)
        if DEBUG:
            print(f"Window height: {self.height()}")

        if self.settingsDict["rememberWinHei"]:
            self.settingsDict["WinHei"] = winhei
            dumpSettings(self.settingsDict)


    # Run a script when user closes app. It may be needed in future. Keep it as a template now.
    # For example, a goodbye message could be shown via this.
    def onAboutToQuit(self):
        pass


    """Classified functions"""
  
    ###############################
    # Row operations
    ###############################

    def clearCurrentRows(self):
        layout = self.layoutForGBR
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().deleteLater()
        self.rowArr.clear()
        self.ui.labelResult.setText("a.bcd")
        self.ui.labelResult.setStyleSheet(whiteLabelSheet)

    def loadRows(self):
        filename = self.ui.comboBoxGuesses.currentText()
        if filename == "Make New Guess":
            return
        else:
            pass
        filePath = guessPath + filename

        self.clearCurrentRows()

        with open(filePath, "r", encoding="utf-8") as fil:
            savedDict = load(fil)
        for i, courseRow in enumerate(savedDict["data"]):
            self.addExistingRow(courseName=courseRow["courseName"], credit=courseRow["credit"], letter=courseRow["letter"],
            grade=courseRow["grade"], weight=courseRow["weight"])
        
        self.isChanged = False
        self.calculateCgpaAuto()

    def addMyRowsToScroll(self, firstRun=False):
        if not firstRun:
            self.layoutForGBR.addWidget(self.rowArr[-1])
            self.rowArr[-1].rowUpdated.connect(self.onRowUpdated)

        self.groupBoxRows.setLayout(self.layoutForGBR)
        self.ui.scrollArea.setWidget(self.groupBoxRows)
        self.ui.scrollArea.setWidgetResizable(True)
        # self.ui.scrollArea.setFixedHeight(400) I will use it later to resize scroll area. Do not delete.

    def onAddRowClicked(self):
        self.rowArr.append(row(rowArray=self.rowArr))
        self.addMyRowsToScroll(firstRun=False)
        self.isChanged = True
        
    def addExistingRow(self, courseName, credit, letter, grade, weight):
        self.rowArr.append(row(rowArray=self.rowArr, courseName=courseName, credit=credit, letter=letter, grade=grade, weight=weight))
        self.addMyRowsToScroll(firstRun=False)

    def findDuplicates(self):
        courses = list( [ row.courseName for row in self.rowArr ] )
        ctr = Counter(courses) # Returns a dict: { array element : count }
        return list( [ courseName for courseName in ctr if ctr[courseName]>1 ] )

    def checkDuplicates(self):
        duplicates = self.findDuplicates()
        if DEBUG:
            print(f"Duplicates: {duplicates}")
        if len(duplicates) == 0:
            return True # Can continue to run
        else:
            self.errorMessage("Duplicates", f"Duplicating courses found: {', '.join(duplicates)}")
            return False # Cannot run
    

    ###############################
    # Dynamic row operations
    ###############################

    def onRowUpdated(self):
        self.calculateCgpaAuto()
        self.isChanged = True


    ###############################
    # Combobox operations
    ###############################

    def onCBoxActivated(self):
        self.setBtnEnsOnGueCboxChange()
        if not self.isChanged:
            self.loadRows()
        elif self.confirmationMsg("Confirm", "You made changes on current guess and did not saved. If you continue this operation, all changes will be lost. Do you really want to continue?"):
            self.loadRows()

        if self.ui.comboBoxGuesses.currentText() == "Make New Guess":
            self.clearCurrentRows()

    def loadCbox(self, selectedText="Make New Guess"):
        self.ui.comboBoxGuesses.clear() 
        files = os.listdir(guessPath)
        files.sort(key=parse_version, reverse=True)
        files.insert(0, "Make New Guess")
        self.ui.comboBoxGuesses.addItems(files)
        self.ui.comboBoxGuesses.setCurrentIndex(files.index(selectedText))
        self.setBtnEnsOnGueCboxChange()
        
    def setBtnEnsOnGueCboxChange(self):
        # set whether buttons enabled or not when the guess combobox index changes
        self.ui.btnRename.setEnabled( self.ui.comboBoxGuesses.currentText() != "Make New Guess" )
        self.ui.btnDelete.setEnabled( self.ui.comboBoxGuesses.currentText() != "Make New Guess" )
        self.ui.btnSave.setEnabled( self.ui.comboBoxGuesses.currentText() != "Make New Guess" ) 


    ###############################
    # File operations
    ###############################

    def rename(self):
        oldName = self.ui.comboBoxGuesses.currentText()
        oldPath = guessPath + oldName
        files = os.listdir(guessPath)
        if oldName in files: # if the combobox's line edit is edited, oldname will not be in list
            files.remove(oldName)
        
        newName = self.inputDialog("Rename", f"Please enter new name for {oldName}")
        if newName == "":
            self.errorMessage("Info", "Please enter a valid filename.")
            return
        elif newName == None:
            self.infoMessage("Info", "Renaming operation cancelled")
            return

        newName += ".json"
        newPath = guessPath + newName
        
        try:
            if newName in files:
                self.errorMessage("Error", "This filename already exists in directory. Try another")
            else:
                os.rename(oldPath, newPath)
                self.refresh(newName)
                
        except (OSError, TypeError) as ose:
            self.errorMessage("Cannot rename", str(ose))


    def delete(self):
        filename = self.ui.comboBoxGuesses.currentText()
        filePath = guessPath + filename
        fileAbsPath = os.path.abspath(filePath)
        try:
            if self.confirmationMsg("Deleting guess", f"Are you sure to delete :\n{fileAbsPath}\nMoreover, current changes also be destroyed."):
                os.remove(fileAbsPath)
                self.infoMessage("Success", "Selected guess deleted successfully")
                self.loadCbox()
                self.clearCurrentRows()
            else:
                self.infoMessage("Information", f"File not deleted:\n{fileAbsPath}")
                self.loadCbox(filename)
        except (Exception, OSError, FileNotFoundError) as ex:
            self.errorMessage("An error occured", str(ex))
        
    def refresh(self, txt=None):
        try:
            if txt:
                self.loadCbox(txt)
            else:
                self.loadCbox(self.ui.comboBoxGuesses.currentText())
        except:
            self.loadCbox()

    
    def saver(self, saveas=True):
        if self.checkDuplicates():
            try:
                customDT = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
                if saveas:
                    filename = "Guess_" + customDT + ".json"
                    filePath = guessPath + filename
                else:
                    filename = self.ui.comboBoxGuesses.currentText()
                    filePath = guessPath + filename

                    if self.confirmationMsg("Question", f"Are you sure to overwrite to existing file: {filePath}"):
                        pass
                    else:
                        return
                
                dumpArr = [] # Array to store values I am about to dump
                for row in self.rowArr:
                    rowdict = {"courseName": row.courseName,
                                "credit": row.credit,
                                "letter": row.letter,
                                "grade": row.grade,
                                "weight": row.weight
                                }
                    dumpArr.append(rowdict)


                dictToDump = { "data" : dumpArr, "date": customDT}
                with open(filePath, "w", encoding="utf-8") as fil:
                    dump(dictToDump, fil) 
            
            except OSError as ose:
                self.errorMessage("Unable to save", f"An error occured: {ose}")
            else:
                self.infoMessage("Success", f"Guess saved to {filePath}")
                self.loadCbox(filename)
                self.isChanged = False
        else:
            pass

    def saveAs(self):
        self.saver(saveas=True)

    def save(self): # Overwrite exising file. So, contrary to conventions, you cannot SAVE a freshly created file; according to my syntax.
        self.saver(saveas=False)

    
    ###############################
    # Calculators
    ###############################

    def calculateCgpaAuto(self):
        cres = 0
        weis = 0
        for row in self.rowArr:
            if DEBUG:
                print(f"Name: {row.courseName}  Weight: {row.weight}")
            
            cres += row.credit
            weis += row.weight

        if cres: # if cre is differen than zero
            cgpa = str(round(weis/cres, 3))
        else:
            cgpa = "Err"

        self.ui.labelResult.setText(cgpa)
        self.ui.labelResult.setStyleSheet(whiteLabelSheet)   
        return cgpa

    def calculateCgpaAutoForced(self):
        if "Err" == self.calculateCgpaAuto():
            self.errorMessage("Division by zero!", "Your weight sum is 0")
        self.ui.labelResult.setStyleSheet(redLabelSheet)
            

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

    def inputDialog(self, title="Input", text="Please enter value..."):
        inputDia = QInputDialog()
        inputDia.setStyleSheet("*{background-color: rgb(70, 70, 70);}\nQLabel{color: white;}\nQPushButton{color: white;}")
        txt, ok = inputDia.getText(self, title, text)
        if ok:
            return txt
        else:
            return None




def app():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    win = myWindow()
    # app.aboutToQuit.connect(win.onAboutToQuit)
    win.show()
    sys.exit(app.exec_())

app()