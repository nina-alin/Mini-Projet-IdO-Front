import datetime
import sqlite3
from flask import current_app, g


def obtain():
	if 'db_instance' not in g:
		g.db_instance = Database()
		g.db_instance.init_schema()
	return g.db_instance


def close_connection(e=None):
	db_instance = g.pop('db_instance', None)

	if db_instance is not None:
		db_instance.close()


class Database:
	def __init__(self):
		self.conn = sqlite3.connect(current_app.config["DB_NAME"])
		self.inp_register = InpRegister(self.conn)

	def init_schema(self):
		self.inp_register.init_schema()

	def close(self):
		self.conn.close()


class InpRegister:
	def __init__(self, conn):
		self.conn = conn

	def init_schema(self):
		cur = self.conn.cursor()
		cur.execute('''
			CREATE TABLE IF NOT EXISTS inp_register(
				id			 INTEGER    PRIMARY KEY    AUTOINCREMENT,
				sensor_date    INTEGER    NOT NULL,
				sensor_state   TEXT       NOT NULL,
				pc_date  INTEGER    NOT NULL       DEFAULT CURRENT_TIMESTAMP
			);
			''')
		self.conn.commit()
		cur.close()

	def insert(self, sensor_date, state):
		cur = self.conn.cursor()
		cur.execute('''
			INSERT INTO inp_register(sensor_date, sensor_state)
			VALUES (?, ?);
		''', (sensor_date.timestamp(), state))
		self.conn.commit()
		cur.close()

	def fetch_all(self, limit=0, offset=0):
		cur = self.conn.cursor()
		if limit > 0:
			result = cur.execute('''
				SELECT *
				FROM inp_register
				LIMIT ?
				OFFSET ?;
			''', (limit, offset))
		else:
			result = cur.execute('''
				SELECT *
				FROM inp_register;
			''')
		records = []
		for record in result.fetchall():
			record[1] = datetime.datetime.fromtimestamp(record[1])
			records.append(record)
		cur.close()
		return records

	def fetch_one(self, identifier):
		cur = self.conn.cursor()
		result = cur.execute('''
			SELECT *
			FROM inp_register
			WHERE id == ?;
		''', identifier)
		cur.close()
		data = result.fetchone()
		data[1] = datetime.datetime.fromtimestamp(data[1])
		return
