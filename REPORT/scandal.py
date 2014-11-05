'''
	Filename: prep_finder.py
	Author: Walker Davis
	Description: Finds the number of stranded prepositions as well as the total
	number of prepositions in a text file and then logs it to a SQLite database.

	Sample Execution: 
		python prep_finder.py filename year
		python prep_finder.py InfiniteJest.txt 1996
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

#Take in the name of the file and publication date from the command line, 
#open it and then read it all in to a long string
filename         = sys.argv[1]
year             = sys.argv[2]
corpus           = open(filename)

#IMPORTANT: Uncomment the read method that will ignore the copyright notice of the file
#story            = corpus.read().split("*END*")[2]
#story            = corpus.read().split("***")[2]
#story            = corpus.read()

cursor.execute('SELECT Total FROM Cumulative_Words WHERE \"year\" = ' + year)
prev_words = cursor.fetchone()[0]
num_words        = str(len(story.split(' ')) + prev_words)

total_overall = 0
total_stranded = 0

#for every word in the preposition list...
for word in prepositions:

	#get the existing values from the tables so that we increment properly
	cursor.execute('SELECT \"' + word 
		+ '\" FROM Cumulative_Overall WHERE \"year\" = ' + year)
	prev_overall = cursor.fetchone()[0]

	cursor.execute('SELECT \"' + word 
		+ '\" FROM Cumulative_Stranded WHERE \"year\" = ' + year)
	prev_stranded = cursor.fetchone()[0]

	#the overall frequency of a word is the number of times we find it in a 
	#substring preceded by a space. We add the previous result.
	num_overall = str(story.count(' ' + word) + prev_overall)
	total_overall = str(int(total_overall) + int(num_overall))

	#the number of stranded prepositions is found by looking at the length
	#of the list of substrings that fulfill the regex. We add the previous result.
	num_stranded = str(len(re.findall('\s' + word + '[.?!;]', story)) + prev_stranded) 
	total_stranded = str(int(total_stranded) + int(num_stranded))

	#update the tables with SQL commands
	cursor.executescript('UPDATE Cumulative_Overall SET \"' 
		+ word + '\" =' + num_overall + ' WHERE year=' + year + ';')

	cursor.executescript('UPDATE Cumulative_Stranded SET \"' 
		+ word + '\"=' + num_stranded + ' WHERE year=' + year + ';')

#Increment word table with number of words in the year
cursor.executescript('UPDATE Cumulative_Words SET Total=' 
	+ num_words + ' WHERE year=' + year)
cursor.executescript('UPDATE Cumulative_Overall SET Total=' 
	+ total_overall + ' WHERE year=' + year)
cursor.executescript('UPDATE Cumulative_Stranded SET Total=' 
	+ total_stranded + ' WHERE year=' + year)

