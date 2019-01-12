import logging
import threading

import six

import kottos.modbus
from kottos.modbus.client import Client
from kottos.modbus.registers import MNS_REGISTER_TABLE
from kottos.modbus.server import data_store, serve


def test_read():
    for k, v in data_store.items():
        print('{}: {}'.format(k, v))

    # Create our server thread
    t = threading.Thread(target=serve)
    # Daemon threads automatically get cleaned up
    t.setDaemon(True)
    t.start()

    c = Client('localhost', 54321, MNS_REGISTER_TABLE)
    states = c.read(0)

    for r in MNS_REGISTER_TABLE:
        print(
            '{} ({}): {}, {}'.format(
                r.label, r.register, states[r.label], data_store[r.register - 1]
            )
        )
        assert data_store[r.register - 1] == states[r.label]
