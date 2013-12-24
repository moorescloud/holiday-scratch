#!/usr/bin/python
#
"""
Scratch Server - MooresCloud preliminary implementation for Holiday

Homepage and documentation: http://dev.moorescloud.com/

Copyright (c) 2013, Mark Pesce.
License: MIT (see LICENSE for details)
"""

__author__ = 'Mark Pesce'
__version__ = '1.0a1'
__license__ = 'MIT'

import json, socket, os, sys
from bottle import Bottle, run, static_file, post, request, error, abort
import holiday

app = Bottle()
hol = None

globenum = 0
red = 0
green = 0
blue = 0


# And here begin the Scratch RESTful interfaces
@app.get('/crossdomain.xml')
def do_crossdomain_request():

	resp = """<cross-domain-policy>
 <allow-access-from domain="*" to-ports="19911"/>
 </cross-domain-policy>\000"""
	return resp

# And here begin the Scratch RESTful interfaces
@app.get('/poll')
def do_scratch_polls():
	global globenum, red, green, blue

	resp = """globe %d
red %2d
green %2d
blue %2d
""" % (globenum, red, green, blue)
	#print resp
	return resp

# And here begin the Scratch RESTful interfaces
@app.get('/reset_all')
def do_scratch_reset_all():
	"""Scratch sends reset_all when it begins execution. We reset all variables, and go to black"""
	global hol, globenum, red, green, blue

	globenum = 0
	red = 0
	green = 0
	blue = 0

	# And reset the string to black right here
	for i in range(hol.NUM_GLOBES):
		hol.setglobe(i, 0, 0, 0)
	hol.render()

	return

@app.get('/setstring')
def do_scratch_setstring():
	"""Set the entire string to the current RGB value"""
	global hol, red, green, blue

	# And reset the string to black right here
	for i in range(hol.NUM_GLOBES):
		hol.setglobe(i, red, green, blue)
	hol.render()

	return	

@app.get('/setglobe/<gn>')
def do_scratch_setglobe(gn):
	"""Set the current globe number, sort of like the pen that we're working on
	   We immediately set the globe to the current RGB value"""
	global hol, globenum, red, green, blue

	gn = int(gn)
	if (gn == 0):
		return			# Don't set it
	elif (gn > hol.NUM_GLOBES):
		return
	
	globenum = gn

	# Draw the current globe with the current RGB values
	hol.setglobe(globenum, red, green, blue)
	hol.render()

	return

@app.get('/setred/<rv>')
def do_scratch_setred(rv):
	"""Set the current red brightness value. We immediately set the globe to the new RGB value"""
	global hol, globenum, red, green, blue

	rv = int(rv)
	if (rv < 0):
		return			# Don't set it
	elif (rv > 255):
		return
	
	red = int(rv)
	print("set red to %s" % red)

	# Draw the current globe with the current RGB values
	hol.setglobe(globenum, red, green, blue)
	hol.render()

	return

@app.get('/setgreen/<gv>')
def do_scratch_setgreen(gv):
	"""Set the current green brightness value. We immediately set the globe to the new RGB value"""
	global hol, globenum, red, green, blue

	gv = int(gv)
	if (gv < 0):
		return			# Don't set it
	elif (gv > 255):
		return
	
	green = gv
	print("set green to %s" % green)

	# Draw the current globe with the current RGB values
	hol.setglobe(globenum, red, green, blue)
	hol.render()

	return

@app.get('/setblue/<bv>')
def do_scratch_setgreen(bv):
	"""Set the current blue brightness value. We immediately set the globe to the new RGB value"""
	global hol, globenum, red, green, blue

	bv = int(bv)
	if (bv < 0):
		return			# Don't set it
	elif (bv > 255):
		return
	
	blue = int(bv)
	print("set blue to %s" % blue)


	# Draw the current globe with the current RGB values
	hol.setglobe(globenum, red, green, blue)
	hol.render()

	return

def run_server():
	""" This is the real run method, we hope"""
	# Instance the devices that we're going to control
	# Add each to the control ring. For no very good reason.
	#

	#the_srv = 'wsgiref'  
	the_srv = 'cherrypy'
	
	print "Running..."
	# Try to run on port 19911, if that fails, dies
	try:
		app.run(host='0.0.0.0', port=19911, debug=False, server=the_srv)
	except socket.error as msg:
		print "Couldn't get the port, this is bad!"
		sys.exit(1)


if __name__ == '__main__':

	# We should have a parameter on the command line which is the IP address (or resolvable name) of the holiday
	if len(sys.argv) < 2:
		print("Usage: python scratch.py <ip address of Holiday>")
		sys.exit(-1)

	hol_ip = sys.argv[1]
	hol = holiday.Holiday(remote=True, addr=hol_ip)
	run_server()

