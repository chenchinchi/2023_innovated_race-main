from PyQt5 import QtWidgets
from controller2 import main_page_controller
import multiprocessing
import os



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = main_page_controller()
    window.show()
    sys.exit(app.exec_())