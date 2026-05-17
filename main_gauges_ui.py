# Libraries
import math
import tkinter as tk

# Local files
import obd_connect
import ui
import data
import utils


gauges_frame = None

rpm_gauge_canvas = None
speed_gauge_canvas = None

throttle_gauge_frame = None
throttle_gauge_label = None
throttle_gauge_canvas = None
throttle_gauge_label_val = None

engine_load_gauge_frame = None
engine_load_gauge_label = None
engine_load_gauge_canvas = None
engine_load_gauge_label_val = None

coolant_temp_gauge_frame = None
coolant_temp_gauge_label = None
coolant_temp_gauge_canvas = None
coolant_temp_gauge_label_val = None


def setup():
	global gauges_frame

	global rpm_gauge_canvas
	global speed_gauge_canvas

	global throttle_gauge_frame
	global throttle_gauge_label
	global throttle_gauge_canvas
	global throttle_gauge_label_val

	global engine_load_gauge_frame
	global engine_load_gauge_label
	global engine_load_gauge_canvas
	global engine_load_gauge_label_val

	global coolant_temp_gauge_frame
	global coolant_temp_gauge_label
	global coolant_temp_gauge_canvas
	global coolant_temp_gauge_label_val

	window_bg_color = utils.get_bg_color(ui.root)

	gauges_frame = tk.Frame(ui.top_frame)

	# RPM
	rpm_gauge_canvas = tk.Canvas(gauges_frame, width = 160, height = 160, bg = window_bg_color)

	# Speed
	speed_gauge_canvas = tk.Canvas(gauges_frame, width = 160, height = 160, bg = window_bg_color)

	# Throttle
	throttle_gauge_frame = tk.Frame(gauges_frame)

	throttle_gauge_label = tk.Label(throttle_gauge_frame, text = "Throttle", font = ("Courier", 12, "bold"))
	throttle_gauge_canvas = tk.Canvas(throttle_gauge_frame, width = 50, height = 100, bg = "white")
	throttle_gauge_label_val = tk.Label(throttle_gauge_frame, text = "0 %")

	# Engine load
	engine_load_gauge_frame = tk.Frame(gauges_frame)

	engine_load_gauge_label = tk.Label(engine_load_gauge_frame, text = "Load", font = ("Courier", 12, "bold"))
	engine_load_gauge_canvas = tk.Canvas(engine_load_gauge_frame, width = 50, height = 100, bg = "white")
	engine_load_gauge_label_val = tk.Label(engine_load_gauge_frame, text = "0 %")

	# Coolant temp
	coolant_temp_gauge_frame = tk.Frame(gauges_frame)

	coolant_temp_gauge_label = tk.Label(coolant_temp_gauge_frame, text = "Temp", font = ("Courier", 12, "bold"))
	coolant_temp_gauge_canvas = tk.Canvas(coolant_temp_gauge_frame, width = 50, height = 100, bg = "white")
	coolant_temp_gauge_label_val = tk.Label(coolant_temp_gauge_frame, text = "0 °C")



def pack():
	gauges_frame.pack(side = tk.LEFT, anchor = "n", pady = 20)

	# RPM
	rpm_gauge_canvas.pack(side = tk.LEFT, padx = 10)

	# Speed
	speed_gauge_canvas.pack(side = tk.LEFT, padx = 10) # LEFT again so it "stacks" from left to right

	# Throttle
	throttle_gauge_frame.pack(side = tk.LEFT, padx = 15)
	throttle_gauge_label.pack()
	throttle_gauge_canvas.pack()
	throttle_gauge_label_val.pack()

	# Engine load
	engine_load_gauge_frame.pack(side = tk.LEFT, padx = 15)
	engine_load_gauge_label.pack()
	engine_load_gauge_canvas.pack()
	engine_load_gauge_label_val.pack()

	# Coolant temp
	coolant_temp_gauge_frame.pack(side = tk.LEFT, padx = 15)
	coolant_temp_gauge_label.pack()
	coolant_temp_gauge_canvas.pack()
	coolant_temp_gauge_label_val.pack()



def init_needles():
	draw_rpm_gauge(160, 160)
	set_rpm_gauge_needle(160, 160, 0)

	draw_speed_gauge(160, 160)
	set_speed_gauge_needle(160, 160, 0)



def reset():
	set_rpm_gauge_needle(160, 160, 0)
	set_speed_gauge_needle(160, 160, 0)
	set_throttle_gauge(0)
	set_engine_load_gauge(0)
	set_coolant_temp_gauge(0)



def update():
	# RPM (PID 0x0C)
	rpm = data.get_last_PID_data(0x0C)
	set_rpm_gauge_needle(160, 160, rpm.value.magnitude if rpm != None else -1)
	
	# Speed (PID 0x0D)
	speed = data.get_last_PID_data(0x0D)
	set_speed_gauge_needle(160, 160, speed.value.magnitude if speed != None else -1)	
	
	# Throttle (PID 0x11)
	throttle = data.get_last_PID_data(0x11)
	set_throttle_gauge(throttle.value.magnitude if throttle != None else -1)

	# Engine load (PID 0x04)
	load = data.get_last_PID_data(0x04)
	set_engine_load_gauge(load.value.magnitude if load != None else -1)

	# Coolant temp (PID 0x05)
	temp = data.get_last_PID_data(0x05)
	set_coolant_temp_gauge(temp.value.magnitude if temp != None else -1)



# ======= DRAWING =======
# --- RPM ---
def draw_rpm_gauge(_width, _height):
	cx, cy, r = _width / 2, _height / 2, _width / 2 - 5
	rpm_gauge_canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill = "white")

	draw_rpm_scale(_width / 2, _height / 2 + (_height * 0.04), _width / 2 - 20)



def draw_rpm_scale(cx, cy, radius, max_rpm = 8000):
	# Needle attachement point
	needle_center_x, needle_center_y = cx, cy - (cy * 0.04)
	needle_attachement_point_radius = 5
	rpm_gauge_canvas.create_oval(needle_center_x - needle_attachement_point_radius, needle_center_y - needle_attachement_point_radius,
								 needle_center_x + needle_attachement_point_radius, needle_center_y + needle_attachement_point_radius, fill = "red")

	# Numerical value
	rpm_box_center_x, rpm_box_center_y = cx, (cy - (cy * 0.07)) * 1.66
	rpm_box_width, rpm_box_height = cx * 0.7, 20

	rpm_gauge_canvas.create_rectangle(rpm_box_center_x - rpm_box_width / 2, rpm_box_center_y - rpm_box_height / 2,
									  rpm_box_center_x + rpm_box_width / 2, rpm_box_center_y + rpm_box_height / 2, fill = "black")
	rpm_gauge_canvas.create_text(cx, cy * 1.3, text = "RPM", fill = "black", font = ("Courier", 12, "bold"))

	steps = int(max_rpm / 1000) + 1
	for i in range(steps):
		rpm_val = int(i * max_rpm / (steps - 1))
		angle = -220 + (rpm_val / max_rpm) * 260
		rad = math.radians(angle)

		# Text
		x = cx + radius * math.cos(rad)
		y = cy + radius * math.sin(rad)

		rpm_gauge_canvas.create_text(x, y, text = f"{rpm_val // 1000}", fill = "black" if rpm_val < 6000 else "red", font = ("Courier", 12))
		
		# Lines
		x = cx + (radius - 15) * math.cos(rad)
		y = cy - (cy * 0.04) + (radius - 15) * math.sin(rad)
		x1 = cx + (radius - 30) * math.cos(rad)
		x2 = cy - (cy * 0.04) + (radius - 30) * math.sin(rad)

		rpm_gauge_canvas.create_line(x, y, x1, x2, fill = "black" if rpm_val < 6000 else "red", width = 1)



def set_rpm_gauge_needle(_width, _height, rpm, max_rpm = 8000):
	rpm_gauge_canvas.delete("needle") # Clear the previous needle
	rpm_gauge_canvas.delete("num_value") # Clear the previous numerical value

	cx, cy = _width / 2, _height / 2 + 3		# Center point
	length = _width / 2 - 30 	 				# Needle length

	# Map rpm to angle: 0 rpm = -220°, max rpm = 40° (260° of total rotation)
	angle = -220 + (rpm / max_rpm) * 260
	rad = math.radians(angle)

	x = cx + length * math.cos(rad)
	y = cy + length * math.sin(rad) # y is inverted in a canvas

	rpm_gauge_canvas.create_line(cx, cy, x, y, fill = "red", width = 3, tags = "needle")

	# Numerical value
	rpm_gauge_canvas.create_text(_width / 2, _height * 0.85, text = f"{int(rpm)}", fill = "yellow", font = ("Courier", 10), tags = "num_value")



# --- Speed ---
def draw_speed_gauge(_width, _height):
	cx, cy, r = _width / 2, _height / 2, _width / 2 - 5
	speed_gauge_canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill = "white")

	draw_speed_scale(_width / 2, _height / 2 + (_height * 0.04), _width / 2 - 20)



def draw_speed_scale(cx, cy, radius, max_speed = 220):
	# Needle attachement point
	needle_center_x, needle_center_y = cx, cy - (cy * 0.04)
	needle_attachement_point_radius = 5
	speed_gauge_canvas.create_oval(needle_center_x - needle_attachement_point_radius, needle_center_y - needle_attachement_point_radius,
								   needle_center_x + needle_attachement_point_radius, needle_center_y + needle_attachement_point_radius, fill = "red")

	# Numerical value
	speed_box_center_x, speed_box_center_y = cx, (cy - (cy * 0.07)) * 1.66
	speed_box_width, speed_box_height = cx * 0.7, 20

	speed_gauge_canvas.create_rectangle(speed_box_center_x - speed_box_width / 2, speed_box_center_y - speed_box_height / 2,
										speed_box_center_x + speed_box_width / 2, speed_box_center_y + speed_box_height / 2, fill = "black")
	speed_gauge_canvas.create_text(cx, cy * 1.3, text = "km/h", fill = "black", font = ("Courier", 12, "bold"))

	steps = int(max_speed / 20) + 1
	for i in range(steps):
		speed_val = int(i * max_speed / (steps - 1))
		angle = -220 + (speed_val / max_speed) * 260
		rad = math.radians(angle)

		# Text
		x = cx + radius * math.cos(rad)
		y = cy + radius * math.sin(rad)

		speed_gauge_canvas.create_text(x, y, text = f"{speed_val}", fill = "black", font = ("Courier", 10))
		
		# Lines
		x = cx + (radius - 15) * math.cos(rad)
		y = cy - (cy * 0.04) + (radius - 15) * math.sin(rad)
		x1 = cx + (radius - 30) * math.cos(rad)
		x2 = cy - (cy * 0.04) + (radius - 30) * math.sin(rad)

		speed_gauge_canvas.create_line(x, y, x1, x2, fill = "black", width = 1)



def set_speed_gauge_needle(_width, _height, speed, max_speed = 220):
	speed_gauge_canvas.delete("needle") # Clear the previous needle
	speed_gauge_canvas.delete("num_value") # Clear the previous numerical value

	cx, cy = _width / 2, _height / 2 + 3		# Center point
	length = _width / 2 - 30 	 				# Needle length

	# Map speed to angle: 0 km/h = -220°, max speed = 40° (260° of total rotation)
	angle = -220 + (speed / max_speed) * 260
	rad = math.radians(angle)

	x = cx + length * math.cos(rad)
	y = cy + length * math.sin(rad) # y is inverted in a canvas

	speed_gauge_canvas.create_line(cx, cy, x, y, fill = "red", width = 3, tags = "needle")

	# Numerical value
	speed_gauge_canvas.create_text(_width / 2, _height * 0.85, text = f"{int(speed)}", fill = "yellow", font = ("Courier", 10), tags = "num_value")



# --- Throttle ---
def set_throttle_gauge(_value): # Value from 0 to 100 %
	throttle_gauge_canvas.delete("value") # Clears the previous value 'rectangle'

	if _value >= 0:
		# Map value to height
		# Canvas size: 50, 100 (+ 1 px to compensate for the outline)
		x1, y1 = 0, 101								# Bottom left corner
		x2, y2 = 51, 100 - _value 					# Top right corner

		throttle_gauge_canvas.create_rectangle(x1, y1, x2, y2, fill = "blue", outline = "", tags = "value")

		# Text label
		throttle_gauge_label_val.config(text = f"{int(_value)}" + " %")
	else:
		throttle_gauge_label_val.config(text = "NaN")



# --- Engine load ---
def set_engine_load_gauge(_value): # Value from 0 to 100 %
	engine_load_gauge_canvas.delete("value") # Clears the previous value 'rectangle'

	if _value >= 0:
		# Map value to height
		# Canvas size: 50, 100 (+ 1 px to compensate for the outline)
		x1, y1 = 0, 101								# Bottom left corner
		x2, y2 = 51, 100 - _value 					# Top right corner

		engine_load_gauge_canvas.create_rectangle(x1, y1, x2, y2, fill = "blue", outline = "", tags = "value")

		# Text label
		engine_load_gauge_label_val.config(text = f"{int(_value)}" + " %")
	else:
		engine_load_gauge_label_val.config(text = "NaN")



# --- Coolant temp ---
def set_coolant_temp_gauge(_temp): # Temp from 0 to 150 °C (OBD allows from -40 to 215 °C)
	coolant_temp_gauge_canvas.delete("value") # Clears the previous value 'rectangle'

	if _temp >= 0:
		# Map value to height
		# Canvas size: 50, 100 (+ 1 px to compensate for the outline)
		x1, y1 = 0, 101										# Bottom left corner
		x2, y2 = 51, 100 - (_temp / 1.5)					# Top right corner

		colorStr = "blue"

		if _temp >= 120:
			colorStr = "red"
		elif _temp > 105:
			colorStr = "orange"

		coolant_temp_gauge_canvas.create_rectangle(x1, y1, x2, y2, fill = colorStr, outline = "", tags = "value")

		# Text label
		coolant_temp_gauge_label_val.config(text = f"{int(_temp)}" + " °C")
	else:
		coolant_temp_gauge_label_val.config(text = "NaN")
