# Jessica Sutantio
# SoftDes Spring 2015
# 2.22.15

""" Very Loud Rants
reads emails from Olin's public mailing list, Therapy, and outputs the most popular terms
"""

from os import getcwd, chdir, listdir
import string

file_names = sorted(listdir('Therapy_Archives/'))
outputfile = open('all_rants.txt','w')
week = ['sun','mon','tue','wed','thu','fri','sat']
year = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
ranting = False


## combines all the archives and filters for only the essential text
def omit_crap(file_names):
	for archive in file_names:
		for line in open('Therapy_Archives/' + archive):
			# change all letters to lowercase
			line = line.lower()

			# checks for line that comes before the body text
			if ('message-id' == line[:10]):
				ranting = True
				continue
			
			# cases that stop recording the body text
			if ('from therapy' == line[:12]):		
				ranting = False
				continue
			if ('from: therapy' == line[:13]):		
				ranting = False
				continue
			if ('from: anonymous' == line[:15]):
				ranting = False
				continue
			if ('-----original message-----' == line[:26]):
				ranting = False
				continue
			if ('----- reply message -----' == line [:25]):
				ranting = False
				continue
			if ('>' == line [0]):
				ranting = False
				continue
			for day in week:
				if ('on ' + day == line[:6]):
					ranting = False
					continue
			for month in year:
				if ('on ' + month == line[:6]):
					ranting = False
					continue

			# records the lines if ranting is true
			if ranting:
				outputfile.write(line)


## count the frequency of words in the text
def word_freq():
	freq_dict = {}
	for line in open('all_rants.txt'):
		# separate the words in the line into a list
		word_list = line.split()
		for word in word_list:
			# remove punctuation
			word = string.strip(word,string.punctuation)
			# increase the word count...
			if word in freq_dict:
				freq_dict[word] += 1
			# ... or add the word to the dictionary
			else:
				freq_dict[word] = 1

	return freq_dict


## determine the most frequent words that are noteworthy
def rants(freq_dict):
	# for word in range(:100)
	pass

omit_crap(file_names)
word_freq()
freq_dict = word_freq()
# print freq_dict
ordered_freq_dict = sorted(freq_dict, key=freq_dict.__getitem__, reverse=True)
# print ordered_freq_dict
print ordered_freq_dict[:200]
# number of words: 4081


# omit the common words (ex. 'the', 'a', 'an', 'what', 'when')
	# try to find a list online
	# or do not output the first 100 most frequent words
	# toggle the max number until something interesting comes out
# find the words with most count


# something visual to show LOUDEST RANTS
	# output text of various sizes
	# most frequent = bigger = louder
	# least frequent = smaller = meh

# something audio to show LOUDEST RANTS
	# output reading of word of various volume
	# most frequent = louder
	# least frequent = quieter
	# use howjsay.com
