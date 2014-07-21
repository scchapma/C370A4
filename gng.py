#!/usr/bin/python

import psycopg2

#test comment - git

#add globals here - cursor, connection
dbconn = psycopg2.connect(host='studentdb.csc.uvic.ca', user='c370_s09', password = 'o4OXQtB5')
cursor = dbconn.cursor()

class Campaign:
	'Base class for all campaigns'
	
	def __init__(self, name, start_date, end_date):
		self.name = name
		self.start_date = start_date
		self.end_date = end_date

	def insertCampaign(self):
		cursor.execute("INSERT INTO Campaigns (id, name, startDate, endDate) VALUES (%s, %s, %s, %s)", ("C7", self.name, self.start_date, self.end_date))

	def insertManager(self):
		#get campaign id#		
		#get manager's employee number or report invalid		
		cursor.execute("INSERT INTO Manages (campaign, employee) VALUES (%s, %s)", ("C7", "E1"))	
		return

	def insertNewVolunteer(self, volunteer):
		return

	def insertVolunteer(self, volunteer):
		return

	def printShortReport(self):
		return

	def printLongReport(self):
		return

#def startMenu(cursor):
def startMenu():
		
	intro_str = """Welcome to the GnG database: \n
	Main menu: \n
	1.  Pre-set database queries
	2.  Set up new campaign
	3.  Accounting
	4.  Membership history
	5.  Phase 5 - *under development*\n  
	Please enter your selection (a number between 1 and 5):\n	
	"""	
	main_menu_use_choice = raw_input(intro_str)
	print main_menu_use_choice

	if (main_menu_use_choice == str(1)):
		menu1(cursor)
		
	elif (main_menu_use_choice == str(2)):
		print 'menu2'		
		menu2(cursor)	

	elif (main_menu_use_choice == str(3)):
		menu3(cursor)

	elif (main_menu_use_choice == str(4)):
		menu4(cursor)	

	elif (main_menu_use_choice == str(5)):
		menu5(cursor)	
	
	#if choice not in range, give user three chances to correct.  If not properly entered, terminate program.
	else: 
		print 'Entered value out of range - returning to main.'
	return

def menu1(cursor):
		
	intro_str = """Please select a query from the following list: \n
	Query menu: \n
	1.   What employees and volunteers work on any campaign managed by Barry Basil (#E2)?
	2.   What employees manage the campaigns that Gary Gold (#V1) works on?
	3.   What is the salary of the employee who manages the TsawassenTelephone campaign (#C3)?
	4.   What are the IDs, names, start dates and end dates for each campaign that Harry Helium (#V2) works on?
	5.   Which campaigns, if any, have only one activity?
	6.   How much was the highest expense, and what was it for?	
	7.   Which employees or volunteers have made a single donation of at least $5000?
	8.   What is the total number of web updates that have been pushed to the website?
	9.   For each campaign, what is the average amount per expense?
	10.  How many activities does each campaign have?
	11.  Find tuples that join website updates to their campaigns.
	  
	Please enter your selection (a number between 1 and 11):\n	
	"""	
	
	#num_choices should be class constant
	num_choices = 11	
	menu1_use_choice = raw_input(intro_str)
	#print menu1_use_choice

	if(menu1_use_choice.isdigit()):
		menu_value = int(menu1_use_choice)
		if (menu_value < 1 or menu_value> num_choices):
			print "Integer entered, out of range - return to main"
			return
		else:
			
			print "\n\tData for query %s:\n " %menu1_use_choice
			cursor.execute('select * from question%s' %menu1_use_choice)
			
			row_number = 0			
			# check to ensure that this works when result is empty (i.e., # rows = 0)
			# needs to set up column headers to be in right place - get len of 			
			for row in cursor.fetchall():
				row_header = '\t'	
				count = 0			
				# print header for first row only				
				if(row_number == 0):				
					for element in row:				
						row_header += '%s\t' %cursor.description[count].name
						count += 1
					print row_header
					row_number += 1
				row_tuple = '\t'				
				for element in row:				
					row_tuple += '%s|\t' %element					
				print row_tuple	

	else:
		print "Malformed input - return to main"
		return
		

def menu2(cursor):
	intro_str = """\tTo create a new campaign, you will need to enter
	data for the several data fields. \n
	To prevent errors, please enter data in accord 
	with the format provided for each field.
	
	1.  Please enter campaign name (40 characters or less): \n	
	"""	
	campaign_name = raw_input(intro_str)
	if len(campaign_name) > 40:
		print '\n\t***Campaign name length out of limits - return to main***\n'
		return
	
	start_date_str = 'Enter campaign start date (YYYY-MM-DD): \n'
	start_date = raw_input(start_date_str) 
	#check for proper format

	end_date_str = 'Enter campaign end date (YYYY-MM-DD): \n'
	end_date = raw_input(end_date_str)
	#check for proper format

	campaign = Campaign(campaign_name, start_date, end_date)

	campaign.insertCampaign()
	cursor.execute('select * from Campaigns')
	
	for row in cursor.fetchall():		
		row_tuple = '\t'				
		for element in row:				
			#print "%s %s %s" % (row[0], row[1], row[2])				
			row_tuple += '%s\t' %element					
		print row_tuple	

	campaign.insertManager()
	cursor.execute('select * from Manages')
	
	#allow user to review table information
	#allow user to edit table information?

	manager_str = 'Enter manager for campaign (e.g. "Vladimir Putin"): \n'
	manager = raw_input(manager_str)
	#check for proper format and that manager is an employee

	volunteer_str = 'Add volunteer for campaign (e.g. "Vladimir Putin"): \n'
	volunteer = raw_input(volunteer_str)
	
def menu3(cursor):
	print menu3

def menu4(cursor):
	print menu4

def menu5(cursor):
	print menu5

def main():
	
	#output menu to user
	#user inputs selection
	#based on input, direct user to new menu

	dbconn = psycopg2.connect(host='studentdb.csc.uvic.ca', user='c370_s09', password = 'o4OXQtB5')
	cursor = dbconn.cursor()

	#startMenu(cursor)
	startMenu()

	cursor.execute("""
	select *
	from Campaigns
	""")

	#for row in cursor.fetchall():
		#print "%s %s %s" % (row[0], row[1], row[2])

	cursor.close()
	dbconn.close()

if __name__ == "__main__":main()
