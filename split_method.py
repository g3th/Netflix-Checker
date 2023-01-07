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
				if " | " in line:
					split_method_type = " | "
				if " || " in line:
					split_method_type = " || "
				if len(line) < 90:
					if len(spaces) < 1:
						split_method_type = "None"
					else:
						split_method_type = "Short_line"
				break
	except FileNotFoundError:
		print("\033[38;5;7m\nNo combo-list found. Add one, and name it 'netflix' before starting the program.\nEnding.\n")
		exit()
	return split_method_type
