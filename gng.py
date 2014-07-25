#!/usr/bin/python

import psycopg2
import psycopg2.errorcodes
import os
import sys
#from ascii_graph import Pyasciigraph

#global variables
dbconn = psycopg2.connect(host='studentdb.csc.uvic.ca', user='c370_s09', password = 'o4OXQtB5')
cursor = dbconn.cursor()

#class constants
num_choices = 11

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
		#get campaign id#	
		#get manager's employee number or report invalid
		#insert try/catch

		cursor.execute("INSERT INTO Manages (campaign, manager) VALUES (%d, %d)" %(campaign_id, employee_id))
		#cursor.execute("select * from Manages where campaign='%s'" %str(campaign_id))
		#dbconn.commit()

	def insertNewVolunteer(self, vol_name, vol_start_date):
				
		cursor.execute("INSERT INTO Volunteers (name, startDate, seniorVolunteer) VALUES (%s, %s, False)", (vol_name, vol_start_date))
		cursor.execute("INSERT INTO VolunteerWorksOn (campaign, ) VALUES (%s, %s, False)", (vol_name, vol_start_date))
		
		return

	def insertVolunteer(self, volunteer):
		return

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
				
				elif (menu_value < 1 or menu_value> num_choices):
					error_str = """\n\tInteger entered out of range: \n
	Please enter a number between 1 and 11 or enter '0' to exit.\n
	"""
					menu1_use_choice = raw_input(error_str)

				else:
					
					os.system('clear')

					print "\n\tData for query %s:\n " %menu1_use_choice
					cursor.execute('select * from question%s' %menu1_use_choice)
					rows = cursor.fetchall()
					header = []
					#what if rows = 0?
					for x in range(0, len(rows[0])):
						header.append(cursor.description[x].name)
					printReport(header, rows)
					input_flag = False

					#check to see if user wants to return to query menu
					query_str = '\tDo you want to return to the query menu? (y/n)\n'
					query_choice = raw_input(query_str)

					if query_choice == 'y':
						dummy_str = ''
					else:
						query_flag = False
						return
			else:
				error_str = """\n\tMalformed input: \n
	Please enter a number between 1 and 11 or enter '0' to exit.\n
	"""
				menu1_use_choice = raw_input(error_str)

	return
		

#def checkManagerNumber(man_id_str):
#	isEmployee = True
#	man_id = int(man_id_str)
#		Select name
#		From Employees
#	""", (man_id,))
#	if cursor.rowcount == 0:
#		isEmployee = False


def addManager(campaign, camp_id):

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
		print "Insert manager failed.\n"
		return

	#confirm that manager correct
	cursor.execute("select name from Employees, Manages where id=manager and campaign=%d" %camp_id)
	manager_str = cursor.fetchall()
	print 'Campaign manager: %s' %manager_str[0]

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

def newVolunteer(campaign, camp_id):

	vol_name_str = """
	Please enter the volunteer's name (first name then last name):  \n
	"""
	vol_name = raw_input(vol_name_str)
	vol_start_date_str = """
	Please enter the volunteer's start date (YYYY-MM-DD):  \n
	"""
	vol_start_date = raw_input(vol_start_date_str)
	campaign.insertNewVolunteer(vol_name, vol_start_date)
	#confirm that volunteer is correct
	cursor.execute("select name from Volunteers where name='%s'" %vol_name)
	vol_name_str = cursor.fetchall()
	cursor.execute("select startdate from Volunteers where name='%s'" %vol_name)
	vol_date_str = cursor.fetchall()

	print "\n\tVolunteer's name: %s" %vol_name_str[0]
	print "\tVolunteer's start date: %s\n" %vol_date_str[0]

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

def oldVolunteer(campaign, camp_id):
	print "Enter oldVolunteer method.\n"
	#enter volunteer's #
	#confirm volunteer information
	return

def addAnotherVolunteer():

	addVolunteerFlag = True
	vol_add_another_str = """
	Would you like to add another volunteer? (y/n)? \n
	"""
	vol_continue = raw_input(vol_add_another_str)
	if vol_continue == 'y':
		dummy = 0
	elif vol_continue == 'n':
		print 'Return to main menu.\n'
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
		cursor.execute('Select * from VolunteerWorksOn where campaign = %s', (int(camp_id),))
		rows = cursor.fetchall()
	except:
		print "Print volunteer list failed.\n"
	if (cursor.rowcount): 
		for x in range(0, len(rows[0])):
			header.append(cursor.description[x].name)
		print "\n\tVolunteers for this campaign: \n"
		printReport(header, rows)
	else:
		print "No volunteers have been added to this campaign.\n"
	return

def addVolunteer(campaign, camp_id):

	addVolunteerFlag = True
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


def menu2():
	
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
			print '\n\tChanges committed.\n'
			review_flag = False
		elif(campaign_review_choice == 'n'):
			dbconn.rollback()
			print '\n\tCampaign deleted - please start again.\n'
			return
		else:
			print '\n\tImproper input - Campaign not saved.\n'

	addManager(campaign, camp_id)
	addVolunteer(campaign, camp_id)
	
def menu3():
	print menu3

def menu4():
	print menu4

def menu5():
	print menu5

def testGraph():

	cursor.execute("""
	select *
	from Expenses 
	""")

	expenses = []
	for row in cursor.fetchall():
		expenses.append(row[3], row[1])

	graph = Pyasciigraph()
	for line in  graph.graph('Expenses', expenses):
   		print(line)

def main():
	
	#startMenu()

	campaign = Campaign('Steve', 2014-02-24, 2014-03-17)
	camp_id = 50
	addVolunteer(campaign, camp_id)

	cursor.close()
	dbconn.close()

if __name__ == "__main__":main()
