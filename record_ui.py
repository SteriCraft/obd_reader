# Libraries
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter

# Local files
import obd_connect
import ui
import data
import commands_units


def make_toggle_button(_parent, _text_, _command = None):
	btn = tk.Button(_parent, text = _text_, relief = tk.RAISED, wraplength = 100, width = 10, height = 4)

	def toggle():
		if btn.config("relief")[-1] == tk.RAISED:
			btn.config(relief = tk.SUNKEN)
		else:
			btn.config(relief = tk.RAISED)

		if _command:
			_command(btn)

	btn.config(command = toggle)
	return btn



# ======= RECORD DIALOG =======
# UI elements
record_dialog = None

pids_selection_container = None
pids_selection_canvas = None
pids_selection_scrollbar = None
pids_selection_frame = None

charts_buttons_frame = None
general_management_frame = None
recordings_list_frame = None

pids_buttons = []

record_stop_button = None
view_raw_data_button = None
export_button = None
recordings_list_label = None
recordings_list_combo = None
record_vehicle_label = None
remove_recording_button = None

# Charts
fig1, fig2 = None, None,
ax1, ax2, ax3, ax4 = None, None, None, None
line1 = None
line2 = None
line3 = None
line4 = None
charts1_2_canvas = None
charts3_4_canvas = None
x_data = []
line1_y_data = []
line2_y_data = []
line3_y_data = []
line4_y_data = []

# Variables
selected_PIDs_count = 0
selected_PIDs = [0, 0, 0, 0] # Fixed length, each element corresponding to a graph line
colors = ["blue", "orange", "red", "green"] # All that for coherences, graph 1 stays blue etc.
selected_recording = None
warning_already_shown = False # Used on graph update, if a PID data cannot be retrieved from the car

def setup_record_dialog():
	global record_dialog

	global pids_selection_container
	global pids_selection_canvas
	global pids_selection_scrollbar
	global pids_selection_frame

	global charts_buttons_frame
	global general_management_frame
	global recordings_list_frame

	global fig1, fig2
	global ax1, ax2, ax3, ax4
	global line1, line2, line3, line4
	global charts1_2_canvas, charts3_4_canvas
	global warning_already_shown

	global record_stop_button
	global view_raw_data_button
	global export_button
	global recordings_list_label
	global recordings_list_combo
	global record_vehicle_label
	global remove_recording_button

	def on_close():
		global warning_already_shown

		if data.recording:
			open_save_recording_dialog(True)
		else:
			if raw_data_dialog != None:
				raw_data_dialog.destroy()

			record_dialog.destroy()

	record_dialog = tk.Toplevel(ui.root)

	record_dialog.title("Record vehicle data")
	record_dialog.geometry("1280x720")
	record_dialog.resizable(False, False)

	record_dialog.transient(ui.root) # Ties the dialog to the main window
	record_dialog.grab_set() # Forbids interactions with the main window
	record_dialog.lift() # Shows up above all other windows already opened
	record_dialog.focus_force() # Catches keyboard focus
	record_dialog.protocol("WM_DELETE_WINDOW", on_close)

	# Necessary to be able to scroll the PID buttons
	pids_selection_container = tk.Frame(record_dialog, width = 130)
	pids_selection_canvas = tk.Canvas(pids_selection_container)
	pids_selection_scrollbar = ttk.Scrollbar(pids_selection_container, orient = tk.VERTICAL, command = pids_selection_canvas.yview)
	pids_selection_frame = tk.Frame(pids_selection_canvas)

	# PID selection buttons
	def on_toggle(btn, _pid):
		global selected_PIDs_count

		if btn.config("relief")[-1] == tk.SUNKEN:
			if selected_PIDs_count >= 4:
				btn.config(relief = tk.RAISED) # Cancel toggle, 4 already toggled
				return

			selected_PIDs_count += 1
			
			# Find a free space to occupy in selected PIDs list
			for i, selected_PID in enumerate(selected_PIDs):
				if selected_PID == 0:
					selected_PIDs[i] = _pid
					btn.config(fg = colors[i])
					break
		else:
			selected_PIDs_count -= 1
			
			# Find the PID to remove in selected PIDs list
			for i, selected_PID in enumerate(selected_PIDs):
				if selected_PID == _pid:
					selected_PIDs[i] = 0
					break

			btn.config(fg = "black")

		record_stop_button.config(state = tk.NORMAL if selected_PIDs_count > 0 else tk.DISABLED)

	# If the dialog was already opened before
	for button in pids_buttons:
		button.destroy()
	pids_buttons.clear()

	for pid, description in data.current_vehicle.supported_pids:
		if commands_units.is_PID_response_recordable.get(pid, False):
			pids_buttons.append(make_toggle_button(pids_selection_frame, f"{("0" if pid < 16 else "") + hex(pid)[2:].upper()}\n{description}", lambda b, p = pid: on_toggle(b, p)))

	charts_buttons_frame = tk.Frame(record_dialog)
	general_management_frame = tk.Frame(charts_buttons_frame)
	recordings_list_frame = tk.Frame(general_management_frame)

	# Charts 1 & 2
	fig1, ax1 = plt.subplots()
	fig1.patch.set_facecolor(record_dialog.cget("bg"))

	ax1.xaxis.set_major_formatter(DateFormatter("%H:%M:%S"))
	ax1.set_ylabel("", color = colors[0])
	ax1.grid(True, linestyle = "--", alpha = 0.5)
	ax1.margins(x = 0)

	ax2 = ax1.twinx()
	ax2.yaxis.set_label_position("right")
	ax2.set_ylabel("", color = colors[1])
	ax2.margins(x = 0)

	line1, = ax1.plot([], [], color = colors[0])
	line2, = ax2.plot([], [], color = colors[1])

	charts1_2_canvas = FigureCanvasTkAgg(fig1, master = charts_buttons_frame)
	charts1_2_canvas.draw()

	# Charts 3 & 4
	fig2, ax3 = plt.subplots()
	fig2.patch.set_facecolor(record_dialog.cget("bg"))

	ax3.xaxis.set_major_formatter(DateFormatter("%H:%M:%S"))
	ax3.set_ylabel("", color = colors[2])
	ax3.grid(True, linestyle = "--", alpha = 0.5)
	ax3.margins(x = 0)

	ax4 = ax3.twinx()
	ax4.yaxis.set_label_position("right")
	ax4.set_ylabel("", color = colors[3])
	ax4.margins(x = 0)

	line3, = ax3.plot([], [], color = colors[2])
	line4, = ax4.plot([], [], color = colors[3])

	charts3_4_canvas = FigureCanvasTkAgg(fig2, master = charts_buttons_frame)
	charts3_4_canvas.draw()

	# Record control buttons
	def start_stop_recording():
		global selected_recording
		global warning_already_shown

		if data.recording:
			warning_already_shown = False
			data.stop_recording_data()
			open_save_recording_dialog()
		else:
			reset_graphs()
			data.start_recording_data()
			selected_recording = data.current_recording

		record_stop_button.config(text = "Stop recording" if data.recording else "Start recording")
		view_raw_data_button.config(state = tk.DISABLED if data.recording else tk.NORMAL) # Not enabled if there is no recording selected (so no recording stored)
		export_button.config(state = tk.DISABLED if data.recording else tk.NORMAL) # Not enabled if there is no recording selected (so no recording stored)

		for btn in pids_buttons:
			btn.config(state = tk.DISABLED if data.recording else tk.NORMAL)

	record_stop_button = tk.Button(general_management_frame, text = "Start recording", width = 30, state = tk.DISABLED, command = start_stop_recording)
	view_raw_data_button = tk.Button(general_management_frame, text = "View raw data", width = 30, state = tk.DISABLED, command = open_raw_data_dialog)
	export_button = tk.Button(general_management_frame, text = "Export data", width = 30, state = tk.DISABLED)

	# Recordings management buttons
	recordings_list_label = tk.Label(recordings_list_frame, text = "Recordings:")

	recordings_list_combo = ttk.Combobox(recordings_list_frame)
	recordings_list_combo.bind("<<ComboboxSelected>>", on_recording_selected)

	record_vehicle_label = tk.Label(general_management_frame, text = f"Vehicle: --")
	remove_recording_button = tk.Button(general_management_frame, text = "Remove recording", width = 30, state = tk.DISABLED, command = remove_selected_recording)

	fill_recordings_list_combo() # Done at the end because the recording selected by default may be about another vehicle



def pack_record_dialog():
	# Necessary to be able to scroll the PID buttons
	pids_selection_container.pack_propagate(False)
	pids_selection_container.pack(side = tk.LEFT, fill = tk.Y)
	pids_selection_canvas.configure(yscrollcommand = pids_selection_scrollbar.set)
	pids_selection_scrollbar.pack(side = tk.LEFT, fill = tk.Y)
	pids_selection_canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
	pids_selection_canvas.create_window((0, 0), window = pids_selection_frame, anchor = "nw")

	for button in pids_buttons:
		button.pack()

	def update_scrollregion(event):
		pids_selection_canvas.configure(scrollregion = pids_selection_canvas.bbox("all"))

	pids_selection_frame.bind("<Configure>", update_scrollregion)

	# Charts
	charts1_2_canvas.get_tk_widget().pack(fill = tk.X)
	charts1_2_canvas.get_tk_widget().config(height = 270)
	charts3_4_canvas.get_tk_widget().pack(fill = tk.X)
	charts3_4_canvas.get_tk_widget().config(height = 270)

	# Frames
	charts_buttons_frame.pack(side = tk.LEFT, anchor = "e", fill = tk.BOTH, expand = True)
	general_management_frame.pack(pady = 20)
	recordings_list_frame.grid(row = 0, column = 1)

	record_stop_button.grid(row = 0, column = 0, padx = 30, pady = 5)
	view_raw_data_button.grid(row = 1, column = 0, padx = 30, pady = 5)
	export_button.grid(row = 2, column = 0, padx = 30)

	recordings_list_label.pack(side = tk.LEFT, anchor = "w")
	recordings_list_combo.pack(side = tk.LEFT, anchor = "e")
	record_vehicle_label.grid(row = 1, column = 1)
	remove_recording_button.grid(row = 2, column = 1)



def open_record_dialog():
	setup_record_dialog()
	pack_record_dialog()



def on_recording_selected(event = None):
	global selected_recording
	global selected_PIDs
	global selected_PIDs_count

	if recordings_list_combo.get().strip():
		for r in data.data_recordings:
			if r.name == recordings_list_combo.get():
				selected_recording = r
				break

		record_vehicle_label.config(text = f"Vehicle: {selected_recording.vehicle.brand} {selected_recording.vehicle.model}")
	else:
		selected_recording = None

	view_raw_data_button.config(state = tk.NORMAL if selected_recording != None else tk.DISABLED)
	export_button.config(state = tk.NORMAL if selected_recording != None else tk.DISABLED)
	remove_recording_button.config(state = tk.NORMAL if selected_recording != None else tk.DISABLED)

	# Update PIDs
	selected_PIDs = [0, 0, 0, 0]
	selected_PIDs_count = 0

	if selected_recording != None: # Only PID buttons related to that recording are enabled
		selected_recording_PIDs = selected_recording.data[-1].values.keys()

		for btn in pids_buttons:
			btn_PID = int(btn.cget("text")[:2], 16)

			if btn_PID in selected_recording_PIDs:
				btn.config(relief = tk.SUNKEN, fg = colors[selected_PIDs_count])
				selected_PIDs[selected_PIDs_count] = btn_PID
				selected_PIDs_count += 1
			else:
				btn.config(relief = tk.RAISED, fg = "black")
	else: # No PID selected
		record_stop_button.config(state = tk.DISABLED)

		for btn in pids_buttons:
			btn.config(relief = tk.RAISED, fg = "black")

	# Update graph
	if selected_recording != None:
		fill_graphs_w_selected_recording()
	else:
		reset_graphs()



def remove_selected_recording():
	global selected_recording

	data.data_recordings.remove(selected_recording)
	selected_recording = None # Will be updated by on_recording_selected(), which will be called by fill_recordings_list_combo()

	fill_recordings_list_combo()



def fill_recordings_list_combo():
	global selected_recording

	recordings_list = []

	for recording in data.data_recordings:
		recordings_list.append(recording.name)

	recordings_list_combo["values"] = recordings_list

	if len(recordings_list) > 0:
		recordings_list_combo.set(recordings_list[-1])
	else:
		recordings_list_combo.set("")
		record_vehicle_label.config(text = f"Vehicle: {data.current_vehicle.brand} {data.current_vehicle.model}")

	on_recording_selected()



def fill_graphs_w_selected_recording():
	global x_data
	global line1_y_data
	global line2_y_data
	global line3_y_data
	global line4_y_data

	if selected_recording == None:
		print("[OBD Reader Error]: Failed to plot graphs for an empty recording selection")
		return

	x_data = []
	line1_y_data = []
	line2_y_data = []
	line3_y_data = []
	line4_y_data = []

	# Fill x_data with timestamps
	for dataUnit in selected_recording.data:
		x_data.append(dataUnit.timestamp)

	# Fill y_data with recording's selected PIDs
	selected_recording_PIDs = list(selected_recording.data[-1].values.keys())

	line1_unit_str = ""
	line2_unit_str = ""
	line3_unit_str = ""
	line4_unit_str = ""

	for dataUnit in selected_recording.data:
		for i, pid in enumerate(selected_recording_PIDs):
			if i == 0:
				if not line1_unit_str == "":
					line1_unit_str = str(dataUnit.values.get(pid).value.units)

				line1_y_data.append(dataUnit.values.get(pid).value.magnitude)

			elif i == 1:
				if not line2_unit_str == "":
					line2_unit_str = str(dataUnit.values.get(pid).value.units)

				line2_y_data.append(dataUnit.values.get(pid).value.magnitude)

			elif i == 2:
				if not line3_unit_str == "":
					line3_unit_str = str(dataUnit.values.get(pid).value.units)

				line3_y_data.append(dataUnit.values.get(pid).value.magnitude)

			else:
				if not line4_unit_str == "":
					line4_unit_str = str(dataUnit.values.get(pid).value.units)

				line4_y_data.append(dataUnit.values.get(pid).value.magnitude)

	# Append 0 to all other graphs so they can all update
	val_count = len(line1_y_data)
	if len(line2_y_data) != val_count:
		line2_y_data = [0] * val_count

	if len(line3_y_data) != val_count:
		line3_y_data = [0] * val_count

	if len(line4_y_data) != val_count:
		line4_y_data = [0] * val_count

	# ======= PLOT GRAPHS =======
	# Selecting PID 1 shows up on the first graph, on the left
	# Selecting PID 2 shows up on the second graph, on the left
	# Selecting PID 3 shows up on the first graph, on the right
	# Selecting PID 4 shows up on the second graph, on the right

	# Graph 1 (dealt with a bit differently, no checks required because we are supposed to have at least on PID data)
	line1.set_data(x_data, line1_y_data) # Selecting PID 1 shows up on the first graph, on the left

	ax1.relim()
	ax1.autoscale_view()
	ax1.set_ylim(0, max(line1_y_data) * 1.1)
	ax1.set_ylabel(line1_unit_str if selected_recording_PIDs[0] != 0 else "")

	# Graph 2
	line3.set_data(x_data, line2_y_data) # Selecting PID 2 shows up on the second graph, on the left

	if len(selected_recording_PIDs) > 1: # This check because the lenght of the data list isn't an indication of real data presence (since it has been filled with '0'')
		ax3.relim()
		ax3.autoscale_view()
		ax3.set_ylim(0, max(line2_y_data) * 1.1)
		ax3.set_ylabel(line2_unit_str if selected_recording_PIDs[1] != 0 else "")
	else:
		ax3.set_ylabel("")

	# Graph 3
	line2.set_data(x_data, line3_y_data) # Selecting PID 3 shows up on the first graph, on the right

	if len(selected_recording_PIDs) > 2:
		ax2.relim()
		ax2.autoscale_view()
		ax2.set_ylim(0, max(line3_y_data) * 1.1)
		ax2.set_ylabel(line3_unit_str if selected_recording_PIDs[2] != 0 else "")
	else:
		ax2.set_ylabel("")

	# Graph 4
	line4.set_data(x_data, line4_y_data) # Selecting PID 4 shows up on the second graph, on the right

	if len(selected_recording_PIDs) > 3:
		ax4.relim()
		ax4.autoscale_view()
		ax4.set_ylim(0, max(line4_y_data) * 1.1)
		ax4.set_ylabel(line4_unit_str if selected_recording_PIDs[3] != 0 else "")
	else:
		ax4.set_ylabel("")

	charts1_2_canvas.draw()
	charts3_4_canvas.draw()



def update_charts():
	global warning_already_shown

	if data.last_data == None or record_dialog == None or obd_connect.is_connection_lost():
		return

	if not data.recording:
		return

	if len(x_data) > 0:
		if x_data[-1] == data.last_data.timestamp:
			return

	# Retrieve values
	failed_PIDs_count = 0
	failed_PIDs = []

	line1_last_val = data.last_data.get(selected_PIDs[0]) if selected_PIDs[0] != 0 else None
	line2_last_val = data.last_data.get(selected_PIDs[1]) if selected_PIDs[1] != 0 else None
	line3_last_val = data.last_data.get(selected_PIDs[2]) if selected_PIDs[2] != 0 else None
	line4_last_val = data.last_data.get(selected_PIDs[3]) if selected_PIDs[3] != 0 else None

	if line1_last_val == None and selected_PIDs[0] != 0: # Gathering precise data about failed PID data retrieval, for the warning dialog
		failed_PIDs_count += 1
		failed_PIDs.append(selected_PIDs[0])

	if line2_last_val == None and selected_PIDs[1] != 0:
		failed_PIDs_count += 1
		failed_PIDs.append(selected_PIDs[1])

	if line3_last_val == None and selected_PIDs[2] != 0:
		failed_PIDs_count += 1
		failed_PIDs.append(selected_PIDs[2])

	if line4_last_val == None and selected_PIDs[3] != 0:
		failed_PIDs_count += 1
		failed_PIDs.append(selected_PIDs[3])

	# X axis update
	if failed_PIDs_count == selected_PIDs_count: # All data retrieval failed, we shall return before incrementing x_data list
		return

	x_data.append(data.last_data.timestamp)
	
	# Show only the last 60 seconds
	cutoff = datetime.now() - timedelta(seconds = 60)
	while x_data and x_data[0] < cutoff:
		x_data.pop(0)
		line1_y_data.pop(0)
		line2_y_data.pop(0)
		line3_y_data.pop(0)
		line4_y_data.pop(0)

	# ======= PLOT GRAPHS =======
	# Selecting PID 1 shows up on the first graph, on the left
	# Selecting PID 2 shows up on the second graph, on the left
	# Selecting PID 3 shows up on the first graph, on the right
	# Selecting PID 4 shows up on the second graph, on the right

	# Graph 1
	if line1_last_val != None:
		line1_y_data.append(line1_last_val.value.magnitude)
		line1.set_data(x_data, line1_y_data) # Selecting PID 1 shows up on the first graph, on the left

		ax1.relim()
		ax1.autoscale_view()
		ax1.set_ylim(0, max(line1_y_data) * 1.1)
		ax1.set_ylabel(str(line1_last_val.value.units) if selected_PIDs[0] != 0 else "")
	else:
		line1_y_data.append(0) # Ensure coherent lists dimensions

	# Graph 2
	if line2_last_val != None:
		line2_y_data.append(line2_last_val.value.magnitude)
		line3.set_data(x_data, line2_y_data) # Selecting PID 2 shows up on the second graph, on the left
		
		ax3.relim()
		ax3.autoscale_view()
		ax3.set_ylim(0, max(line2_y_data) * 1.1)
		ax3.set_ylabel(str(line2_last_val.value.units) if selected_PIDs[1] != 0 else "")
	else:
		line2_y_data.append(0) # Ensure coherent lists dimensions

	# Graph 3
	if line3_last_val != None:
		line3_y_data.append(line3_last_val.value.magnitude)
		line2.set_data(x_data, line3_y_data) # Selecting PID 3 shows up on the first graph, on the right
		
		ax2.relim()
		ax2.autoscale_view()
		ax2.set_ylim(0, max(line3_y_data) * 1.1)
		ax2.set_ylabel(str(line3_last_val.value.units) if selected_PIDs[2] != 0 else "")
	else:
		line3_y_data.append(0) # Ensure coherent lists dimensions

	# Graph 4
	if line4_last_val != None:
		line4_y_data.append(line4_last_val.value.magnitude)
		line4.set_data(x_data, line4_y_data) # Selecting PID 4 shows up on the second graph, on the right
		
		ax4.relim()
		ax4.autoscale_view()
		ax4.set_ylim(0, max(line4_y_data) * 1.1)
		ax4.set_ylabel(str(line4_last_val.value.units) if selected_PIDs[3] != 0 else "")
	else:
		line4_y_data.append(0) # Ensure coherent lists dimensions

	charts1_2_canvas.draw()
	charts3_4_canvas.draw()

	# Warning if a value is 'None' (shown at the very end so the graph code has had a chance to finish running entirely, warning message boxes stop code execution)
	if failed_PIDs_count > 0 and not warning_already_shown:
		warning_str = "The following PIDs data failed to retrieve data from the vehicle:\n\n"

		for pid in failed_PIDs:
			description = next((description for supported_PID, description in data.current_vehicle.supported_pids if supported_PID == pid), None)

			if description != None:
				warning_str += f"- {description}\n"
			else:
				warning_str += f"- {("0" if pid < 16 else "") + hex(pid)[2:].upper()}" # Hexadecimal string without the "0x" prefix

		warning_already_shown = True
		messagebox.showwarning("Warning", warning_str)



def reset_graphs():
	global x_data
	global line1_y_data
	global line2_y_data
	global line3_y_data
	global line4_y_data

	x_data = []
	line1_y_data = []
	line2_y_data = []
	line3_y_data = []
	line4_y_data = []

	line1.set_data(x_data, line1_y_data)
	line2.set_data(x_data, line2_y_data)
	line3.set_data(x_data, line3_y_data)
	line4.set_data(x_data, line4_y_data)

	ax1.set_ylabel("")
	ax2.set_ylabel("")
	ax3.set_ylabel("")
	ax4.set_ylabel("")

	charts1_2_canvas.draw()
	charts3_4_canvas.draw()



# ======= SAVE RECORDING DIALOG =======
def open_save_recording_dialog(_on_close = False):
	dialog = tk.Toplevel(record_dialog)
	dialog.title("Save recording")
	dialog.resizable(False, False)

	dialog.transient(record_dialog) # Ties the dialog to the record dialog
	dialog.grab_set() # Forbids interactions with the main window
	dialog.lift() # Shows up above all other windows already opened
	dialog.focus_force() # Catches keyboard focus
	dialog.protocol("WM_DELETE_WINDOW", lambda : None) # Not closable

	default_name = selected_recording.vehicle.model + " " + selected_recording.data[-1].timestamp.strftime("%d/%m/%Y %H:%M")

	tk.Label(dialog, text = "Recording name:").pack(padx = 20, pady = (20, 5))

	def check_name(*args):
		ok_button.config(state = tk.NORMAL if name_var.get().strip() else tk.DISABLED)

	name_var = tk.StringVar(value = default_name)
	name_var.trace("w", check_name)
	name_entry = tk.Entry(dialog, textvariable = name_var, width = 40)
	name_entry.pack(padx = 20, pady = (0, 10))

	def on_save():
		selected_recording.name = name_var.get()
		fill_recordings_list_combo()
		dialog.destroy()

		if _on_close:
			if raw_data_dialog != None:
				raw_data_dialog.destroy()

			record_dialog.destroy()

	def on_discard():
		global warning_already_shown

		warning_already_shown = False
		data.stop_recording_data()

		if raw_data_dialog != None:
			raw_data_dialog.destroy()

		record_dialog.destroy()

	# Buttons
	buttons_frame = tk.Frame(dialog)
	buttons_frame.pack(pady = (0, 20))

	ok_button = tk.Button(buttons_frame, text = "Save", command = on_save, state = tk.NORMAL if name_var.get().strip() else tk.DISABLED)
	ok_button.pack(side = tk.LEFT, padx = 5)

	if _on_close:
		discard_button = tk.Button(buttons_frame, text = "Discard", command = on_discard)
		discard_button.pack(side = tk.LEFT, padx = 5)

		cancel_button = tk.Button(buttons_frame, text = "Cancel", command = dialog.destroy)
		cancel_button.pack(side = tk.LEFT, padx = 5)



# ======= RAW DATA DIALOG =======
raw_data_dialog = None
recorded_data_table = None
columns = None


def open_raw_data_dialog():
	global raw_data_dialog
	global recorded_data_table
	global columns

	if selected_recording == None:
		return

	def on_close():
		global raw_data_dialog

		raw_data_dialog.destroy()
		raw_data_dialog = None

	raw_data_dialog = tk.Toplevel(record_dialog)

	raw_data_dialog.title(f"\"{selected_recording.name}\" raw data")
	raw_data_dialog.geometry("1280x720")
	raw_data_dialog.resizable(False, False)

	raw_data_dialog.transient(record_dialog) # Ties the dialog to the record dialog
	raw_data_dialog.grab_set() # Forbids interactions with the record dialog
	raw_data_dialog.lift() # Shows up above all other windows already opened
	raw_data_dialog.focus_force() # Catches keyboard focus
	raw_data_dialog.protocol("WM_DELETE_WINDOW", on_close) # Closing the dialog will reset "dialog" global variable

	columns = ["timestamp"]
	column_width = int(1080 / selected_PIDs_count)

	for pid in selected_PIDs:
		if pid != 0:
			for supported_pid, description in data.current_vehicle.supported_pids:
				if supported_pid == pid:
					column_name = ("0" if pid < 16 else "") + hex(pid)[2:].upper() # Hexadecimal string without the "0x" prefix
					column_name += f" - {description} ("
					column_name += str(selected_recording.data[-1].get(pid).value.units)
					column_name += ")"

					columns.append(column_name)
					break

	recorded_data_table = ttk.Treeview(raw_data_dialog, columns = columns, show = "headings", height = 30)

	for col in columns:
		if col == "timestamp":
			recorded_data_table.heading("timestamp", text = "Time")
			recorded_data_table.column("timestamp", width = 200, anchor = "center")
		else:
			recorded_data_table.heading(col, text = col)
			recorded_data_table.column(col, width = column_width, anchor = "center")

	recorded_data_table.pack()
	fill_raw_data_dialog()



def fill_raw_data_dialog():
	if selected_recording == None:
		return

	for dataUnit in selected_recording.data:
		values = []
		values.append(dataUnit.timestamp)

		for pid in selected_PIDs:
			if pid != 0:
				values.append(dataUnit.get(pid).value.magnitude) # The unit is shown in the table's first row

		recorded_data_table.insert("", tk.END, values = tuple(values))
