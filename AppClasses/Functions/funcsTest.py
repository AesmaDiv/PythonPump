from PyQt5.QtCore import QPoint, QPointF, Qt
from PyQt5.QtGui import QPen

from AesmaLib import AesmaFuncs, Journal
from AesmaLib.GraphWidget.Chart import Chart
from AppClasses.Functions import funcsTable, funcsGraph
import vars


is_logged = True
is_test_running = False
__ENGIGE_MSG = {False: 'ЗАПУСК ДВИГАТЕЛЯ', True: 'ОСТАНОВКА ДВИГАТЕЛЯ'}


def switch_test_running_state():
    if is_logged: Journal.log(__name__, "\tswitching test running state to", str(is_test_running))
    vars.wnd_main.btnTest.setText(__ENGIGE_MSG[is_test_running])
    vars.wnd_main.btnGoBack.setEnabled(not is_test_running)


def switch_charts_visibility():
    vars.graph_info.setVisibileCharts(['lift', 'power', 'test_lift', 'test_power'] if is_test_running else 'all')
    funcsGraph.display_charts(vars.markers)


def move_markers():
    flow, lift, power = get_flow_lift_power()
    vars.markers.moveMarker(QPointF(flow, lift), 'test_lift')
    vars.markers.moveMarker(QPointF(flow, power), 'test_power')


def add_point_to_list():
    flow, lift, power = get_flow_lift_power()
    data = {'flow': flow, 'lift': lift, 'power': power}
    if is_logged: Journal.log(__name__, "\tadding point to list", data)
    funcsTable.add_row(vars.wnd_main.tablePoints, data)
    pass


def remove_last_point_from_list():
    if is_logged: Journal.log(__name__, "\tremoving last point from list")
    funcsTable.remove_last_row(vars.wnd_main.tablePoints)


def clear_points_from_list():
    if is_logged: Journal.log(__name__, "\tclearing points from list")
    funcsTable.clear_table(vars.wnd_main.tablePoints)


def add_points_to_charts():
    flow, lift, power = get_flow_lift_power()
    add_point_to_chart('test_lift', flow, lift)
    add_point_to_chart('test_power', flow, power)


def add_point_to_chart(chart_name: str, value_x: float, value_y: float):
    chart: Chart = vars.graph_info.getChart(chart_name)
    if chart is not None:
        print(__name__, '\t adding point to chart', value_x, value_y)
        point = QPointF(value_x, value_y)
        chart.addPoint(point)
    else:
        print(__name__, '\tError: no such chart', chart_name)
        ethalon: Chart = vars.graph_info.getChart(chart_name.replace('test_', ''))
        if ethalon is not None:
            chart: Chart = Chart(name=chart_name)
            chart.setAxes(ethalon.getAxes())
            chart.setPen(QPen(ethalon.getPen().color(), 2, Qt.SolidLine))
            vars.graph_info.addChart(chart, chart_name)
            add_point_to_chart(chart_name, value_x, value_y)
        else:
            print(__name__, '\tError: cant find ethalon for', chart_name)


def remove_last_points_from_charts():
    remove_last_point_from_chart('test_lift')
    remove_last_point_from_chart('test_power')


def remove_last_point_from_chart(chart_name: str):
    chart: Chart = vars.graph_info.getChart(chart_name)
    if chart is not None:
        chart.removePoint()


def clear_points_from_charts():
    clear_points_from_chart('test_lift')
    clear_points_from_chart('test_power')


def clear_points_from_chart(chart_name: str):
    chart: Chart = vars.graph_info.getChart(chart_name)
    if chart is not None:
        chart.clearPoints()


def display_current_marker_point(data: dict):
    name = list(data.keys())[0]
    point: QPointF = list(data.values())[0]
    if 'test_lift' == name:
        vars.wnd_main.txtFlow.setText('%.4f' % point.x())
        vars.wnd_main.txtLift.setText('%.4f' % point.y())
    elif 'test_power' == name:
        vars.wnd_main.txtPower.setText('%.4f' % point.y())
    pass


def get_chart(chart_name: str):
    chart: Chart = vars.graph_info.getChart(chart_name)
    if chart is None:
        ethalon: Chart = vars.graph_info.getChart(chart_name.replace('test_', ''))
        if ethalon is not None:
            chart: Chart = Chart(name=chart_name)
            chart.setAxes(ethalon.getAxes())
            chart.setPen(QPen(ethalon.getPen().color(), 2, Qt.SolidLine))
            vars.graph_info.addChart(chart, chart_name)
        else:
            print(__name__, 'Error: cant find ethalon for', chart_name)
    return chart


def get_flow_lift_power():
    flow = AesmaFuncs.safe_parse_to_float(vars.wnd_main.txtFlow.text())
    lift = AesmaFuncs.safe_parse_to_float(vars.wnd_main.txtLift.text())
    power = AesmaFuncs.safe_parse_to_float(vars.wnd_main.txtPower.text())
    return flow, lift, power
