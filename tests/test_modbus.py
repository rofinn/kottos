import logging
import struct
import threading

from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server
from umodbus.utils import log_to_stream
from socketserver import TCPServer

from kottos.modbus import CC_REGISTER_TABLE, Client

# Add stream handler to logger 'uModbus'.
log_to_stream(level=logging.DEBUG)

# Extract the addresses from our default dict
addresses = [r[0] for r in CC_REGISTER_TABLE.values()]

# A very simple data store which maps addresses against their values.
data_store = dict(zip(addresses, range(0, len(addresses))))

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True

TCPServer.allow_reuse_address = True
app = get_server(TCPServer, ('localhost', 54321), RequestHandler)

@app.route(slave_ids=[0], function_codes=[3], addresses=addresses)
def read_data_store(slave_id, function_code, address):
    """" Return value of address. """
    return data_store[address]


def modbus_server():
    try:
        app.serve_forever()
    finally:
        app.shutdown()
        app.server_close()


def test_read():
    for k, v in data_store.items():
        print('{}: {}'.format(k, v))

    t = threading.Thread(target=modbus_server, daemon=True)
    t.start()
    c = Client('localhost', 54321, CC_REGISTER_TABLE)
    states = c.read(0)

    for k, v in CC_REGISTER_TABLE.items():
        print('{}: {}'.format(k, v))
        assert v[1](data_store[v[0]]) == states[k]


if __name__ == '__main__':
    modbus_server()