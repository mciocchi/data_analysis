# data_analysis.py
# by Matt Ciocchi 
# Tested under Python 2.7.3 on Ubuntu 12.04
#
# Runtime instructions:
# 
# In a linux, Unix, or OSX environment, place comma separated artists file to be parsed in user $HOME directory.
# Make sure data_analysis.py is executable. From the prompt move into the directory containing data_analysis.py, and type:
#
# chmod +x data_analysis.py
# python data_analysis.py
#
# After that, script should produce appropriate output in a matter of minutes.

import csv
from os.path import expanduser

def isartistinline(artist, line):
	"""
	Simple boolean check that returns True if an artist is in a given line of the csv, False otherwise.
	"""
	results= [artist['artist'] == otherartist for otherartist in line['line']]
	return True in results

def check(artist1, artist2):
	"""
	Return True if two artists occur together in 50 or more lines, False otherwise.
	"""
	return len(artist1['line_numbers'].intersection(artist2['line_numbers'])) >= 50 and artist2 != artist1

def filterdupes(artists_with_50_matches):
	"""
	Filter duplicate artists from artists_with_50_matches, return a list of unique entries.
	"""
	uniqueitems= []
	for artist in artists_with_50_matches:
		if artist not in uniqueitems and artist['matches']:
			uniqueitems.append(artist)
	return uniqueitems

def pairupartists(artists_with_50_matches):
	"""
	Pull in artists_with_50_matches, return a list of paired names to prepare them for output.
	"""
	pairs= []

	for artist in artists_with_50_matches:
		for match in artist['matches']:
			pairs.append((artist['artist'], match))

	def reversepair(pair):
		return (pair[1], pair[0])

	def filterreversepairs(pairs):
		"""
		Consider pairs with ('foo', 'bar') equivalent to ('bar', foo') and weed them out.
		"""
		for pair1 in pairs:
			for pair2 in pairs:
				if pair2 == reversepair(pair1):
					pairs.remove(pair2)
		return pairs
	pairs= filterreversepairs(pairs)
	return pairs

def outputpair(pair):
	"""
	Format output accordingly, and print.
	"""
	outputline= ''
	outputline= outputline+pair[0]+','+' '+pair[1]
	print(outputline)

lines= []
artists_list_small= open(expanduser('~')+'/Artist_lists_small.txt', 'r')
reader= csv.reader(artists_list_small)
[lines.append({'line_number':reader.line_num,'line':line}) for line in reader]
artists_list_small.close()

artists= []
[artists.extend(line['line']) for line in lines]
artists= list(set(artists))
artists=[{'artist':artist, 'line_numbers':set([]), 'matches':set([])} for artist in artists]

# If an artist is in the line, append the number of the line to the artist.
for artist in artists:
	for line in lines:
		if isartistinline(artist, line):
			artist['line_numbers'].add(line['line_number'])

# Check every artist against every other artist to see if they coexist on 50 or more lines. If they do, add them to the list "artists_with_50_matches."
artists_with_50_matches= []
for artist in artists:
	for otherartist in artists:
		if check(artist, otherartist):
			otherartist['matches'].add(artist['artist'])
			artists_with_50_matches.append(otherartist)

artists_with_50_matches= filterdupes(artists_with_50_matches)

pairs_of_artists_to_output= pairupartists(artists_with_50_matches)

for pair in pairs_of_artists_to_output:
	outputpair(pair)
