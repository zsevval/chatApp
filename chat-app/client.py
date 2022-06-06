from collections import UserString
import socket

import pickle
import sys
from PyQt5.QtCore import QThread
from PyQt5 import QtCore, QtGui, QtWidgets


class Client(QThread):
    def __init__(self, host, port, sendBtn, nickname, password, messageEdit, receivedMessage):
        super(Client, self).__init__(parent=None)

        self.receivedMessage = receivedMessage
        self.nickname = nickname
        self.port = port                # sunucuya baglanmak icin kullanilan port
        self.host = host                # sunucuya baglanmak icin kullanilan host adi
        self.messageEdit = messageEdit  # gonderilecek mesaj
        self.password = password

        self.message = ""

        # istemcinin calisip calismadigini gosteren bayrak
        self.running = True

        # gonder dügmesine tiklandiginda gonderme fonksiyonu cagrilir

        sendBtn.clicked.connect(self.send)

        self.messageEdit.returnPressed.connect(self.send)

        # client icin bir soket  olusturun
        self.clientsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # servera baglan

        try:
            self.clientsoc.connect((self.host, self.port))
            self.clientsoc.send(pickle.dumps(self.nickname))
            self.receivedMessage.append("Connected to server")
        except:
            print("Could not connect to server")
            self.stop()         # serverla baglantiyi kes
            sys.exit()

    def run(self):
        while self.running:
            self.receive()

   # sunucu tarafindan iletilen mesajlari alir
    def receive(self):
        while self.running:

            try:
                # sunucudan mesajlari  byte formatinda alir
                self.data = self.clientsoc.recv(1024)
                # byte formatindan phyton listesine cevirir
                # ilk index göndericinin nicknamei, ikinci index mesaj
                self.data = pickle.loads(self.data)

                if self.data:

                    print(str(self.data[0] + ": " + self.data[1]))

                    if self.data[0] != self.nickname:

                        self.receivedMessage.append(
                            str(self.data[0] + ": " + self.data[1]))
            except:

                print("Error receiving")
                self.stop()                    # serverla baglantiyi kes
                sys.exit()                     # programi durdur

    def send(self):
        # text alaninda olan mesaji al
        self.message = self.messageEdit.text()
        # mesaji konusma ekraninda gösterir
        self.receivedMessage.append("You: " + self.message)
        # text alanini temizler
        self.messageEdit.setText("")
        self.data = (self.nickname, self.message)
        # listeyi byte formatina cevirir
        self.data = pickle.dumps(self.data)

        try:
            self.clientsoc.send(self.data)          # servera mesaj gönderir
        except:
            print("Error sending message")

    # serverla baglantiyi kapatir
    def stop(self):
        self.running = False        # bayragi false olarak degistirir
        self.clientsoc.close()      # soketi kapatir


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(420, 315)
        Form.setMinimumSize(QtCore.QSize(420, 315))
        Form.setMaximumSize(QtCore.QSize(420, 315))
        self.connectButton = QtWidgets.QPushButton(Form)
        self.connectButton.setGeometry(QtCore.QRect(1, 278, 418, 34))
        self.connectButton.setObjectName("connectButton")
        self.InfoLabel = QtWidgets.QLabel(Form)
        self.InfoLabel.setGeometry(QtCore.QRect(90, 20, 251, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.InfoLabel.setFont(font)
        self.InfoLabel.setObjectName("InfoLabel")
        self.lblNickname = QtWidgets.QLabel(Form)
        self.lblNickname.setGeometry(QtCore.QRect(40, 89, 125, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblNickname.setFont(font)
        self.lblNickname.setObjectName("lblNickname")

        font = QtGui.QFont()
        font.setPointSize(14)

        self.nicknameField = QtWidgets.QLineEdit(Form)
        self.nicknameField.setGeometry(QtCore.QRect(180, 89, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nicknameField.setFont(font)
        self.nicknameField.setObjectName("nicknameField")

        font = QtGui.QFont()
        font.setPointSize(12)

        self.passwordField = QtWidgets.QLineEdit(Form)
        self.passwordField.setGeometry(QtCore.QRect(180, 200, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.passwordField.setFont(font)
        self.passwordField.setInputMethodHints(QtCore.Qt.ImhNone)
        self.passwordField.setObjectName("passwordField")
        self.lblPassword = QtWidgets.QLabel(Form)
        self.lblPassword.setGeometry(QtCore.QRect(40, 200, 125, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblPassword.setFont(font)
        self.lblPassword.setObjectName("lblPassword")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.connectButton.setText(_translate("Form", "Connect to Server"))
        self.InfoLabel.setText(_translate(
            "Form", "Leave fields empty for default values"))
        self.lblNickname.setText(_translate("Form", "Chat nickname"))
        self.lblPassword.setText(_translate("Form", "Password"))


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(423, 314)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.messageEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.messageEdit.setGeometry(QtCore.QRect(1, 200, 421, 74))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.messageEdit.setFont(font)
        self.messageEdit.setObjectName("messageEdit")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 180, 421, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.receivedMessages = QtWidgets.QTextBrowser(self.centralwidget)
        self.receivedMessages.setGeometry(QtCore.QRect(1, 2, 421, 181))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.receivedMessages.setFont(font)
        self.receivedMessages.setObjectName("receivedMessages")
        self.sendBtn = QtWidgets.QPushButton(self.centralwidget)
        self.sendBtn.setGeometry(QtCore.QRect(1, 280, 421, 31))
        self.sendBtn.setObjectName("sendBtn")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.nickname = ""
        self.password = ""
        self.port = 8080
        self.hostname = "127.0.0.1"

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Client"))
        self.sendBtn.setText(_translate("MainWindow", "Send"))
