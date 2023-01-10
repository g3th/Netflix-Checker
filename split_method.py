from header import title

def determine_split_method():

	title()
	split_method_type = "No_Method"
	try:
		with open('netflix', 'r') as determine_combo:
			spaces = []
			for line in determine_combo.readline():
				if ' ' in line:
					spaces.append(line)
					
			for line in determine_combo.readlines():
				line = line[:76]
				if " | " in line and "https://" not in line and "android" not in line:
					split_method_type = " | "
				elif " | https://" in line or " | android" in line:
					split_method_type = " |"
				elif " || " in line and " || https" not in line:
					split_method_type = " || "
				elif "https://www.netflix.com" in line:
					split_method_type = ";"
				elif len(line) < 90:
					if len(spaces) < 1:
						split_method_type = "None"
					else:
						split_method_type = "Short_line"
				break
	except FileNotFoundError:
		print("\033[38;5;7m\nNo combo-list found. Add one, and name it 'netflix' before starting the program.\nEnding.\n")
		exit()
	return split_method_type
determine_split_method()
