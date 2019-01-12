import logging

from six.moves.socketserver import TCPServer

import kottos.modbus
from kottos.modbus.client import Client
from kottos.modbus.registers import MNS_REGISTER_TABLE
from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server
from umodbus.utils import log_to_stream

# Add stream handler to logger 'uModbus'.
log_to_stream(level=logging.DEBUG)

# Extract the addresses from our default dict
addresses = [r.register - 1 for r in MNS_REGISTER_TABLE]

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


def serve():
    try:
        app.serve_forever()
    finally:
        app.shutdown()
        app.server_close()


if __name__ == '__main__':
    serve()
