import serial_conn
from enum import Enum
from flask import current_app, g


def obtainInputRegister():
    if 'in_register' not in g:
        serial = serial_conn.obtain()
        g.in_register = InRegister(serial)

    return g.in_register


def close_in_reg(e=None):
    in_register = g.pop('in_register', None)


class Addr(Enum):
    YEAR = 1

    @staticmethod
    def valid(addr):
        if addr.value in Addr.__members__:
            current_app.logger.log("An error occurred. Expected command to be one of %, Got: %", list(Addr), addr)
            return False
        return True


class Func(Enum):
    READ = 6


class InRegister:
    def __init__(self, serial):
        self.serial_conn = serial

    def read_val(self, addr, num, slave=1):
        if addr.value in Addr.__members__:
            current_app.logger.log("An error occurred. Expected command to be one of %, Got: %", list(Addr), addr)
            return None

        slave = f"{slave}".rjust(2, "0")
        func = f"{Func.READ.value}".rjust(2, "0")
        addr = f"{addr.value}".rjust(4, "0")
        num = f"{num}".rjust(4, "0")

        content = f"{slave}{func}{addr}{num}"
        self.serial_conn.send(content)
        return self.serial_conn.receive()


def obtainHoldRegister():
    if 'hold_register' not in g:
        serial = serial_conn.obtain()
        g.hold_register = HoldRegister(serial)

    return g.hold_register


def close_hold_reg(e=None):
    hold_register = g.pop('hold_register', None)


class Addr(Enum):
    YEAR = 1

    @staticmethod
    def valid(addr):
        if addr.value in Addr.__members__:
            current_app.logger.log("An error occurred. Expected command to be one of %, Got: %", list(Addr), addr)
            return False
        return True


class Func(Enum):
    READ = 6
    WRITE = 6


class HoldRegister:
    def __init__(self, serial):
        self.serial_conn = serial

    def read_val(self, addr, num, slave=1):
        if not Addr.valid(addr):
            return None

        slave = f"{slave}".rjust(2, "0")
        func = f"{Func.READ.value}".rjust(2, "0")
        addr = f"{addr.value}".rjust(4, "0")
        num = f"{num}".rjust(4, "0")

        content = f"{slave}{func}{addr}{num}"
        self.serial_conn.send(content)
        return self.serial_conn.receive()

    def write_val(self, addr, val, slave=1):
        if not Addr.valid(addr):
            return None

        slave = f"{slave}".rjust(2, "0")
        func = f"{Func.WRITE.value}".rjust(2, "0")
        addr = f"{addr.value}".rjust(4, "0")
        val = f"{val}".rjust(4, "0")

        content = f"{slave}{func}{addr}{val}"
        self.serial_conn.send(content)
        return self.serial_conn.receive()
