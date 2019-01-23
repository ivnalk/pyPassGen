#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QPushButton, QMessageBox, QLineEdit, QWidget, QDesktopWidget
from PyQt5 import uic 
from PyQt5.QtGui import QIcon
import sys, os, shutil
from pathlib import Path
import subprocess

__author__    = 'Ivan Abascal'
__title__     = 'pyPassGen'
__copyright__ = 'Copyright 2019, Alkmx'
__license__   = 'GPL'
__version__   = '0.1'
__email__     = 'ivan@alk.mx'

if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
pathGUI = os.path.join( bundle_dir, 'ui/wndMain.ui' )

ventana = uic.loadUiType(pathGUI)[0]

class wndMain(QMainWindow, ventana):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        self.title   = __title__
        self.version = __version__
        self.setWindowTitle(self.title)
        self.center()

        self.tabs.setTabText(0, 'Generador')
        self.tabs.setTabText(1, 'Configuración')
        self.tabs.setTabText(2, 'Acerca de')
        
        self.btnSelArchivo.clicked.connect(self.seleccionarArchivo)
        self.txtFrase.textChanged.connect(self.on_escribirFrase)
        # self.txtArchivoTexto.clicked.connect(self.seleccionarArchivo)

        self.btnGenerarPass.clicked.connect(self.generarPass)
        self.sliderCuantas.valueChanged.connect(self.on_modifCuantas)
        self.sliderLargo.valueChanged.connect(self.on_modifLargo)

        self.cbxMayus.stateChanged.connect(self.on_modifCbx)
        self.cbxVocales.stateChanged.connect(self.on_modifCbx)
        self.cbxNumeros.stateChanged.connect(self.on_modifCbx)
        self.cbxSimbolos.stateChanged.connect(self.on_modifCbx)
        self.cbxAmbiguos.stateChanged.connect(self.on_modifCbx)

        self.cbxVer.stateChanged.connect(self.on_verFrase)

        # Defaults
        self._cuantas     = 20
        self._largo       = 8
        self._cbxMayus    = 1
        self._cbxVocales  = 1
        self._cbxNumeros  = 1
        self._cbxSimbolos = 0
        self._cbxAmbiguos = 1
        self._frase       = ""
        self._archivo     = ""

        self.cbxMayus.setChecked(self._cbxMayus)
        self.cbxVocales.setChecked(self._cbxVocales)
        self.cbxNumeros.setChecked(self._cbxNumeros)
        self.cbxSimbolos.setChecked(self._cbxSimbolos)
        self.cbxAmbiguos.setChecked(self._cbxAmbiguos)

        self.sliderCuantas.setValue(self._cuantas)
        self.sliderLargo.setValue(self._largo)

        self.preInicio()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def preInicio(self):
        try:
            checker = subprocess.call("pwgen")
        except OSError as e:
            errorMsg = QMessageBox()
            errorMsg.setIcon(QMessageBox.Critical)
            errorMsg.setText("No se puede iniciar el programa debido que no se encontró el binario de pwgen")
            errorMsg.setInformativeText("Verifica los detalles para mayor información")
            errorMsg.setWindowTitle("No se puede iniciar el programa")
            errorMsg.setDetailedText("Tienes que instalar primero pwgen:\n\n apt-get install pwgen \n\n dnf install pwgen\n\n ")
            showError = errorMsg.exec_()
            sys.exit(1)

    def on_modifCbx(self):
        cbxSender = self.sender()
        cbxObject = "_" + cbxSender.objectName()

        if cbxSender.isChecked():
            setattr(self, cbxObject, 1)
        else:
            setattr(self, cbxObject, 0)

    def on_modifCuantas(self):
        self._cuantas = str(self.sliderCuantas.value())
        self.lblQtyCuantas.setText(self._cuantas)

    def on_modifLargo(self):
        self._largo = str(self.sliderLargo.value())
        self.lblQtyLargo.setText(self._largo)
        
    def seleccionarArchivo(self):
        options                = QFileDialog.Options()
        archivoSeleccionado, _ = QFileDialog.getOpenFileNames(self)
        if archivoSeleccionado:
            self._archivo = archivoSeleccionado[0]

            self.txtArchivoTexto.setText(self._archivo)
            self.txtFrase.setEnabled(True)
            self.cbxVer.setEnabled(True)
            self.txtFrase.setFocus()

    def on_verFrase(self):
        if self.cbxVer.isChecked():
            echoMode = QLineEdit.Normal
        else:
            echoMode = QLineEdit.Password
        self.txtFrase.setEchoMode(echoMode)

    def on_escribirFrase(self):
        chars = len( self.txtFrase.text() )
        if chars > 0:
            self.btnGenerarPass.setEnabled(True)
            self._frase = self.txtFrase.text()
            self.cbxVer.setEnabled(True)
        else:
            self._frase = ""
            self.btnGenerarPass.setEnabled(False)

    def limpiarPass(self):
        self.lstPasswords.clear()

    def construirComando(self):
        cmd = "-"

        if self._cbxMayus:
            cmd = cmd + "c"
        else:
            cmd = cmd + "A"

        if self._cbxVocales == 0:
            cmd = cmd + "v"

        if self._cbxNumeros == 0:
            cmd = cmd + "0"

        if self._cbxSimbolos:
            cmd = cmd + "y"

        if self._cbxAmbiguos:
            cmd = cmd + "B"

        cmd = cmd + "H"

        return cmd

    def generarPass(self):
        if ' ' in self._frase:
            errorMsg = QMessageBox()
            errorMsg.setIcon(QMessageBox.Information)
            errorMsg.setText("La frase no puede contener espacios")
            errorMsg.setWindowTitle("Error")
            showError = errorMsg.exec_()

            self.txtFrase.setFocus()
        else:
            self.limpiarPass()
            self.lstPasswords.setEnabled(True)
            opts = self.construirComando()

            theCMD    = "pwgen " + opts + " " + self._archivo + "#" + self._frase + " " + self._largo + " " + self._cuantas
            
            passwords = subprocess.getoutput(theCMD)
            for password in passwords.split():
                self.lstPasswords.addItem(password)

app      = QApplication(sys.argv)
myWindow = wndMain(None)
myWindow.show()
app.exec_()