from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QPushButton, QListWidget, \
    QFileDialog, QListWidgetItem, QGridLayout, QLabel


class Thumbnail(QVideoWidget):

    def __init__(self, labelPrefix=None):
        super(Thumbnail, self).__init__()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setMuted(True)
        self.mediaPlayer.setVideoOutput(self)
        self.thumbnailLabel = QLabel()
        self.mediaPlayer.durationChanged.connect(self.changedVideoLength)
        self.fileName = ""
        self.labelPrefix = labelPrefix
        self.videoFile = None
        self.setMaximumSize(200, 200)

    def loadVideo(self, videoFile):
        self.videoFile = videoFile
        filePath = self.videoFile.filePath
        splitFilePath = filePath.split("/")
        self.fileName = splitFilePath[-1]
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filePath)))
        self.mediaPlayer.setPosition(1000)
        self.mediaPlayer.pause()
        self.show()

    def removeVideo(self):
        self.mediaPlayer.stop()
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("")))
        self.thumbnailLabel.setText("")
        self.videoFile = None

    def changedVideoLength(self):
        seconds, milliseconds = divmod(self.mediaPlayer.duration(), 1000)
        minutes, seconds = divmod(seconds, 60)
        timeFormat = "{0} - {1}:{2}"
        if seconds < 10:
            timeFormat = "{0} - {1}:0{2}"
        if self.labelPrefix:
            timeFormat = "{0}: {1}".format(self.labelPrefix, timeFormat)
        self.thumbnailLabel.setText(
            timeFormat.format(self.fileName, minutes, seconds))


class VideoFile(QListWidgetItem):
    def __init__(self, filePath):
        super().__init__()
        self.autoPlayNext = False
        self.autoLoop = False
        self.enableFade = False
        self.filePath = filePath
        self.setTitle()

    def setTitle(self):
        splitFilePath = self.filePath.split("/")

        features = []
        if self.enableFade:
            features.append("Fade")
        if self.autoPlayNext:
            features.append("Play Next")
        elif self.autoLoop:
            features.append("Loop")

        features.append(splitFilePath[-1])
        self.setData(0, " - ".join(features))

    #Set auto play next type
    def setAutoPlayNext(self):
        self.autoPlayNext = not self.autoPlayNext
        if self.autoPlayNext:
            if self.autoLoop:
                self.autoLoop = False

        self.setTitle()

    #set auto loop type
    def setAutoLoop(self):
        self.autoLoop = not self.autoLoop
        if self.autoLoop:
            if self.autoPlayNext:
                self.autoPlayNext = False

        self.setTitle()

    def setEnableFade(self):
        self.enableFade = not self.enableFade
        self.setTitle()

    def getAutoPlayType(self):
        return (self.autoPlayNext, self.autoLoop, self.enableFade)


class VideoFolderControlLayout(QGridLayout):
    def __init__(self, videoPlayer):
        super(VideoFolderControlLayout, self).__init__()
        self.currentVideo = None
        self.videoPlayer = videoPlayer
        self.setup()
        self.updateButtonStatus()

    def setup(self):
        self.videoBank = QListWidget()
        self.videoQueue = QListWidget()

        self.videoBank.itemSelectionChanged.connect(self.updateVideoBankChange)
        self.videoQueue.itemSelectionChanged.connect(self.updateVideoQueueChange)

        self.addToQueueButton = QPushButton('Add')
        self.addToQueueButton.clicked.connect(self.addVideoToQueue)

        self.upButton = QPushButton('&Up')
        self.upButton.clicked.connect(self.moveVideoUp)
        self.downButton = QPushButton('&Down')

        self.downButton.clicked.connect(self.moveVideoDown)
        self.addFilesButton = QPushButton("+")
        self.addFilesButton.clicked.connect(self.addVideoFiles)
        self.removeFilesButton = QPushButton("-")
        self.removeFilesButton.clicked.connect(self.removeVideoFiles)
        self.removeFromQueueButton = QPushButton("Remove")
        self.removeFromQueueButton.clicked.connect(self.removeVideoFromQueue)
        self.clearVideosButton = QPushButton("Clear")
        self.clearVideosButton.clicked.connect(self.clearVideoQueue)

        self.autoPlayNextButton = QPushButton("Auto Play Next")
        self.autoPlayNextButton.clicked.connect(self.setAutoPlayNext)
        self.autoLoopButton = QPushButton("Auto Loop")
        self.autoLoopButton.clicked.connect(self.setAutoLoop)
        self.enableFadeButton = QPushButton("Enable Fade")
        self.enableFadeButton.clicked.connect(self.setEnableFade)

        self.prevThumbnail = Thumbnail("Previous")
        self.currentThumbnail = Thumbnail("Current")
        self.nextThumbnail = Thumbnail("Next")
        self.addWidget(self.prevThumbnail, 0, 0, 6, 8)
        self.addWidget(self.currentThumbnail, 0, 8, 6, 8)
        self.addWidget(self.nextThumbnail, 0, 16, 6, 8)

        prevLabel = self.prevThumbnail.thumbnailLabel
        currentLabel = self.currentThumbnail.thumbnailLabel
        nextLabel = self.nextThumbnail.thumbnailLabel
        self.addWidget(prevLabel, 6, 2)
        self.addWidget(currentLabel, 6, 11)
        self.addWidget(nextLabel, 6, 20)

        self.selectedVideoBankVideo = Thumbnail()
        self.videoBankLabel = self.selectedVideoBankVideo.thumbnailLabel
        self.selectedVideoQueueVideo = Thumbnail()
        self.videoQueueLabel = self.selectedVideoQueueVideo.thumbnailLabel

        self.addWidget(self.videoBank, 7, 0, 12, 6)
        self.addWidget(self.addFilesButton, 19, 0)
        self.addWidget(self.removeFilesButton, 19, 1)

        self.addWidget(self.selectedVideoBankVideo, 7, 6, 4, 6)
        self.addWidget(self.addToQueueButton, 12, 8)
        #Add timestamp of videoBank
        self.addWidget(self.videoBankLabel, 11, 8)

        self.addWidget(self.videoQueue, 7, 12, 12, 6)
        self.addWidget(self.removeFromQueueButton, 19, 12)
        self.addWidget(self.clearVideosButton, 19, 13)

        self.addWidget(self.selectedVideoQueueVideo, 7, 18, 4, 6)
        self.addWidget(self.upButton, 12, 20)
        self.addWidget(self.downButton, 13, 20)
        self.addWidget(self.autoPlayNextButton, 14, 20)
        self.addWidget(self.autoLoopButton, 14, 21)
        self.addWidget(self.enableFadeButton, 14, 22)
        #Add timestamp of videoQueue
        self.addWidget(self.videoQueueLabel, 11, 20)

    def getVideoQueueFilePath(self, index):
        return self.videoQueue.item(index).filePath

    def updateVideoBankChange(self):
        self.addToQueueButton.setDisabled(
            not bool(self.videoBank.selectedItems() or self.videoBank.count() != 0))
        videoFile = self.videoBank.item(self.videoBank.currentRow())
        if videoFile:
            self.selectedVideoBankVideo.loadVideo(videoFile)

    def updateVideoQueueChange(self):
        videoFile = self.videoQueue.item(self.videoQueue.currentRow())
        if videoFile:
            self.selectedVideoQueueVideo.loadVideo(videoFile)
        else:
            self.selectedVideoQueueVideo.removeVideo()
        self.updateButtonStatus()

    def updateButtonStatus(self):
        self.removeFilesButton.setDisabled(self.videoBank.count() == 0)
        self.addToQueueButton.setDisabled(
            not bool(self.videoBank.selectedItems() or self.videoBank.count() != 0))
        self.removeFromQueueButton.setDisabled(
            not bool(self.videoQueue.selectedItems() or self.videoQueue.count() != 0))
        self.clearVideosButton.setDisabled(self.videoQueue.count() == 0)
        self.upButton.setDisabled(
            bool(not self.videoQueue.selectedItems() or self.videoQueue.currentRow() == 0))
        self.downButton.setDisabled(bool(not self.videoQueue.selectedItems(
        ) or self.videoQueue.currentRow() == self.videoQueue.count()-1))
        self.autoPlayNextButton.setDisabled(self.videoQueue.count() == 0)
        self.autoLoopButton.setDisabled(self.videoQueue.count() == 0)
        self.enableFadeButton.setDisabled(self.videoQueue.count() == 0)

        if self.videoQueue.count() == 0:
            self.autoPlayNextButton.setStyleSheet("")
            self.autoLoopButton.setStyleSheet("")
            self.enableFadeButton.setStyleSheet("")

        if self.selectedVideoQueueVideo.videoFile:
            if self.selectedVideoQueueVideo.videoFile.autoPlayNext:
                self.autoPlayNextButton.setStyleSheet(
                    "background-color : green")
            else:
                self.autoPlayNextButton.setStyleSheet("background-color : red")

            if self.selectedVideoQueueVideo.videoFile.autoLoop:
                self.autoLoopButton.setStyleSheet("background-color : green")
            else:
                self.autoLoopButton.setStyleSheet("background-color : red")

            if self.selectedVideoQueueVideo.videoFile.enableFade:
                self.enableFadeButton.setStyleSheet("background-color : green")
            else:
                self.enableFadeButton.setStyleSheet("background-color : red")

    def addVideoToQueue(self):
        videoFile = self.videoBank.item(self.videoBank.currentRow())
        newVideo = VideoFile(videoFile.filePath)
        prevCount = self.videoQueue.count()

        #Check before addding
        if prevCount == 0:
            self.videoPlayer.loadFirstVideo(videoFile.filePath)
        elif self.videoQueue.row(self.currentVideo) == self.videoQueue.count() - 1:
            self.nextThumbnail.loadVideo(newVideo)
        self.videoQueue.addItem(newVideo)

        #Check after adding
        if self.videoQueue.count() == 1:
            self.currentVideo = self.videoQueue.item(0)
            self.currentVideo.setBackground(Qt.red)
            self.currentThumbnail.loadVideo(self.currentVideo)
            self.selectedVideoQueueVideo.loadVideo(self.currentVideo)

        self.updateButtonStatus()

    def moveVideo(self, movement):
        rowIndex = self.videoQueue.currentRow()
        currentItem = self.videoQueue.takeItem(rowIndex)
        self.videoQueue.insertItem(rowIndex + movement, currentItem)
        self.videoQueue.setCurrentRow(rowIndex + movement)
        self.updateVideoQueueChange()
        self.updateThumbnails()
        self.updateButtonStatus()

    def moveVideoUp(self):
        self.moveVideo(-1)

    def moveVideoDown(self):
        self.moveVideo(1)

    def addVideoFiles(self):
        fileNameFilter = "Video Files (*.mov *.mp4)"
        output = QFileDialog.getOpenFileNames(
            None, "Open files", "C\\Desktop", fileNameFilter)
        if output:
            prevCount = self.videoBank.count()
            filePaths = output[0]
            for filePath in filePaths:
                self.videoBank.addItem(VideoFile(filePath))
            self.updateButtonStatus()
            if prevCount == 0:
                self.videoBank.setCurrentRow(0)

    def removeVideoFiles(self):
        index = self.videoBank.currentRow()
        self.videoBank.takeItem()
        self.updateButtonStatus()
        self.updateVideoBankChange()
        if self.videoBank.count() == 0:
            self.selectedVideoBankVideo.removeVideo()
        else:
            self.selectedVideoBankVideo.loadVideo(
                self.videoBank.item(index))

    def updateThumbnails(self):
        if self.currentVideo:
            index = self.videoQueue.row(self.currentVideo)
            self.currentThumbnail.loadVideo(
                self.videoQueue.item(index))

            if index - 1 >= 0:
                self.prevThumbnail.loadVideo(
                    self.videoQueue.item(index - 1))
                self.prevThumbnail.changedVideoLength()
            else:
                self.prevThumbnail.removeVideo()

            if index + 1 <= self.videoQueue.count()-1:
                self.nextThumbnail.loadVideo(
                    self.videoQueue.item(index + 1))
                self.nextThumbnail.changedVideoLength()
            else:
                self.nextThumbnail.removeVideo()
        else:
            self.currentThumbnail.removeVideo()
            self.prevThumbnail.removeVideo()
            self.nextThumbnail.removeVideo()

    def removeVideoFromQueue(self):
        index = self.videoQueue.row(self.currentVideo)
        rowIndex = self.videoQueue.currentRow()
        currentVideoQueueCount = self.videoQueue.count()

        self.videoQueue.takeItem(rowIndex)
        if rowIndex == index or rowIndex == index-1 or rowIndex == index+1:
            if currentVideoQueueCount == 1:
                self.currentVideo = None
                self.videoPlayer.clearVideo()
            elif rowIndex == index:
                if rowIndex < currentVideoQueueCount-1:
                    self.currentVideo = self.videoQueue.item(rowIndex)
                else:
                    self.currentVideo = self.videoQueue.item(0)
                self.currentVideo.setBackground(Qt.red)
                self.videoPlayer.loadFirstVideo(self.currentVideo.filePath)
            self.updateThumbnails()
        self.updateButtonStatus()

    def clearVideoQueue(self):
        self.videoQueue.clear()
        self.currentVideo = None
        self.updateThumbnails()
        self.updateVideoQueueChange()
        self.videoPlayer.clearVideo()

    def getVideo(self, playType):
        if playType == "current":
            return self.getCurrentVideo()
        elif playType == "next":
            return self.getNextVideo()
        elif playType == "prev":
            return self.getPrevVideo()

    def getCurrentVideo(self):
        return self.currentVideo.filePath

    #Should fetch the current video looping or play next setting
    def getCurrentVideoPlayNextLoopType(self):
        return self.currentVideo.getAutoPlayType()

    def updateCurrentVideo(self, index):
        if index <= self.videoQueue.count() - 1 and index >= 0:
            self.currentVideo.setBackground(Qt.white)
            self.currentVideo = self.videoQueue.item(index)
            self.currentVideo.setBackground(Qt.red)
            self.updateThumbnails()

    def getNextVideo(self):
        if self.currentVideo:
            index = self.videoQueue.row(self.currentVideo)
            self.updateCurrentVideo(index + 1)
            return self.currentVideo.filePath

    def getPrevVideo(self):
        if self.currentVideo:
            index = self.videoQueue.row(self.currentVideo)
            self.updateCurrentVideo(index - 1)
            return self.currentVideo.filePath

    def setAutoPlayNext(self):
        videoFile = self.selectedVideoQueueVideo.videoFile
        videoFile.setAutoPlayNext()
        if videoFile.autoPlayNext:
            self.autoPlayNextButton.setStyleSheet("background-color : green")
            self.autoLoopButton.setStyleSheet("background-color : red")
        else:
            self.autoPlayNextButton.setStyleSheet("background-color : red")

    def setAutoLoop(self):
        videoFile = self.selectedVideoQueueVideo.videoFile
        videoFile.setAutoLoop()
        if videoFile.autoLoop:
            self.autoLoopButton.setStyleSheet("background-color : green")
            self.autoPlayNextButton.setStyleSheet("background-color : red")
        else:
            self.autoLoopButton.setStyleSheet("background-color : red")

    def setEnableFade(self):
        videoFile = self.selectedVideoQueueVideo.videoFile
        videoFile.setEnableFade()
        if videoFile.enableFade:
            self.enableFadeButton.setStyleSheet("background-color : green")
        else:
            self.enableFadeButton.setStyleSheet("background-color : red")
