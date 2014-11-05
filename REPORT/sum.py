'''
	Filename: prep_finder.py
	Author: Walker Davis
	Description: Returns the accumulated values for each preposition.

	Sample Execution: 
		python sum.py
'''
import sys #open files
import re #regular expression 
import sqlite3 as lite #SQLite database module

#Important files
database_file    = 'data.sqlite'
stranded_table   = 'Cumulative_Stranded'
overall_table    = 'Cumulative_Overall'
word_table       = 'Cumulative_Words'
preposition_file = 'prepositions.txt'

#Connect to SQLite database
connnection = lite.connect(database_file)
cursor = connnection.cursor()

#Turn preposition file into a list of prepositions
preposition_blob = open(preposition_file).read()
prepositions = preposition_blob.splitlines() 

#Print the total usage of each preposition
for preposition in prepositions:
	cursor.execute('SELECT sum(\"' + preposition + '\") FROM Cumulative_Overall;')
	print cursor.fetchone()[0] 