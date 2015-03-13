""" Analyzes the word frequencies in a book downloaded from
	Project Gutenberg """

import string

def get_word_list(file_name):
	""" Reads the specified project Gutenberg book.  Header comments,
		punctuation, and whitespace are stripped away.  The function
		returns a list of the words used in the book as a list.
		All words are converted to lower case.
	"""
	freq_dict = {}
	recordingLine = False
	for line in open(file_name):
		# wait for the start of the book to start word list
		if "*** START OF THIS PROJECT GUTENBERG EBOOK THE ADVENTURES OF HUCKLEBERRY FINN ***" in line:
			recordingLine = True

		if recordingLine:
			# change all letters to lowercase
			line = line.lower()
			# separate the words in the line (by white spaces) into a list
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


def get_top_n_words(freq_dict, n):
	""" Takes a list of words as input and returns a list of the n most frequently
		occurring words ordered from most to least frequently occurring.

		freq_dict: a dictionary of words (assumed to all be in lower case with no
					punctuation
		n: the number of words to return
		returns: a list of n most frequently occurring words ordered from most
				 frequently to least frequentlyoccurring
	"""
	# sort the dictionary by most to least frequent
	ordered_freq_dict = sorted(freq_dict, key=freq_dict.__getitem__, reverse=True)
	# goes up to the nth most frequent word
	freqList = ordered_freq_dict[:n]
	
	return freqList	


if __name__ == '__main__':
	file_name = 'pg32325.txt'
	n = 1000
	freq_dict = get_word_list(file_name)
	print get_top_n_words(freq_dict,n)