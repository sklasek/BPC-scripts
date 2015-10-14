#! python

import sys
import mysql_util as util
import shared #use shared to call connection from outside of the module
from argparse import RawTextHelpFormatter

# todo:
# *) add verbose to print outs
# *) remove -* at the end (see Euk example! python findprimers119.py -domain "Eukar" -f "CCAGCA[CG]C[CT]GCGGTAATTCC" -r "[CT][CT][AG]ATCAAGAACGAAAGT")
#########################################
#
# findprimers: finds primer locations in RefSSU
#
# Author: Susan Huse, shuse@mbl.edu
#
# Date: Sun Oct 14 19:56:25 EDT 2007
#
# Copyright (C) 2008 Marine Biological Laboratory, Woods Hole, MA
# 
# This program is free software you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# For a copy of the GNU General Public License, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# or visit http://www.gnu.org/copyleft/gpl.html
#
# Keywords: primer database 454 align refssu
# 
# Assumptions: 
#
# Revisions: work with "." Jul 27 2013
#            Usage statements to include all valid options Aug 14 2015
#	           Change table names (joins) to use with Silva119 (ASh) Sep 24 2015
#            Show accession_id with start and stop. (Ash) Oct 1 2015
#            Search for both primers (Ash) Oct 13 2015
#
# Programming Notes:
# Rewritten in python Oct 13 2015. Anna Shipunova (ashipunova@mbl.edu)
# Search for primers in db, then for both or one in alingned result (convert primer_seq to "-*" first)

#######################################
#
# Definition statements
#
#######################################

#Runtime variables
refID_field = "refssu_name_id"
refssu_name = "CONCAT_WS('_', accession_id, start, stop)"
ref_table = "refssu_119_ok"
align_table = "refssu_119_align"
cnt = 0
primerSeq = f_primerSeq = r_primerSeq = domain = version = ""

# todo:
# *) ref_table, align_table - add to arguments with default values
#######################################
#
# SQL statements
#
#######################################
# regexp1 = "CCAGCAGC[CT]GCGGTAA."
# domain = "Bacter"

def get_sql_queries(regexp1, domain):
  select_ref_seqs = """SELECT %s, r.sequence as unalignseq, a.sequence as alignseq 
    FROM %s as r
    JOIN refssu_119_taxonomy_source on(refssu_taxonomy_source_id = refssu_119_taxonomy_source_id) 
    JOIN taxonomy_119 on (taxonomy_id = original_taxonomy_id)
    JOIN %s as a using(%s) 
    WHERE taxonomy like '%s%%' and deleted=0 and r.sequence REGEXP '%s'
      LIMIT 1""" % (refssu_name, ref_table, align_table, refID_field, domain, regexp1)
    
  if args.verbose:
    print "select_ref_seqs from get_sql_queries(): %s" % (select_ref_seqs)

  get_counts_sql = """SELECT count(refssuid_id)
  FROM %s AS r
    JOIN refssu_119_taxonomy_source ON(refssu_taxonomy_source_id = refssu_119_taxonomy_source_id) 
    JOIN taxonomy_119 ON (taxonomy_id = original_taxonomy_id)
      WHERE taxonomy like \"%s%%\" and deleted=0 and r.sequence REGEXP '%s'""" % (ref_table, domain, regexp1)

  if args.verbose:
    print "get_counts_sql from get_sql_queries(): %s" % (get_counts_sql)
      
  return (select_ref_seqs, get_counts_sql)

# 
# if (domain eq "all")
# {
# select_ref_seqs = "SELECT refssu_name, r.sequence as unalignseq, a.sequence as alignseq 
#   FROM refTable as r
#   JOIN refssu_119_taxonomy_source on(refssu_taxonomy_source_id = refssu_119_taxonomy_source_id) 
#   JOIN taxonomy_119 on (taxonomy_id = original_taxonomy_id)
#   JOIN alignTable as a using(refID_field) 
#     WHERE deleted=0 and r.sequence REGEXP 'regexp1' 
#     LIMIT 1"
# } else 
# {
# select_ref_seqs = "SELECT refssu_name, r.sequence as unalignseq, a.sequence as alignseq 
#   FROM refTable as r
#   JOIN refssu_119_taxonomy_source on(refssu_taxonomy_source_id = refssu_119_taxonomy_source_id) 
#   JOIN taxonomy_119 on (taxonomy_id = original_taxonomy_id)
#   JOIN alignTable as a using(refID_field) 
#     WHERE taxonolike \"domain%\" and deleted=0 and r.sequence REGEXP 'regexp1'
#     LIMIT 1"
# }
# #######################################
# #
# # Find a valid sequence to search through, for each silva alignment version
# #
# #######################################

# ===

def test_mysql_conn():
  query_1 = """show tables;		
"""
  if args.verbose:
    print "from test_mysql_conn"
    print query_1
  shared.my_conn.cursor.execute (query_1)
  res_names = shared.my_conn.cursor.fetchall ()
  if args.verbose:
    print "from test_mysql_conn"
    print res_names[-1]
  
def convert_regexp(regexp):

  d_from_letter = {
  'R':'[AG]',
  'Y':'[CT]',
  'S':'[CG]',
  'W':'[AT]',
  'K':'[GT]',
  'M':'[AC]',
  'B':'[CGT]',
  'D':'[AGT]',
  'H':'[ACT]',
  'V':'[ACG]',
  '.':'[ACGT]'
  }

  if args.verbose:
  print "From convert_regexp, switching keys and values in d_from_letter"
  d_to_letter = {y:x for x,y in d_from_letter.items()}
  if args.verbose:
    print "from convert_regexp, d_to_letter = "
    print d_to_letter

# http://stackoverflow.com/questions/2400504/easiest-way-to-replace-a-string-using-a-dictionary-of-replacements
  regexp_rep1 = reduce(lambda x, y: x.replace(y, d_to_letter[y]), d_to_letter, regexp)
  if args.verbose:
    print "From convert_regexp. all changes = %s" % (regexp_rep1)

  regexp_ch = [ch + "-*" for ch in regexp_rep1]
  return reduce(lambda x, y: x.replace(y, d_from_letter[y]), d_from_letter, ''.join(regexp_ch))
  
  # C-*C-*A-*G-*C-*A-*G-*C-*[-*C-*T-*]-*G-*C-*G-*G-*T-*A-*A-*.-*
  
def get_ref_seqs_position(align_seq, regexp_ext):  
  import re
  
  if args.verbose:
    print "From get_ref_seqs_position(), removes fuzzy matching from the rigt side, otherwise it gets "-" at the end of the result."
  regexp_ext1 = regexp_ext.rstrip("*").rstrip("-") 
  if args.verbose:
    print "regexp_ext1 from get_ref_seqs_position(): %s" % (regexp_ext1)

  m = re.search(regexp_ext1, align_seq)
  aligned_primer  = m.group(0)
  align_start_pos = m.start() + 1
  align_end_pos   = m.end()


  return  "aligned_primer = %s\nalign_start_pos\t= %s\nalign_end_pos\t= %s\n" %(aligned_primer, align_start_pos, align_end_pos)
  # C-*C-*A-*G-*C-*A-*G-*C-*[CT]-*G-*C-*G-*G-*T-*A-*A-*.
  # aligned_primer  = C-CA--G-C---A--G-C--CG---C-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------GG--TA-AT
  # align_start_pos = 13127
  # align_end_pos = 13862

#######################################
#
# Set up usage statement
#
#######################################
description = """Find the location of a primer sequence in the aligned RefSSU.
Primer sequence must be inserted as read in 5\'-3\' direction (reverse complement the distal primers).
You can provide both forward and reverse primers or just one of them.
Primers can have this regular expressions (note the order in square brackets):               
   'R':'[AG]',
   'Y':'[CT]',
   'S':'[CG]',
   'W':'[AT]',
   'K':'[GT]',
   'M':'[AC]',
   'B':'[CGT]',
   'D':'[AGT]',
   'H':'[ACT]',
   'V':'[ACG]'.
Use dot '.' instead of 'N'.
At least one of primer sequences and domain should be provided.
"""

usage =  """%(prog)s -seq primerseq -domain domainname
ex: python %(prog)s -seq \"CCAGCAGC[CT]GCGGTAA.\" -domain Bacteria
    python findprimers119.py -domain 'Eukar' -f 'CCAGCA[CG]C[CT]GCGGTAATTCC' -r '[CT][CT][AG]ATCAAGAACGAAAGT' -cnt
"""
# 


def parse_arguments():
  import argparse
  
  # parser = ArgumentParser(description='test', formatter_class=RawTextHelpFormatter)
  
  parser = argparse.ArgumentParser(usage = "%s" % usage, description = "%s" % description, formatter_class=RawTextHelpFormatter)
  
  parser.add_argument('-domain', dest = "domain", help = 'superkingdom (in short form: Archae, Bacter, Eukar)')
  parser.add_argument('-ref'   , dest = "ref_table", help = 'reference table (default: refssu)')
  parser.add_argument('-align' , dest = "align_table", help = 'align table (default: refssu_align)')
  parser.add_argument('-cnt'   , action="count", default=0, help = 'count amount of sequences where primer was found (useful if found in both directions)')
  parser.add_argument('-f'     , dest = "f_primer_seq", help = 'forward primer')
  parser.add_argument('-r'     , dest = "r_primer_seq", help = 'reverse primer')
  parser.add_argument('-seq'   , dest = "primer_seq", help = 'primer with unknown direction')
  parser.add_argument('-v'     , '--verbose', action='store_true', help = 'VERBOSITY')

  args = parser.parse_args()
  return args

#######################################
#
# Test for commandline arguments
#
#######################################

def form_seq_regexp():
  if (args.primer_seq):
    return convert_regexp(args.primer_seq)  
  elif (args.f_primer_seq):
    return convert_regexp(args.f_primer_seq)  
  elif (args.r_primer_seq):
    return convert_regexp(args.r_primer_seq)  
# todo: DRY

def get_counts(get_counts_sql):
  shared.my_conn.cursor.execute (get_counts_sql)
  res = shared.my_conn.cursor.fetchall ()
  print "%s is found in %s sequences." % (search_in_db, res[0][0])
  # ((35200L,),)

# ===
# time findprimers119 -domain Bacteria -r CCAGCAGC[CT]GCGGTAA. -ref refssu_119_ok -align refssu_119_align -cnt

if __name__ == '__main__':

  select_ref_seqs = refssu_name_res = ""
  if args.verbose:
    print parse_arguments()
  args = parse_arguments()
  
  both = False
  search_in_db = form_seq_regexp()
  if (args.f_primer_seq and args.r_primer_seq):
    both         = True
    search_in_db = args.f_primer_seq  + ".*" + args.r_primer_seq
    
  if args.verbose:
    print "In main, search_in_db = %s" % (search_in_db)

  regexp_ext = form_seq_regexp()
  if args.verbose:
    print "In main, regexp_ext   = %s" % (regexp_ext)
    print "both = %s" % (both)
  
  # domain = "Bacter"
  domain = args.domain

  select_ref_seqs, get_counts_sql = get_sql_queries(search_in_db, domain)
  
  shared.my_conn = util.MyConnection(read_default_group="clientenv454")
  
  # test_mysql_conn()
  shared.my_conn.cursor.execute (select_ref_seqs)    
  res = shared.my_conn.cursor.fetchall ()
  
  if args.verbose:
    print "In main, regexp_ext = %s" % (regexp_ext)
  # CCAGCAGC[CT]GCGGTAA.
  
  align_seq = res[0][2]
  if (both):
    f_primer = get_ref_seqs_position(align_seq, convert_regexp(args.f_primer_seq))
    r_primer = get_ref_seqs_position(align_seq, convert_regexp(args.r_primer_seq))
    print """Both primers are in the same sequence:\n
F primer: %s\n
R primer: %s
    """ % (f_primer, r_primer)
  else:
    print get_ref_seqs_position(align_seq, regexp_ext)
  
  refssu_name_res = res[0][0]
  print "refssu_name_res = %s" % (refssu_name_res)
  
  if args.cnt:
    get_counts(get_counts_sql)
  