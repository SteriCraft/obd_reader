# Libraries
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Local files
import obd_connect
import ui
import main_gauges_ui
import custom_gauges_ui
import vehicle_information_ui
import pending_dtc_ui
import vehicles_ui
import record_ui
import data


conn_frame = None
status_frame = None
protocol_frame = None
buttons_frame = None

elm_status_label = None
elm_status_label_val = None

obd_status_label = None
obd_status_label_val = None

car_status_label = None
car_status_label_val = None

port_status_label = None
port_status_label_val = None

baudrate_status_label = None
baudrate_status_label_val = None

protocol_status_label = None
protocol_status_label_val = None

record_button = None
disconnect_button = None



def setup():
	global conn_frame
	global labels_frame
	global status_frame
	global protocol_frame
	global buttons_frame

	global elm_status_label
	global elm_status_label_val

	global obd_status_label
	global obd_status_label_val

	global car_status_label
	global car_status_label_val

	global port_status_label
	global port_status_label_val

	global baudrate_status_label
	global baudrate_status_label_val

	global protocol_status_label
	global protocol_status_label_val

	global record_button
	global disconnect_button

	conn_frame = tk.LabelFrame(ui.top_frame, text = "Connection", width = 526, height = 170)
	labels_frame = tk.Frame(conn_frame)
	status_frame = tk.Frame(labels_frame)
	protocol_frame = tk.Frame(labels_frame)
	buttons_frame = tk.Frame(conn_frame)

	elm_status_label = tk.Label(status_frame, text = "ELM327 adapter:")
	elm_status_label_val = tk.Label(status_frame, text = "Not connected", fg = "red")

	obd_status_label = tk.Label(status_frame, text = "OBD port:")
	obd_status_label_val = tk.Label(status_frame, text = "Not connected", fg = "red")

	car_status_label = tk.Label(status_frame, text = "Car:")
	car_status_label_val = tk.Label(status_frame, text = "Unknown", fg = "orange")

	port_status_label = tk.Label(protocol_frame, text = "Port:")
	port_status_label_val = tk.Label(protocol_frame, text = "--")

	baudrate_status_label = tk.Label(protocol_frame, text = "Baudrate:")
	baudrate_status_label_val = tk.Label(protocol_frame, text = "--")

	protocol_status_label = tk.Label(protocol_frame, text = "Protocol:")
	protocol_status_label_val = tk.Label(protocol_frame, text = "--")

	record_button = tk.Button(buttons_frame, text = "Record", command = record_ui.open_record_dialog, state = tk.DISABLED)
	disconnect_button = tk.Button(buttons_frame, text = "Disconnect", command = disconnect, state = tk.DISABLED)



def pack():
	conn_frame.pack_propagate(False)
	conn_frame.pack(side = tk.LEFT, anchor = "nw", padx = 20, pady = 10)
	labels_frame.pack()
	status_frame.pack(side = tk.LEFT, anchor = "n", padx = 20)
	protocol_frame.pack(side = tk.LEFT, anchor = "n", padx = 20) # LEFT again so it "stacks" from left to right
	buttons_frame.pack(pady = (10, 0))

	elm_status_label.grid(row = 0, column = 0, sticky = "w", padx = 5)
	elm_status_label_val.grid(row = 0, column = 1, sticky = "w")

	obd_status_label.grid(row = 1, column = 0, sticky = "w", padx = 5)
	obd_status_label_val.grid(row = 1, column = 1, sticky = "w")

	car_status_label.grid(row = 2, column = 0, sticky = "w", padx = 5)
	car_status_label_val.grid(row = 2, column = 1, sticky = "w")

	port_status_label.grid(row = 0, column = 0, sticky = "w", padx = 5)
	port_status_label_val.grid(row = 0, column = 1, sticky = "w")

	baudrate_status_label.grid(row = 1, column = 0, sticky = "w", padx = 5)
	baudrate_status_label_val.grid(row = 1, column = 1, sticky = "w")

	protocol_status_label.grid(row = 2, column = 0, sticky = "w", padx = 5)
	protocol_status_label_val.grid(row = 2, column = 1, sticky = "w")

	record_button.pack(side = tk.LEFT)
	disconnect_button.pack(side = tk.LEFT)



def update_status_labels(_connectionStatus, _port = "--", _baudrate = "--", _protocol = "--", _afterConnect = False): # Also changes connection related buttons status
	match _connectionStatus:
		case obd_connect.OBDStatus.NOT_CONNECTED:
			elm_status_label_val.config(text = "Failed" if _afterConnect else "Not connected", fg = "red")
			obd_status_label_val.config(text = "Failed" if _afterConnect else "Not connected", fg = "red")
			car_status_label_val.config(text = "Unknown", fg = "orange")

		case obd_connect.OBDStatus.ELM_CONNECTED:
			elm_status_label_val.config(text = "Connected", fg = "green")
			obd_status_label_val.config(text = "Failed" if _afterConnect else "Not connected", fg = "red")
			car_status_label_val.config(text = "Unknown", fg = "orange")

		case obd_connect.OBDStatus.OBD_CONNECTED:
			elm_status_label_val.config(text = "Connected", fg = "green")
			obd_status_label_val.config(text = "Connected", fg = "green")
			car_status_label_val.config(text = "Ignition off", fg = "orange")

		case obd_connect.OBDStatus.CAR_CONNECTED:
			elm_status_label_val.config(text = "Connected", fg = "green")
			obd_status_label_val.config(text = "Connected", fg = "green")
			car_status_label_val.config(text = "Ignition on", fg = "green")

		case _:
			elm_status_label_val.config(text = "Error", fg = "red")
			obd_status_label_val.config(text = "Error", fg = "red")
			car_status_label_val.config(text = "Error", fg = "red")

	if _connectionStatus != obd_connect.OBDStatus.NOT_CONNECTED:
		port_status_label_val.config(text = f"{_port}")
		baudrate_status_label_val.config(text = f"{_baudrate}")
		protocol_status_label_val.config(text = f"{_protocol}")

		record_button.config(state = tk.NORMAL)
		disconnect_button.config(state = tk.NORMAL)
	else:
		port_status_label_val.config(text = "--")
		baudrate_status_label_val.config(text = "--")
		protocol_status_label_val.config(text = "--")

		record_button.config(state = tk.DISABLED)
		disconnect_button.config(state = tk.DISABLED)



def open_connection_dialog():
	dialog = tk.Toplevel(ui.root)

	dialog.title("Connection")
	dialog.geometry("300x200")
	dialog.resizable(False, False)

	dialog.transient(ui.root)
	dialog.grab_set() # Forbids interactions with the main window
	dialog.lift() # Shows up above all other windows already opened
	dialog.focus_force() # Catches keyboard focus
	dialog.protocol("WM_DELETE_WINDOW", ui.root.destroy) # Closing the dialog will close the whole program

	dialog.columnconfigure(0, weight = 1)
	dialog.columnconfigure(1, weight = 1)

	def on_connect():
		port = port_combo.get().strip()
		baudrate = baudrate_combo.get().strip()
		protocol = get_selected_protocol(protocol_combo)
		protocol_str = protocol_combo.get().strip()

		if connect(port, baudrate, protocol, protocol_str):
			dialog.destroy()
		else:
			info_label.config(text = "Connection failed")

	def on_baudrate_selection_changed(event):
		protocol_combo.config(state = tk.DISABLED if baudrate_combo.get() == "Auto" else tk.NORMAL)

	# COM port combobox
	port_combo_label = tk.Label(dialog, text="COM Port:")
	port_combo = ttk.Combobox(dialog, width = 20, state = tk.NORMAL)

	port_combo_label.grid(row = 0, column = 0, sticky = "e", padx = 5, pady = (20, 5))
	port_combo.grid(row = 0, column = 1, sticky = "w", padx = 5, pady = (20, 5))

	# Baudrates combobox
	baudrate_combo_label = tk.Label(dialog, text = "Baudrate:")
	baudrate_combo = ttk.Combobox(dialog, width = 20, state = tk.NORMAL)

	baudrate_combo_label.grid(row = 1, column = 0, sticky = "e", padx = 5, pady = 5)
	baudrate_combo.grid(row = 1, column = 1, sticky = "w", padx = 5)
	baudrate_combo.bind("<<ComboboxSelected>>", on_baudrate_selection_changed)

	# Protocols combobox
	protocol_combo_label = tk.Label(dialog, text = "Protocol:")
	protocol_combo = ttk.Combobox(dialog, width = 20, state = tk.DISABLED)

	protocol_combo_label.grid(row = 2, column = 0, sticky = "e", padx = 5, pady = 5)
	protocol_combo.grid(row = 2, column = 1, sticky = "w", padx = 5)

	# Buttons
	buttons_frame = tk.Frame(dialog)
	buttons_frame.grid(row = 3, column = 0, columnspan = 2, pady = (20, 5))

	refresh_ports_button = tk.Button(buttons_frame, text = "Refresh ports", command = lambda: refresh_ports(port_combo))
	connect_button = tk.Button(buttons_frame, text = "Connect", command = on_connect)

	refresh_ports_button.pack(side = tk.LEFT, padx = 5)
	connect_button.pack(side = tk.RIGHT, padx = 5)

	# Information label
	info_label = tk.Label(dialog, text = "", fg = "red")
	info_label.grid(row = 4, columnspan = 2)

	load_connection_dialog(port_combo, baudrate_combo, protocol_combo)



def refresh_ports(_combo):
	ports = obd_connect.get_ports()
	_combo["values"] = ports

	usb_port = next((port for port in ports if "ttyUSB" in port), None)
	_combo.set(usb_port if usb_port else ports[0])



def load_baudrates(_combo):
	_combo["values"] = obd_connect.baudrates_list
	_combo.set(obd_connect.baudrates_list[0])



def load_protocols(_combo):
	_combo["values"] = obd_connect.protocols_list
	_combo.set(obd_connect.protocols_list[0])



def get_selected_protocol(_protocol_combo):
	# Protocol ID 0 for OBD-python library is "SAE J1850 PWM"
	# Protocol autoselect option is ID 3, aka "ISO 9141-2"
	# The first protocol, "SAE J1850 PWM", is 1, and so on

	return 3 if (_protocol_combo.current() == 0) else _protocol_combo.current()



def load_connection_dialog(_port_combo, _baudrate_combo, _protocol_combo):
	refresh_ports(_port_combo)
	load_baudrates(_baudrate_combo)
	load_protocols(_protocol_combo)



def connect(_port, _baudrate, _protocol, _protocol_str):
	pending_dtc_ui.dtcs_table.delete(*pending_dtc_ui.dtcs_table.get_children()) # Empty the table
	success = obd_connect.connect(_port, _baudrate, _protocol)
	update_status_labels(obd_connect.get_connection_status(), _port, _baudrate, _protocol_str, True)

	if success:
		pending_dtc_ui.reset_dtcs_table()
		vehicles_ui.open_choose_vehicle_dialog()

	return success



def disconnect(_connection_lost = False):
	obd_connect.disconnect()
	
	update_status_labels(obd_connect.get_connection_status())
	main_gauges_ui.reset()
	custom_gauges_ui.reset()
	vehicle_information_ui.reset()

	data.stop_recording_data()

	if record_ui.raw_data_dialog != None:
		record_ui.raw_data_dialog.destroy()

	if record_ui.record_dialog != None:
		record_ui.record_dialog.destroy()

	open_connection_dialog()

	if _connection_lost:
		messagebox.showwarning("Warning", "Connection lost")
