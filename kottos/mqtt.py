import os
import socket
import ssl

import paho.mqtt.client as paho
from time import sleep
from random import uniform

from contextlib import contextmanager


@contextmanager
def connect(host, port=502):
    mqttc.tls_set(
        caPath,
        certfile=certPath,
        keyfile=keyPath,
        cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLSv1_2,
        ciphers=None
    )

    mqttc.connect(awshost, awsport, keepalive=60)
    loop_start()
    yield mqttc
    loop_stop()
