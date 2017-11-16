#!/usr/bin/python3

#*********************************************************************************************************
#*   __     __               __     ______                __   __                      _______ _______   *
#*  |  |--.|  |.---.-..----.|  |--.|   __ \.---.-..-----.|  |_|  |--..-----..----.    |       |     __|  *
#*  |  _  ||  ||  _  ||  __||    < |    __/|  _  ||     ||   _|     ||  -__||   _|    |   -   |__     |  *
#*  |_____||__||___._||____||__|__||___|   |___._||__|__||____|__|__||_____||__|      |_______|_______|  *
#* http://www.blackpantheros.eu | http://www.blackpanther.hu - kbarcza[]blackpanther.hu * Charles Barcza *
#*************************************************************************************(c)2002-2016********

import sys, os, time
import gettext

from PyQt5.QtCore import Qt, QTimer, QObject, QMetaObject, QThread
from PyQt5.QtDBus import QDBusConnection
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QWidget, QDialog, QApplication


from argparse import ArgumentParser


import modules

from modules import window1

gettext.install("pydialog", "/usr/share/locale")

#class Thread(QThread):
#    def __init__(self):
#        QThread.__init__(self)
#
#    def run(self):
#        thread_func()

class ReturnClass():
    def __init__(self, value):
        self.value = value
    def __call__(self):
        sys.exit(self.value)

class MainWindow(QDialog, QThread, window1.Ui_PyDialog):
    def __init__(self, parent=None, arguments=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.ctimer = QTimer()
        #self.stimer = QTimer()

        self.null_extra_arg = False

        if arguments.title:
            self.setWindowTitle(arguments.title)
        if arguments.icon:
            icon = QIcon(arguments.icon)
            self.setWindowIcon(icon)
        if not arguments.progressbar:
            self.progressBar.hide()
        else:
            self.constant()
            self.ctimer.timeout.connect(self.constantUpdate)
            QMetaObject.connectSlotsByName(self)


        self.button_ids = ["details_button", "ok_button", "yes_button", "no_button", "continue_button", "cancel_button"]
        self.button_names = {
            "details_button":_("Details"), 
            "ok_button":_("Ok"), 
            "yes_button":_("Yes"), 
            "no_button":_("No"), 
            "continue_button":_("Continue"),
            "cancel_button":_("Cancel")
        }
        self.active_buttons = dict((e, False) for e in self.button_names)
        self.null_extra_arg = True

        if arguments.yesno or arguments.warningyesno:
            self.enable_buttons(["yes_button", "no_button"])
            if arguments.yesno:
                self.label.setText(arguments.yesno)
            else:
                self.label.setText(arguments.warningyesno)

        elif arguments.yesnocancel or arguments.warningyesnocancel:
            self.enable_buttons(["yes_button", "no_button", "cancel_button"])
            if arguments.yesnocancel:
                self.label.setText(arguments.yesnocancel)
            else:
                self.label.setText(arguments.warningyesnocancel)

        elif arguments.sorry or arguments.error or arguments.msgbox:
            self.enable_buttons(["ok_button"])
            if arguments.sorry:
                self.label.setText(arguments.sorry)
            elif arguments.error:
                self.label.setText(arguments.error)
            else:
                self.label.setText(arguments.msgbox)

        elif arguments.detailedsorry or arguments.detailederror:
            self.enable_buttons(["details_button", "ok_button"])
            if arguments.detailedsorry:
                self.label.setText(arguments.detailedsorry[0])
                self.details = arguments.detailedsorry[1]
            else:
                self.label.setText(arguments.detailederror[0])
                self.details = arguments.detailederror[1]

        elif arguments.warningcontinuecancel:
            self.enable_buttons(["continue_button", "cancel_button"])
            self.label.setText(arguments.warningcontinuecancel)
        
        elif arguments.progressbar:
            self.label.setText(arguments.progressbar[0])
            

        if not self.null_extra_arg:
            if not arguments.extra_arguments:
                sys.exit(_("There is no extra argument!"))

        self.create_buttons()

        if arguments.yeslabel and self.active_buttons["yes_button"]:
            self.buttons["yes_button"].setText(arguments.yeslabel)
        if arguments.nolabel and self.active_buttons["no_button"]:
            self.buttons["no_button"].setText(arguments.nolabel)
        if arguments.cancellabel and self.active_buttons["cancel_button"]:
            self.buttons["cancel_button"].setText(arguments.cancellabel)
        if arguments.continuelabel and self.active_buttons["continue_button"]:
            self.buttons["continue_button"].setText(arguments.continuelabel)

    def constant(self):
        self.ctimer.start(800)
    
    def constantUpdate(self):
        val = self.progressBar.value() + 15
        if val > 100:
                sys.exit()
                val = 0
        self.progressBar.setValue(val)

    def create_buttons(self):
        self.buttons = {}
        
        noab = len(list(filter(lambda x: self.active_buttons[x], self.active_buttons)))
        i = 0
        for button_id in self.button_ids:
            if self.active_buttons[button_id]:
                self.buttons[button_id] = QPushButton(self.button_names[button_id])
                self.horizontalLayout.addWidget(self.buttons[button_id])
                if button_id == "details_button":
                    noab -= 1
                    self.buttons["details_button"].clicked.connect(self.details_button_clicked)
                else:
                    if i < noab-1:
                        objname = button_id[:-7]
                        self.__dict__[objname] = ReturnClass(i)
                        self.buttons[button_id].clicked.connect(self.__dict__[objname])
                    else:
                       self.reject = ReturnClass(i)
                       self.buttons[button_id].clicked.connect(self.reject)
                    i += 1


    def enable_buttons (self, button_list):
        for button in button_list:
            self.active_buttons[button] = True
            
    def details_button_clicked (self):
        self.label.setText(self.label.text() + '\n\n' + self.details)
        self.buttons["details_button"].setDisabled(True)

        
#   This can stop the close event
#    def closeEvent(self, event):
#        event.ignore()


def call_parser():
    parser = ArgumentParser()

    parser.add_argument("--title", help=_("Dialog title"), metavar=_("<text>"))
    parser.add_argument("--yesnocancel", help=_("Question message box with yes/no/cancel buttons"))
    parser.add_argument("--yesno", help=_("Question message box with yes/no buttons"))

    parser.add_argument("--yes-label", help=_("The label of the yes-button"), dest="yeslabel", metavar=_("<text>"))
    parser.add_argument("--no-label", help=_("The label of the no-button"), dest="nolabel", metavar=_("<text>"))
    parser.add_argument("--cancel-label", help=_("The label of the cancel-button"), dest="cancellabel", metavar=_("<text>"))
    parser.add_argument("--continue-label", help=_("Use text as Continue button label"), dest="continuelabel", metavar=_("<text>"))

    # TODO: icons needed
    parser.add_argument("--sorry", help=_("Sorry message box"), metavar=_("<text>"))
    parser.add_argument("--warningyesno", metavar=_("<text>"), help=_("Warning message box with yes/no buttons"))
    parser.add_argument("--warningyesnocancel", metavar=_("<text>"), help=_("Warning message box with yes/no/cancel buttons"))
    parser.add_argument("--error", metavar=_("<text>"), help=_("'Error' message box"))
    parser.add_argument("--msgbox", metavar=_("<text>"), help=_("Message Box dialog"))

    # TODO: the return value is not compatible with the kdialog
    parser.add_argument("--detailedsorry", help=_("Sorry message box with expendable Details field"), nargs=2, metavar=_("<text> <details>")) 
    parser.add_argument("--warningcontinuecancel", metavar=_("<text>"), help=_("Warning message box with continue/cancel buttons"))
    parser.add_argument("--detailederror", metavar=_("<text> <details>"), help=_("'Error' message box with expandable Details field"), nargs=2)

    # TODO: Untested options below
    
    parser.add_argument("--icon", help=_("Use icon as the application icon."), dest="icon", metavar=_("<path>"))

    # TODO: Unfinished options below

    parser.add_argument("--progressbar", help=_("Progress bar dialog, returns a D-Bus reference for communication"), dest="progressbar", nargs="+", metavar=_("<text> [totalsteps]"))
#    parser.add_argument("--inputbox", metavar=_("<text> <init>"), help=_("Input Box dialog"), nargs=2)
#    parser.add_argument("--password", metavar=_("<text>"), help=_("Password dialog"))
#    parser.add_argument("--textbox", metavar=_("<file> [width] [height]"), help=_("Text Box dialog"), nargs='+')
#    parser.add_argument("--textinputbox", metavar=_("<text> <init> [width] [height]"), help=_("Text Input Box dialog"), nargs='+')
#    parser.add_argument("--combobox", metavar=_("<text> item [item] [item] ..."), help=_("ComboBox dialog"), nargs='+')
#    parser.add_argument("--menu", metavar=_("<text> [tag item] [tag item] ..."), help=_("Menu dialog"))
#    parser.add_argument("--checklist", metavar=_("<text> [tag item status] ..."), help=_("Check List dialog"))
#    parser.add_argument("--radiolist", metavar=_("<text> [tag item status] ..."), help=_("Radio List dialog"))
#    parser.add_argument("--passivepopup", metavar=_("<text> <timeout>"), help=_("Passive Popup"))
#    parser.add_argument("--getopenfilename", metavar=_("[startDir] [filter]"), help=_("File dialog to open an existing file"))
#    parser.add_argument("--getsavefilename", metavar=_("[startDir] [filter]"), help=_("File dialog to save a file"))
#    parser.add_argument("--getexistingdirectory", metavar=_("[startDir]"), help=_("File dialog to select an existing directory"))
#    parser.add_argument("--getopenurl", metavar=_("[startDir] [filter]"), help=_("File dialog to open an existing URL"))
#    parser.add_argument("--getsaveurl", metavar=_("[startDir] [filter]"), help=_("File dialog to save a URL"))
#    parser.add_argument("--geticon", metavar=_("[group] [context]"), help=_("Icon chooser dialog"))
#    parser.add_argument("--getcolor", help=_("Color dialog to select a color"))
#    parser.add_argument("--default", metavar=_("<text>"), help=_("Default entry to use for combobox, menu and color"))
#    parser.add_argument("--multiple", help=_("Allows the --getopenurl and --getopenfilename options to return multiple files"))
#    parser.add_argument("--separate-output", help=_("Return list items on separate lines (for checklist option and file open with --multiple)"))
#    parser.add_argument("--print-winid", help=_("Outputs the winId of each dialog"))
#    parser.add_argument("--dontagain", metavar=_("<file:entry>"), help=_("Config file and option name for saving the 'do-not-show/ask-again' state"))
#    parser.add_argument("--slider", metavar=_("<text> [minvalue] [maxvalue] [step]"), help=_("Slider dialog box, returns selected value"))
#    parser.add_argument("--calendar", metavar=_("<text>"), help=_("Calendar dialog box, returns selected date"))
#    parser.add_argument("--attach", metavar=_("<winid>"), help=_("Makes the dialog transient for an X app specified by winid"))

    parser.add_argument("extra_arguments", help=_("These depends from the used options"), nargs='*')

    return parser.parse_args()
    

if __name__ == '__main__':

    arguments = call_parser()
    app = QApplication(sys.argv) # NOTE: Be careful, the QApplication can remove from the sys.argv! Call the parse_args before it if you want to use everything.

    form = MainWindow(arguments=arguments)
    form.show()

    app.exec_()
