import pygtk
import gtk
import gtk.glade
import os
import dbus
import time
import at
from datetime import datetime

import gobject

# TODO Delete job when task is closed (done, delete, ...)
# TODO For now, gtg have to be open when notification appears

# TODO icon
# TODO doc
# TODO design

class TimePicker:
	
	def __init__(self,plugin_api,notificationValue):
	
		self.oldNotificationId = ""
		self.notificationValue = notificationValue
		self.plugin_api = plugin_api
		self.getUI()
		
		# DBus
		bus = dbus.SessionBus()
		obj = bus.get_object("org.gnome.Shell","/org/freedesktop/Notifications")
		iface = dbus.Interface(obj,'org.freedesktop.Notifications')
		iface.connect_to_signal("ActionInvoked", self.notificationActionSignal)
		
	# Get ui from glade file and set default values
	def getUI(self):
		# Set UI from glade file
		path = os.path.dirname(__file__) + "/window.glade"
		self.builder = gtk.Builder()
		self.builder.add_from_file(path)
		
		# Get widgets
		self.window = self.builder.get_object ("MainWindow")
		self.check = self.builder.get_object("checkEnable")
		self.boxHour = self.builder.get_object("boxHour")
		self.calendar = self.builder.get_object("calendar")
		self.spinHours = self.builder.get_object("spinHours")
		self.spinMinutes = self.builder.get_object("spinMinutes")
		self.labelIndicator = self.builder.get_object("labelIndicator")
		self.buttonCancel = self.builder.get_object("buttonCancel")
		self.buttonConfirm = self.builder.get_object("buttonConfirm")
		
		#
		time = datetime.now()
		parent = self.plugin_api.get_ui().window
		self.hoursValue = self.spinHours.get_value()
		
		# Set default values
		self.window.set_transient_for(parent)
		self.boxHour.set_sensitive(0)
		self.calendar.set_sensitive(0)
		self.spinHours.set_value(time.hour%12)
		self.spinMinutes.set_value(time.minute)
		if time.hour > 12 : self.labelIndicator.set_text("PM")
		else : self.labelIndicator.set_text("AM")
		
		# Signals
		self.check.connect("toggled", self.checkSignal)
		self.spinHours.connect("value-changed", self.hoursChangedSignal)
		self.buttonCancel.connect("clicked", lambda x : self.window.destroy())
		self.buttonConfirm.connect("clicked", self.confirmSignal)
		
		# Load existing data
		self.window.show_all()
		self.loadNotificationValue()
	
	# Display notification data from current attribute (if existing)
	def loadNotificationValue(self):
		if self.notificationValue:
			array = self.notificationValue.split(",")
			
			# Check
			self.check.set_active(array[0] == "enabled")
			
			# Time
			timeArray = array[1].split(":")
			self.spinHours.set_value(float(timeArray[0]))
			self.spinMinutes.set_value(float(timeArray[1]))
			self.labelIndicator.set_text(timeArray[2])
			
			# Date
			dateArray = array[2].split(":")
			self.calendar.select_month(int(dateArray[1]),int(dateArray[0]))
			self.calendar.select_day(int(dateArray[2]))
			
			# TODO decocher case quand notification affichee
			timeStr = ""
			if timeArray[2] == "PM":
				timeStr += str(int(timeArray[0])+12)
			else:  timeStr += timeArray[0]
			timeStr += ":" + timeArray[1] + "/"
			timeStr += array[2]
			
			date = datetime.strptime(timeStr, "%H:%M/%Y:%m:%d")
			print date
		else:
			task = self.plugin_api.get_ui().get_task()
			start_date = task.get_start_date();
			due_date = task.get_due_date();
			
			if start_date:
				self.calendar.select_month(start_date.month-1,start_date.year)
				self.calendar.select_day(start_date.day)
			elif due_date:
				self.calendar.select_month(due_date.month-1,due_date.year)
				self.calendar.select_day(due_date.day)
			else:
				today = time.gmtime()
				self.calendar.select_month(today.tm_mon-1,today.tm_year)
				self.calendar.select_day(today.tm_mday)
	
	# Called when "confirm button" is pressed
	def confirmSignal(self,data):
		task = self.plugin_api.get_ui().get_task()
		if self.check.get_active() :
			# Format time
			notification = "enabled,%d:%d:%s," % (self.spinHours.get_value(),
						self.spinMinutes.get_value(),
						self.labelIndicator.get_text())
			# Format date
			date = self.calendar.get_date();
			notification += "%d:%d:%d" % (date[0], date[1], date[2])
			
			# Remove old notification if any
			oldNotification = task.get_attribute("notification")
			if oldNotification:	
				values = oldNotification.split(",")
				if len(values) >= 4:
					at.removeJob(values[3])
			
			# Launch at command
			title = "\\\"" + task.get_title() + "\\\""
			text = task.get_text().replace("<content>","").replace("</content>","")
			text = "\\\"" + text + "\\\""
			
			jobId = at.addJob(task.get_id(),title,
				text,
				date[1]+1,date[2],date[0],
				self.spinHours.get_value(),self.spinMinutes.get_value(),
				self.labelIndicator.get_text())
			
			notification += "," + jobId
			# Set data to task
			task.set_attribute("notification", notification)
			
		else :
			if self.notificationValue:
				# Remove job
				notification = task.get_attribute("notification")
				values = notification.split(",")
				
				if len(values) >= 4:
					at.removeJob(values[3])
				
				# Disable notification attribute
				n = self.notificationValue.replace("enabled","disabled")
				task.set_attribute("notification",n)
			
		self.window.destroy()
	
	# Called when checkbox state changed
	def checkSignal(self,data):
		checked = self.check.get_active()
		if not checked:
			# Hide widgets
			self.boxHour.set_sensitive(0)
			self.calendar.set_sensitive(0)
		else:
			# Show widgets
			self.boxHour.set_sensitive(1)
			self.calendar.set_sensitive(1)
	
	# Called when spin button value for hours changed
	def hoursChangedSignal(self,data):
	
		# Get previous and current values
		old = self.hoursValue
		new = self.spinHours.get_value()
		self.hoursValue = self.spinHours.get_value()
		
		# Change state of indicator if needed
		if (old == 12 and new == 1) or (old == 1 and new == 12):
			if self.labelIndicator.get_text() == "AM":
				self.labelIndicator.set_text("PM")
			else:
				self.labelIndicator.set_text("AM")
				
				
	# Called when user click on a button in a notification
		# TODO Move to extension when daemon implemented
	def notificationActionSignal(self,id,value):
		
		# Si different de l'ancienne
		if id != self.oldNotificationId:
		
			self.oldNotificationId = id
			result = value.split(':')
			if result[0] == 'edit':
				#cmd = "python " + sys.path[0] + "/openeditor.py"
				cmd = "python " + os.path.dirname(os.path.abspath(__file__)) + "/openeditor.py "
				cmd += result[1]
				cmd += " &"
				print cmd
				os.system(cmd)
			elif result[0] == 'done':
				task = self.plugin_api.get_ui().get_task()
				task.set_status("Done")

