# -*- coding: utf-8 -*-
# The above line is needed because ° is not an ASCII symbol

import struct
import sys

from umodbus import conf
from umodbus.client import tcp

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True


class Register:
    """
    A class for describing and manipulating individual modbus registers.
    """
    def __init__(self, name, reg, func, units=None):
        self._name = name
        self._reg = reg
        self._func = func
        self._units = units

    @property
    def name(self):
        return self._name

    @property
    def register(self):
        return self._reg

    @property
    def units(self):
        return self._units

    @property
    def label(self):
        if self.units is None:
            return self.name
        else:
            return '{} ({})'.format(self.name, self.units)

    def read(self, sock, slave_id=0):
        """
        Attempt to read a raw value from the register.
        This function has debugging logging that will print all bytes returned
        from the server.
        """
        # NOTE: Addresses are 0 indexed, but the documented registers are 1 indexed.
        msg = tcp.read_holding_registers(slave_id, self.register - 1, 1)
        resp = tcp.send_message(msg, sock)

        # Extract the single value from the results
        val = resp[0]
        print('{} ({}): {}'.format(self.name, self.register, val))

        return val

    def convert(self, x):
        return self._func(x)


#########################################################################################
#                  MIDNITESOLAR CONSTANTS                                               #
#                                                                                       #
# - Table are hard coded using the midnitesolar register map                            #
# - http://www.midnitesolar.com/pdfs/classic_register_map_Rev-C5-December-8-2013.pdf    #
#########################################################################################

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
    38: "Other charging sources appear to be active",
}

# See table 4120-1 for details
CHARGE_STATES = {
    0: 'Resting',
    1: 'Waking / Starting',
    2: 'Waking / Starting',
    3: 'Absorb',
    4: 'BulkMppt',
    5: 'Float',
    6: 'FloatMppt',
    7: 'Equalize',
    10: 'HyperVoc',
    18: 'EqMppt',
}

# Primary table
MNS_REGISTER_TABLE = [
    Register(
        name='Resting Reason',
        reg=4275,
        func=lambda x: RESTING_REASONS[x],
        units=None,
    ),
    Register(
        name='Battery Voltage',
        reg=4115,
        func=lambda x: float(x) / 10.0,
        units="V",
    ),
    Register(
        name='Input Voltage',
        reg=4116,
        func=lambda x: float(x) / 10.0,
        units="V",
    ),
    Register(
        name='Battery Current',
        reg=4117,
        func=lambda x: float(x) / 1.0,
        units="A",
    ),
    Register(
        name='Batter Energy',
        reg=4118,
        func=lambda x: float(x) / 10.0,
        units="kWh",
    ),
    Register(
        name='Battery Power',
        reg=4119,
        func=lambda x: float(x),
        units="W",
    ),
    Register(
        name='Charge State',
        reg=4120,
        func=lambda x: CHARGE_STATES[x >> 8],
        units=None,
    ),
    Register(
        name='Input Current',
        reg=4121,
        func=lambda x: float(x) / 10.0,
        units="A",
    ),
    Register(
        name='Last Measured Voltage',
        reg=4122,
        func=lambda x: float(x) / 10.0,
        units="V",
    ),
    Register(
        name='Amp Hours',
        reg=4125,
        func=lambda x: float(x),
        units="Ah",
    ),
    Register(
        name='Battery Temp',
        reg=4132,
        func=lambda x: float(x) / 10.0,
        units="°C",
    ),
    Register(
        name='FET Temp',
        reg=4133,
        func=lambda x: float(x) / 10.0,
        units="°C",
    ),
    Register(
        name='PCB Temp',
        reg=4134,
        func=lambda x: float(x) / 10.0,
        units="°C",
    ),
]
