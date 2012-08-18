import gtk
from timepicker import TimePicker
from GTG import _
import dbus

class Notification:
	def __init__(self):
		self.example = "This can initialize a class"

	def activate(self, plugin_api):
		print "the plugin is initialized"

	def onTaskOpened(self, plugin_api):
		self.plugin_api = plugin_api
		
		# If editor is opened
		if not plugin_api.is_browser():
			# Add button to toolbar	
			self.hourButton = gtk.ToolButton()
			plugin_api.add_toolbar_item(self.hourButton)
			self.hourButton.show()
			self.hourButton.connect("clicked", self.openTimePicker)

	# Open time picker
	def openTimePicker(self,data):
		# Get current value
		notificationValue = self.plugin_api.get_ui().get_task().get_attribute("notification")
		task = self.plugin_api.get_ui().get_task()
		self.timePicker = TimePicker(self.plugin_api,notificationValue)
		
	def deactivate(self, plugin_api):
		print "the plugin was deactivated"
		
