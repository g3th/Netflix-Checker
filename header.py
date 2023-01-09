def title():
	print("\x1bc")
	print("\033[38;5;52m███╗   ██╗███████╗████████╗███████╗██╗     ██╗██╗  ██╗")
	print("\033[38;5;88m████╗  ██║██╔════╝╚══██╔══╝██╔════╝██║     ██║╚██╗██╔╝")
	print("\033[38;5;124m██╔██╗ ██║█████╗     ██║   █████╗  ██║     ██║ ╚███╔╝ ")
	print("\033[38;5;160m██║╚██╗██║██╔══╝     ██║   ██╔══╝  ██║     ██║ ██╔██╗ ")
	print("\033[38;5;196m██║ ╚████║███████╗   ██║   ██║     ███████╗██║██╔╝ ██╗")
	print("\033[38;5;160m╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝     ╚══════╝╚═╝╚═╝  ╚═╝")
	print("\033[38;5;124m    =========== https://github.com/g3th =========    ")

def user_options():
	print("\n\033[38;5;7m--------- Pick an Option: ---------\n")
	print("1) Check Accounts")
	print("2) Check Countries in Combo-List\n")
	option = str(input("Option or (q)uit: "))
	while True:
		if option == "1" or option == "2":
			title()
			return option
		elif option == "q":
			exit()
		else:
			title()
			user_options()
			
		
