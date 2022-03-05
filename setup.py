#!/usr/bin/env python

from distutils.core import setup

setup(
    name="capture_frames",
    version="0.0.1",
    packages=["camera4me"],
    install_requires=["requests"],
    py_modules=["cv2"],
    entry_points={
      "console_scripts": [
        "smart-grab=camera4me.main:__main__",
      ]
    }
)