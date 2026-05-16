# Libraries

# Local files


is_PID_response_recordable = {
	0x00: False,				# Supported PIDs [01-20]
	0x01: False,				# Status since DTCs cleared
	0x02: False,				# DTC that triggered the freeze frame
	0x03: False,				# Fuel System Status
	0x04: True,					# Calculated Engine Load
	0x05: True,					# Engine Coolant Temperature
	0x06: True,					# Short Term Fuel Trim - Bank 1
	0x07: True,					# Long Term Fuel Trim - Bank 1
	0x08: True,					# Short Term Fuel Trim - Bank 2
	0x09: True,					# Long Term Fuel Trim - Bank 2
	0x0A: True,					# Fuel Pressure
	0x0B: True,					# Intake Manifold Pressure
	0x0C: True,					# Engine RPM
	0x0D: True,					# Vehicle Speed
	0x0E: True,					# Timing Advance
	0x0F: True,					# Intake Air Temp
	0x10: True,					# Air Flow Rate (MAF)
	0x11: True,					# Throttle Position
	0x12: False,				# Secondary Air Status
	0x13: True,					# O2 Sensors Present
	0x14: True,					# O2: Bank 1 - Sensor 1 Voltage
	0x15: True,					# O2: Bank 1 - Sensor 2 Voltage
	0x16: True,					# O2: Bank 1 - Sensor 3 Voltage
	0x17: True,					# O2: Bank 1 - Sensor 4 Voltage
	0x18: True,					# O2: Bank 2 - Sensor 1 Voltage
	0x19: True,					# O2: Bank 2 - Sensor 2 Voltage
	0x1A: True,					# O2: Bank 2 - Sensor 3 Voltage
	0x1B: True,					# O2: Bank 2 - Sensor 4 Voltage
	0x1C: False,				# OBD Standards Compliance
	0x1D: False,				# O2 Sensors Present (alternate)
	0x1E: False,				# Auxiliary input status (power take off)
	0x1F: False,				# Engine Run Time

	0x20: False,				# Supported PIDs [21-40]
	0x21: False,				# Distance Traveled with MIL on
	0x22: True,					# Fuel Rail Pressure (relative to vacuum)
	0x23: True,					# Fuel Rail Pressure (direct inject)
	0x24: True,					# 02 Sensor 1 WR Lambda Voltage
	0x25: True,					# 02 Sensor 2 WR Lambda Voltage
	0x26: True,					# 02 Sensor 3 WR Lambda Voltage
	0x27: True,					# 02 Sensor 4 WR Lambda Voltage
	0x28: True,					# 02 Sensor 5 WR Lambda Voltage
	0x29: True,					# 02 Sensor 6 WR Lambda Voltage
	0x2A: True,					# 02 Sensor 7 WR Lambda Voltage
	0x2B: True,					# 02 Sensor 8 WR Lambda Voltage
	0x2C: True,					# Commanded EGR
	0x2D: True,					# EGR Error
	0x2E: True,					# Commanded Evaporative Purge
	0x2F: True,					# Fuel Level Input
	0x30: False,				# Number of warm-ups since codes cleared
	0x31: False,				# Distance traveled since codes cleared
	0x32: True,					# Evaporative system vapor pressure
	0x33: True,					# Barometric Pressure
	0x34: True,					# 02 Sensor 1 WR Lambda Current
	0x35: True,					# 02 Sensor 2 WR Lambda Current
	0x36: True,					# 02 Sensor 3 WR Lambda Current
	0x37: True,					# 02 Sensor 4 WR Lambda Current
	0x38: True,					# 02 Sensor 5 WR Lambda Current
	0x39: True,					# 02 Sensor 6 WR Lambda Current
	0x3A: True,					# 02 Sensor 7 WR Lambda Current
	0x3B: True,					# 02 Sensor 8 WR Lambda Current
	0x3C: True,					# Catalyst Temperature: Bank 1 - Sensor 1
	0x3D: True,					# Catalyst Temperature: Bank 2 - Sensor 1
	0x3E: True,					# Catalyst Temperature: Bank 1 - Sensor 2
	0x3F: True,					# Catalyst Temperature: Bank 2 - Sensor 2

	0x40: False,				# Supported PIDs [41-60]
	0x41: False,				# Monitor status this drive cycle
	0x42: True,					# Control module voltage
	0x43: True,					# Absolute load value
	0x44: True,					# Commanded equivalence ratio
	0x45: True,					# Relative throttle position
	0x46: True,					# Ambient air temperature
	0x47: True,					# Absolute throttle position B
	0x48: True,					# Absolute throttle position C
	0x49: True,					# Absolute throttle position D
	0x4A: True,					# Absolute throttle position E
	0x4B: True,					# Absolute throttle position F
	0x4C: True,					# Commanded throttle actuator
	0x4D: False,				# Time run with MIL on
	0x4E: False,				# Time since trouble codes cleared
	0x4F: False,				# Various Max values
	0x50: False,				# Maximum value for mass air flow sensor
	0x51: False,				# Fuel Type
	0x52: False,				# Ethanol Fuel Percent
	0x53: True,					# Absolute Evap system Vapor Pressure
	0x54: True,					# Evap system vapor pressure
	0x55: True,					# Short term secondary O2 trim - Bank 1
	0x56: True,					# Long term secondary O2 trim - Bank 1
	0x57: True,					# Short term secondary O2 trim - Bank 2
	0x58: True,					# Long term secondary O2 trim - Bank 2
	0x59: True,					# Fuel rail pressure (absolute)
	0x5A: True,					# Relative accelerator pedal position
	0x5B: True,					# Hybrid battery pack remaining life
	0x5C: True,					# Engine oil temperature
	0x5D: True,					# Fuel injection timing
	0x5E: True,					# Engine fuel rate
	0x5F: False					# Designed emission requirements
}
