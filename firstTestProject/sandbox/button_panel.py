from qtpy.QtWidgets import QPushButton, QWidget, QApplication, QGridLayout, QComboBox, QLineEdit

import sys


class buttonwidget(QWidget):

    def __init__(self):
        # how connect
        super(buttonwidget, self).__init__()
        self.grid = QGridLayout()
        self.btnConnect = QPushButton("Connect")
        self.grid.addWidget(self.btnConnect, 0, 0, 1, 5)

        self.btnLock = QPushButton("Lock Cassette")
        self.grid.addWidget(self.btnLock, 1, 0, 1, 5)

        self.btnPurge = QPushButton("Purge")
        self.grid.addWidget(self.btnPurge, 2, 0, 1, 2)

        self.cbxPurgeType = QComboBox()
        self.cbxPurgeType.addItems(["Normal", "Extended", "Add Conditioner", "Custom"])
        self.grid.addWidget(self.cbxPurgeType, 2, 2, 1, 2)

        self.txtNumPurge = QLineEdit()
        self.grid.addWidget(self.txtNumPurge, 2, 4, 1, 1)

        self.btnRecover = QPushButton("Recover")
        self.grid.addWidget(self.btnRecover, 3, 0, 1, 5)

        self.btnHelp = QPushButton("Help")
        self.grid.addWidget(self.btnHelp, 4, 0, 1, 5)

        self.setLayout(self.grid)

    def updateButtonText(self):
        print('updating text')

    def EnableDisableButtons(self):
        print('enabeling,disabeling buttons')

app = QApplication(sys.argv)
win = buttonwidget()
win.setGeometry(100, 100, 200, 100)
win.setWindowTitle("PyQt")
win.show()
sys.exit(app.exec_())

