# Libraries
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Local files
import obd_connect
import ui


dtcs_frame = None
dtcs_top_frame = None
dtcs_buttons_frame = None
dtcs_labels_frame = None

get_pending_dtcs_button = None
get_current_dtcs_button = None
clear_dtcs_button = None

generic_dtcs_label = None
generic_dtcs_label_val = None

manufacturer_dtcs_label = None
manufacturer_dtcs_label_val = None

shown_dtcs_cycle_label = None
shown_dtcs_cycle_label_val = None

dtcs_table_info_label = None
dtcs_table = None


def setup():
	global dtcs_frame
	global dtcs_top_frame
	global dtcs_buttons_frame
	global dtcs_labels_frame

	global get_pending_dtcs_button
	global get_current_dtcs_button
	global clear_dtcs_button

	global generic_dtcs_label
	global generic_dtcs_label_val

	global manufacturer_dtcs_label
	global manufacturer_dtcs_label_val

	global shown_dtcs_cycle_label
	global shown_dtcs_cycle_label_val

	global dtcs_table_info_label
	global dtcs_table

	dtcs_frame = tk.LabelFrame(ui.center_frame, text = "Diagnostic Trouble Codes")
	dtcs_top_frame = tk.Frame(dtcs_frame)
	dtcs_buttons_frame = tk.Frame(dtcs_top_frame)
	dtcs_labels_frame = tk.Frame(dtcs_top_frame)

	get_pending_dtcs_button = tk.Button(dtcs_buttons_frame, text = "Get all DTCs", command = retrieve_pending_dtcs)
	get_current_dtcs_button = tk.Button(dtcs_buttons_frame, text = "Get last cycle DTCs", command = retrieve_current_dtcs)
	clear_dtcs_button = tk.Button(dtcs_buttons_frame, text = "Clear DTCs", fg = "red", command = open_clear_dtcs_warning_dialog)

	generic_dtcs_label = tk.Label(dtcs_labels_frame, text = "Generic DTCs:")
	generic_dtcs_label_val = tk.Label(dtcs_labels_frame, text = "0")

	manufacturer_dtcs_label = tk.Label(dtcs_labels_frame, text = "Manufacturer DTCs:")
	manufacturer_dtcs_label_val = tk.Label(dtcs_labels_frame, text = "0")

	shown_dtcs_cycle_label = tk.Label(dtcs_labels_frame, text = "Cycle:")
	shown_dtcs_cycle_label_val = tk.Label(dtcs_labels_frame, text = "None")

	dtcs_table_info_label = tk.Label(dtcs_frame, text = "", height = 1, font = ("Courier", 10, "italic"))

	dtcs_table = ttk.Treeview(dtcs_frame, columns = ("code", "description"), show = "headings", height = 8)
	dtcs_table.heading("code", text = "DTC")
	dtcs_table.heading("description", text = "Description")
	dtcs_table.column("code", width = 100, anchor = "center")
	dtcs_table.column("description", width = 400)
	dtcs_table.bind("<Double-Button-1>", on_dtc_double_click)



def pack():
	dtcs_frame.grid(row = 1, column = 0)
	dtcs_top_frame.pack(padx = 10, pady = 10)
	dtcs_buttons_frame.pack(side = tk.LEFT)
	dtcs_labels_frame.pack(side = tk.LEFT)
	dtcs_table.pack(padx = 10, pady = 10)
	dtcs_table_info_label.pack(padx = 10)

	get_pending_dtcs_button.grid(row = 0, column = 0, sticky = "w", padx = 10, pady = 2)
	get_current_dtcs_button.grid(row = 0, column = 1, sticky = "w", padx = 10, pady = 2)
	clear_dtcs_button.grid(row = 1, column = 0, columnspan = 2, sticky = "ew", padx = 10, pady = 2)

	generic_dtcs_label.grid(row = 0, column = 0, sticky = "w", padx = 10)
	generic_dtcs_label_val.grid(row = 0, column = 1, sticky = "w")
	manufacturer_dtcs_label.grid(row = 1, column = 0, sticky = "w", padx = 10)
	manufacturer_dtcs_label_val.grid(row = 1, column = 1, sticky = "w")
	shown_dtcs_cycle_label.grid(row = 2, column = 0, sticky = "w", padx = 10)
	shown_dtcs_cycle_label_val.grid(row = 2, column = 1, sticky = "w")



def retrieve_pending_dtcs(): # Mode 03
	shown_dtcs_cycle_label_val.config(text = "All")

	dtcs = obd_connect.getPendingDTCs()
	dtcs_table.delete(*dtcs_table.get_children()) # Empty the table

	generic_dtcs_qty, manufacturer_dtcs_qty = 0, 0

	for code, description in dtcs:
		if code != "":
			if description == "":
				description = "Manufacturer specific error (no data)"
				manufacturer_dtcs_qty += 1
			else:
				generic_dtcs_qty += 1

			dtcs_table.insert("", tk.END, values = (code, description))

	generic_dtcs_label_val.config(text = str(generic_dtcs_qty))
	manufacturer_dtcs_label_val.config(text = str(manufacturer_dtcs_qty))

	if (generic_dtcs_qty + manufacturer_dtcs_qty) == 0:
		dtcs_table_info_label.config(text = "Vehicle clear of any DTCs.")
		ui.root.after(10000, lambda: dtcs_table_info_label.config(text = "")) # Label cleared after 10 seconds



def retrieve_current_dtcs(): # Mode 07
	shown_dtcs_cycle_label_val.config(text = "Last")

	dtcs = obd_connect.getCurrentDTCs()
	dtcs_table.delete(*dtcs_table.get_children()) # Empty the table

	generic_dtcs_qty, manufacturer_dtcs_qty = 0, 0

	for code, description in dtcs:
		if code != "":
			if description == "":
				description = "Manufacturer specific error (no data)"
				manufacturer_dtcs_qty += 1
			else:
				generic_dtcs_qty += 1

			dtcs_table.insert("", tk.END, values = (code, description))

	generic_dtcs_label_val.config(text = str(generic_dtcs_qty))
	manufacturer_dtcs_label_val.config(text = str(manufacturer_dtcs_qty))

	if (generic_dtcs_qty + manufacturer_dtcs_qty) == 0:
		dtcs_table_info_label.config(text = "No DTCs during the last driving cycle.")
		ui.root.after(10000, lambda: dtcs_table_info_label.config(text = "")) # Label cleared after 10 seconds



def clear_dtcs(): # Mode 04
	obd_connect.clearDTCs()
	retrieve_pending_dtcs()

	if len(dtcs_table.get_children()) > 0:
		dtcs_table_info_label.config(text = "Remaining permanent DTCs shown above.")
	else:
		dtcs_table_info_label.config(text = "DTCs erased successfuly.")

	ui.root.after(10000, lambda: dtcs_table_info_label.config(text = "")) # Label cleared after 10 seconds



def open_clear_dtcs_warning_dialog():
	dialog_message = "Clearing DTCs will not remove permanent DTCs. "
	dialog_message += "Those are cleared by the ECU once the mechanical issue is fixed.\n\n"
	dialog_message += "Fuel delivery strategies will be cleared as well. "
	dialog_message += "The ECU will determine them again after a few driving cycles.\n\n"
	dialog_message += "Do you wish to continue?"

	if messagebox.askyesno(title = "Clear DTCs", message = dialog_message, icon = messagebox.WARNING):
		clear_dtcs()



def on_dtc_double_click(event): # If the DTC is manufacturer specific, the description isn't copied to the clipboard
	row = dtcs_table.identify_row(event.y)

	if row:
		code, description = dtcs_table.item(row, "values")
		ui.root.clipboard_clear()
		ui.root.clipboard_append(f"{code} {description}" if "(no data)" not in description else f"{code}")
		dtcs_table_info_label.config(text = f"{code} data copied to the clipboard.")
		ui.root.after(10000, lambda: dtcs_table_info_label.config(text = "")) # Label cleared after 10 seconds



def reset_dtcs_table():
	dtcs_table.delete(*dtcs_table.get_children()) # Empty the table
	generic_dtcs_label_val.config(text = "0")
	manufacturer_dtcs_label_val.config(text = "0")
	shown_dtcs_cycle_label_val.config(text = "None")
	dtcs_table_info_label.config(text = "")
