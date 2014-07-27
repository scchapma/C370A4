#!/usr/bin/python

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
	
	def __init__(self, name, start_date, end_date):
		self.name = name
		self.start_date = start_date
		self.end_date = end_date

	def insertCampaign(self):
		#insert try/catch
		cursor.execute("INSERT INTO Campaigns (name, startDate, endDate) VALUES (%s, %s, %s)", (self.name, self.start_date, self.end_date))

	def insertManager(self, campaign_id, employee_id):
		
		cursor.execute("INSERT INTO Manages (campaign, manager) VALUES (%d, %d)" %(campaign_id, employee_id))
		#cursor.execute("select * from Manages where campaign='%s'" %str(campaign_id))
		#dbconn.commit()

	def insertNewVolunteer(self, vol_name, vol_start_date):
				
		cursor.execute("INSERT INTO Volunteers (name, startDate, seniorVolunteer) VALUES (%s, %s, False)", (vol_name, vol_start_date))
		#change to select max id
		cursor.execute("Select id from Volunteers where name=%s", (vol_name,))
		row = cursor.fetchall()
		vol_id = int(row[0][0])
		return vol_id

	def insertVolunteerWorksOn(self, camp_id, vol_id):

		cursor.execute("INSERT INTO VolunteerWorksOn (campaign, volunteer) VALUES (%s, %s)", (int(camp_id), int(vol_id)))
		return

	def insertActivity(self, activity_start, activity_end, activity_city, activity_address, activity_memo, camp_id):
				
		cursor.execute("INSERT INTO Activities (startTime, endTime, city, address, memo) VALUES (%s, %s, %s, %s, %s)", (activity_start, activity_end, activity_city, activity_address, activity_memo))
		#obtain Activity ID
		cursor.execute("Select max(id) from Activities")
		row = cursor.fetchall()
		activity_id = int(row[0][0])
		cursor.execute("INSERT INTO Includes VALUES (%d, %d)" %(int(camp_id), activity_id))
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

	#print header
	header_str = ''
	count = 0
	for x in range(0, len(col_widths)):
		#center each header within header width	
		header_str += header[x].center(col_widths[x])
		header_str += '|'
	#delete last char
	header_str = header_str[:-1]
	print header_str
	
	#print divider
	print '-'*len(header_str)	
	
	#print rows
	for r in rows:
		row_str = ''
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
	5.  Phase 5 - *under development*\n  
	Please enter your selection (a number between 1 and 5):\n	
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
			menu4()	
			input_flag = False

		elif (main_menu_use_choice == str(5)):
			menu5()	
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
	1.   What employees and volunteers work on any campaign managed by Barry Basil (#E2)?
	2.   What employees manage the campaigns that Gary Gold (#V1) works on?
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

					print "\n\tData for query %s:\n " %menu1_use_choice
					try: 
						cursor.execute('select * from question%s' %menu1_use_choice)
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

	campaign = Campaign(campaign_name, start_date, end_date)

	###need try/catch here in case Date (or other field) not properly formed###
	
	try:
		campaign.insertCampaign()
		cursor.execute("select * from Campaigns where name='%s'" %campaign.name)
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

	os.system('clear')

	manager_str = """
	The campaign manager must be entered by employee number.
	For instance, for Amy Arugula, you would enter '1'.

	Please enter employee number: \n
	"""
	manager_emp_id = raw_input(manager_str)

	#check to see that emp_id is within range - if not, exit
	try:
		campaign.insertManager(camp_id, int(manager_emp_id))
	except:
		dbconn.rollback()
		print "Insert manager failed.\n"
		return

	#confirm that manager correct
	try:
		cursor.execute("select name from Employees, Manages where id=manager and campaign=%d" %camp_id)
		manager_str = cursor.fetchall()
		print 'Campaign manager: %s' %manager_str[0]
	except:
		dbconn.rollback()
		print "Error - could not print campaign manager.\n"

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
		print 'Changes committed.\n'
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
		cursor.execute("select name from Volunteers where name='%s'" %vol_name)
		vol_name_str = cursor.fetchall()
	except:
		dbconn.rollback()
		print "Error - could not return volunteer's name.\n"
	try:
		cursor.execute("select startdate from Volunteers where name='%s'" %vol_name)
		vol_date_str = cursor.fetchall()
	except:
		dbconn.rollback()
		print "Error - could not return volunteer's start date.\n"

	print "\n\tVolunteer's name: %s" %vol_name_str[0]
	print "\tVolunteer's start date: %s\n" %vol_date_str[0]

	confirmVolunteer()
	return
		

def oldVolunteer(campaign, camp_id):
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
		cursor.execute("select name from Volunteers where id=%d" %int(vol_id))
		old_vol_str = cursor.fetchall()
	except:
		dbconn.rollback()
		print "Insert volunteer failed - no such volunteer.\n"
		return
		
	print 'Volunteer: %s' %old_vol_str[0]

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
		print 'Exiting.\n'
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
		cursor.execute('Select * from (Volunteers join VolunteerWorksOn on id = volunteer) where campaign = %s', (int(camp_id),))
		rows = cursor.fetchall()
	except:
		dbconn.rollback()
		print "Print volunteer list failed.\n"
	if (cursor.rowcount > 0): 
		for x in range(0, len(rows[0])):
			header.append(cursor.description[x].name)
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
		print "Exiting - no volunteers added.\n"
		return
	elif query_choice == 'y':
		os.system('clear')
	else:
		print "Exiting - improper input.\n"	
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
		cursor.execute("Select * from Activities where id=%d" %(int(activity_id)))
		rows = cursor.fetchall()
	except:
		dbconn.rollback()
		print "Print activity failed.\n"
	if (cursor.rowcount > 0): 
		for x in range(0, len(rows[0])):
			header.append(cursor.description[x].name)
		print "\n\tCurrent activity: \n"
		printReport(header, rows)
	else:
		print "No activity added.\n"
	return

def showActivityList(camp_id):
	rows = []
	header = []
	try:
		cursor.execute('Select * from (Activities join Includes on id = activityid) where campaignid = %s', (int(camp_id),))
		rows = cursor.fetchall()
	except:
		dbconn.rollback()
		print "Print activity list failed.\n"
	if (cursor.rowcount > 0): 
		for x in range(0, len(rows[0])):
			header.append(cursor.description[x].name)
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
		print "Exiting - no activities added.\n"
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
	print "Welcome to menu 3 - accounting information.\n"
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
	
	#balance string
	balance = income - expenses
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
	start_date = modifyDate(start_date)
	getBalance(start_date)

	#income string
	income = getIncome(end_date) - getIncome(start_date)	
	income_header_str = "Total income for this period: "
	income_value_str = "$%s\n" %income
	income_str = income_header_str.ljust(ACCT_HEADER_WIDTH)
	income_str += income_value_str.rjust(ACCT_VALUE_WIDTH)
	print income_str
		
	#expenses string
	expenses = getExpenses(end_date) - getExpenses(start_date)
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

	getBalance(end_date)
	return

def modifyDate(start_date):
	Date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
	EndDate = Date - datetime.timedelta(days=1)
	end_date = EndDate.strftime("%Y-%m-%d")
	return end_date

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

	#obtain input information for Donations 
	#obtain input information for Expenses - max, values, labels
	donations_input = []
	expenses_input = []

	donations_str = "Select * from Donations where (donationdate >= '%s') and (donationdate <= '%s')" %(start_date, end_date)
	#donations_str = "Select * from Donations where ((donationdate >= '%s') and (donationdate <= '%s')) group by donationdate)" %(start_date, end_date)
	expenses_str = "Select * from Expenses where (expensedate >= '%s') and (expensedate <= '%s')" %(start_date, end_date)
	#expenses_str = 'Select * from Expenses'

	donations_input = processInput(donations_str)
	expenses_input = processInput(expenses_str)
	
	#produce graph for Donations
	graph("Donations", donations_input, DONATION_AMOUNT_FIELD, DONATION_TAG_FIELD)
	#produce graph for Expenses
	graph("Expenses", expenses_input, EXPENSE_AMOUNT_FIELD, EXPENSE_TAG_FIELD)
	
	accountSummary(start_date, end_date)
	return

def menu4():
	print menu4

def menu5():
	print menu5

def main():
	
	startMenu()

	#campaign = Campaign('Steve', 2014-02-24, 2014-03-17)
	#camp_id = 5
	#addActivity(campaign, camp_id)

	cursor.close()
	dbconn.close()

if __name__ == "__main__":main()