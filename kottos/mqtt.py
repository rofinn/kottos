import os
import socket
import ssl
from contextlib import contextmanager
from random import uniform
from time import sleep

import paho.mqtt.client as paho


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
