# Libraries
import json
import os
import threading
import time
from time import sleep
import datetime
from datetime import datetime
import copy
from copy import copy

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
		self.values = {} # Empty dictionnary (pid, obd_response or value)
		self.timestamp = datetime.now()

	def set(self, _pid, _value):
		self.values[_pid] = _value

	def get(self, pid):
		return self.values.get(pid, None) # Returns 'None' if the PID isn't present


class OBD_Data_Record_Cycle:
	def __init__(self, _vehicle, _recorded_PIDs):
		self.name = ""
		self.vehicle = _vehicle
		self.recorded_PIDs = [pid for pid in _recorded_PIDs if pid != 0] # Given list holds 0s for unselected PIDs
		self.data = [] # Empty list of OBD_Data_Unit

	def addDataUnit(self, _data_unit):
		self.data.append(_data_unit)

vehicles = []
current_vehicle = Vehicle()

recording = False
data_recordings = []
current_recording = None
temp_data = None # Used to store data as it is retrieved by the thread, the UI doesn't use it
last_data = None # Last available data for the UI

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
update_thread = None # Keeps a reference to the thread
update_data_flag = False # Tells the thread when to stop
update_frequency_target = 20 # Hz

def update_data_thread_fun():
	global temp_data
	global update_data_flag
	global last_data

	while update_data_flag:
		start = time.time()

		temp_data = OBD_Data_Unit() # Holds temporary data, not for the UI

		if recording:
			retrieve_record_selected_PID_data()
			current_recording.addDataUnit(temp_data)
		else:
			retrieve_ELM_data()
			retrieve_main_window_PID_data()

		last_data = copy(temp_data) # Data is now available for the UI to use

		# Stop updating if the connection is lost
		if obd_connect.is_connection_lost():
			ui.root.after(0, lambda: connection_ui.disconnect(True))
			update_data_flag = False
			break

		# Frequency target management
		elapsed = (time.time() - start) * 1000 # milliseconds
		sleepTime = (1000.0 / update_frequency_target) - elapsed

		if sleepTime > 0: # No need to wait if it was too long
			sleep(sleepTime / 1000) # seconds

	print("Data update thread stops")



def start_update_cycle():
	global update_thread
	global update_data_flag

	if update_thread != None and update_thread.is_alive():
		print("[OBD Reader Error]: Data update thread is already running")
		return

	update_data_flag = True

	update_thread = threading.Thread(target = update_data_thread_fun)
	update_thread.daemon = True
	update_thread.start()



def stop_update_cycle():
	global update_data_flag

	update_data_flag = False

	if update_thread != None and update_thread.is_alive():
		update_thread.join()



def retrieve_ELM_data():
	if obd_connect.is_connection_lost():
		return

	# Battery voltage
	voltage = obd_connect.get_battery_voltage()

	if voltage != "NaN":
		temp_data.set("BATT_VOLT", voltage)



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
		if obd_connect.is_connection_lost():
			return

		if obd_connect.is_PID_supported(pid):
			value = obd_connect.retrieve_PID_value(pid)

			if value != "NaN":
				temp_data.set(pid, value)



def retrieve_record_selected_PID_data():
	for pid in record_ui.selected_PIDs:
		if obd_connect.is_connection_lost():
			return

		if obd_connect.is_PID_supported(pid):
			value = obd_connect.retrieve_PID_value(pid)

			if value != "NaN":
				temp_data.set(pid, value)



def get_last_PID_data(_pid):
	if last_data == None:
		return None

	return last_data.get(_pid)



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
	data_recordings.append(OBD_Data_Record_Cycle(current_vehicle, record_ui.selected_PIDs))
	current_recording = data_recordings[-1]



def stop_recording_data():
	global recording
	global current_recording

	recording = False
	current_recording = None
