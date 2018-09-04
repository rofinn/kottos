import socket
import sys

from umodbus import conf
from umodbus.client import tcp

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True


# TODO: Get name of charge controller model
# The following is a hard coded TriStar register table
# https://www.morningstarcorp.com/wp-content/uploads/2014/02/TSMPPT.APP_.Modbus.EN_.10.2.pdf
# Values are tuples of (addr, unit)
CC_REGISTER_TABLE = {
    'Voltage scaling': (1, ''),
    'Current scaling': (3, ''),
    'Battery voltage': (25, 'V'),
    'Array voltage': (28, 'V'),
    'Batter current': (29, 'A'),
    'Array current': (30, 'A'),
    'Controller faults': (45, ''),
    'Charging state': (51, 'kWh'),
    'Charge total': (58, 'kWh'),
    'Output power': (59, 'W'),
    'Total daily charge': (69, 'kWh'),
}

class Client:
    """
    A modbus client for managing connections and provides a more human 
    readable interface for reading state from a server based on the 
    specified register table.
    """
    def __init__(self, host, port, table):
        self.host = host
        self.port = port
        self.table = table
        
    
    def read(self, slave_id=0):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        d = {}

        try:
            for var in self.table.keys():
                resp = tcp.read_holding_registers(slave_id, self.table[var][0], 1)
                print('\n{} - {}'.format(var, resp))
                
                for i in range(0, len(resp)):
                    j = i + 1
                    n = int.from_bytes(resp[i:j], sys.byteorder, signed=True)
                    print('{}:{} - {}'.format(i, j, n))
                
                d[var] = int.from_bytes(resp[9:10], sys.byteorder, signed=True)
        finally:
            sock.close()

        return d

