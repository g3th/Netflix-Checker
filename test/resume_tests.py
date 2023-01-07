import os
from pathlib import Path

user=[]
passw=[]
files = []

directory = str(Path(__file__).parent)

for file_ in os.listdir(directory):
	files.append(file_)
for file_ in range(len(files)):
	if 'resume' in files[file_]:
		print("resume exists")
		break;
	elif file_ == len(files)-1:
		print("resume not found")		
		with open('netflix','r') as net:
			for line in net.readlines():
				user.append(line.split(":")[0])
				passw.append(line.split(":")[1].split(" | ")[0])
		net.close()

		for line in range(len(user)):
			with open('resume','a') as resume:
				resume.write("{}:{}\n".format(user[line],passw[line]))
			resume.close()

