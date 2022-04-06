#!/usr/bin/env python

from setuptools import setup

setup(
    name="capture_frames",
    version="0.0.1",
    packages=["camera4me"],
    install_requires=["opencv-python"],
    data_files=[("cfg", ["config/camera.cfg"])],
    entry_points={
      "console_scripts": [
        "smart-grab=camera4me.main:main_grab",
        "file-watchdog=camera4me.space_protector:run_watchdog",
        "polite-messenger=camera4me.messenger:__main_mq_client__",
      ]
    }
)