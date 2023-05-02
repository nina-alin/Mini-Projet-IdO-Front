import datetime
from flask import g

# TODO: se connecter au capteur

def obtain():
	if 'sensor' not in g:
		g.sensor = Sensor(None, None)

	return g.sensor


def close_sensor(e=None):
	sensor = g.pop('sensor', None)


class Sensor:
	def __init__(self, inp_registry, hold_registry):
		self.inp_register = inp_registry
		self.hold_register = hold_registry

	def fetch_time(self):
		current_time = datetime.datetime.now()
		return current_time

	def fetch_state(self):
		return "EN ATTENTE"
