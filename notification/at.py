import os
import sys

# Add given job to jobs using the at command
def addJob(id,title,text,month,day,year,hour,minute,indicator):
	
	path = os.path.dirname(os.path.abspath(__file__)) + "/notify.py"
	command = "python " + path + " " + str(id) + " " + title + " " + text
	#print command
	
	# Get current jobs
	os.system("atq > jobs")
	
	# Launch "at" command
	strMinute = ""
	if minute < 10: strMinute = "0"
	strMinute += "%.0f"% minute
	
	date = "%.0f"% hour+":"+strMinute+indicator+" "+str(month)+"/"+str(day)+"/"+str(year)
	os.system("echo \"export DISPLAY=:0.0;"+command+"\" | at " + date)
	
	# Get current jobs
	os.system("atq > jobsNew")
	
	id = findNewId()
	
	return id

# Remove job with the given id
def removeJob(id):

	os.system("atrm " + str(id))
	
# Find id of the job just added
def findNewId():

	f1 = open("jobs", "r")
	f2 = open("jobsNew", "r")
	
	jobs = f1.readlines()
	jobsNew = f2.readlines()
	
	f1.close()
	f2.close()
	
	os.remove('jobs')
	os.remove('jobsNew')
	
	newJob = ""
	exists = False
	for jobNew in jobsNew:
		exists = False
		for job in jobs:
			if job == jobNew: exists = True
		if exists == False: newJob = jobNew
	
	# Get only id
	id,rest = newJob.split('\t',1)
	return id

