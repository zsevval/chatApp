from socket import *
import threading
import random
import pickle
import queue
from PyQt5.QtCore import QThread, QTimer
from PyQt5 import QtCore, QtGui, QtWidgets


class Server(QThread):

    def __init__(self, host, port, clientField, debugField):
        super(Server, self).__init__(parent=None)
        self.connections = []
        self.messageQueue = queue.Queue()
        self.host = host
        self.port = port
        self.clientField = clientField
        self.debugField = debugField

        # soket olustur
        self.serversock = socket(AF_INET, SOCK_STREAM)
        self.serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        self.timer = QTimer()
        self.timer.timeout.connect(self.sendMsgs)
        self.timer.start(500)

        try:
            self.port = int(self.port)
            self.serversock.bind((self.host, self.port))
        except Exception as e:
            print(e)
            self.port = int(self.port) + random.randint(1, 1000)
            self.serversock.bind((self.host, self.port))

        self.serversock.listen(5)

        debugMsg = "Server running on {} at port {}".format(
            self.host, self.port)
        self.debugField.addItem(debugMsg)
        print(debugMsg)

    def run(self):
        while True:
            self.clientsock, self.addr = self.serversock.accept()

            if self.clientsock:
                self.data = self.clientsock.recv(1024)
                self.nickname = pickle.loads(self.data)
                self.clientField.addItem(self.nickname)
                self.connections.append(
                    (self.nickname, self.clientsock, self.addr))
                threading.Thread(target=self.receiveMsg, args=(
                    self.clientsock, self.addr), daemon=True).start()

    def receiveMsg(self, sock, addr):
        length = len(self.connections)
        debugMsg = "{} is connected with {} on port {} ".format(
            self.connections[length-1][0], self.connections[length-1][2][0], self.connections[length-1][2][1])
        self.debugField.addItem(debugMsg)

        while True:
            try:
                self.data = sock.recv(1024)
            except:
                self.data = None

            if self.data:
                self.data = pickle.loads(self.data)

                # set the nickname and message
                self.messageQueue.put(self.data)

    def sendMsgs(self):
        while(not self.messageQueue.empty()):
            if not self.messageQueue.empty():
                self.message = self.messageQueue.get()
                self.message = pickle.dumps(self.message)
                if self.message:
                    for i in self.connections:
                        try:
                            i[1].send(self.message)
                        except:
                            debugMsg = "[ERROR] Sending message to " + \
                                str(i[0])
                            print(debugMsg)
                            self.debugField.addItem(debugMsg)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(350, 250)
        MainWindow.setMinimumSize(QtCore.QSize(350, 321))
        MainWindow.setMaximumSize(QtCore.QSize(350, 321))
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.start_stop_server = QtWidgets.QPushButton(self.centralwidget)
        self.start_stop_server.setGeometry(QtCore.QRect(1, 260, 348, 41))
        self.start_stop_server.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Server"))
        self.start_stop_server.setText(
            _translate("MainWindow", "Start Server"))


class Ui_Form_List(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(348, 185)
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(1, 41, 346, 135))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setSortingEnabled(True)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(150, 10, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.listWidget.setFont(font)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Clients"))

    def addClient(self, client):
        self.listWidget.addItem(client)


class Ui_Form_Setup(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(348, 191)
        self.lblPortNo = QtWidgets.QLabel(Form)
        self.lblPortNo.setGeometry(QtCore.QRect(20, 70, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblPortNo.setFont(font)
        self.lblPortNo.setObjectName("lblPortNo")
        self.portNoField = QtWidgets.QLineEdit(Form)
        self.portNoField.setGeometry(QtCore.QRect(140, 70, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.portNoField.setFont(font)
        self.portNoField.setObjectName("hostField_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(50, 20, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lblPortNo.setText(_translate("Form", "Port Number"))
        self.label.setText(_translate(
            "Form", "Leave fields empty for default values"))


class Ui_Form_Debug(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(348, 80)
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(1, 1, 346, 75))
        self.listWidget.setObjectName("listWidget")
        font = QtGui.QFont()
        font.setPointSize(9)
        self.listWidget.setFont(font)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

    def addDebugMsg(self, msg):
        self.listWidget.addItem(msg)
