from PyQt5 import QtTest
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QStyle, QPushButton, QLabel, QSizePolicy

from videoFolder import VideoFolderControlLayout


class MainVideoWindow:

    def __init__(self, handleError, mediaStateChanged, checkFade):
        self.vBottom = SubVideoWindow("v2", False, handleError)
        self.vTop = SubVideoWindow(
            "v1", True, handleError, mediaStateChanged, checkFade, self.vBottom)
        self.mediaStateChanged = mediaStateChanged
        self.checkFade = checkFade

    def minimizeWindow(self):
        self.vTop.setWindowFlag(Qt.FramelessWindowHint)
        self.vBottom.setWindowFlag(Qt.FramelessWindowHint)
        self.vTop.showMaximized()
        self.vBottom.showMaximized()
        self.vTop.show()
        # self.vBottom.show()
        self.vTop.raise_()

    def maximizeWindow(self):
        self.vTop.resize(600, 400)
        self.vBottom.resize(600, 400)
        self.vTop.setWindowFlags(
            self.vTop.windowFlags() & ~Qt.FramelessWindowHint)
        self.vBottom.setWindowFlags(
            self.vBottom.windowFlags() & ~Qt.FramelessWindowHint)
        self.vTop.show()
        # self.vBottom.show()

    def state(self):
        return self.vTop.state()

    def setVideo(self, fileName):
        self.vTop.loadVideo(fileName)

    def clear(self):
        self.stop()
        self.setVideo("")

    def stop(self):
        self.vTop.stop()

    def pause(self):
        self.vTop.pause()

    def play(self):
        self.vTop.play()

    def playFile(self, fileName, fade):
        self.vBottom.loadVideo(fileName)
        self.vBottom.play()

        self.vBottom.show()
        self.vTop.raise_()
        self.vBottom.setWindowOpacity(1)

        if fade:
            for i in range(1, 100):
                self.vTop.setWindowOpacity(1 - 0.01 * i)
                # self.vBottom.setWindowOpacity(0.01*i)
                QtTest.QTest.qWait(0.0005)
            print("finished fading")
            self.vBottom.raise_()
        else:
            for i in range(1, 10):
                self.vTop.setWindowOpacity(1 - 0.004 * i)
                QtTest.QTest.qWait(0.00000005)
            self.vBottom.raise_()

        self.vTop.resetBottomVideoPlayer(
            self.mediaStateChanged, self.checkFade)
        self.vBottom.setBottomVideoPlayer(
            self.vTop, self.mediaStateChanged, self.checkFade)

        vTemp = self.vBottom
        self.vBottom = self.vTop
        self.vTop = vTemp

        self.vBottom.stop()

        print("hiding now")
        self.vBottom.setWindowOpacity(0)
        self.vBottom.hide()

    def getDuration(self):
        return self.vTop.getDuration()


class SubVideoWindow(QVideoWidget):

    def __init__(self, title, onTop, handleError, mediaStateChanged=None, checkFade=None, bottomVideoPlayer=None, parent=None):
        super(SubVideoWindow, self).__init__(parent)
        if bottomVideoPlayer:
            self.bottomVideoPlayer = bottomVideoPlayer
            self.bottomVideoPlayer.hide()
        self.onTop = onTop
        self.setWindowTitle(title)
        self.resize(640, 480)
        self.show()

        self.media = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media.setMuted(True)
        self.media.setVideoOutput(self)
        if mediaStateChanged:
            self.media.stateChanged.connect(mediaStateChanged)
        if checkFade:
            self.media.positionChanged.connect(checkFade)
        self.handleError = handleError
        self.media.error.connect(self.subVideoWindowError)
        self.media.setNotifyInterval(500)

    def state(self):
        return self.media.state()

    def loadVideo(self, fileName):
        print(fileName)
        self.media.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))

    def stop(self):
        self.media.stop()

    def pause(self):
        self.media.pause()

    def play(self):
        self.media.play()

    def getDuration(self):
        return self.media.duration()

    def resetBottomVideoPlayer(self, stateChanged, positionChanged):
        self.media.stateChanged.disconnect(stateChanged)
        self.media.positionChanged.disconnect(positionChanged)
        self.bottomVideoPlayer = None
        self.onTop = False

    def setBottomVideoPlayer(self, bottomVideoPlayer, stateChanged, positionChanged):
        self.media.stateChanged.connect(stateChanged)
        self.media.positionChanged.connect(positionChanged)
        self.bottomVideoPlayer = bottomVideoPlayer
        self.onTop = True

    def moveEvent(self, event):
        if self.onTop:
            self.bottomVideoPlayer.move(self.pos())

    def subVideoWindowError(self):
        print(self.media.errorString)
        self.handleError(self.media.errorString())
