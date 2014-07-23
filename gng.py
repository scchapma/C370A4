#!/usr/bin/python

import psycopg2
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
		cursor.execute("INSERT INTO Campaigns (id, name, startDate, endDate) VALUES (%s, %s, %s, %s)", ("C12", self.name, self.start_date, self.end_date))

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
		
	#os.system('clear')

	intro_str = """\tPlease select a query from the following list: \n
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
					
					#row_number = 0			
					# check to ensure that this works when result is empty (i.e., # rows = 0)
					# needs to set up column headers to be in right place - get len of 			
					#for row in cursor.fetchall():
					#	row_header = '\t'	
					#	count = 0			
					#	# print header for first row only				
					#	if(row_number == 0):				
					#		for element in row:				
					#			row_header += '%s\t' %cursor.description[count].name
					#		print row_header
					#		row_number += 1
					#	row_tuple = '\t'				
					#	for element in row:				
					#		row_tuple += '%s|\t' %element					
					#	#print ascii black block - ASCII number 178 or 219
					#	row_tuple += chr(35)
					#	row_tuple += '\n'
					#	print row_tuple	
					#	input_flag = False

			else:
				error_str = """\n\tMalformed input: \n
	Please enter a number between 1 and 11 or enter '0' to exit.\n
	"""
				menu1_use_choice = raw_input(error_str)

	return
		

def menu2():
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
	#cursor.execute('select * from Campaigns where campaign_name = %s', campaign.name)
	#cursor.execute('select * from Campaigns where name = "Steve"')
	#***Review this line***
	cursor.execute("select * from Campaigns")

	#display to user
	#any changes?  if so, which fields?  if not, commit
	print "You have entered the follwing information: \n"
	
	for row in cursor.fetchall():		
		row_tuple = '\t'				
		for element in row:				
			#print "%s %s %s" % (row[0], row[1], row[2])				
			row_tuple += '%s\t' %element					
		print row_tuple	

	campaign_review_string = "Is this information correct (yes/no) ?\n"
	campaign_review_choice = raw_input(campaign_review_string)
	if (campaign_review_choice == 'yes'):
		print 'yes'
	elif(campaign_review_choice == 'no'):
		print 'no'
	else:
		print 'Improper input - return to main'
		return 

	#campaign.insertManager()
	#cursor.execute('select * from Manages')
	
	#allow user to review table information
	#allow user to edit table information?

	manager_str = 'Enter manager for campaign (e.g. "Vladimir Putin"): \n'
	manager = raw_input(manager_str)
	#check for proper format and that manager is an employee

	volunteer_str = 'Add volunteer for campaign (e.g. "Vladimir Putin"): \n'
	volunteer = raw_input(volunteer_str)
	
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
	
	startMenu()

	dbconn.commit()

	cursor.close()
	dbconn.close()

if __name__ == "__main__":main()
