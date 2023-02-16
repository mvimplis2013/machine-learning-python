#!/usr/bin/env python

from setuptools import setup

setup(
    name="video_converter",
    version="0.0.1",
    packages=["camera4me"],
    install_requires=["opencv-python"],
    data_files=[],
    entry_points={
      "console_scripts": [
        "video-creator=camera4me.frames_to_video:video_main"
      ]
    }
)