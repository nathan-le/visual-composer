from PyQt5 import QtTest
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QStyle, QPushButton, QLabel, QSizePolicy

from videoFolder import VideoFolderControlLayout
from videoWindow import MainVideoWindow


class VideoButton(QPushButton):

    def __init__(self, clickConnect, icon=None, text=None, parent=None):
        super(VideoButton, self).__init__(parent)

        self.setEnabled(False)
        if not text:
            self.setIcon(self.style().standardIcon(icon))
        else:
            self.setText(text)
        self.clicked.connect(clickConnect)

        self.buttonFunction = clickConnect

    def replaceIcon(self, icon):
        self.setIcon(self.style().standardIcon(icon))


class VideoPlayer:

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        # Video construction
        self.videoFolderControlLayout = VideoFolderControlLayout(self)
        self.mainVideoWindow = MainVideoWindow(
            self.handleError, self.mediaStateChanged, self.checkFade)
        self.locked = False

        self.locked = False
        self.maximized = False

        self.playButton = VideoButton(self.play, QStyle.SP_MediaPlay)
        self.playNextButton = VideoButton(self.playRequest(
            "next", False), QStyle.SP_MediaSkipForward)
        self.playPrevButton = VideoButton(self.playRequest(
            "prev", False), QStyle.SP_MediaSkipBackward)
        self.playNextWithFadeButton = VideoButton(
            self.playRequest("next", True), None, "Play Next With Fade")
        self.playPrevWithFadeButton = VideoButton(
            self.playRequest("prev", True), None, "Play Previous With Fade")
        self.maxMinButton = VideoButton(self.maxMin, None, "Maximize Video")
        self.maxMinButton.setEnabled(True)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Maximum)

    def loadFirstVideo(self, fileName):
        self.playButton.setEnabled(True)
        self.playButton.replaceIcon(QStyle.SP_MediaPlay)
        self.playButton.setStyleSheet("")
        self.playNextButton.setEnabled(True)
        self.playPrevButton.setEnabled(True)
        self.playNextWithFadeButton.setEnabled(True)
        self.playPrevWithFadeButton.setEnabled(True)
        self.mainVideoWindow.setVideo(fileName)

    def clearVideo(self):
        self.playButton.setEnabled(False)
        self.playButton.replaceIcon(QStyle.SP_MediaPlay)
        self.playButton.setStyleSheet("")
        self.playNextButton.setEnabled(False)
        self.playPrevButton.setEnabled(False)
        self.playNextWithFadeButton.setEnabled(False)
        self.playPrevWithFadeButton.setEnabled(False)
        self.mainVideoWindow.clear()

    def maxMin(self):
        if not self.maximized:
            self.mainVideoWindow.minimizeWindow()
            self.maximized = True
            self.maxMinButton.setStyleSheet("background-color : red")
            self.maxMinButton.setText("Minimize Window")
        else:
            self.mainVideoWindow.maximizeWindow()
            self.maximized = False
            self.maxMinButton.setStyleSheet("")
            self.maxMinButton.setText("Maximize Window")

    def play(self):
        if self.mainVideoWindow.state() == QMediaPlayer.PlayingState:
            self.mainVideoWindow.pause()
            self.playButton.setStyleSheet("")
        else:
            self.mainVideoWindow.play()
            self.playButton.setStyleSheet("background-color : red")

    def playRequest(self, playType, fade):
        return lambda: self.playRequestedVideo(playType, fade)

    def playRequestedVideo(self, playType, fade):
        fileName = self.videoFolderControlLayout.getVideo(playType)
        print(fileName)
        if fileName != '':
            self.playButton.replaceIcon(QStyle.SP_MediaPause)
            self.playButton.setStyleSheet("background-color : red")

            self.mainVideoWindow.playFile(fileName, fade)

            self.mainWindow.raise_()
            self.mainWindow.activateWindow()

    def mediaStateChanged(self):
        if self.mainVideoWindow.state() == QMediaPlayer.PlayingState:
            self.playButton.replaceIcon(QStyle.SP_MediaPause)
            self.playButton.setStyleSheet("background-color : red")
        else:
            self.playButton.replaceIcon(QStyle.SP_MediaPlay)
            self.playButton.setStyleSheet("")

    def checkFade(self, position):
        if not self.locked:
            if self.mainVideoWindow.getDuration() - 2000 > 0 and position > (self.mainVideoWindow.getDuration() - 2000):
                self.locked = True

                autoPlayNext, autoLoop, enableFade = self.videoFolderControlLayout.getCurrentVideoPlayNextLoopType()

                if autoPlayNext:
                    self.playRequestedVideo("next", enableFade)
                elif autoLoop:
                    self.playRequestedVideo("current", enableFade)

                self.locked = False

    def handleError(self, errorString):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + str(errorString))
