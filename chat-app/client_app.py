import sys
from PyQt5 import  QtWidgets
import client

import random


class main(QtWidgets.QMainWindow, client.Ui_MainWindow):
    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        self.setupUi(self)
        self.setupWidget = QtWidgets.QWidget(self)
        self.config = client.Ui_Form()
        self.config.setupUi(self.setupWidget)
        self.show()

        
        self.centralwidget.setHidden(True)

        # örnek hostname ve port numarasini ayarla
        self.hostname = "127.0.0.1"
        self.port = 8080
        self.nickname = "User " + str(random.randint(1, 1000))    

     
        self.config.nicknameField.returnPressed.connect(self.start)
        self.config.passwordField.returnPressed.connect(self.start)        
        self.config.connectButton.clicked.connect(self.start)           

    


    def start(self):
        
        
        if self.config.nicknameField.text() != "":
            # kullanici nickname girer ise girileni kabul et 
            self.nickname = self.config.nicknameField.text()
        if self.config.passwordField.text() != "":
            # kullanici  sifre girer ise girileni kabul et 
            self.password = self.config.passwordField.text()    

        self.setWindowTitle(self.nickname + "'s chat")      
        self.receivedMessages.append("Your nickname is " + self.nickname)       
        print("Nickname ----:", self.nickname)  
         
        print("Password ----:", self.password)      
        print("Hostname: ---:", self.hostname)     
        print("Port number -:", self.port)         

        
        
           
        self.client = client.Client(self.hostname, self.port, self.sendBtn, self.nickname,self.password, self.messageEdit, self.receivedMessages)
        
        self.client.start()
     
       
        self.setupWidget.setHidden(True)
       
        self.centralwidget.setVisible(True)

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = main()         
    sys.exit(app.exec())      

