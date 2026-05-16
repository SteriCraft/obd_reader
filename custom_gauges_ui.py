# Libraries
import tkinter as tk
from tkinter import ttk

# Local files
import obd_connect
import ui
import data


custom_gauge1_selected_PID = -1
custom_gauge2_selected_PID = -1
custom_gauge3_selected_PID = -1
custom_gauge4_selected_PID = -1

custom_gauges_frame = None

user_selected_gauge1_frame = None
user_selected_gauge2_frame = None
user_selected_gauge3_frame = None
user_selected_gauge4_frame = None

user_selected_gauge1_combo = None
user_selected_gauge2_combo = None
user_selected_gauge3_combo = None
user_selected_gauge4_combo = None

user_selected_gauge1_data_val = None
user_selected_gauge2_data_val = None
user_selected_gauge3_data_val = None
user_selected_gauge4_data_val = None


def setup():
	global custom_gauges_frame

	global user_selected_gauge1_frame
	global user_selected_gauge2_frame
	global user_selected_gauge3_frame
	global user_selected_gauge4_frame

	global user_selected_gauge1_combo
	global user_selected_gauge2_combo
	global user_selected_gauge3_combo
	global user_selected_gauge4_combo

	global user_selected_gauge1_data_val
	global user_selected_gauge2_data_val
	global user_selected_gauge3_data_val
	global user_selected_gauge4_data_val

	custom_gauges_frame = tk.Frame(ui.center_frame)

	user_selected_gauge1_frame = tk.LabelFrame(custom_gauges_frame, text = "User selected value", width = 336, height = 245)
	user_selected_gauge2_frame = tk.LabelFrame(custom_gauges_frame, text = "User selected value", width = 336, height = 245)
	user_selected_gauge3_frame = tk.LabelFrame(custom_gauges_frame, text = "User selected value", width = 336, height = 244)
	user_selected_gauge4_frame = tk.LabelFrame(custom_gauges_frame, text = "User selected value", width = 336, height = 244)

	user_selected_gauge1_combo = ttk.Combobox(user_selected_gauge1_frame)
	user_selected_gauge2_combo = ttk.Combobox(user_selected_gauge2_frame)
	user_selected_gauge3_combo = ttk.Combobox(user_selected_gauge3_frame)
	user_selected_gauge4_combo = ttk.Combobox(user_selected_gauge4_frame)

	user_selected_gauge1_combo.bind("<<ComboboxSelected>>", on_custom_gauge1_selection_changed)
	user_selected_gauge2_combo.bind("<<ComboboxSelected>>", on_custom_gauge2_selection_changed)
	user_selected_gauge3_combo.bind("<<ComboboxSelected>>", on_custom_gauge3_selection_changed)
	user_selected_gauge4_combo.bind("<<ComboboxSelected>>", on_custom_gauge4_selection_changed)

	user_selected_gauge1_data_val = tk.Label(user_selected_gauge1_frame, text = "--", font = ("Courier", 12))
	user_selected_gauge2_data_val = tk.Label(user_selected_gauge2_frame, text = "--", font = ("Courier", 12))
	user_selected_gauge3_data_val = tk.Label(user_selected_gauge3_frame, text = "--", font = ("Courier", 12))
	user_selected_gauge4_data_val = tk.Label(user_selected_gauge4_frame, text = "--", font = ("Courier", 12))


def pack():
	custom_gauges_frame.grid(row = 0, column = 1, rowspan = 2, padx = 10)

	user_selected_gauge1_combo.pack(anchor = "n", padx = 10, pady = 10, fill = tk.X)
	user_selected_gauge2_combo.pack(anchor = "n", padx = 10, pady = 10, fill = tk.X)
	user_selected_gauge3_combo.pack(anchor = "n", padx = 10, pady = 10, fill = tk.X)
	user_selected_gauge4_combo.pack(anchor = "n", padx = 10, pady = 10, fill = tk.X)

	user_selected_gauge1_data_val.pack(anchor = "n", padx = 10, pady = 60)
	user_selected_gauge2_data_val.pack(anchor = "n", padx = 10, pady = 60)
	user_selected_gauge3_data_val.pack(anchor = "n", padx = 10, pady = 60)
	user_selected_gauge4_data_val.pack(anchor = "n", padx = 10, pady = 60)

	user_selected_gauge1_frame.pack_propagate(False)
	user_selected_gauge2_frame.pack_propagate(False)
	user_selected_gauge3_frame.pack_propagate(False)
	user_selected_gauge4_frame.pack_propagate(False)

	user_selected_gauge1_frame.grid(row = 0, column = 1, padx = 5, pady = 5)
	user_selected_gauge2_frame.grid(row = 0, column = 2, padx = 5, pady = 5)
	user_selected_gauge3_frame.grid(row = 1, column = 1, padx = 5, pady = 5)
	user_selected_gauge4_frame.grid(row = 1, column = 2, padx = 5, pady = 5)



def on_custom_gauge1_selection_changed(event):
	global custom_gauge1_selected_PID

	if user_selected_gauge1_combo.get() != "":
		custom_gauge1_selected_PID = int(user_selected_gauge1_combo.get()[:2], 16)
	else:
		custom_gauge1_selected_PID = -1



def on_custom_gauge2_selection_changed(event):
	global custom_gauge2_selected_PID

	if user_selected_gauge1_combo.get() != "":
		custom_gauge2_selected_PID = int(user_selected_gauge2_combo.get()[:2], 16)
	else:
		custom_gauge2_selected_PID = -1



def on_custom_gauge3_selection_changed(event):
	global custom_gauge3_selected_PID

	if user_selected_gauge1_combo.get() != "":
		custom_gauge3_selected_PID = int(user_selected_gauge3_combo.get()[:2], 16)
	else:
		custom_gauge3_selected_PID = -1



def on_custom_gauge4_selection_changed(event):
	global custom_gauge4_selected_PID

	if user_selected_gauge4_combo.get() != "":
		custom_gauge4_selected_PID = int(user_selected_gauge4_combo.get()[:2], 16)
	else:
		custom_gauge4_selected_PID = -1



def update():
	if custom_gauge1_selected_PID != -1:
		obd_response = data.last_data.get(custom_gauge1_selected_PID)
		user_selected_gauge1_data_val.config(text = f"{obd_response.value}" if obd_response != None else "NaN")

	if custom_gauge2_selected_PID != -1:
		obd_response = data.last_data.get(custom_gauge2_selected_PID)
		user_selected_gauge2_data_val.config(text = f"{obd_response.value}" if obd_response != None else "NaN")

	if custom_gauge3_selected_PID != -1:
		obd_response = data.last_data.get(custom_gauge3_selected_PID)
		user_selected_gauge3_data_val.config(text = f"{obd_response.value}" if obd_response != None else "NaN")

	if custom_gauge4_selected_PID != -1:
		obd_response = data.last_data.get(custom_gauge4_selected_PID)
		user_selected_gauge4_data_val.config(text = f"{obd_response.value}" if obd_response != None else "NaN")



def reset():
	custom_gauge1_selected_PID = -1
	custom_gauge2_selected_PID = -1
	custom_gauge3_selected_PID = -1
	custom_gauge4_selected_PID = -1

	user_selected_gauge1_combo["values"] = []
	user_selected_gauge2_combo["values"] = []
	user_selected_gauge3_combo["values"] = []
	user_selected_gauge4_combo["values"] = []

	user_selected_gauge1_combo.set("")
	user_selected_gauge2_combo.set("")
	user_selected_gauge3_combo.set("")
	user_selected_gauge4_combo.set("")

	user_selected_gauge1_data_val.config(text = "--")
	user_selected_gauge2_data_val.config(text = "--")
	user_selected_gauge3_data_val.config(text = "--")
	user_selected_gauge4_data_val.config(text = "--")



def fill_custom_cauge_combobox(_combo, _defautIndex):
	availablePIDs = []
	alreadyUsedPIDs = [0x03, 0x04, 0x05, 0x0C, 0x0D, 0x11, 0x2F] # In default window

	for pid, description in data.current_vehicle.supported_pids:
		if not any(usedPID == pid for usedPID in alreadyUsedPIDs):
			hexPIDstr = ("0" if pid < 16 else "") + hex(pid)[2:].upper() # Hexadecimal string without the "0x" prefix
			availablePIDs.append(f"{hexPIDstr}: {description}")

	_combo["values"] = availablePIDs

	if _defautIndex < len(availablePIDs):
		_combo.set(availablePIDs[_defautIndex])
	elif len(availablePIDs) > 0:
		_combo.set(availablePIDs[0])
	else:
		_combo.set("")



def fill_custom_gauges_selections():
	fill_custom_cauge_combobox(user_selected_gauge1_combo, 0)
	fill_custom_cauge_combobox(user_selected_gauge2_combo, 1)
	fill_custom_cauge_combobox(user_selected_gauge3_combo, 2)
	fill_custom_cauge_combobox(user_selected_gauge4_combo, 3)

	on_custom_gauge1_selection_changed(None)
	on_custom_gauge2_selection_changed(None)
	on_custom_gauge3_selection_changed(None)
	on_custom_gauge4_selection_changed(None)
