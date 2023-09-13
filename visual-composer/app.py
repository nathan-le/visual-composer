#!/usr/local/bin/python
# coding: latin-1
from PyQt5.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QVBoxLayout, QMainWindow, QWidget, QAction, QShortcut
from PyQt5.QtGui import QIcon, QKeySequence
import sys

import signal

from videoPlayer import VideoPlayer


class ControlWindow(QMainWindow):

    def __init__(self, parent=None):
        super(ControlWindow, self).__init__(parent)

        self.videoPlayer = VideoPlayer(self)

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setWindowTitle("Control Box")
        self.setCentralWidget(wid)

        #3/26/2022 testing playing with space bar
        self.spacebar = QShortcut(QKeySequence("Space"), self)
        self.spacebar.activated.connect(
            self.videoPlayer.playNextButton.buttonFunction)

        self.playNextShortcut = QShortcut(QKeySequence("Right"), self)
        self.playNextShortcut.activated.connect(
            self.videoPlayer.playNextButton.buttonFunction)

        self.playPrevShortcut = QShortcut(QKeySequence("Left"), self)
        self.playPrevShortcut.activated.connect(
            self.videoPlayer.playPrevButton.buttonFunction)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.videoPlayer.playButton)
        controlLayout.addWidget(self.videoPlayer.playPrevButton)
        controlLayout.addWidget(self.videoPlayer.playNextButton)

        manualControlLayout = QHBoxLayout()
        manualControlLayout.addWidget(self.videoPlayer.playPrevWithFadeButton)
        manualControlLayout.addWidget(self.videoPlayer.playNextWithFadeButton)

        setupControlLayout = QHBoxLayout()
        setupControlLayout.addWidget(self.videoPlayer.maxMinButton)

        layout = QVBoxLayout()
        layout.addLayout(setupControlLayout)
        layout.addLayout(controlLayout)
        layout.addLayout(manualControlLayout)
        layout.addLayout(self.videoPlayer.videoFolderControlLayout)
        layout.addWidget(self.videoPlayer.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

    def exitCall(self):
        sys.exit(app.exec_())


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    player = ControlWindow()
    player.resize(1000, 800)
    player.setMaximumSize(1000, 800)
    player.show()
    sys.exit(app.exec_())
