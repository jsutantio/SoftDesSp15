# -*- coding: utf-8 -*-
"""
1.31.14 SoftDes Spring 2015
Gene Finder
Jessica Sutantio
"""

# Import variables
from amino_acids import aa, codons, aa_table
import random
from load import load_seq

def shuffle_string(s):
    """ Shuffles the characters in the input string
        NOTE: this is a helper function, you do not have to modify this in any way """
    return ''.join(random.sample(s,len(s)))

### YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###
# Returns the complementary nucleotide
def get_complement(nucleotide):
    """
    nucleotide: a nucleotide (A, C, G, or T) represented as a string
    returns: the complementary nucleotide
    
    ## DOCTEST
    >>> get_complement('A')
    'T'
    >>> get_complement('T')
    'A'
    >>> get_complement('C')
    'G'
    >>> get_complement('G')
    'C'
    >>> get_complement('H')
    Not a valid nucleotide type.
    >>> get_complement(169)
    Not a valid nucleotide type.
    """

    if nucleotide == 'A':
        return 'T'
    if nucleotide == 'T':
        return 'A'
    if nucleotide == 'C':
        return 'G'
    if nucleotide == 'G':
        return 'C'
    else:
        # Prevents rest of code from running
        raise Exception('Not a valid nucleotide type.')

"""
Computes the reverse complementary sequence of DNA for the specfied 
DNA sequence
"""
def get_reverse_complement(dna):
    """ 
    dna: a DNA sequence represented as a string
    returns: the reverse complementary DNA sequence represented as a string

    ## DOCTEST
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    """
    
    """
    reads the input and finds the complement of each nucleotide
    outputs a list of strings of the indiv. nucleotides
    """
    length = len(dna)
    sequence = []
    # for x in range(0,length):
    #     nucleotide = dna[x]
    #     # For ea. nucleotide, return its complement
    #     complement = get_complement(nucleotide)
    #     sequence.append(complement)

    for nucleotide in dna:
        complement = get_complement(nucleotide)
        sequence.append(complement)
    
    # Returns the reversed DNA sequence and joins it into a string
    sequence.reverse()
    reverseSequence = ''.join(sequence)
    return reverseSequence

"""
Determines the number of codons in the DNA sequence provided.
This ignores any extra nucleotides that do not fit in the triplet.
"""
def triplet(dna):
    length = len(dna)
    triplets = length/3
    return triplets

"""
Takes a DNA sequence that is assumed to begin with a start codon and returns
the sequence up to but not including the first in frame stop codon.  If there
is no in frame stop codon, returns the whole string.
"""
def rest_of_ORF(dna):
    """        
    dna: a DNA sequence
    returns: the open reading frame represented as a string
    
    ## DOCTEST
    >>> rest_of_ORF('ATGTGAA')
    ('ATG', 1)
    >>> rest_of_ORF('ATGAGATAGG')
    ('ATGAGA', 2)
    >>> rest_of_ORF('ATGGAATTTGCCG')
    ('ATGGAATTTGCCG', 4)
    """
    triplets = triplet(dna)
    snippet = ''

    for x in range (0,triplets):
        codon = dna[3*(x):3*(x+1)]

        if codon in ['TAG','TAA','TGA']:
            # print 'End of the line!'
            return snippet, x
        else:
            snippet = snippet + codon
            # print snippet

    # If no stop codon, return entire DNA sequence
    return dna, triplets

""" 
Finds all non-nested open reading frames in the given DNA sequence and returns
them as a list.  This function should only find ORFs that are in the default
frame of the sequence (i.e. they start on indices that are multiples of 3).
By non-nested we mean that if an ORF occurs entirely within
another ORF, it should not be included in the returned list of ORFs.
"""
def find_all_ORFs_oneframe(dna):
    """  
    dna: a DNA sequence
    returns: a list of non-nested ORFs
    
    ## DOCTEST
    >>> find_all_ORFs_oneframe('ATGCATGAATGTAGATAGATGTGCCC')
    ['ATGCATGAATGTAGA', 'ATGTGCCC']
    >>> find_all_ORFs_oneframe('TAAATGCATGAATAGTTT')
    ['ATGCATGAA']
    >>> find_all_ORFs_oneframe('TAAATGCATGAATAGTTTTAAATGCTGCGGTAATGA')
    ['ATGCATGAA', 'ATGCTGCGG']
    >>> find_all_ORFs_oneframe('TAGATGCCCATGCCCTAACGG')
    ['ATGCCCATGCCC']
    """

    triplets = triplet(dna)

    allORFs = []
    x = 0    

    while x <= triplets:
        # print 'triplets: ' + str(triplets)
        codon = dna[3*(x):3*(x+1)]
        # print 'counter: ' + str(x)

        if codon == 'ATG':
            # Finds a single ORF until the next stop codon; ORF end location
            ORFsnippet, endLocation = rest_of_ORF(dna[3*x:])
            # print ORFsnippet
            # print 'endLocation: ' + str(endLocation)
            x = endLocation + x
            # print 'Modified x: ' + str(x)
            
            # Puts ORFs together in a list called allORFs
            allORFs.append(ORFsnippet)
            
        x = x + 1

    return allORFs
    
"""
Finds all non-nested open reading frames in the given DNA sequence in all 3
possible frames and returns them as a list.  By non-nested we mean that if an
ORF occurs entirely within another ORF and they are both in the same frame,
it should not be included in the returned list of ORFs.
"""
def find_all_ORFs(dna):
    """   
    dna: a DNA sequence
    returns: a list of non-nested ORFs

    ## DOCTEST
    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    """
    
    allORFs = find_all_ORFs_oneframe(dna)

    # Offset the DNA sequence by 1
    def one_offset(dna):
        return dna[1:]

    dna1 = one_offset(dna)   
    allORFs1 = find_all_ORFs_oneframe(dna1)
    

    # Offset the DNA sequence by 2
    def two_offset(dna):
        return dna[2:]

    dna2 = two_offset(dna)   
    allORFs2 = find_all_ORFs_oneframe(dna2)
    
    # Combine all the lists
    allORFs = allORFs + allORFs1 + allORFs2

    return allORFs

""" 
Finds all non-nested open reading frames in the given DNA sequence on both
strands.
"""
def find_all_ORFs_both_strands(dna):
    """ 
    dna: a DNA sequence
    returns: a list of non-nested ORFs
    
    ## DOCTEST
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    allORFs_original = find_all_ORFs(dna)

    reverse_dna = get_reverse_complement(dna)
    allORFs_reverse = find_all_ORFs(reverse_dna)

    allORFs = allORFs_original + allORFs_reverse

    return allORFs

def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """
    # TODO: implement this
    pass

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    # TODO: implement this
    pass

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
    """
    # TODO: implement this
    pass

def gene_finder(dna):
    """ Returns the amino acid sequences that are likely coded by the specified dna
        
        dna: a DNA sequence
        returns: a list of all amino acid sequences coded by the sequence dna.
    """
    # TODO: implement this
    pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()