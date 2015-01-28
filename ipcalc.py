#!/usr/bin/env python

##
# ipcalc.py - IP Subnet Calculator
# v1.0
#
# Author: Nick Corso-Passaro
# Date: 11/25/14
# Usage: python ipcalc.py <network>
## 

import sys

if len(sys.argv) < 2:
	print "Usage: ipcalc.py <network> Example: 192.168.1.0/24"
	sys.exit()

#Get address string and CIDR string from command line
address = sys.argv[1]
chop = address.split('/')
ip = chop[0].split('.')
cidr = int(chop[1])

if len(ip) != 4:
	print "Invalid IP address!"
	sys.exit()

if cidr < 0 or cidr > 32:
	print "Invalid CIDR notation!"
	sys.exit()

#Initialize the netmask and calculate based on CIDR mask
mask = [0, 0, 0, 0]
for i in range(cidr):
    mask[i/8] = mask[i/8] + (1 << (7 - i % 8))#binary left shift 

#Initialize net and binary and netmask (net) with addr to get network
net = []
for i in range(4):
    net.append(int(ip[i]) & mask[i])

#Duplicate net into broad array, gather host bits, and generate broadcast
broad = list(net)
brange = 32 - cidr
for i in range(brange):
    broad[3 - i/8] = broad[3 - i/8] + (1 << (i % 8))

#This gives you usable hosts for the given subnet
xhost = 2 ** brange #This is 2^32-cidr
host = "{:,}".format(xhost)

#Initialize o for wildcard mask (imask) with broadcast - net 
o = [0, 0, 0, 0]
for i in range(4):
	o[i] = broad[i] - net[i]

#This gives the wildcard mask for the given subnet	
imask = []
for i in range (4):
	imask.append(int(o[i]) & broad[i])

#Print information, mapping integer lists to strings for easy printing
print "~*" * 40
print "IP Address (Given): " , chop[0]
print "Netmask (CIDR): " , ".".join(map(str, mask))
print "Wildcard Mask: " , ".".join(map(str, imask))
print "Network Address: " , ".".join(map(str, net))
print "Broadcast Address: " , ".".join(map(str, broad))
print "Usable IPs: " , host
print "NOTE: Usable IPs includes the Network and Broadcast addresses."
print "~*" * 40
