from PyQt5.QtCore import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

my_array = [['00','01','02'],
            ['10','11','12'],
            ['20','21','22']]

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())

class MyWindow(QtWidgets.QTableView):
    def __init__(self, *args):
        QtWidgets.QTableView.__init__(self, *args)

        tablemodel = MyTableModel(my_array, self)
        self.setModel(tablemodel)

class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        # vvvv this is the magic part
        elif role == Qt.BackgroundRole:
            if index.row() % 2 == 0:
                return QBrush(Qt.yellow)
            else:
                return QBrush(Qt.red)
        # ^^^^ this is the magic part
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

if __name__ == "__main__":
    main()