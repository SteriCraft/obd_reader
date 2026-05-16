# Libraries
import json
import os
import threading
import time
import datetime
from datetime import datetime

# Local files
import obd_connect
import ui
import connection_ui
import vehicle_information_ui
import main_gauges_ui
import custom_gauges_ui
import record_ui


CONFIG_PATH = os.path.expanduser("~/.config/obd_reader/vehicles.json")

class Vehicle:
	def __init__(self):
		self.brand = ""
		self.model = ""
		self.fuel_tank_capacity = 0 # Liters
		self.supported_pids = []

class OBD_Data_Unit:
	def __init__(self):
		self.values = {} # Empty dictionnary
		self.timestamp = datetime.now()

	def set(self, _pid, _value):
		self.values[_pid] = _value

	def get(self, pid):
		return self.values.get(pid, None) # Returns 'None' if the PID isn't present


class OBD_Data_Record_Cycle:
	def __init__(self, _vehicle):
		self.name = ""
		self.vehicle = _vehicle
		self.data = [] # Empty list of OBD_Data_Unit

	def addDataUnit(self, _data_unit):
		self.data.append(_data_unit)

vehicles = []
current_vehicle = Vehicle()

recording = False
data_recordings = []
current_recording = None
last_data = None

followed_PIDs = []
main_window_default_PIDs = [0x03, 0x04, 0x05, 0x0C, 0x0D, 0x11, 0x2F]


# ======= INTERNAL DATA METHODS =======
def add_vehicle(_new_vehicle):
	if _new_vehicle.model == "" or _new_vehicle.brand == "":
		return False

	vehicles.append(_new_vehicle)
	save_vehicles_data()

	return True



def has_vehicle(_brand, _model):
	return any(v.brand == _brand and v.model == _model for v in vehicles)



def remove_vehicle(_vehicle):
	if _vehicle not in vehicles:
		return False

	vehicles.remove(_vehicle)
	save_vehicles_data()

	return True



# ======= UPDATE =======
next_thread_root_after_ID = None

def update_data_thread_fun():
	global last_data
	global next_thread_root_after_ID

	last_data = OBD_Data_Unit()

	if recording:
		retrieve_record_selected_PID_data()
		current_recording.addDataUnit(last_data)
	else:
		retrieve_ELM_data()
		retrieve_main_window_PID_data()

	try:
		ui.root.after(0, ui.update_data) # Main thread updates UI
		
		if not obd_connect.is_connection_lost():
			next_thread_root_after_ID = ui.root.after(10, start_update_data_cycle) # 100 Hz, will create the next thread and this one dies
	except tk.TclError:
		pass



def start_update_data_cycle():
	if obd_connect.is_connection_lost():
		ui.root.after(0, lambda: connection_ui.disconnect(True))
		return

	update_thread = threading.Thread(target = update_data_thread_fun)
	update_thread.daemon = True

	update_thread.start()



def retrieve_ELM_data():
	if not obd_connect.is_connection_lost():
		# Battery voltage
		voltage = obd_connect.get_battery_voltage()

		if voltage != "NaN":
			last_data.set("BATT_VOLT", voltage)



def retrieve_main_window_PID_data():
	# PIDs to retrieve: 2F, 03, 0C, 0D, 11, 04, 05, 4 user selected PIDs
	# Corresponding to: Fuel level, fuel system status, rpm, speed, throttle position, engine load, coolant temperature + user selected PIDs

	global followed_PIDs

	followed_PIDs = main_window_default_PIDs.copy()

	# Adding user selected PIDs in the main window
	followed_PIDs.append(custom_gauges_ui.custom_gauge1_selected_PID)
	followed_PIDs.append(custom_gauges_ui.custom_gauge2_selected_PID)
	followed_PIDs.append(custom_gauges_ui.custom_gauge3_selected_PID)
	followed_PIDs.append(custom_gauges_ui.custom_gauge4_selected_PID)

	for pid in followed_PIDs:
		if not obd_connect.is_connection_lost():
			if obd_connect.is_PID_supported(pid):
				value = obd_connect.retrieve_PID_value(pid)

				if value != "NaN":
					last_data.set(pid, value)



def retrieve_record_selected_PID_data():
	for pid in record_ui.selected_PIDs:
		if not obd_connect.is_connection_lost():
			if obd_connect.is_PID_supported(pid):
				value = obd_connect.retrieve_PID_value(pid)

				if value != "NaN":
					last_data.set(pid, value)



# ======= DISK METHODS =======
def save_vehicles_data():
	os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok = True)

	data = [
		{
			"brand": v.brand,
			"model": v.model,
			"fuel_tank_capacity": v.fuel_tank_capacity
		}
		for v in vehicles
	]
	
	with open(CONFIG_PATH, "w") as f:
		json.dump(data, f, indent = 4)



def load_vehicles_data():
	if not os.path.exists(CONFIG_PATH):
		return # No saved data
	
	with open (CONFIG_PATH, "r") as f:
		data = json.load(f)

		for entry in data:
			v = Vehicle()

			v.brand = entry.get("brand", "")
			v.model = entry.get("model", "")
			v.fuel_tank_capacity = entry.get("fuel_tank_capacity", "")

			vehicles.append(v)
		
		return vehicles



# ======= DATA RECORDING METHODS =======
def start_recording_data():
	global recording
	global current_recording

	recording = True
	data_recordings.append(OBD_Data_Record_Cycle(current_vehicle))
	current_recording = data_recordings[-1]



def stop_recording_data():
	global recording
	global current_recording

	recording = False
	current_recording = None
