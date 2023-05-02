from flask import Flask, render_template, redirect
import db_manager
import sensor
import registers
import serial_conn

app = Flask(__name__)
app.config.from_object('config')


@app.teardown_appcontext
def close_connections(exception):
	db_manager.close()
	sensor.close()
	registers.close_in_reg()
	registers.close_hold_reg()
	serial_conn.close()


@app.route('/')
def homepage():
	db = db_manager.get()

	records = db.inp_register.fetch_all()

	return render_template('pages/home.html', records=records)


@app.route('/read-sensor', methods=['POST'])
def read_sensor():
	db = db_manager.get()
	s = sensor.get()

	sensor_time = s.fetch_time()
	sensor_state = s.fetch_state()

	db.inp_register.insert(sensor_time, sensor_state)

	return redirect('/')


# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
	app.run()
