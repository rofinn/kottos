#!/usr/bin/env python
import inspect
import time
import kottos
import kottos.modbus
from kottos.modbus.client import Client
from kottos.modbus.registers import MNS_REGISTER_TABLE

c = Client("192.168.1.90", 502, MNS_REGISTER_TABLE)
i = 0

while i < 10:
    results = c.scan()

    for (k, v) in results.items():
        print('{}: {}'.format(k, v))

    time.sleep(1)
    i = i + 1

print('Terminating')
