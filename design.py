from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(894, 574)
        MainWindow.setStyleSheet(
            "QWidget {\n"
            "    background-color: #e4e6b5;\n"
            "    color: #fff;\n"
            "}\n"
            "\n"
            "QLabel {\n"
            "    font-size: 18px;\n"
            "    background-color: rgba(255, 255, 255, 0.0);\n"
            "}\n"
            "\n"
            "QPushButton {\n"
            "    background-color: #bec18a;\n"
            "    color: #fff;\n"
            "    border: none;\n"
            "    padding: 8px 16px;\n"
            "    border-radius: 5px;\n"
            "}\n"
            "\n"
            "QPushButton:hover {\n"
            "    background-color: #b1b463;\n"
            "}\n"
            "")
        self.DateStyleSheet = """
        QDateEdit {
            background-color: #e4e6b5;
            border-radius: 5px;
            border: 2px solid #bec18a;
            padding-left: 10px;
            color: #fff;
        }

        QDateEdit:hover {
            border: 2px solid #b1b463;
        }

        QDateEdit::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 25px;
            background-position: center;
            background-repeat: no-repeat;
        }

        QDateEdit QAbstractItemView {
            color: #fff;
            background-color: #bec18a;
            selection-background-color: #b1b463;
        }

        #qt_calendar_prevmonth,
        #qt_calendar_nextmonth {
            border: none;
            font-weight: bold;
            qproperty-icon: none;
            background-color: #e4e6b5;
        }

        QCalendarWidget QWidget {
            alternate-background-color: #e4e6b5;
        }

        #qt_calendar_prevmonth {
            qproperty-text: "<";
        }
        #qt_calendar_nextmonth {
            qproperty-text: ">";
        }

        #qt_calendar_prevmonth:hover,
        #qt_calendar_nextmonth:hover {
            background-color: rgba(225, 225, 225, 1);
        }

        #qt_calendar_prevmonth:pressed,
        #qt_calendar_nextmonth:pressed {
            background-color: rgba(235, 235, 235, 1);
        }

        #qt_calendar_yearbutton,
        #qt_calendar_monthbutton {
            color: #fff;
            background-color: #e4e6b5;
            min-width: 85px;
            border-radius: 30px;
            margin: -1px -11px -1px -11px;
        }

        #qt_calendar_yearbutton:hover,
        #qt_calendar_monthbutton:hover {
            background-color: rgba(225, 225, 225, 1);
        }

        #qt_calendar_yearbutton:pressed,
        #qt_calendar_monthbutton:pressed {
            background-color: rgba(235, 235, 235, 1);
        }

        /* Поле ввода года */
        #qt_calendar_yearedit {
            color: #fff;
            background: transparent;
            min-width: 60px;
        }

        #qt_calendar_yearedit::up-button {
            color: #e4e6b5;
            width: 20px;
            subcontrol-position: right;
        }

        #qt_calendar_yearedit::down-button {
            color: #e4e6b5;
            width: 20px;
            subcontrol-position: left;
        }

        /* меню выбора месяца */
        CalendarWidget QToolButton QMenu {
            background-color: #bec18a;
        }

        CalendarWidget QToolButton QMenu::item {
            padding: 10px;
        }

        CalendarWidget QToolButton QMenu::item:selected:enabled {
            background-color: #b1b463;
        }

        #qt_calendar_calendarview {
            outline: 0px;
            selection-background-color: #ff79c6;
            color: #fff;
            border-radius: 5px;
        }
        """

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(230, 50, 651, 511))

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 231, 201))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("image/summer.png"))
        self.label.setScaledContents(True)

        self.label_date_from = QtWidgets.QLabel(self.centralwidget)
        self.label_date_from.setGeometry(QtCore.QRect(30, 360, 165, 30))
        self.label_date_from.setText("От")

        self.date_from = QtWidgets.QDateEdit(self.centralwidget)
        self.date_from.setGeometry(QtCore.QRect(30, 390, 165, 30))
        self.date_from.setCalendarPopup(True)
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate(2024, 4, 1))
        self.date_from.setDateRange(QDate(2024, 4, 1), QDate(2024, 7, 30))
        self.date_from.setStyleSheet(self.DateStyleSheet)

        self.label_date_to = QtWidgets.QLabel(self.centralwidget)
        self.label_date_to.setGeometry(QtCore.QRect(30, 420, 165, 30))
        self.label_date_to.setText("До")

        self.date_to = QtWidgets.QDateEdit(self.centralwidget)
        self.date_to.setGeometry(QtCore.QRect(30, 450, 165, 30))
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate(2024, 4, 2))
        self.date_to.setDateRange(QDate(2024, 4, 2), QDate(2024, 7, 31))
        self.date_to.setStyleSheet(self.DateStyleSheet)

        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(30, 490, 165, 30))
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(30, 530, 165, 30))
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(230, 10, 170, 35))
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(410, 10, 250, 35))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_6.setText(_translate("MainWindow", "Передбачити"))
        self.pushButton_7.setText(_translate("MainWindow", "Всі Дані"))
        self.pushButton_4.setText(_translate("MainWindow", "Весь Гріфік"))
        self.pushButton_3.setText(_translate("MainWindow", "Весь Графік с Передбаченням"))
