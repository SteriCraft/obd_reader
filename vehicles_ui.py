# Libraries
import tkinter as tk
from tkinter import ttk

# Local files
import obd_connect
import ui
import connection_ui
import custom_gauges_ui
import vehicle_information_ui
import data


vehicles_list_combo = None
edit_vehicle_button = None
remove_vehicle_button = None
ok_button = None


def load_vehicles_list():
	vehicles_str_list = []

	for vehicle in data.vehicles:
		vehicles_str_list.append(vehicle.get_full_name())

	vehicles_list_combo["values"] = vehicles_str_list
	vehicles_list_combo.set(vehicles_str_list[0] if len(vehicles_str_list) > 0 else "")

	edit_vehicle_button.config(state = tk.NORMAL if len(vehicles_str_list) > 0 else tk.DISABLED)
	remove_vehicle_button.config(state = tk.NORMAL if len(vehicles_str_list) > 0 else tk.DISABLED)
	ok_button.config(state = tk.NORMAL if len(vehicles_str_list) > 0 else tk.DISABLED)



def open_choose_vehicle_dialog(_while_connected = False):
	global vehicles_list_combo
	global edit_vehicle_button
	global remove_vehicle_button
	global ok_button

	def on_close():
		connection_ui.disconnect()
		dialog.destroy()

	dialog = tk.Toplevel(ui.root)

	dialog.title("Choose vehicle")
	dialog.geometry("300x250")
	dialog.resizable(False, False)

	dialog.transient(ui.root) # Ties the dialog to the main window
	dialog.grab_set() # Forbids interactions with the main window
	dialog.lift() # Shows up above all other windows already opened
	dialog.focus_force() # Catches keyboard focus

	if not _while_connected:
		dialog.protocol("WM_DELETE_WINDOW", on_close) # Closing the dialog will close the connection

	def select_vehicle():
		data.current_vehicle = find_selected_vehicle()

		if data.current_vehicle.brand != "":
			vehicle_information_ui.vehicle_brand_label_val.config(text = f"{data.current_vehicle.brand}")

		if data.current_vehicle.model != "":
			vehicle_information_ui.vehicle_model_label_val.config(text = f"{data.current_vehicle.model}")

		if not _while_connected:
			vehicle_information_ui.vehicle_vin_label_val.config(text = f"{obd_connect.get_VIN()}")
			data.current_vehicle.supported_pids = obd_connect.getSupportedPIDs()

			custom_gauges_ui.fill_custom_gauges_selections()
			data.start_update_cycle()
			ui.start_update_cycle()

		dialog.destroy()

	def find_selected_vehicle():
		selection = vehicles_list_combo.get()
		return next((v for v in data.vehicles if f"{v.get_full_name()}" == selection), None)

	# Saved vehicles list
	vehicles_list_label = tk.Label(dialog, text = "Saved vehicles")
	vehicles_list_combo = ttk.Combobox(dialog, width = 20, state = tk.NORMAL)

	# Buttons
	new_vehicle_button = tk.Button(dialog, text = "Create new vehicle", command = lambda: open_edit_vehicle_dialog(dialog))
	edit_vehicle_button = tk.Button(dialog, text = "Edit selected vehicle", command = lambda: open_edit_vehicle_dialog(dialog, find_selected_vehicle()))
	remove_vehicle_button = tk.Button(dialog, text = "Remove selected vehicle", command = lambda: remove_vehicle(find_selected_vehicle()))
	ok_button = tk.Button(dialog, text = "Ok", command = select_vehicle)

	load_vehicles_list()

	# Packing
	vehicles_list_label.pack(pady = (10, 0))
	vehicles_list_combo.pack(pady = (0, 10))

	new_vehicle_button.pack()
	edit_vehicle_button.pack()
	remove_vehicle_button.pack(pady = 5)
	ok_button.pack(pady = 5)



def open_edit_vehicle_dialog(_previous_dialog, _vehicle = None):
	dialog = tk.Toplevel(_previous_dialog)

	dialog.title("Edit vehicle" if _vehicle else "New vehicle")
	dialog.resizable(False, False)

	dialog.transient(_previous_dialog) # Ties the dialog to the previous dialog
	dialog.grab_set() # Forbids interactions with the previous dialog
	dialog.lift() # Shows up above all other windows already opened
	dialog.focus_force() # Catches keyboard focus

	# Make both columns share space equally so things center properly
	dialog.columnconfigure(0, weight = 1)
	dialog.columnconfigure(1, weight = 1)

	def save_button_validity_check(*args):
		if data.has_vehicle(custom_name_var.get()):
			info_label.config(text = "Already exists")
			save_button.config(state = tk.DISABLED)
		else:
			info_label.config(text = "")
			save_button.config(state = tk.NORMAL if custom_name_var.get() != "" else tk.DISABLED)

	def validate_text_input(new_value): # Max 16 characters
		return len(new_value) <= 16

	def validate_fuel_tank_capacity_input(new_value): # Max 200 L
		if new_value == "":
			return True

		return new_value.isdigit() and int(new_value) <= 200

	valid_text_entry_cmd = ui.root.register(validate_text_input)
	valid_fuel_tank_cap_entry_cmd = ui.root.register(validate_fuel_tank_capacity_input)

	# Custom name input field
	custom_name_var = tk.StringVar()
	custom_name_var.set(_vehicle.custom_name if _vehicle else "")
	custom_name_var.trace("w", save_button_validity_check)

	custom_name_label = tk.Label(dialog, text = "*Custom name:")
	custom_name_entry = tk.Entry(dialog, width = 20, textvariable = custom_name_var, state = tk.NORMAL, validate = "key", validatecommand = (valid_text_entry_cmd, "%P"))

	custom_name_label.grid(row = 0, column = 0, sticky = "e", padx = (10, 5), pady = (10, 5))
	custom_name_entry.grid(row = 0, column = 1, sticky = "w", padx = (10, 5), pady = (10, 5))

	# Brand input field
	brand_var = tk.StringVar()
	brand_var.set(_vehicle.brand if _vehicle else "")

	brand_label = tk.Label(dialog, text = "Brand:")
	brand_entry = tk.Entry(dialog, width = 20, textvariable = brand_var, state = tk.NORMAL, validate = "key", validatecommand = (valid_text_entry_cmd, "%P"))

	brand_label.grid(row = 1, column = 0, sticky = "e", padx = (10, 5), pady = (10, 5))
	brand_entry.grid(row = 1, column = 1, sticky = "w", padx = (10, 5), pady = (10, 5))

	# Model input field
	model_var = tk.StringVar()
	model_var.set(_vehicle.model if _vehicle else "")

	model_label = tk.Label(dialog, text = "Model:")
	model_entry = tk.Entry(dialog, width = 20, textvariable = model_var, state = tk.NORMAL, validate = "key", validatecommand = (valid_text_entry_cmd, "%P"))

	model_label.grid(row = 2, column = 0, sticky = "e", padx = (10, 5), pady = 5)
	model_entry.grid(row = 2, column = 1, sticky = "w", padx = (10, 5))

	# Fuel tank capacity input field
	fuel_tank_capacity_label = tk.Label(dialog, text = "Fuel tank (L):")
	fuel_tank_capacity_entry = tk.Entry(dialog, width = 20, state = tk.NORMAL, validate = "key", validatecommand = (valid_fuel_tank_cap_entry_cmd, "%P"))
	fuel_tank_capacity_entry.insert(0, str(_vehicle.fuel_tank_capacity) if _vehicle else "")

	fuel_tank_capacity_label.grid(row = 3, column = 0, sticky = "e", padx = (10, 5), pady = 5)
	fuel_tank_capacity_entry.grid(row = 3, column = 1, sticky = "w", padx = (10, 5))

	# Buttons
	buttons_frame = tk.Frame(dialog)
	buttons_frame.grid(row = 4, column = 0, columnspan = 2, pady = (20, 5))

	# Information label
	info_label = tk.Label(dialog, text = "", fg = "red")
	info_label.grid(row = 5, columnspan = 2, padx = 5, pady = (0, 15))

	def save_vehicle_infos(_custom_name, _brand, _model, _fuel_tank_capacity):
		if _vehicle:
			_vehicle.custom_name = _custom_name
			_vehicle.brand = _brand
			_vehicle.model = _model
			_vehicle.fuel_tank_capacity = _fuel_tank_capacity

			data.save_vehicles_data()
			load_vehicles_list()
		else:
			new_vehicle = data.Vehicle(_custom_name)
			new_vehicle.brand = _brand
			new_vehicle.model = _model
			new_vehicle.fuel_tank_capacity = _fuel_tank_capacity

			if not data.add_vehicle(new_vehicle):
				print("[ERROR]: Failed to save the new vehicle")
			else:
				load_vehicles_list()

		dialog.destroy()

	save_button = tk.Button(buttons_frame, text = "Save", command = lambda: save_vehicle_infos(custom_name_entry.get(), brand_entry.get(), model_entry.get(), fuel_tank_capacity_entry.get()))
	save_button_validity_check()
	cancel_button = tk.Button(buttons_frame, text = "Cancel", command = dialog.destroy)

	save_button.pack(side = tk.LEFT, padx = 5)
	cancel_button.pack(side = tk.RIGHT, padx = 5)



def remove_vehicle(_vehicle):
	if _vehicle == None:
		return

	if data.remove_vehicle(_vehicle):
		load_vehicles_list()
