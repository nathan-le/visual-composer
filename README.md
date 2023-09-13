# visual-composer

visual-composer is an open source software for automating video playback, looping, and sequencing. This tool was developed to allow an artist/musician without a designated visual professional to create a playlist of videos that can be triggered manually or automatically throughout a live performance and be synced with their setlist. visual-composer creates a control plane that manages all the video sequencing and generates a separate video screen that can be viewed on a projector or separate monitor.

# Features

visual-composer allows loading all video assets into a video bank and then pushing those assets to a video queue for creating the playlist. Each video in the video queue has the option to automatically play the next video in the queue or continuously loop the current selection. When playing the next video, a fade can be enabled to allow for smoother transitions. For manual playback, visual-composer allows commands from the user keyboard for triggering the video selection. The space bar and right arrow allow for playing the next video, while the left arrow allows playing the previous video.


![alt text](https://github.com/nathan-le/visual-composer/blob/main/images/control-interface.png)




# Installation

This Python application uses PyQt5 for its GUI interface and video processing. This software has been developed mainly in Python3.

1) Download and install [pip](https://pip.pypa.io/en/stable/installation/#get-pip-py) as your package manager
2) git clone https://github.com/nathan-le/visual-composer.git
3) cd visual-composer
4) pip3 install -r requirements.txt

# Packaging as Excutable

This Python application uses [pyinstaller](https://pyinstaller.org/en/stable/) to package this project as an executable:

1) cd visual-composer
2) pyinstaller visual-composer/app.py


# Running visual-composer

Running software as python script:

1) cd visual-composer
2) python3 visual-composer/app.py

Running software as python executable:
1) cd visual-composer/dist/app
2) open app

# Live Usage

I am hugely inspired by musicians such as Godspeed! You Black Emperor for their incorporation of film projections throughout their live performances. My musical group played some covers of their music and I used visual-composer to project archival super 8 footage alongside our preformance.

![alt text](https://github.com/nathan-le/visual-composer/blob/main/images/warehouse.jpeg)

# Other Notes

Currently, PyQt5 does not support gapless video playback. I encountered several issues when trying to sequence and play different video clips back to back. The native solution incurs a momentary delay and shows a blank screen for a couple seconds between transitions. To mitigate this issue, I created a wrapper class that overlays 2 video screens on top of one another and will quickly fade/swap between the 2 screens. This allowed for a smoother transition even though it will cut a couple milliseconds off the end of each video.
