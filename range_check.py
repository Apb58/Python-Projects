#!/usr/bin/python3

## Intrarange checker:
## Adrian Bubie
## 12/03/18
## ------------
## This program takes 2 files of genomic positions as inputs, a reference and a query, and returns the positions
## in the query that fall within the positions of the reference. The reference file should be structured with
## 'chromosome:range_start-range_end' and should only contain one position range per line. The query file can contain
## either a list of ranges in the same style of the reference, such that any overalp in the ranges will return a positive
## result, or a list of single positions in the structure 'chromosome:gen_position'. 
## 
## The output can be specified as either an output of every query position with indication of whether they match a reference ## range ('all'), or just the list of query positions that overlap with the reference ('match')
## 
## Execute the program: ./range_check.py -r [path/reference] -q [path/query] -o [path/output] -t [output_type]

import sys
import textwrap
import argparse as ap
import math
import json

def get_arguments():
	parser = ap.ArgumentParser(prog='./range_check.py', formatter_class=ap.RawDescriptionHelpFormatter, description=textwrap.dedent('''\
	IntraRange Checker
	---------------------
	Takes genomic postition queries and determines whether they fall within a series of user provided
	reference positional ranges, both in sudo-BED style format (see /examples for details)
	
	Returns to specified output file either a list of queries that fall into the reference ranges, or all queries with a positive or negative result indication.
	'''))
	parser.add_argument("-r", help="Reference file of genomic ranges. Must include absolute path the file. <str>", required=True, type=str)
	parser.add_argument("-q", help="Query file of genomic positions (or ranges). Must include absolute path the file. <str>", required=True, type=str)
	parser.add_argument("-o", help="Output file. Must include absolute path the file. <str>", required=True, type=str)
	parser.add_argument("-t", help="Output file format; choice of 'all', which includes each query and result, or 'match' which only includes queries that overlapped with reference. <str>", required=True, type=str)
	return parser.parse_args()


class genomic_ranges():
	'''Genomic Range object: collection of reference genomic ranges that can be used to check queries.
	object contains a chromosome, base pair start and base pair end.'''
	def __init__(self, ref):
		self.chr = str(ref.split(':')[0])
		self.start = int(ref.split(':')[1].split('-')[0])
		self.end = int(ref.strip('\n').split('-')[1])


def compile_ref_ranges(Reference):
	ref_dict = []
	ref = Reference.readline()
	while ref:
		if ref.startswith('chr') != True:
			raise ValueError("Error: Reference file contains a malformed genomic range. Correct before continuing")
		else:
			ref_dict.append(genomic_ranges(ref))

		ref = Reference.readline()

	return set(ref_dict)



def overlap_check_single(ref_ranges,query):
	match = False # Start by setting the match status to false
	# Query parts:
	qchr = str(query.split(':')[0])
	qpos = int(query.split(':')[1])
	if qchr.startswith('chr') != True:
		raise ValueError("Error: Query file contains a malformed genomic range. Correct before continuing")

	pot_mat_ref = [x for x in ref_ranges if x.chr == qchr]
	mat_ref_abv = [x for x in pot_mat_ref if x.start <= qpos]
	match_ref = [x for x in mat_ref_abv if x.end >= qpos]
	if len(match_ref) > 0: #If there is at least one reference range returned, the query 'match' flag is flipped to true
		match = True

	return match


#TO DO
#def overlap_check_range(ref_ranges,query_range):



###################
## Main Function ##
###################
args = get_arguments()
Reference = open(args.r, 'r')
Query = open(args.q, 'r')
Output = open(args.o, 'w')
ret_type = args.t

if ret_type not in ['all','match']:
	raise ValueError('Error: please select appropriate output format')

ref_ranges = compile_ref_ranges(Reference)
Qresults = dict()
qur = Query.readline()

while qur:
	Qresults[qur.strip('\n')] = overlap_check_single(ref_ranges,qur)
	qur = Query.readline()

if ret_type == 'all':
	p = json.dumps(Qresults).replace(',','\n')
	Output.write(p)

if ret_type == 'match':
	subQres = [x for x in Qresults if Qresults[x] == True ]
	Output.write('\n'.join(subQres))

Reference.close()
Query.close()
Output.close()
