#!/home/crazutyx/coding/python/elm327_emulator/elm-venv/bin/python3

# Libraries
import tkinter as tk
import time

# Local files
import obd_connect
import ui
import connection_ui
import data


ui.setup()
ui.pack()

data.load_vehicles_data()
connection_ui.open_connection_dialog()

ui.root.mainloop() # Starts the UI
