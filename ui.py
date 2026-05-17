# Libraries
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import time

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
	top_frame.pack(fill = tk.BOTH, expand = True)
	center_frame.pack(expand = True)

	connection_ui.pack()
	vehicle_information_ui.pack()
	main_gauges_ui.pack()
	custom_gauges_ui.pack()
	pending_dtc_ui.pack()

	main_gauges_ui.init_needles()


# ======= UI UPDATE =======
update = False
fps_target = 30 # Hz
root_after_ID = None # Keep track of UI update scheduling

def update_data():
	global root_after_ID

	if update:
		start = time.time()

		# Update process
		vehicle_information_ui.update()
		main_gauges_ui.update()
		custom_gauges_ui.update()
		record_ui.update_charts()

		# FPS target management
		elapsed = (time.time() - start) * 1000 # milliseconds
		waitTime = (1000.0 / fps_target) - elapsed

		if waitTime < 0: # No need to wait
			waitTime = 0

		root_after_ID = root.after(int(waitTime), update_data)



def start_update_cycle():
	global update

	update = True
	update_data()



def stop_update_cycle():
	global update

	update = False
	
	if root_after_ID != None:
		root.after_cancel(root_after_ID) # Cancel next UI update scheduled
