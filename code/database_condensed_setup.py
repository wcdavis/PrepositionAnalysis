'''
	Filename: database_setup.py
	Author: Walker Davis
	Description: Creates the databases needed for the preposition finder to 
	function properly, and inserts values of zero into every cell so that 
	null errors are avoided.

	Sample Execution:
		python database_setup.py
'''

import sys #open files
import sqlite3 as lite #SQLite database module

#File locations
database_file    = 'data.sqlite'
preposition_file = 'prepositions.txt'

#Connect to SQLite database
connnection = lite.connect(database_file)
cursor      = connnection.cursor()

#Turn preposition file into a list of prepositions
preposition_blob = open(preposition_file).read()
prepositions     = preposition_blob.splitlines() 

#Begin constructing creation commands. 
make_overall  = 'CREATE TABLE Cumulative_Overall(year INTEGER'
make_stranded = 'CREATE TABLE Cumulative_Stranded(year INTEGER'
make_word     = 'CREATE TABLE Cumulative_Words(year INTEGER, Total INTEGER); '

#Enclose preposition in parens to avoid overlap issues with SQL keywords. 
for word in prepositions:
	make_overall  = make_overall + ', \"' + word + '\" INTEGER'
	make_stranded = make_stranded + ', \"' + word + '\" INTEGER'

#Close the expression to make it a command.
make_overall  = make_overall + ', Total INTEGER); '
make_stranded = make_stranded + ', Total INTEGER); '

#Now turn it all into a script that will drop an existing table, make the new one, 
#and then put in zeros for all the values by default. This will prevent a lot of 
#weird issues that crop up when you query a non-existent value
overall_script  = 'DROP TABLE IF EXISTS Cumulative_Overall; ' + make_overall
stranded_script = 'DROP TABLE IF EXISTS Cumulative_Stranded; ' + make_stranded
word_script     = 'DROP TABLE IF EXISTS Cumulative_Words; ' + make_word

#Make a line in the script for every year.
for year in range(1000, 2014, 50):

	word_script     = word_script + 'INSERT INTO Cumulative_Words VALUES(' + str(year) + ', 0); '
	overall_script  = overall_script + 'INSERT INTO Cumulative_Overall VALUES(' + str(year)
	stranded_script = stranded_script + 'INSERT INTO Cumulative_Stranded VALUES(' + str(year)

	#Add a number of zeros equal to the number of prepositions.	
	for preposition in prepositions:
		overall_script  = overall_script + ', 0'
		stranded_script = stranded_script + ', 0'

	#Close the expression to make it a command.
	overall_script  = overall_script + ', 0); ' 
	stranded_script = stranded_script + ', 0); '

cursor.executescript(overall_script)
cursor.executescript(stranded_script)
cursor.executescript(word_script)

