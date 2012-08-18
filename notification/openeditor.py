# This script open GTG task editor for given task id

import dbus
import sys

def openTaskEditor():
	
	if len(sys.argv) == 2:
		bus = dbus.SessionBus()
		obj = bus.get_object("org.gnome.GTG","/org/gnome/GTG")
		iface = dbus.Interface(obj,'org.gnome.GTG')
		iface.OpenTaskEditor(sys.argv[1])

openTaskEditor()
