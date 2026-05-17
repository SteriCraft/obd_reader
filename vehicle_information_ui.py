# Libraries
import tkinter as tk
from tkinter import ttk

# Local files
import obd_connect
import ui
import connection_ui
import vehicles_ui
import data


vehicle_infos_frame = None
vehicle_brand_label = None
vehicle_brand_label_val = None
vehicle_model_label = None
vehicle_model_label_val = None
vehicle_vin_label = None
vehicle_vin_label_val = None
vehicle_battery_voltage_label = None
vehicle_battery_voltage_label_val = None
vehicle_fuel_level_label = None
vehicle_fuel_level_label_val = None
vehicle_fuel_sys_status_label = None
vehicle_fuel_sys_status_label_val = None
vehicle_infos_set_button = None
vehicle_supported_PIDs_button = None


def setup():
	global vehicle_infos_frame
	global vehicle_brand_label
	global vehicle_brand_label_val
	global vehicle_model_label
	global vehicle_model_label_val
	global vehicle_vin_label
	global vehicle_vin_label_val
	global vehicle_battery_voltage_label
	global vehicle_battery_voltage_label_val
	global vehicle_fuel_level_label
	global vehicle_fuel_level_label_val
	global vehicle_fuel_sys_status_label
	global vehicle_fuel_sys_status_label_val
	global vehicle_infos_set_button
	global vehicle_supported_PIDs_button

	vehicle_infos_frame = tk.LabelFrame(ui.center_frame, text = "Vehicle information", width = 526, height = 150)

	vehicle_brand_label = tk.Label(vehicle_infos_frame, text = "Brand:")
	vehicle_brand_label_val = tk.Label(vehicle_infos_frame, text = "--")

	vehicle_model_label = tk.Label(vehicle_infos_frame, text = "Model:")
	vehicle_model_label_val = tk.Label(vehicle_infos_frame, text = "--")

	vehicle_vin_label = tk.Label(vehicle_infos_frame, text = "VIN:")
	vehicle_vin_label_val = tk.Label(vehicle_infos_frame, text = "--")

	vehicle_battery_voltage_label = tk.Label(vehicle_infos_frame, text = "Battery voltage:")
	vehicle_battery_voltage_label_val = tk.Label(vehicle_infos_frame, text = "--")

	vehicle_fuel_level_label = tk.Label(vehicle_infos_frame, text = "Fuel level:")
	vehicle_fuel_level_label_val = tk.Label(vehicle_infos_frame, text = "--")

	vehicle_fuel_sys_status_label = tk.Label(vehicle_infos_frame, text = "Fuel system status:")
	vehicle_fuel_sys_status_label_val = tk.Label(vehicle_infos_frame, text = "--")

	vehicle_infos_set_button = tk.Button(vehicle_infos_frame, text = "Edit vehicle informations", command = lambda: vehicles_ui.open_choose_vehicle_dialog(True))
	vehicle_supported_PIDs_button = tk.Button(vehicle_infos_frame, text = "See supported PIDs", command = show_supported_PIDs_dialog)



def pack():
	vehicle_infos_frame.grid_propagate(False)
	vehicle_infos_frame.grid(row = 0, column = 0)

	vehicle_brand_label.grid(row = 0, column = 0, sticky = "w", padx = 20, pady = 2)
	vehicle_brand_label_val.grid(row = 0, column = 1)

	vehicle_model_label.grid(row = 1, column = 0, sticky = "w", padx = 20, pady = 2)
	vehicle_model_label_val.grid(row = 1, column = 1)

	vehicle_vin_label.grid(row = 2, column = 0, sticky = "w", padx = 20, pady = 2)
	vehicle_vin_label_val.grid(row = 2, column = 1)

	vehicle_battery_voltage_label.grid(row = 0, column = 2, sticky = "w", padx = 30, pady = 2)
	vehicle_battery_voltage_label_val.grid(row = 0, column = 3)

	vehicle_fuel_level_label.grid(row = 1, column = 2, sticky = "w", padx = 30, pady = 2)
	vehicle_fuel_level_label_val.grid(row = 1, column = 3)

	vehicle_fuel_sys_status_label.grid(row = 2, column = 2, sticky = "w", padx = 30, pady = 2)
	vehicle_fuel_sys_status_label_val.grid(row = 2, column = 3)

	vehicle_infos_set_button.grid(row = 3, column = 0, columnspan = 2, pady = 5)
	vehicle_supported_PIDs_button.grid(row = 3, column = 2, columnspan = 2, pady = 5)



def update(): # Retrieved from the ECU
	# Battery voltage
	battery_voltage = data.get_last_PID_data("BATT_VOLT")

	if battery_voltage != None:
		vehicle_battery_voltage_label_val.config(text = f"{battery_voltage} V")
	else:
		vehicle_battery_voltage_label_val.config(text = "NaN")

	# Fuel level (PID 0x2F)
	fuel_level = data.get_last_PID_data(0x2F)

	if fuel_level != None:
		fuel_level_str = f"{fuel_level.value.magnitude} %"

		data.current_vehicle.fuel_tank_capacity = 45
		if data.current_vehicle.fuel_tank_capacity > 0:
			remaining_fuel = fuel_level.value.magnitude / 100 * data.current_vehicle.fuel_tank_capacity # Liters
			fuel_level_str += f" ({int(remaining_fuel)} L)"

		vehicle_fuel_level_label_val.config(text = fuel_level_str)
	else:
		vehicle_fuel_level_label_val.config(text = "Not supported")
	
	# Fuel system status (PID 0x03)
	fuel_system_status = data.get_last_PID_data(0x03)
	
	if fuel_system_status != None:
		vehicle_fuel_sys_status_label_val.config(text = f"{fuel_system_status}")
	else:
		vehicle_fuel_sys_status_label_val.config(text = "Not supported")



def reset():
	vehicle_brand_label_val.config(text = "--")
	vehicle_model_label_val.config(text = "--")
	vehicle_vin_label_val.config(text = "--")
	vehicle_battery_voltage_label_val.config(text = "--")
	vehicle_fuel_level_label_val.config(text = "--")
	vehicle_fuel_sys_status_label_val.config(text = "--")



def show_supported_PIDs_dialog():
	dialog = tk.Toplevel(ui.root)

	dialog.title("Supported generic PIDs")
	dialog.geometry("550x400")
	dialog.resizable(False, False)

	dialog.transient(ui.root) # Ties the dialog to the main window
	dialog.grab_set() # Forbids interactions with the main window
	dialog.lift() # Shows up above all other windows already opened
	dialog.focus_force() # Catches keyboard focus

	# UI setup
	supported_pids_table = ttk.Treeview(dialog, columns = ("code", "description"), show = "headings", height = 10)
	supported_pids_table.heading("code", text = "PID")
	supported_pids_table.heading("description", text = "Description")
	supported_pids_table.column("code", width = 100, anchor = "center")
	supported_pids_table.column("description", width = 400)

	for code, description in data.current_vehicle.supported_pids:
		supported_pids_table.insert("", tk.END, values = (code, description))

	supported_pids_nb_label = tk.Label(text = f"{len(data.current_vehicle.supported_pids)} PIDs available")

	ok_button = tk.Button(dialog, text = "Ok", command = dialog.destroy)
	
	# Packing
	supported_pids_table.pack(pady = 20)
	supported_pids_nb_label.pack(pady = 20)
	ok_button.pack()
