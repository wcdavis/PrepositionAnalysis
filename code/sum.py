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

for preposition in prepositions:
	cursor.execute('SELECT sum(\"' + preposition + '\") FROM Cumulative_Overall;')
	print cursor.fetchone()[0] 

