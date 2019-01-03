import logging
import six
import threading

import kottos.modbus
from kottos.modbus.registers import MNS_REGISTER_TABLE
from kottos.modbus.client import Client
from kottos.modbus.server import serve, data_store


def test_read():
    for k, v in data_store.items():
        print('{}: {}'.format(k, v))

    t = threading.Thread(target=serve, daemon=True)
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