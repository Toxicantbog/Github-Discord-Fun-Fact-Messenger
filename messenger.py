from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QLabel, QLineEdit
from PySide6.QtCore import QTimer
import requests, json, random, sys, os

#file_path = 'facts.json'



if hasattr(sys, '_MEIPASS'):
    file_path = os.path.join(sys._MEIPASS, 'facts.json')
else:
    file_path = os.path.join(os.path.dirname(__file__), 'facts.json'

with open(file_path, 'r', encoding='utf-8') as file:
    data = file.read()

facts = json.loads(data)

message_count = 0

class mainWindow(QWidget):
    def __init__(self):
        super(mainWindow, self).__init__()

        self.setWindowTitle("Discord Messenger")
        self.setFixedSize(650,150)

        self.label_1 = QLabel("URL:")
        self.type_1 = QLineEdit(self)

        self.label_2 = QLabel("Authorization:")
        self.type_2 = QLineEdit(self)

        self.label_3 = QLabel("Interval (seconds):")
        self.type_3 = QLineEdit(self)

        self.label_4 = QLabel()

        self.label_5 = QLabel("Message Count: 0")

        self.button = QPushButton("Start")
        self.button.setCheckable(True)
        self.button.toggled.connect(self.toggle)

        self.H_Layout_1 = QHBoxLayout()
        self.H_Layout_1.addWidget(self.label_1)
        self.H_Layout_1.addWidget(self.type_1)

        self.H_Layout_2 = QHBoxLayout()
        self.H_Layout_2.addWidget(self.label_2)
        self.H_Layout_2.addWidget(self.type_2)

        self.H_Layout_3 = QHBoxLayout()
        self.H_Layout_3.addWidget(self.label_3)
        self.H_Layout_3.addWidget(self.type_3)

        self.H_Layout_4 = QHBoxLayout()
        self.H_Layout_4.addWidget(self.label_4)
        self.H_Layout_4.addWidget(self.label_5)

        self.V_Layout = QVBoxLayout()
        self.V_Layout.addLayout(self.H_Layout_1)
        self.V_Layout.addLayout(self.H_Layout_2)
        self.V_Layout.addLayout(self.H_Layout_3)
        self.V_Layout.addWidget(self.button)
        self.V_Layout.addLayout(self.H_Layout_4)

        self.timer = QTimer()
        self.timer.timeout.connect(self.sendMessage)


        self.setLayout(self.V_Layout)


    def toggle(self, checked):
        if checked:
            interval = self.type_3.text()
            if interval.isdigit():
               self.timer.start(int(interval) * 1000)
               self.button.setText("Stop") 
            else: 
                self.label_3.setText("Invalid interval")
                self.button.setChecked(False)

        else:
            self.timer.stop()
            self.button.setText("Start")
            self.label_4.setText("Messages Stopped")


    def sendMessage(self):

        global message_count

        url = self.type_1.text()
        authorization = self.type_2.text()

        if url and authorization:

            headers = {
            "Authorization" : authorization
            }

            random_number = random.randint(0,2500)
            fact = facts["facts"][random_number]
            message = "Yo did you know that " + fact

            payload = {
            "content" : message
            }

            try:
                res = requests.post(url,payload, headers=headers)
                message_count += 1
                self.label_4.setText("Message Sent")
                self.label_5.setText("Message Count: " + str(message_count))
            except:
                self.label_4.setText("Message Failed To Send, check url or authorization")

        else:
            self.label_4.setText("Enter Valid Url and Authorication")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    app.exec()