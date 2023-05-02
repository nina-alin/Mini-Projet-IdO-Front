import serial
from enum import Enum
from flask import current_app, g


def get():
	if 'serial_port' not in g:
		g.serial_port = SerialPort()
	return g.serial_port


def close(e=None):
	serial_port = g.pop('serial_port', None)

	if serial_port is not None:
		serial_port.close()


class SerialPort:
	def __init__(self):
		self.connection = serial.Serial(
			port=current_app.config['SERIAL_PORT'],
			baudrate=current_app.config['SERIAL_BAUDRATE'],
			parity=current_app.config['SERIAL_PARITY'],
			stopbits=current_app.config['SERIAL_STOPBITS'],
			bytesize=current_app.config['SERIAL_BYTESIZE'],
			timeout=current_app.config['SERIAL_TIMEOUT']
		)

	def close(self):
		self.connection.close()

	def send(self, content):
		lrc = self.calculate_lrc(content)
		cmd = f":{content}{lrc}\r\n"
		current_app.logger.debug("Serial Data send: '%'", cmd)
		cmd = [ord(c) for c in cmd]
		self.connection.write(cmd)

	def receive(self):
		data = self.connection.read_until(expected=serial.LF).decode("utf-8")
		current_app.logger.debug("Serial Data receive: '%'", data)
		return SerialPort.check_error(data)

	@staticmethod
	def calculate_lrc(data):
		lrc = 0
		for i in range(0, len(data), 2):
			lrc = lrc + int(data[i: i + 2], 16)

		lrc = (~lrc + 1) & 0xff
		return f"{lrc:02X}"

	@staticmethod
	def check_error(data):
		current_lrc = data[-4:-2]
		valid_lrc = SerialPort.calculate_lrc(data[1:-4])

		if current_lrc != valid_lrc:
			current_app.logger.error("An error occurred. Expected LRC to be '%', Got: '%'", valid_lrc, current_lrc)
			return None

		if data[3:4] == 83:
			current_app.logger.error(f"An error occurred during reading holding register. Code: %", data[5:7])
			return None
		if data[3:4] == 84:
			current_app.logger.error(f"An error occurred during reading input register. Code: %", data[5:7])
			return None
		if data[3:4] == 86:
			current_app.logger.error(f"An error occurred during writing holding register . Code: %", data[5:7])
			return None
		return data
