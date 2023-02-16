#!/usr/bin/env python

from setuptools import setup

setup(
    name="video_converter",
    version="0.0.1",
    packages=["camera4me"],
    install_requires=["opencv-python"],
    data_files=[("cfg", ["config/camera.cfg"])],
    entry_points={
      "console_scripts": [
        "smart-grab=camera4me.main:main_grab",
        "file-watchdog=camera4me.space_protector:run_watchdog",
        "polite-messenger=camera4me.messenger:__main_mq_client__",
        "influxdb-caller=camera4me.influxdb_main:__influx_main__",
        "system-monitoring=datadrill.central_platform:platform_22",
        "rabbitmq-consumer=messageKit.rabbitmq.consume:main",
        "async-consumer-rabmq=messageKit.rabbitmq.asynchronous_consumer:asynchronous_consumer_main",
        "async-publisher-rabmq=messageKit.rabbitmq.asynchronous_publisher:main",
        "video-creator=camera4me.frames_to_video:video_main"
      ]
    }
)