from pyqtgraph import QtGui, QtCore
import pyqtgraph as pg
from collections import deque
import deviceinfo as info
import time


"""
In order to display time on x axis overriding tickStrings() from
AxisItem module.
"""


class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super(TimeAxisItem, self).__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        strns = []
        for x in values:
            try:
                strns.append(time.strftime("%M:%S", time.gmtime(x/1000)))    # time_t --> time.struct_time
            except ValueError:  # Windows can't handle dates before 1970
                strns.append('')
        return strns


class MonitorStats:

    def __init__(self, sampleinterval=2000):
        """
            Monitor System Statistics

            Input Args:
                sampleinterval (int) = polling interval for collecting data
        """
        self.sampleinterval = sampleinterval
        self.data = deque(maxlen=20)
        self.device_info = info.InformationStatistics()
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow(title="Monitor System Statistics")
        self.win.resize(800, 600)
        self.plot = self.win.addPlot(
            title='CPU and Swap Mem Usage',
            axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plot.addLegend()
        self.plot.setLimits(yMin=0, yMax=100, xMin=0)
        self.plot.showGrid(x=True, y=True)
        self.plot.setMouseEnabled(False, False)
        self.plot.setRange(yRange=(0, 100), disableAutoRange=True)  # Trying to fix y-axis at 0,100
        self.plot.setLabel('left', "Percentage Utilization")
        self.plot.setLabel('bottom', "Time (s)")
        self.cpu_stats = self.plot.plot(pen='r', name="CPU Usage")
        self.swap_mem_stats = self.plot.plot(pen='b', name="Swap Mem Usage")
        self.time = QtCore.QTime()
        self.time.start()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(self.sampleinterval)

    def update_plot(self):
        """
            Fetch data from system
        """
        self.data.append({
            'x': self.time.elapsed(),
            'y1': self.device_info.get_cpu_usage(),
            'y2': self.device_info.get_swap_mem_usage()
            })
        x = [item['x'] for item in self.data]
        y1 = [item['y1'] for item in self.data]
        y2 = [item['y2'] for item in self.data]
        self.cpu_stats.setData(x=x, y=y1)
        self.swap_mem_stats.setData(x=x, y=y2)
        self.app.processEvents()

    def run(self):
        self.app.exec_()


if __name__ == "__main__":
    start = MonitorStats(sampleinterval=2000)
    start.run()
