import sys
import csv
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from design import Ui_MainWindow
from datetime import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_7.clicked.connect(self.open_table_window)
        self.ui.pushButton_4.clicked.connect(self.show_graph_all)
        self.ui.pushButton_3.clicked.connect(self.show_graph_next_month)
        self.canvas = None

    def open_table_window(self):
        table_window = TableWindow()
        table_window.load_data_from_csv("data_day.csv")
        table_window.exec_()

    def show_graph_all(self):
        dates = []
        temperatures = []

        with open("data/data_day.csv", "r", newline = "") as file:
            reader = csv.DictReader(file)
            for row in reader:
                date = datetime.strptime(row['datetime'], '%Y%m%dT%H%M')
                dates.append(date)
                temperatures.append(float(row['temperature']))

        # Создание графического холста Matplotlib
        if self.canvas is None:
            self.canvas = FigureCanvas(plt.Figure())
        else:
            self.canvas.close()
            self.canvas = FigureCanvas(plt.Figure())

        ax = self.canvas.figure.subplots()
        ax.plot(dates, temperatures, linestyle = '-')
        ax.set_xlabel('Дата')
        ax.set_ylabel('Температура')
        ax.set_title('Температура за 2 роки')
        ax.grid(True)
        self.canvas.draw()

    def show_graph_next_month(self):
        pass


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



#         self.scene = QtWidgets.QGraphicsScene()
#         self.graphicsView.setScene(self.scene)
#
#         self.figure = Figure()
#         self.axes = self.figure.gca()
#         self.axes.set_title("My Plot")
#
#     def graph(self):
#         x = [random.randrange(1, 100) for _ in range(10)]
#         y = [random.randrange(1, 100) for _ in range(10)]
#
#         self.axes.clear()
#         self.axes.plot(x, y, "-k", label = "График внутри виджета QGraphicsView")
#
#         self.axes.legend()
#         self.axes.grid(True)
#
#         self.canvas = FigureCanvas(self.figure)
#         self.proxy_widget = self.scene.addWidget(self.canvas)

