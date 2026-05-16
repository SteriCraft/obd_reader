# Libraries
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

# Local files
import obd_connect
import connection_ui
import main_gauges_ui
import custom_gauges_ui
import vehicle_information_ui
import pending_dtc_ui
import record_ui
import data


root = None
top_frame = None
center_frame = None



def setup():
	global root
	global top_frame
	global center_frame

	def on_main_window_close():
		connection_ui.disconnect()

		if data.next_thread_root_after_ID != None:
			root.after_cancel(data.next_thread_root_after_ID)

		plt.close("all")
		root.destroy()

	root = tk.Tk()
	root.title("OBD Reader - v0.4")
	root.geometry("1280x720")
	root.resizable(False, False)
	root.protocol("WM_DELETE_WINDOW", on_main_window_close)

	top_frame = tk.Frame(root)
	center_frame = tk.Frame(root)

	connection_ui.setup()
	vehicle_information_ui.setup()
	main_gauges_ui.setup()
	custom_gauges_ui.setup()
	pending_dtc_ui.setup()



def pack():
	top_frame.pack(fill = tk.BOTH, expand = True) # 'expand' claims extra space on a resize event, 'fill' uses that space
	center_frame.pack(expand = True)

	connection_ui.pack()
	vehicle_information_ui.pack()
	main_gauges_ui.pack()
	custom_gauges_ui.pack()
	pending_dtc_ui.pack()

	main_gauges_ui.init_needles()



def update_data():
	vehicle_information_ui.update()
	main_gauges_ui.update()
	custom_gauges_ui.update()
	record_ui.update_charts()
