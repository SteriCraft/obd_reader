# Libraries
import obd
from obd import OBDStatus

import os
import serial.tools.list_ports

# Local files
import data


connection = None


# ============ CONNECTION DATA ============
baudrates_list = ["Auto", "9600", "19200", "38400", "57600", "115200"]
protocols_list = ["Auto", "SAE J1850 PWM", "SAE J1850 VPW",
				  "ISO 9141-2", "ISO 14230-4 (KWP 5BAUD)",
				  "ISO 14230-4 (KWP FAST)", "ISO 15765-4 (CAN 11/500)",
				  "ISO 15765-4 (CAN 29/500)", "ISO 15765-4 (CAN 11/250)",
				  "ISO 15765-4 (CAN 29/250)", "SAE J1939 (CAN 29/250)"]


def get_ports():
	real_ports = [p.device for p in serial.tools.list_ports.comports()]

	try:
		pts_ports = [f"/dev/pts/{f}" for f in os.listdir("/dev/pts") if f.isdigit()]
		pts_ports.sort()
	except Exception:
		pts_ports = []

	all_ports = real_ports + pts_ports
	return all_ports if all_ports else ["No port found"]



# ============ CONNECTION PROTOCOL ============
def connect(_port, _baudrate, _protocol):
	global connection

	if (_baudrate == "Auto"):
		connection = obd.OBD(_port)
	else:
		if (_protocol == 3): # Protocol auto select
			connection = obd.OBD(_port, _baudrate)
		else:
			_protocol = hex(_protocol)[2:].upper() # Converts protocol to a hexadecimal string without the "0x" prefix, because it expects "1" to "A"
			connection = obd.OBD(_port, _baudrate, _protocol)

	return connection.is_connected()



def get_connection_status():
	if connection == None:
		return OBDStatus.NOT_CONNECTED

	return connection.status()



def is_connected():
	if connection == None:
		return False

	return connection.status() == OBDStatus.CAR_CONNECTED



def is_connection_lost():
	if connection == None:
		return True

	return connection.status() == OBDStatus.NOT_CONNECTED



def disconnect():
	if connection != None:
		connection.close()



# ============ DATA ============
# --- Diagnostic Trouble Codes (DTCs) ---
def getPendingDTCs(): # Mode 03
	response = connection.query(obd.commands.GET_DTC)
	return response.value



def getCurrentDTCs(): # Mode 07
	response = connection.query(obd.commands.GET_CURRENT_DTC)
	return response.value



def clearDTCs(): # Mode 04
	connection.query(obd.commands.CLEAR_DTC)



# --- PIDs ---
def getSupportedPIDs(): # Mode 01, returns a list of tuples of type: (PID, description)
	pidsList = []
	
	if connection.supports(obd.commands.PIDS_A):
		response = connection.query(obd.commands.PIDS_A)
		if not response.is_null():
			pidsList += decodePIDs(response.value)

	if connection.supports(obd.commands.PIDS_B):
		response = connection.query(obd.commands.PIDS_B)
		if not response.is_null():
			pidsList += decodePIDs(response.value, 32)
	
	if connection.supports(obd.commands.PIDS_C):
		response = connection.query(obd.commands.PIDS_C)
		if not response.is_null():
			pidsList += decodePIDs(response.value, 64)

	return pidsList



def decodePIDs(_bitArray, _offset = 0):
	pidsList = []

	for index, bit in enumerate(_bitArray):
		if bit:
			pid = index + _offset + 1 # + 1 because the car response starts at index #1

			if pid % 32 != 0: # Avoid other "Supported PIDs" command
				pidsList.append((pid, obd.commands[1][pid].desc))

	return pidsList



def is_PID_supported(_pid):
	return any(pid == _pid for pid, description in data.current_vehicle.supported_pids)



def get_VIN(): # Mode 09
	response = connection.query(obd.commands.PIDS_9A) # Retrieve available PIDs in mode 09, to check if that PID is available

	if response.is_null():
		return "Not supported"

	if response.value[0] == True: # Check mode 09 VIN PID
		response = connection.query(obd.commands.VIN)
		return response.value

	return "Not supported"



def get_battery_voltage(): # ELM
	response = connection.query(obd.commands.ELM_VOLTAGE)

	if response.is_null():
		return "NaN"

	return response.value.magnitude



def retrieve_PID_value(_pid):
	response = connection.query(obd.commands[1][_pid])

	if response.is_null():
		return "NaN"

	return response # CAUTION: Not the value itself
