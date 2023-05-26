from header import title

def determine_split_method():
	title()
	split_method_type = ''
	try:
		with open('netflix', 'r') as determine_combo:
			spaces = []
			lines_list = determine_combo.readlines()
			for line in lines_list[0]:
				if ' ' in line:
					spaces.append(line)
			for line in lines_list:
				line = line[:76]
				if " | " in line and "https://" not in line and "android" not in line:
					split_method_type = " | "
				if " | https://" in line or " | android" in line:
					split_method_type = " |"
				if " || " in line and " || https" not in line:
					split_method_type = " || "
				if "https://www.netflix.com" in line:
					split_method_type = ";"
				if "[NETFLIX]" in line:
					split_method_type = "[NETFLIX]"
				if "https://" in line:
					split_method_type = "https"
				elif len(spaces) < 1:
					split_method_type = "None"
				else:
					split_method_type = "Short_line"
	except FileNotFoundError:
		print("\033[38;5;7m\nNo combo-list found. Add one, and name it 'netflix' before starting the program.\nEnding.\n")
		exit()		
	return split_method_type
	
def return_error():
	print("\033[38;5;7m\nThere is something wrong with the combo-list\n\nPlease check:\n\n1) There are no invalid characters\n2) There are no extra lines at the bottom of the file (i.e. ASCII graphics etc)\n3) There is no extra information (i.e. made by) at the top or bottom of the file\n4) There are no extra spaces at the top or bottom of the file\n")
	input("Press Enter to return")
