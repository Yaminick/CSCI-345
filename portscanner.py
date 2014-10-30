#!/usr/bin/env python

##
# portscanner.py - TCP Port Scanner
# v1.0
#
# Author: Nick Corso-Passaro
# Date: 10/29/14
# Usage: python portscanner.py <host> <start> <end>
## 

import socket
import subprocess
import sys
from datetime import datetime

if len(sys.argv) < 4:
	print "Usage: portscanner.py <host> <start> <end>"
	exit(0)

# Clear the screen
subprocess.call('clear', shell=True)

# Arguments
remoteServer = sys.argv[1]
startPort = int(sys.argv[2])
endPort = int(sys.argv[3])
remoteServerIP  = socket.gethostbyname(remoteServer)

# Print a nice banner with information on which host we are about to scan
print "-" * 60
print "Please wait, scanning remote host", remoteServerIP
print "-" * 60

# Check what time the scan started
t1 = datetime.now()

# Using the range function to specify ports (here it will scan all ports between startPort and endPort)
# We also put in some error handling

try:
	for port in range(startPort,endPort):  
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result = sock.connect_ex((remoteServerIP, port))
		if result == 0:
			output = subprocess.check_output("grep -w " + str(port) + "/tcp /etc/services", shell=True)
			print "Port {}: \t Open".format(port)
			print output
		sock.close()

except KeyboardInterrupt:
	print "You pressed Ctrl+C"
	sys.exit()

except socket.gaierror:
	print 'Hostname could not be resolved. Exiting'
	sys.exit()

except socket.error:
	print "Couldn't connect to server"
	sys.exit()

# Checking the time again
t2 = datetime.now()

# Calculates the difference of time, to see how long it took to run the script
total =  t2 - t1

# Printing the information to screen
print 'Scanning Completed in: ', total

