import sys
from PyQt5 import QtWidgets
import server

class main(QtWidgets.QMainWindow, server.Ui_MainWindow):
    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        self.setupUi(self)

        self.userInput = server.Ui_Form_Setup()
        self.client = server.Ui_Form_List()
        self.debug = server.Ui_Form_Debug()

        self.inputWidget = QtWidgets.QWidget(self)
        self.clientwidget = QtWidgets.QWidget(self)
        self.debugWidget = QtWidgets.QWidget(self)

        self.clientwidget.setGeometry(0, 0, 348, 200)
        self.debugWidget.setGeometry(0, 180, 348, 100)

        self.userInput.setupUi(self.inputWidget)
        self.client.setupUi(self.clientwidget)
        self.debug.setupUi(self.debugWidget)

        self.inputWidget.setVisible(True)
        self.clientwidget.setHidden(True)
        self.debugWidget.setHidden(True)

        # start ya da stop butonuna basilirsa
        self.start_stop_server.clicked.connect(self.start_stop)

        self.userInput.portNoField.returnPressed.connect(self.start_stop)

        self.show()

        # ornek hostname ve port numarasi ayarlanir
        self.hostname = "127.0.0.1"
        self.port = 8080

    def start_stop(self):
        # eger bir port numarasi girilirse onu kullanir
        # girilmez ise örnek deger atanir
        if self.userInput.portNoField.text() != "":
            self.port = self.userInput.portNoField.text()

        if self.start_stop_server.text() == "Start Server":
            self.start_stop_server.setText("Stop Server")
            self.clientwidget.setVisible(True)
            self.debugWidget.setVisible(True)
            self.inputWidget.setHidden(True)

            self.server = server.Server(
                self.hostname, self.port, self.client.listWidget, self.debug.listWidget)
            self.server.start()
        else:

            self.inputWidget.setVisible(True)
            self.debugWidget.setHidden(True)
            self.clientwidget.setHidden(True)
            self.start_stop_server.setText("Start Server")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = main()
    mainWindow.show()
    sys.exit(app.exec())
