#GTG integration with GNOME Shell

The integration of GTG with GNOME Shell was a 2012 Summer of Code project realized by Baptiste Saleil.  
Homepage : [GNOME Live](https://live.gnome.org/SummerOfCode2012/Projects/BaptisteSaleil_GTG_GNOME_Shell)  
Repository : [bsaleil on Github](https://github.com/bsaleil)  
Blog : [Project blog](http://bsaleil.org/blog/)  

##Installation

This plugin add possibility to be notified about your tasks on GTG.
* Download archive, or clone repo
* Copy content on GTG plugins folder
* Active it on GTG

##Usage

###Open time picker

![alt text](http://bsaleil.org/blog/wp-content/uploads/2012/08/gtgtaskeditor.png "Task editor")

If you open task editor for a task, you'll se a new button ("Notification")
When you click it, the time picker is opened.

###Select time/date

![alt text](http://bsaleil.org/blog/wp-content/uploads/2012/08/gtgtimepicker.png "Time picker")

Here you can chose a date/time to be notified for this task.
Now you just have to confirm and an job will be remotly created with at command.

####Notification

![alt text](http://bsaleil.org/blog/wp-content/uploads/2012/08/gtg-notification.png "Notification")

When job is executed, a python script (notifify.py) will be lauch and notification will appear with "Edit" and "Done" button. For now, if GTG is closed when you click on one of the two buttons, nothing will happen so, GTG must stay open.
If you click on "Edit" button, the task editor will be open for this task.
If you click on "Done" button, the task will be mark as done on GTG.
