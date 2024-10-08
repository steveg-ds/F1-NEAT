import time
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import QTimer
from queue import Empty

class App(QMainWindow):
    """
    A PyQt5 application for visualizing real-time data from a queue using PyQtGraph.

    This application features two line plots:
    - Reward Plot: Displays reward values over iterations.
    - Speed Plot: Displays speed values over iterations.

    The application also updates the plots and a label showing the mean frame rate.
    """

    def __init__(self, queue, parent=None):
        """
        Initializes the application with a data queue.

        Args:
            queue (queue.Queue): Queue from which data will be retrieved for plotting.
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
        super(App, self).__init__(parent)
        self.queue = queue

        # Create and set up GUI elements
        self.mainbox = QWidget()
        self.setCentralWidget(self.mainbox)
        self.mainbox.setLayout(QVBoxLayout())

        self.canvas = pg.GraphicsLayoutWidget()
        self.mainbox.layout().addWidget(self.canvas)
        self.canvas.setStyleSheet("background-color: rgb(50, 50, 50);")  # Set background color to grey

        self.label = QLabel()
        self.mainbox.layout().addWidget(self.label)

        self.view = self.canvas.addViewBox()
        self.view.setAspectLocked(True)

        # Line plot for reward values
        self.plot1 = self.canvas.addPlot(row=1, col=0)
        self.curve1 = self.plot1.plot(pen=pg.mkPen(color='r', width=2), name='Reward')
        self.plot1.setMaximumWidth(600)  # Set maximum width for plot1
        self.plot1.setLabel('left', 'Reward')
        self.plot1.setLabel('bottom', 'Iterations')
        self.plot1.setTitle('Reward Plot')
        self.plot1.addLegend()

        # Line plot for speed values
        self.plot2 = self.canvas.addPlot(row=0, col=0)
        self.curve2 = self.plot2.plot(pen=pg.mkPen(color='b', width=2), name='Speed')
        self.plot2.setMaximumWidth(600)  # Set maximum width for plot2
        self.plot2.setLabel('left', 'Speed')
        self.plot2.setLabel('bottom', 'Iterations')
        self.plot2.setTitle('Speed Plot')
        self.plot2.addLegend()

        # Initialize plot data variables
        self.x = 0
        self.y1 = np.array([])
        self.y2 = np.array([])
        self.current_genome_id = None
        self.counter = 0
        self.fps = 0.0
        self.lastupdate = time.time()

        # Start the update loop
        self._update()

    def _update(self):
        """
        Updates the plots and the frame rate label. Retrieves data from the queue, 
        updates the plots with new data, and refreshes the frame rate label.
        """
        try:
            # Retrieve data from the queue
            data = self.queue.get()
            y1 = data['reward']
            y2 = data['speed']

            # Check if genome_id has changed
            if self.current_genome_id != data['genome_id']:
                self.current_genome_id = data['genome_id']
                self.x = 0
                self.y1 = np.array([])
                self.y2 = np.array([])

            # Update plot titles with current data
            title1 = f"Reward Plot"
            title2 = f"Speed Plot (Generation: {data['generation']}, Genome ID: {data['genome_id']}, Pop #: {data['pop_num']})"
            self.plot1.setTitle(title1)
            self.plot2.setTitle(title2)

            title_font_size = 32
            self.plot1.titleLabel.setFont(pg.QtGui.QFont("Arial", title_font_size, pg.QtGui.QFont.Bold))
            self.plot2.titleLabel.setFont(pg.QtGui.QFont("Arial", title_font_size, pg.QtGui.QFont.Bold))

            # Append new data to arrays
            self.y1 = np.append(self.y1, y1)
            self.y2 = np.append(self.y2, y2)

            # Update the plots with new data
            x_range = np.arange(0, min(len(self.y1), 120))
            self.curve1.setData(x_range, self.y1[:len(x_range)])
            self.curve2.setData(x_range, self.y2[:len(x_range)])

        except Empty:
            pass

        # Update the FPS label
        now = time.time()
        dt = (now - self.lastupdate)
        if dt <= 0:
            dt = 0.000000000001
        fps2 = 1.0 / dt
        self.lastupdate = now
        self.fps = self.fps * 0.9 + fps2 * 0.1
        tx = 'Mean Frame Rate:  {fps:.2f} FPS'.format(fps=self.fps)
        self.label.setText(tx)

        # Schedule the next update
        QTimer.singleShot(1000, self._update)
