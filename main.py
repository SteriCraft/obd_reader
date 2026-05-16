#!/home/crazutyx/coding/python/elm327_emulator/elm-venv/bin/python3

# Libraries
import tkinter as tk
import time

# Local files
import obd_connect
import ui
import connection_ui
import data


# ============ TODO LIST ============
# Fix bugs
# When looking at a saved recording, should have a horizontal scrollbar to go back further than one minute


ui.setup()
ui.pack()

data.load_vehicles_data()
connection_ui.open_connection_dialog()

ui.root.mainloop() # Starts the UI
