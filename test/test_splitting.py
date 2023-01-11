email = []
password = []

with open('netflix','r') as net:
	for line in net.readlines():
		email.append(line.split(":")[0])
		password.append(line.split(":")[1].split(" ")[0])
		


print(email[2],password[1])
