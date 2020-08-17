import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager
from mainUi import Ui_MainWindow
import json
class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.ui.pushButton_Search.clicked.connect(lambda: self.search(self.ui.lineEdit.text()))
        self.ui.pushButton_Next.clicked.connect(self.showNext)
        self.ui.pushButton_Prev.clicked.connect(self.showPrev)
        self.ui.actionAbout.triggered.connect(self.showAbout)
        self.ui.actionExit.triggered.connect(self.close)
    def search(self, query):

        dict_key="069cc3b0-be37-4c48-9d24-c5950099748b"
        
        url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/{}?key={}".format(query, dict_key)
        req = QNetworkRequest(QtCore.QUrl(url))

        self.nam = QNetworkAccessManager()
        self.nam.finished.connect(self.handleResponse)
        self.nam.get(req)


    def handleResponse(self, reply):
        self.my_list = []
        bytes_string = reply.readAll()
        result = json.loads(str(bytes_string, 'UTF-8'))
        if type(result[0]) == dict:
            for item in result:
                if item["shortdef"]:
                    for subitem in item["shortdef"]:
                        self.my_list.append(subitem)

            self.len_list = len(self.my_list) - 1
            self.index = 0
            self.ui.textEdit.setText(self.my_list[0])
        else:
            QtWidgets.QMessageBox.information(self, "Not Found!", "Please try another query")

    def showNext(self):
        if self.index >= self.len_list:
            self.index = 0
        else:
            self.index += 1
        self.ui.textEdit.setText(self.my_list[self.index])

    def showPrev(self):
        if self.index <= 0:
            self.index = self.len_list
        else:
            self.index -= 1
        self.ui.textEdit.setText(self.my_list[self.index])

    def showAbout(self):
        QtWidgets.QMessageBox.information(self, "About", """Powered by Merriam-Webster collegiate dictionary \nDeveloped by: Arian Sherafati
        
                                                            V 1.0
                                                            """)

    def closeEvent(self,e):
        r = QtWidgets.QMessageBox.question(self, "Exit?", "Are you sure you want to exit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if r ==QtWidgets.QMessageBox.Yes:
            e.accept()
        elif r == QtWidgets.QMessageBox.No:
            e.ignore()



app = QtWidgets.QApplication(sys.argv)
ex = Main()
sys.exit(app.exec_())