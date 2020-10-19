from PyQt5.QtChart import QChartView, QChart, QSplineSeries, QValueAxis
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QBrush


class DynamicSpline(QChart):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._axies = []
        self._axies_flags = [False, False]

    def addPoints(self, name: str, array_x: list, array_y: list, color: QBrush):
        series = self.__createSeries(name, color)
        self.__fillSeries(series, array_x, array_y)
        self.__addAxis(series, min(array_x), max(array_x), 'x')
        self.__addAxis(series, min(array_y), max(array_y), 'y')

    def __createSeries(self, name, color):
        pen = QPen(color)
        pen.setWidth(3)
        series = QSplineSeries(self)
        series.setName(name)
        series.setPen(pen)
        self.addSeries(series)
        return series

    def __fillSeries(self, series: QSplineSeries, array_x: list, array_y: list):
        count = min(len(array_x), len(array_y))
        for i in range(count):
            series.append(array_x[i], array_y[i])

    def __addAxis(self, series: QSplineSeries, minimum: float, maximum: float, axis_type='x'):
        if axis_type == 'x':
            if len(self._axies) == 0:
                axis = QValueAxis()
                self.addAxis(axis, Qt.AlignBottom)
                axis.setMin(minimum * 0.9)
                axis.setMax(maximum * 1.1)
                self._axies.append(axis)
            else:
                axis = self._axies[0]
            series.attachAxis(axis)
        else:
            axis = QValueAxis()
            self.addAxis(axis, Qt.AlignRight if len(self._axies) >= 2 else Qt.AlignLeft)
            axis.setMin(minimum * 0.9)
            axis.setMax(maximum * 1.1)
            series.attachAxis(axis)
            self._axies.append(axis)
# def temp(x, y, xx, yy, xxx, yyy):
#     hbox: QHBoxLayout = vars.wnd_main.horizontalLayout
#     hbox.children().clear()
#     hbox.removeItem(hbox.itemAt(0))
#
#     # m_x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
#     # m_y = [x*x for x in m_x]
#
#     chart = NewChart.DynamicSpline()
#     chart.setTitle("Dynamic spline chart")
#     chart.legend().hide()
#     chart.addPoints('first', x, y, Qt.blue)
#     chart.addPoints('second', xx, yy, Qt.red)
#     chart.addPoints('third', xxx, yyy, Qt.green)
#     # chart.setAnimationOptions(QChart.AllAnimations)
#     view = QChartView(chart)
#     view.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
#     hbox.addWidget(view)
