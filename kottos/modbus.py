import socket
import sys

from umodbus import conf
from umodbus.client import tcp

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True

# See table 4275-1 for details
RESTING_REASONS = {
    1: "Anti-Click. Not enough power available (Wake Up)",
    2: "Insane Ibatt Measurement (Wake Up)",
    3: "Negative Current (load on PV input ?) (Wake Up)",
    4: "PV Input Voltage lower than Battery V (Vreg state)",
    5: "Too low of power out and Vbatt below set point for > 90 seconds",
    6: "FET temperature too high (Cover is on maybe ?)",
    7: "Ground Fault Detected",
    8: "Arc Fault Detected",
    9: "Too much negative current while operating (backfeed from battery out of PV input)",
    10: "Battery is less than 8.0 Volts",
    11: "PV input is available but V is rising too slowly. Low Light or bad connection (Solar mode)",
    12: "Voc has gone down from last Voc or low light. Re-check (Solar mode)",
    13: "Voc has gone up from last Voc enough to be suspicious. Re-check (Solar mode)",
    14: "Voc has gone down from last Voc or low light. Re-check (Solar mode)",
    15: "Voc has gone up from last Voc enough to be suspicious. Re-check (Solar mode)",
    16: "Mppt MODE is OFF (Usually because user turned it off)",
    17: "PV input is higher than operation range (too high for 150V Classic)",
    18: "PV input is higher than operation range (too high for 200V Classic)",
    19: "PV input is higher than operation range (too high for 250V or 250KS)",
    22: "Average Battery Voltage is too high above set point",
    25: "Battery Voltage too high of Overshoot (small battery or bad cable ?)",
    26: "Mode changed while running OR Vabsorb raised more than 10.0 Volts at once OR Nominal Vbatt changed by modbus command AND MpptMode was ON when changed",
    27: "bridge center == 1023 (R132 might have been stuffed) This turns MPPT Mode to OFF",
    28: "NOT Resting but RELAY is not engaged for some reason",
    29: "ON/OFF stays off because WIND GRAPH is illegal (current step is set for > 100 amps)",
    30: "PkAmpsOverLimit... Software detected too high of PEAK output current",
    31: "AD1CH.IbattMinus > 900 Peak negative battery current > 90.0 amps (Classic 250)",
    32: "Aux 2 input commanded Classic off. for HI or LO (Aux2Function == 15 or 16)",
    33: "OCP in a mode other than Solar or PV-Uset",
    34: "AD1CH.IbattMinus > 900 Peak negative battery current > 90.0 amps (Classic 150, 200)",
    35: "Battery voltage is less than Low Battery Disconnect (LBD) Typically Vbatt is less than 8.5 volts",
}

# See table 4120-1 for details
CHARGE_STATES = {
    0: 'Resting',
    3: 'Absorb',
    4: 'BulkMppt',
    5: 'Float',
    6: 'FloatMppt',
    7: 'Equalize',
    10: 'HyperVoc',
    18: 'EqMppt',
}

# Our table is harded coded using the midnitesolar register map
# http://www.midnitesolar.com/pdfs/classic_register_map_Rev-C5-December-8-2013.pdf
# Values are tuples of (reg, f(x) -> str)
CC_REGISTER_TABLE = {
    'Resting Reason': (4275, lambda x: RESTING_REASONS[int(x)]),
    'Battery Voltage': (4115, lambda x: "{} V".format(float(x) / 10.0)),
    'Input Voltage': (4116, lambda x: "{} V".format(float(x) / 10.0)),
    'Battery Current': (4117, lambda x: "{} A".format(float(x) / 1.0)),
    'Batter Energy': (4118, lambda x: "{} kWh".format(float(x) / 10.0)),
    'Battery Power': (4119, lambda x: "{} W".format(float(x))),
    'Charge State': (4120, lambda x: CHARGE_STATES[int(x)]),
    'Input Current': (4121, lambda x: "{} A".format(float(x) / 10.0)),
    'Last Measured Voltage': (4122, lambda x: "{} V".format(float(x) / 10.0)),
    'Amp Hours': (4125, lambda x: "{} Ah".format(float(x))),
    'Battery Temp': (4132, lambda x: "{}°C".format(float(x) / 10.0)),
    'FET Temp': (4133, lambda x: "{}°C".format(float(x) / 10.0)),
    'PCB Temp': (4134, lambda x: "{}°C".format(float(x) / 10.0)),
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
                print('\n{}({}) - {}'.format(var, self.table[var][0], resp))
                
                for i in range(0, len(resp)):
                    j = i + 1
                    n = int.from_bytes(resp[i:j], sys.byteorder, signed=True)
                    print('{}:{} - {}'.format(i, j, n))
                
                d[var] = self.table[var][1](
                    int.from_bytes(resp[9:10], sys.byteorder, signed=True)
                )
                print('{}: {}'.format(var, d[var]))
        finally:
            sock.close()

        return d

