#!/usr/bin/python

#Summer 2014 - CSC 370 - Assignment #4
#Steve Chapman (#V00190898)
#Database application for "Green-Not-Greed"

import psycopg2
import psycopg2.errorcodes
from psycopg2 import Date
import os
import sys
import datetime

#global variables
dbconn = psycopg2.connect(host='studentdb.csc.uvic.ca', user='c370_s09', password = 'o4OXQtB5')
cursor = dbconn.cursor()

#class constants
NUM_CHOICES = 11

#class constants - graph
AMOUNT_WIDTH = 50
AMOUNT_TAG_WIDTH = 15
MEMO_WIDTH = 15
DONATION_AMOUNT_FIELD = 1
DONATION_TAG_FIELD = 3
EXPENSE_AMOUNT_FIELD = 1
EXPENSE_TAG_FIELD = 3

#class constants - accounting summary
ACCT_HEADER_WIDTH = 40
ACCT_VALUE_WIDTH = 10

#git comment

class Campaign:
	'Base class for all campaigns'
	
	def __init__(self, name, start_date, end_date, memo):
		self.name = name
		self.start_date = start_date
		self.end_date = end_date
		self.memo = memo

	def insertCampaign(self):
		
		cursor.execute("INSERT INTO Campaigns (name, startDate, endDate, memo) VALUES (%s, %s, %s, %s)", [self.name, self.start_date, self.end_date, self.memo])

	def insertManager(self, campaign_id, employee_id):
		
		cursor.execute("INSERT INTO Manages (campaign, manager) VALUES (%s, %s)", [campaign_id, employee_id])
		#cursor.execute("select * from Manages where campaign='%s'" %str(campaign_id))
		#dbconn.commit()

	def insertNewVolunteer(self, vol_name, vol_start_date):
				
		cursor.execute("INSERT INTO Volunteers (name, startDate, seniorVolunteer) VALUES (%s, %s, False)", [vol_name, vol_start_date])
		#change to select max id
		cursor.execute("Select id from Volunteers where name=%s", [vol_name])
		row = cursor.fetchall()
		vol_id = int(row[0][0])
		return vol_id

	def insertVolunteerWorksOn(self, camp_id, vol_id):

		cursor.execute("INSERT INTO VolunteerWorksOn (campaign, volunteer) VALUES (%s, %s)", [int(camp_id), int(vol_id)])
		return

	def insertActivity(self, activity_start, activity_end, activity_city, activity_address, activity_memo, camp_id):
				
		cursor.execute("INSERT INTO Activities (startTime, endTime, city, address, memo) VALUES (%s, %s, %s, %s, %s)", [activity_start, activity_end, activity_city, activity_address, activity_memo])
		#obtain Activity ID
		cursor.execute("Select max(id) from Activities")
		row = cursor.fetchall()
		activity_id = int(row[0][0])
		cursor.execute("INSERT INTO Includes VALUES (%s, %s)", [int(camp_id), activity_id])
		#dbconn.commit()
		return activity_id

#print report
#input: list of rows, list of header fields
def printReport(header, rows):
	
	#prepare list with baseline widths for header fields
	col_widths = []


	for item in header:
		col_widths.append(len(item))
	
	#traverse each column of table to determine max length of table items
	for x in range(0, len(header)):
		for r in rows:
			
			#set header width to max of baseline header field and max length of columns
			if len(str(r[x])) > col_widths[x]:
				col_widths[x] = len(str(r[x]))
			#add padding
			col_widths[x] += 1

	#print header
	header_str = '\t'
	count = 0
	for x in range(0, len(col_widths)):
		#center each header within header width	
		header_str += header[x].center(col_widths[x])
		header_str += '|'
	#delete last char
	header_str = header_str[:-1]
	print header_str
	
	#print divider
	divider_str = '\t'
	divider_str +='-'*len(header_str)
	print divider_str	
	
	#print rows
	for r in rows:
		row_str = '\t'
		for x in range(0, len(col_widths)):
			row_str += str(r[x]).ljust(col_widths[x])
			row_str += '|'
		#delete last char
		row_str = row_str[:-1]
		print row_str	
	print '\n'
	return 

def startMenu():
		
	os.system('clear')

	intro_str = """\n\tWelcome to the GnG database: \n
	Main menu: \n
	1.  Pre-set database queries
	2.  Set up new campaign
	3.  Accounting
	4.  Membership history
	5.  Edit existing campaign
	6.  Supporters\n  
	Please enter your selection (a number between 1 and 6):\n	
	"""	
	
	main_menu_use_choice = raw_input(intro_str)
	input_flag = True

	while (input_flag):

		if (main_menu_use_choice == str(0)):
			return

		elif (main_menu_use_choice == str(1)):
			menu1()
			input_flag = False
			
		elif (main_menu_use_choice == str(2)):
			os.system('clear')		
			menu2()	
			input_flag = False

		elif (main_menu_use_choice == str(3)):
			menu3()
			input_flag = False

		elif (main_menu_use_choice == str(4)):
			os.system('clear')
			menu4()	
			input_flag = False

		elif (main_menu_use_choice == str(5)):
			menu5()	
			input_flag = False

		elif (main_menu_use_choice == str(6)):
			menu6()	
			input_flag = False
	
		else: 
			error_str = """\n\tEntered value out of range: \n
	Please enter a number between 1 and 5 or enter '0' to exit.\n
	"""
			main_menu_use_choice = raw_input(error_str)
	
	return

def menu1():

	intro_str = """\tPlease select a query from the following list: \n
	Query menu: \n
	1.   What volunteers (by ID number) work on any campaign managed by Barry Basil (#E2)?
	2.   What employees (by ID number) manage the campaigns that Gary Gold (#V1) works on?
	3.   What is the salary of the employee who manages the TsawassenTelephone campaign (#C3)?
	4.   What are the IDs, names, start dates and end dates for each campaign that Harry Helium (#V2) works on?
	5.   Which campaigns, if any, have only one activity?
	6.   How much was the highest expense, and what was it for?	
	7.   Which employees or volunteers have made a single donation of at least $5000?
	8.   What is the total number of webInsert manager updates that have been pushed to the website?
	9.   For each campaign, what is the average amount per expense?
	10.  How many activities does each campaign have?
	11.  Find tuples that join website updates to their campaigns.
	  
	Please enter your selection (a number between 1 and 11):\n	
	"""	
		
	#Initially set to true - set to false if user does not desire additional queries
	query_flag = True
	while (query_flag):		

		os.system('clear')
		menu1_use_choice = raw_input(intro_str)
		input_flag = True

		while (input_flag):

			if(menu1_use_choice.isdigit()):
				menu_value = int(menu1_use_choice)
				
				if (menu_value == 0):
					return
				
				elif (menu_value < 1 or menu_value> NUM_CHOICES):
					error_str = """\n\tInteger entered out of range: \n
	Please enter a number between 1 and 11 or enter '0' to exit.\n
	"""
					menu1_use_choice = raw_input(error_str)

				else:
					
					os.system('clear')

					print "\n\tAnswer for query %s:\n " %menu1_use_choice
					try: 
						sql = "Select * from question"
						sql += menu1_use_choice
						cursor.execute(sql)
						rows = cursor.fetchall()
						header = []
						#what if rows = 0?
						for x in range(0, len(rows[0])):
							header.append(cursor.description[x].name)
						printReport(header, rows)
						input_flag = False
					except:
						dbconn.rollback()
						print "Error - could not return query.\n"

					#check to see if user wants to return to query menu
					query_str = '\tDo you want to return to the query menu? (y/n)\n'
					query_choice = raw_input(query_str)

					if query_choice == 'y':
						input_flag = False
					else:
						print "\n\tExiting.\n"
						query_flag = False
						return
			else:
				error_str = """\n\tMalformed input: \n
	Please enter a number between 1 and 11 or enter '0' to exit.\n
	"""
				menu1_use_choice = raw_input(error_str)
	return
		

def addCampaign():
	
	intro_str = """\tTo create a new campaign, you will need to enter
	data for several data fields. \n
	To prevent errors, please enter data in accord 
	with the format provided for each field.
	
	1.  Please enter campaign name (25 characters or less): \n	
	"""	
	campaign_name = raw_input(intro_str)
	if len(campaign_name) > 25:
		print '\n\t***Campaign name length out of limits - return to main***\n'
		return
	
	start_date_str = '\n\t2.  Enter campaign start date (YYYY-MM-DD): \n\n\t'
	start_date = raw_input(start_date_str) 
	#check for proper format

	end_date_str = '\n\t3.  Enter campaign end date (YYYY-MM-DD): \n\n\t'
	end_date = raw_input(end_date_str)
	#check for proper format

	campaign = Campaign(campaign_name, start_date, end_date, '')
	
	try:
		campaign.insertCampaign()
		cursor.execute("select * from Campaigns where name=%s", [campaign.name])
	except:
		dbconn.rollback()
		print "Insert campaign failed.\n"
		return

	try:
		rows = cursor.fetchall()
	except:
		print "No rows to print."
		return

	header = []
	#what if rows = 0?
	for x in range(0, len(rows[0])):
		header.append(cursor.description[x].name)
	
	#display input to user
	print "\n\tYou have entered the following information: \n"
	printReport(header, rows)

	#camp_id = ''
	review_flag = True
	
	while (review_flag):
		#allow user to accept or reject campaign before commit
		campaign_review_string = "\n\tIs this information correct (y/n) ?\n\n\t"
		campaign_review_choice = raw_input(campaign_review_string)
		
		if (campaign_review_choice == 'y'):
			camp_id = rows[0][0]
			dbconn.commit()
			os.system('clear')
			print '\n\tChanges committed.\n'
			review_flag = False
		elif(campaign_review_choice == 'n'):
			dbconn.rollback()
			print '\n\tCampaign deleted - please start again.\n'
			return
		else:
			print '\n\tImproper input - Campaign not saved.\n'

	camp_list = []
	camp_list.append(campaign)
	camp_list.append(camp_id)
	return camp_list

def addManager(campaign, camp_id):

	no_manager_entered = True
	os.system('clear')
	count = 0
	
	while no_manager_entered:
		
		showEmployees()
		manager_emp_id = None

		manager_str = """
		Your campaign needs a campaign manager.
		
		The campaign manager must be an employee of GNG.

		Please enter the campaign manager by employee ID:The campaign manager must be entered by employee number.
		For instance, for Amy Arugula, you would enter '1'.

		Please enter employee number: \n
		"""
		manager_emp_id = raw_input(manager_str)

		#check to see that emp_id is within range - if not, exit
		try:
			campaign.insertManager(camp_id, int(manager_emp_id))
			no_manager_entered = False
		except:
			dbconn.rollback()
			os.system('clear')
			count += 1
			print "\tInsert manager failed - please try again.\n"
			print count

	#confirm that manager correct
	try:
		cursor.execute("select name from Employees, Manages where id=manager and campaign=%s", [camp_id])
		manager_str = cursor.fetchall()
		print '\n\tCampaign manager: %s' %manager_str[0]
	except:
		dbconn.rollback()
		print "Error - could not print campaign manager.\n"
		return

	manager_review_flag = True

	while (manager_review_flag):
		#allow user to accept or reject campaign before commit
		manager_review_string = "\n\tIs this information correct (y/n) ?\n\n\t"
		manager_review_choice = raw_input(manager_review_string)
		
		if (manager_review_choice == 'y'):
			dbconn.commit()
			print '\n\tChanges committed.\n'
			manager_review_flag = False
		elif(manager_review_choice == 'n'):
			dbconn.rollback()
			print '\n\tManager deleted - please start again.\n'
			return
		else:
			print '\n\tImproper input - Manager not saved.\n'
	return

def confirmVolunteer():

	#confirm that volunteer is correct
	vol_info_str = """
	Is this information correct? (y/n)? \n
	"""
	vol_info = raw_input(vol_info_str)
	if vol_info == 'y':
		dbconn.commit()
		print '\tChanges committed.\n'
	elif vol_info  == 'n':
		dbconn.rollback()
		print '\n\tVolunteer deleted - please start again.\n'
				
	else:
		print '\n\tImproper input - Volunteer not saved.\n'
	return

def newVolunteer(campaign, camp_id):

	vol_name_str = """
	Please enter the volunteer's name (first name then last name):  \n
	"""
	vol_name = raw_input(vol_name_str)
	vol_start_date_str = """
	Please enter the volunteer's start date (YYYY-MM-DD):  \n
	"""
	vol_start_date = raw_input(vol_start_date_str)
	
	try:
		vol_id = campaign.insertNewVolunteer(vol_name, vol_start_date)
		campaign.insertVolunteerWorksOn(camp_id, vol_id)
	except:
		dbconn.rollback()
		print "Insert new volunteer failed.\n"
		return

	try:
		cursor.execute("select name from Volunteers where name=%s", [vol_name])
		vol_name_str = cursor.fetchall()
	except:
		dbconn.rollback()
		print "Error - could not return volunteer's name.\n"
		return
	try:
		cursor.execute("select startdate from Volunteers where name=%s", [vol_name])
		vol_date_str = cursor.fetchall()
	except:
		dbconn.rollback()
		print "Error - could not return volunteer's start date.\n"
		return

	print "\n\tVolunteer's name: %s" %vol_name_str[0]
	print "\tVolunteer's start date: %s\n" %vol_date_str[0]

	confirmVolunteer()
	return
		

def oldVolunteer(campaign, camp_id):
	
	showVolunteers()

	vol_str = """
	The volunteer must be entered by existing volunteer number.
	For instance, for Gary Gold, you would enter '1'.

	Please enter volunteer number: \n
	"""
	vol_id = raw_input(vol_str)
	
	old_vol_str = ''
	try:
		campaign.insertVolunteerWorksOn(camp_id, vol_id)
		#confirm that manager correct
		cursor.execute("select name from Volunteers where id=%s", [int(vol_id)])
		old_vol_str = cursor.fetchall()
	except:
		dbconn.rollback()
		print "Insert volunteer failed - no such volunteer.\n"
		return
		
	print '\tVolunteer: %s' %old_vol_str[0]

	confirmVolunteer()
	return

def addAnotherVolunteer():

	addVolunteerFlag = True

	vol_add_another_str = """
	Would you like to add another volunteer? (y/n)? \n
	"""
	vol_continue = raw_input(vol_add_another_str)
	if vol_continue == 'y':
		os.system('clear')
	elif vol_continue == 'n':
		#print 'Exiting.\n'
		addVolunteerFlag = False
	else:
		print 'Improper input - exiting.\n'
		addVolunteerFlag = False
		#return
	return addVolunteerFlag

def showVolunteerList(campaign, camp_id):
	rows = []
	header = []
	try:
		cursor.execute('Select id, name, memo from (Volunteers join VolunteerWorksOn on id = volunteer) where campaign = %s', [int(camp_id)])
		rows = cursor.fetchall()
	except:
		dbconn.rollback()
		print "Print volunteer list failed.\n"
		return
	if (cursor.rowcount > 0):
		header = ["ID", "Name", "Start Date"]
		print "\n\tVolunteers for this campaign: \n"
		printReport(header, rows)
	else:
		print "No volunteers have been added to this campaign.\n"
	return

def addVolunteer(campaign, camp_id):

	addVolunteerFlag = True

	#os.system('clear')
	query_str = """
	Would you like to add any volunteers (y/n)? \n 
	"""
	query_choice = raw_input(query_str)
	if query_choice == 'n':
		print "\n\tNo volunteers added.\n"
		return
	elif query_choice == 'y':
		os.system('clear')
	else:
		print "\n\tExiting - improper input.\n"	
		return

	while (addVolunteerFlag):
		
		#new or existing volunteer?		
		volunteer_str = """
	Is the volunteer new (y/n)? \n
	"""
		volunteer_status = raw_input(volunteer_str)
	
		if(volunteer_status == 'y'):	
			newVolunteer(campaign, camp_id)

		elif(volunteer_status == 'n'):
			oldVolunteer(campaign, camp_id)

		else:
			print "\n\tImproper input - exiting program - volunteer not saved.\n"
			return

		showVolunteerList(campaign, camp_id)
		addVolunteerFlag = addAnotherVolunteer()
	return

def showActivity(activity_id):
	rows = []
	header = []
	try:
		cursor.execute("Select id, starttime, endtime, city, address, memo from Activities where id=%s", [int(activity_id)])
		rows = cursor.fetchall()
	except:
		dbconn.rollback()
		print "Print activity failed.\n"
		return
	if (cursor.rowcount > 0): 
		header = ["ID", "Start Time", "End Time", "City", "Address", "Memo"]
		print "\n\tActivities for this campaign: \n"
		printReport(header, rows)
	else:
		print "No activity added.\n"
	return

def showActivityList(camp_id):
	rows = []
	header = []
	try:
		cursor.execute('Select id, starttime, endtime, city, address, memo from (Activities join Includes on id = activityid) where campaignid = %s', [int(camp_id)])
		rows = cursor.fetchall()
	except:
		dbconn.rollback()
		print "Print activity list failed.\n"
		return
	if (cursor.rowcount > 0): 
		header = ["ID", "Start Time", "End Time", "City", "Address", "Memo"]
		print "\n\tActivities for this campaign: \n"
		printReport(header, rows)
	else:
		print "No activities have been added to this campaign.\n"
	return

def confirmActivity(activity_id):

	#print out report
	try:
		showActivity(activity_id)
	except:
		print "Error - could not generate report.\n"
		return

	#confirm that activity is correct
	activity_info_str = """
	Is this information correct? (y/n)? \n
	"""
	activity_info = raw_input(activity_info_str)
	if activity_info == 'y':
		dbconn.commit()
		print 'Changes committed.\n'
	elif activity_info  == 'n':
		dbconn.rollback()
		print '\n\tActivity deleted - please start again.\n'				
	else:
		print '\n\tImproper input - Activity not saved.\n'
	return

def addAnotherActivity():

	addActivityFlag = True

	activity_add_another_str = """
	Would you like to add another activity? (y/n)? \n
	"""
	activity_continue = raw_input(activity_add_another_str)
	if activity_continue == 'y':
		os.system('clear')
	elif activity_continue == 'n':
		print 'Exiting - campaign set up complete.\n'
		addActivityFlag = False
	else:
		print 'Improper input - exiting.\n'
		addActivityFlag = False
		#return
	return addActivityFlag

def addActivity(campaign, camp_id):
	
	addActivityFlag = True

	#os.system('clear')
	query_str = """
	Would you like to add any activities (y/n)? \n 
	"""
	query_choice = raw_input(query_str)
	if query_choice == 'n':
		print "Exiting - campaign complete - no activities added.\n"
		return
	elif query_choice == 'y':
		os.system('clear')
	else:
		print "Exiting - improper input.\n"	
		return

	while (addActivityFlag):
		
		#Add start	time	
		start_str = """
	Please enter the start time (YYYY-MM-DD HH:MM:SS): \n
	"""
		start_time = raw_input(start_str)

		#Add end time
		end_str = """
	Please enter the end time (YYYY-MM-DD HH:MM:SS): \n
	"""
		end_time = raw_input(end_str)
	
		#Add city
		city_str = """
	Please enter the city (e.g., 'Victoria' or 'Nanaimo' - max 15 characters): \n
	"""
		city = raw_input(city_str)

		#Add address
		address_str = """
	Please enter the address (e.g., 'Main Street' or 'Centennial Square' - max 20 characters): \n
	"""
		address = raw_input(address_str)

		#Add memo (25 chars max)
		memo_str = """
	If desired, enter memo information (max 25 characters).
	Otherwise, press return:  \n
	"""
		memo = raw_input(memo_str)

		#insert activity into Activities table
		#insert acitivity and campaign into Includes table
		activity_id = None
		try:
			activity_id = campaign.insertActivity(start_time, end_time, city, address, memo, camp_id)
		except:
			dbconn.rollback()
			print "Error - could not insert new activity.\n"

		if (activity_id):
			confirmActivity(activity_id)

		showActivityList(camp_id)
		addActivityFlag = addAnotherActivity()
	return


def menu2():
	
	#pass back values for campaign and camp_id
	camp_list = addCampaign()
	if(camp_list == None or camp_list[0] == None or camp_list[1] == None):
		print "Error - Campaign not added.\n"
		return
	campaign = camp_list[0]
	camp_id = camp_list[1]
	addManager(campaign, camp_id)
	addVolunteer(campaign, camp_id)
	addActivity (campaign,camp_id)
	#print final summary?
	return
	
def intro_menu3():
	os.system('clear')
	intro_str = """
	Welcome to Menu 3.

	This menu provides detailed accounting information for
	any given time period.

	Please input your desired start date and end date.

	The program will return all donations and contributions for the given period.

	The program will also return all expenses for the given period.
	"""
	print intro_str
	return

def graph(header, rows, amount_field, tag_field):
	
	#count = 0
	values = []
	labels = []
	
	if len(rows) <= 0:
		print "\n\n\n%s - No data to print.\n" %header
		return

	for r in rows:
		#need to hard code these - use class constants
		values.append(r[amount_field])
		labels.append(r[tag_field])

	max_value = max(values)	

	header_str = '\n\n\n'
	header_str += header
	print header_str
	print '-'*85
	for x in range(0, len(values)):
		row_str = ''
		unit = max_value/AMOUNT_WIDTH
		units = (values[x]/unit)
		bar = '#'*units
		row_str += bar.ljust(AMOUNT_WIDTH)
		row_str += str(values[x]).rjust(AMOUNT_TAG_WIDTH)
		row_str += ' '*5
		row_str += str(labels[x]).ljust(MEMO_WIDTH)
		print row_str
	return

def processInput(input_string):
	rows = []
	try:
		cursor.execute(input_string)
		rows = cursor.fetchall()
	except:
		dbconn.rollback()
		print "Error - could not return input for graph.\n"
	return rows

def getBalance(input_date):	

	#SQL = "SELECT SUM(amount) FROM Donations WHERE donationdate <= date('2014-01-01')"
	#SQL = "SELECT SUM(amount) FROM Donations WHERE donationdate <= convert(datetime, input_date)" %input_date 
	
	income = 0
	expenses = 0
	balance = 0

	#get income
	sql = "Select sum(amount) from Donations where donationdate <= '%s'" %input_date
	try:
		cursor.execute(sql)
		rows = cursor.fetchall()
		if rows[0][0] == None:
			#print "No donations to date.\n"
			pass
		elif cursor.rowcount <= 0:
			print "Error - no sum returned from Donations.\n"
		else:
			income = rows[0][0]
	except:
		dbconn.rollback()
		print "Error - could not obtain current balance.\n"
		return balance

	#get expenses
	sql2 = "Select sum(amount) from Expenses where expensedate <= '%s'" %input_date
	try:
		cursor.execute(sql2)
		rows2 = cursor.fetchall()
		if rows2[0][0] == None:
			#print "No expenses to date.\n"
			pass
		elif cursor.rowcount <= 0:
			print "Error - no sum returned from Expenses.\n"
		else:
			expenses = rows2[0][0]
	except:
		dbconn.rollback()
		print "Error - could not obtain current balance.\n"
		return balance
	
	balance = income - expenses
	return balance

def printBalance(balance, input_date):

	#balance string
	balance_header_str = "Balance at %s: " %(input_date)
	balance_value_str = "$%d\n" %(balance,)	
	balance_str = balance_header_str.ljust(ACCT_HEADER_WIDTH)
	balance_str += balance_value_str.rjust(ACCT_VALUE_WIDTH)
	print balance_str
	return 


def getIncome(input_date):
	
	income = 0
	sql = "Select sum(amount) from Donations where donationdate <= '%s'" %input_date
	
	try:
		cursor.execute(sql)
		rows = cursor.fetchall()
		income = rows[0][0]
		if income == None:
			income = 0
		#print "Income: $%s" %income
	except:
		print "Error - could not return income for this period.\n"
		return income
	return income

def getExpenses(input_date):
	
	expenses = 0	
	sql = "Select sum(amount) from Expenses where expensedate <= '%s'" %input_date
	
	try:
		cursor.execute(sql)
		row = cursor.fetchall()
		expenses = row[0][0]
		if expenses == None:
			expenses = 0
		#print "Expenses: $%s" %expenses
	except:
		print "Error - could not return expenses for this period.\n"
		return expenses
	return expenses

def accountSummary(start_date, end_date):
	intro_str = "\n\n\nAccounting Summary: "
	print intro_str
	header_str = '-'*len(intro_str)
	header_str += '\n'
	print header_str
	new_start_date = modifyDate(start_date)
	if not new_start_date:
		print "Error - malformed input - exiting.\n"
		return
	start_balance = getBalance(new_start_date)
	printBalance(start_balance, start_date)

	#income string
	income = getIncome(end_date) - getIncome(new_start_date)	
	income_header_str = "Total income for this period: "
	income_value_str = "$%s\n" %income
	income_str = income_header_str.ljust(ACCT_HEADER_WIDTH)
	income_str += income_value_str.rjust(ACCT_VALUE_WIDTH)
	print income_str
		
	#expenses string
	expenses = getExpenses(end_date) - getExpenses(new_start_date)
	expenses_header_str = "Total expenses for this period: "
	expenses_value_str = "$%s\n" %expenses
	expenses_str = expenses_header_str.ljust(ACCT_HEADER_WIDTH)
	expenses_str += expenses_value_str.rjust(ACCT_VALUE_WIDTH)
	print expenses_str

	#net income string
	net_income = income - expenses
	net_income_header_str = "Net income for this period: "
	net_income_value_str = "$%s\n" %net_income
	net_income_str = net_income_header_str.ljust(ACCT_HEADER_WIDTH)
	net_income_str += net_income_value_str.rjust(ACCT_VALUE_WIDTH)
	print net_income_str

	end_balance = getBalance(end_date)
	printBalance(end_balance, end_date)
	return

def modifyDate(start_date):
	try:
		Date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
		EndDate = Date - datetime.timedelta(days=1)
		end_date = EndDate.strftime("%Y-%m-%d")
		return end_date
	except:
		print "Error - improper format for entered date.\n"
		return

def menu3():
	#intro string - gives accounting information for any chosen time interval
	intro_menu3()
	
	#Add start	date	
	start_str = """
	Please enter the start date (YYYY-MM-DD): \n
	"""
	start_date = raw_input(start_str)

	#Add end date
	end_str = """
	Please enter the end date (YYYY-MM-DD): \n
	"""
	end_date = raw_input(end_str)

	donations_input = []
	expenses_input = []

	donations_str = "Select * from Donations where (donationdate >= '%s') and (donationdate <= '%s')" %(start_date, end_date)
	expenses_str = "Select * from Expenses where (expensedate >= '%s') and (expensedate <= '%s')" %(start_date, end_date)
	
	donations_input = processInput(donations_str)
	expenses_input = processInput(expenses_str)
	
	#produce graph for Donations
	graph("Donations", donations_input, DONATION_AMOUNT_FIELD, DONATION_TAG_FIELD)
	#produce graph for Expenses
	graph("Expenses", expenses_input, EXPENSE_AMOUNT_FIELD, EXPENSE_TAG_FIELD)
	
	accountSummary(start_date, end_date)
	return

def volunteerHistory():
	
	os.system('clear')

	#return list of volunteers by id number
	sql1 = "Select id from Volunteers"
	try:
		cursor.execute(sql1)
		rows = cursor.fetchall()

		for r in rows:
			value_str = str(r[0])

			#get name
			name_query = "Select name from Volunteers where id = %s"
			cursor.execute(name_query, value_str)
			names = cursor.fetchall()
			name = names[0]
			print "\tReport for %s\n" %name 

			#get campaigns
			campaign_query = "Select name, id, startdate, enddate from Campaigns, (select campaign from VolunteerWorksOn where volunteer = %s) V1C where Campaigns.id = V1C.campaign"
			cursor.execute(campaign_query, value_str)
			rows2 = cursor.fetchall()
			header = ["Campaigns", "ID", "Start", "End"]
			printReport(header, rows2) 	
	except:
		print "Error - could not return volunteer history.\n"
	return

def showCampaigns():
	
	print "\n\n\n\tCampaign Summary:\n"
	try:
		sql = "Select id, name, memo from Campaigns order by id"
		cursor.execute(sql)
		rows = cursor.fetchall()
		header = ["ID", "Name", "Memo"]
		printReport(header, rows)
	except:
		print "Error - could not print list of campaigns.\n"
	return

def showVolunteers():
	
	print "\n\n\n\tVolunteer Summary:\n"
	try:
		sql = "Select id, name, memo from Volunteers order by id"
		cursor.execute(sql)
		rows = cursor.fetchall()
		header = ["ID", "Name", "Memo"]
		printReport(header, rows)
	except:
		print "Error - could not print list of volunteers.\n"
	return

def showSupporters():
	
	print "\n\n\n\tSupporter Summary:\n"
	try:
		sql = "Select id, name from Supporters order by id"
		cursor.execute(sql)
		rows = cursor.fetchall()
		header = ["ID", "Name"]
		printReport(header, rows)
	except:
		print "Error - could not print list of supporters.\n"
	return

def showEmployees():
	
	print "\n\n\n\tEmployee Summary:\n"
	try:
		sql = "Select id, name from Employees order by id"
		cursor.execute(sql)
		rows = cursor.fetchall()
		header = ["ID", "Name"]
		printReport(header, rows)
	except:
		print "Error - could not print list of employees.\n"
	return

def addCampaignMemo():

	#list campaigns by id, name
	showCampaigns()
	intro_str = """
	Please select your desired campaign by ID number: \n
	"""	
	camp_id_str = raw_input(intro_str)

	memo_str = """
	Please enter your memo (25 characters max): \n
	"""
	memo = raw_input(memo_str)

	#try to update DB
	try:
		sql = "Update Campaigns set memo = %s where id = %s"
		data = [memo, camp_id_str]
		cursor.execute(sql, data)
		sql = "Select id, name, memo from Campaigns where id = %s"
		data = [camp_id_str]
		cursor.execute(sql,data)
		rows = cursor.fetchall()
		if cursor.rowcount == 0:
			print "Campaign ID does not exist.\n"
			return
		header = ['ID', 'Name', 'Memo']
		printReport(header, rows)
		dbconn.commit()
	except:
		dbconn.rollback()
		print "Error - could not update campaign memo.\n"

	#if invalid, will not update DB

	return

def addVolunteerMemo():

	#list campaigns by id, name
	showVolunteers()

	intro_str = """
	Please select your desired volunteer by ID number: \n
	"""	
	vol_id_str = raw_input(intro_str)

	memo_str = """
	Please enter your memo (25 characters max): \n
	"""
	memo = raw_input(memo_str)

	#try to update DB
	try:
		sql = "Update Volunteers set memo = %s where id = %s"
		data = [memo, vol_id_str]
		cursor.execute(sql, data)
		sql = "Select id, name, memo from Volunteers where id = %s"
		data = [vol_id_str]
		cursor.execute(sql,data)
		rows = cursor.fetchall()
		if cursor.rowcount == 0:
			print "Volunteer ID does not exist.\n"
			return
		header = ['ID', 'Name', 'Memo']
		printReport(header, rows)
		dbconn.commit()
	except:
		dbconn.rollback()
		print "Error - could not update volunteer memo.\n"

	#if invalid, will not update DB

	return

def menu4():

	menu4_flag = True
	while menu4_flag:	

		intro_str = """\tPlease select an option from the following list: \n
		
		1.   Display volunteer history
		2.   Display campaign names and IDs
		3.   Display volunteer names and IDs
		4.   Add/edit campaign memo
		5.   Add/edit volunteer memo

		Please enter your selection (a number between 1 and 5)
		or exit by typing 0:\n	
		"""	

		menu4_choice = raw_input(intro_str)

		if menu4_choice == '0':
			return

		elif menu4_choice == '1':
			os.system('clear')
			volunteerHistory()

		elif menu4_choice == '2':
			os.system('clear')
			showCampaigns()

		elif menu4_choice == '3':
			os.system('clear')
			showVolunteers()

		elif menu4_choice == '4':
			os.system('clear')
			addCampaignMemo()

		elif menu4_choice == '5':
			os.system('clear')
			addVolunteerMemo()

		else:
			os.system('clear')
			print "Improper input - please try again.\n"
		
		if (menu4_choice == '1') or (menu4_choice == '2') or (menu4_choice == '3') or (menu4_choice == '4') or (menu4_choice == '5'):

			menu_str = """
			Press 1 to return to the last menu 
			or any other key to exit the program: \n
			"""

			menu4_return_choice = raw_input(menu_str)
			if menu4_return_choice == '1':
				os.system('clear')
			else:		
				print "Exiting program.\n"
				menu4_flag = False
	return

def updatedCampaign(cursor, rows):

	if cursor.rowcount == 0:
		print "Campaign ID does not exist.\n"
		return
	header = ['ID', 'Name', 'Start Date', 'End Date', 'Memo']
	print "\n\tUpdated name of Campaign: \n"
	printReport(header, rows)

def showCampaignSummary():
	
	print "\n\n\n\tCampaign Summary:\n"
	try:
		sql = "Select * from Campaigns order by id"
		cursor.execute(sql)
		rows = cursor.fetchall()
		header = ["ID", "Name", "Start Date", "End Date", "Memo"]
		printReport(header, rows)
	except:
		print "Error - could not print list of campaigns.\n"
	return


def confirmID(camp_choice):
	sql = "Select id from Campaigns"
	cursor.execute(sql)
	rows = cursor.fetchall()

	return

def menu5():
	#show campaigns
	
	exit_flag = False
	while exit_flag == False:
		os.system('clear')
		showCampaignSummary()

		#select campaign by ID number
		intro_str = """
		Please enter the ID of the campaign you wish to edit:\n
		"""
		camp_choice = raw_input(intro_str)

		#confirm valid ID
		confirmID(camp_choice)

		#choose attribute to update
		#os.system('clear')
		menu_str = """
		You can edit any of the following campaign attributes:
		
		1.    Name
		2.    Start Date
		3.    End Date

		Please enter the campaign attribute that you wish to edit:\n
		"""
		attribute_choice = raw_input(menu_str)

		str_1 = "\n\tPlease enter the new campaign name (25 characters max):\n\n\t"
		str_2 = "\n\tPlease enter the new start date (YYYY-MM-DD):\n\n\t"
		str_3 = "\n\tPlease enter the new end date (YYYY-MM-DD):\n\n\t"

		if (attribute_choice == '1'):

			os.system('clear')
			input_correct_flag = False
			while input_correct_flag == False:
				
				new_name = raw_input(str_1)
				try:
					sql = "Update Campaigns set name = %s where id = %s"
					data = [new_name, camp_choice]
					cursor.execute(sql, data)
					sql = "Select * from Campaigns where id = %s"
					data = [camp_choice]
					cursor.execute(sql,data)
					rows = cursor.fetchall()
					if cursor.rowcount == 0:
						print "Campaign ID does not exist.\n"
						return
					header = ['ID', 'Name', 'Start Date', 'End Date', 'Memo']
					print "\n\tUpdated Campaign: \n"
					printReport(header, rows)
					confirm_str = "\n\tIs this information correct? (y/n)\n\t"
					confirm_choice = raw_input(confirm_str)
					if confirm_choice =='y':
						dbconn.commit()
						print "\tInformation saved.\n"
						input_correct_flag = True
						exit_flag = True
					else:
						os.system('clear')
						print "\n\tInformation not saved - please try again.\n"
				except:
					dbconn.rollback()
					print "Error - could not update campaign name.\n"

		elif (attribute_choice == '2'):
			
			os.system('clear')
			input_correct_flag = False
			while input_correct_flag == False:
				new_start_date = raw_input(str_2)
				try:
					sql = "Update Campaigns set startDate = '%s' where id = %s" %(new_start_date, camp_choice)
					data = [new_start_date, camp_choice]
					cursor.execute(sql, data)
					sql = "Select * from Campaigns where id = %s"
					data = [camp_choice]
					cursor.execute(sql,data)
					rows = cursor.fetchall()
					if cursor.rowcount == 0:
						print "Campaign ID does not exist.\n"
						return
					header = ['ID', 'Name', 'Start Date', 'End Date', 'Memo']
					print "\n\tUpdated Campaign: \n"
					printReport(header, rows)
					confirm_str = "\n\tIs this information correct? (y/n)\n\t"
					confirm_choice = raw_input(confirm_str)
					if confirm_choice =='y':
						dbconn.commit()
						print "\tInformation saved.\n"
						input_correct_flag = True
						exit_flag = True
					else:
						os.system('clear')
						print "\n\tInformation not saved - please try again.\n"
				except:
					dbconn.rollback()
					print "Error - could not update campaign start date.\n"	
		
		elif (attribute_choice == '3'):
			
			os.system('clear')
			input_correct_flag = False
			while input_correct_flag == False:
				new_end_date = raw_input(str_2)
				try:
					sql = "Update Campaigns set endDate = '%s' where id = %s" %(new_end_date, camp_choice)
					data = [new_end_date, camp_choice]
					cursor.execute(sql, data)
					sql = "Select * from Campaigns where id = %s"
					data = [camp_choice]
					cursor.execute(sql,data)
					rows = cursor.fetchall()
					if cursor.rowcount == 0:
						print "Campaign ID does not exist.\n"
						return
					header = ['ID', 'Name', 'Start Date', 'End Date', 'Memo']
					print "\n\tUpdated Campaign: \n"
					printReport(header, rows)
					confirm_str = "\n\tIs this information correct? (y/n)\n\t"
					confirm_choice = raw_input(confirm_str)
					if confirm_choice =='y':
						dbconn.commit()
						print "\tInformation saved - exiting.\n"
						input_correct_flag = True
						exit_flag = True
					else:
						os.system('clear')
						print "\n\tInformation not saved - please try again.\n"
				except:
					dbconn.rollback()
					print "Error - could not update campaign end date.\n"
		else:
			print "\n\tImproper input - please enter a valid attribute number.\n"	
	print "\n\tExiting.\n"		
	return

def showVolunteersByCampaign(camp_id):

	#os.system('clear')

	#return list of volunteers by id number
	try:
		sql = "Select id, name from Volunteers, VolunteerWorksOn where (volunteer = id) and (campaign=%s)"
		data = [camp_id]
		cursor.execute(sql, data)
		rows = cursor.fetchall()
		header = ["ID", "Volunteer Name"]
		printReport(header, rows)
	except:
		print "Error - could not return campaign's volunteer list.\n"
	return

def convertToVolunteer(vol_id):
	#cursor.execute("INSERT INTO Volunteers (name, startDate, seniorVolunteer) VALUES (%s, %s, False)", [vol_name, vol_start_date])
	try:
		sql = "Select name from Supporters where id=%s"
		data = [vol_id]
		cursor.execute(sql, data)
		rows = cursor.fetchall()
		vol_name = rows[0][0]
		sql = "Insert into Volunteers (name, startDate, seniorVolunteer) values (%s, '2014-01-01', False)"
		data = [vol_name]
		cursor.execute(sql, data)
		dbconn.commit()
		cursor.execute("Select id from Volunteers where name=%s", [vol_name])
		row = cursor.fetchall()
		vol_id = int(row[0][0])
		return vol_id
	except:
		print "\n\tError - could not convert support to volunteer.\n"
	return

def menu6():
	#menu: show volunteers, add new volunteer, update existing volunteer
	#add new volunteer
	#update - show volunteer chart
	intro_str = """
	This option allows you to add a volunteer or supporter 
	to an existing campaign.

	Please make your selection from the following list:

	1.   Add volunteer
	2.   Add supporter

	Press '0' to exit.\n
	"""

	intro_choice = raw_input(intro_str)

	if intro_choice == '0':
		"\n\tExiting.\n"
		return

	elif intro_choice == '1':
		#show campaigns
		showCampaigns()
		#pick a campaign
		camp_str = "\n\tSelect a campaign by campaign ID: \n\t"
		camp_choice = raw_input(camp_str)
		#show volunteers
		showVolunteers()
		#pick a volunteer
		vol_str = "\n\tSelect a volunteer by volunteer ID: \n\t"
		vol_choice = raw_input(vol_str)
		#add volunteer to campaign - worksOn
		#add check to see if volunteer already works on campaign 
		try:
			sql = "Insert into VolunteerWorksOn (campaign, volunteer) values (%s, %s)"
			data = [int(camp_choice), int(vol_choice)]
			cursor.execute(sql, data)
			dbconn.commit()
		except:
			print "\n\tError: could not insert volunteer.\n"
			print "\n\tExiting.\n"
		#show volunteer list for campaign
		print "\n\tUpdated Campaign Volunteers:\n"
		showVolunteersByCampaign(camp_choice)
		print "\n\tExiting.\n"
		return

	elif intro_choice == '2':
		#show campaigns
		showCampaigns()
		#pick a campaign
		camp_str = "\n\tSelect a campaign by campaign ID: \n\t"
		camp_choice = raw_input(camp_str)
		#show supporter
		showSupporters()
		#pick a supporter
		sup_str = "\n\tSelect a supporter by supporter ID: \n\t"
		sup_choice = raw_input(sup_str)
		vol_id = convertToVolunteer(sup_choice)
		#get new vol_id #

		#add volunteer to campaign - worksOn
		#add check to see if volunteer already works on campaign 
		try:
			sql = "Insert into VolunteerWorksOn (campaign, volunteer) values (%s, %s)"
			data = [int(camp_choice), int(vol_id)]
			cursor.execute(sql, data)
			dbconn.commit()
		except:
			print "\n\tError: could not insert supporter.\n"
			print "\n\tExiting.\n"
		#show volunteer list for campaign
		print "\n\tUpdated Campaign Volunteers:\n"
		showVolunteersByCampaign(camp_choice)
		print "\n\tExiting.\n"
		return

	return


def main():
	
	startMenu()

	#campaign = Campaign('Steve', '2014-02-24', '2014-03-17')
	#camp_id = 5
	#addActivity(campaign, camp_id)

	cursor.close()
	dbconn.close()

if __name__ == "__main__":main()
