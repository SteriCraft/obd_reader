# Libraries

# Local files


def hex_to_str_2_digits(_val):
	return ("0" if _val < 16 else "") + hex(_val)[2:].upper() # Hexadecimal string without the "0x" prefix



def get_bg_color(_widget):
	r, g, b = _widget.winfo_rgb(_widget.cget("bg"))

	return f"#{(r // 256):02x}{(g // 256):02x}{(b // 256):02x}"
