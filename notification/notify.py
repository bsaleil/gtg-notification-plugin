# This script send a notification to the Shell with :
# Args : id, title, description

import dbus
import sys

if len(sys.argv) >= 3 :
	
	debug = open("/home/bapt/Bureau/debug", "w")
	#print sys.argv
	debug.write(str(sys.argv))
	debug.close()

	# Get args
	id = sys.argv[1]
	title = sys.argv[2]
	if len(sys.argv) == 3 : description = " "
	else : 
		description = sys.argv[3]
		if len(description) > 200:
			description = description[:200]
			description += "..."

	# DBus
	bus = dbus.SessionBus()
	remote_object = bus.get_object("org.gnome.Shell","/org/freedesktop/Notifications")
	iface = dbus.Interface(remote_object, 'org.freedesktop.Notifications')

	# Send notification
	edit = 'edit:' + id
	done = 'done:' + id
	iface.Notify('GTG',0,'gtg',title,description,[edit,'Edit...',done,'Done!'],[],4)
