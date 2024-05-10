import sys
import csv
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate
from design import Ui_MainWindow
from datetime import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import train


class PlotViewer(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(PlotViewer, self).__init__(parent)

        self.figure = plt.figure(figsize = (16, 5))
        self.figureCanvas = FigureCanvas(self.figure)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.figureCanvas)
        self.setLayout(layout)

    def PlotPredict(self, days):
        self.ax = self.figure.add_subplot()
        data = train.load_data('data/data_4_years.csv')
        regressorLSTM = train.load_model("modelLSTM.h5")
        X_train, y_train, X_test, y_test, scaler, test_data = train.prepare_data(data)
        forecast_data = train.forecast_temperature(days, regressorLSTM, X_test, scaler)
        train.plot_forecast(self.ax, days, data, forecast_data, test_data)

    def PlotAll(self):
        dates = []
        temperatures = []

        with open("./data/data_day.csv", "r", newline = "") as file:
            reader = csv.DictReader(file)
            for row in reader:
                date = datetime.strptime(row['datetime'], '%Y%m%dT%H%M')
                dates.append(date)
                temperatures.append(float(row['temperatureMean']))

        self.ax = self.figure.add_subplot()
        self.ax.plot(dates, temperatures, linestyle = '-')
        self.ax.set_xlabel('Дата')
        self.ax.set_ylabel('Температура')
        self.ax.set_title('Графік Температур')
        self.ax.grid(True)

        self.figureCanvas.show()


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_7.clicked.connect(self.open_table_window)
        self.ui.pushButton_4.clicked.connect(self.show_graph_all)
        self.ui.pushButton_3.clicked.connect(self.show_graph_predict)
        self.ui.pushButton_6.clicked.connect(self.show_graph_predict)

    def open_table_window(self):
        table_window = TableWindow()
        table_window.load_data_from_csv("./data/data_day.csv")
        table_window.exec_()

    def show_graph_all(self):
        self.plot_viewer = PlotViewer()
        self.plot_viewer.PlotAll()
        self.scene = QtWidgets.QGraphicsScene(self)
        self.ui.graphicsView.setScene(self.scene)
        self.scene.addWidget(self.plot_viewer)

    def show_graph_predict(self):
        days = self.ui.date_from.date().daysTo(self.ui.date_to.date())

        self.plot_viewer = PlotViewer()
        self.plot_viewer.PlotPredict(days)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.ui.graphicsView.setScene(self.scene)
        self.scene.addWidget(self.plot_viewer)


class TableWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Table Window")
        self.table_view = QtWidgets.QTableView()
        self.table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.table_view)
        self.setLayout(self.layout)

    def load_data_from_csv(self, filename):
        with open(filename, "r", newline = "") as file:
            reader = csv.reader(file)
            data = list(reader)
        self.set_data(data)

    def set_data(self, data):
        model = QtGui.QStandardItemModel()
        for row_number, row_data in enumerate(data):
            if row_number == 0:
                model.setHorizontalHeaderLabels(row_data)
            else:
                items = [QtGui.QStandardItem(field) for field in row_data]
                model.appendRow(items)
        self.table_view.setModel(model)


app = QtWidgets.QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
