import socket


class Client:
    """
    A modbus client for managing connections and provides a more human
    readable interface for reading state from a server based on the
    specified register table.
    """

    def __init__(self, host, port, table):
        self._host = host
        self._port = port
        self._table = table

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def table(self):
        return self._table

    def scan(self, slave_id=0):
        """
        Reads raw values from the modbus server and converts the
        values to an appropriate format.
        """
        vals = self.read(slave_id)
        return self.convert(vals)

    def read(self, slave_id=0):
        """
        Reads the raw values from the registers specified by the register table.
        Returns a dict with
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        resp = {}

        try:
            for reg in self.table:
                # Read the raw data from the register
                print(reg.label)
                resp[reg.label] = reg.read(sock, slave_id)
        finally:
            sock.close()

        return resp

    def convert(self, vals):
        """
        Converts the raw values passed in to the appropriate format.
        """
        resp = {}

        for reg in self.table:
            try:
                resp[reg.label] = reg.convert(vals[reg.label])
            except KeyError as err:
                print(err)
                resp[reg.label] = "Failed to convert {}".format(vals[reg.label])

        return resp
