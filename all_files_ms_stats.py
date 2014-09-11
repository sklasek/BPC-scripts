#! /bioware/python-2.7.5/bin/python

import os
count_all_reads = 0
count_good_reads = 0

files = []
current_dir = os.getcwd()
for (dirpath, dirname, filenames) in os.walk(current_dir):
    files.extend(filenames)
    break

Number_of_pairs_analyzed = 0
Prefix_failed_in_read_1 = 0
Prefix_failed_in_read_2 = 0
Prefix_failed_in_both = 0
Passed_prefix_total = 0
Failed_prefix_total = 0
Merged_total = 0
Complete_overlap_forced_total = 0
Merge_failed_total = 0
Merge_discarded_due_to_P = 0
Merge_discarded_due_to_Ns = 0
Merge_discarded_due_to_Q30 = 0
Pairs_discarded_due_to_min_expected_overlap = 0
Num_mismatches_found_in_merged_reads = 0
Mismatches_recovered_from_read_1 = 0
Mismatches_recovered_from_read_2 = 0
Mismatches_replaced_with_N = 0

for f in files:
  if f.endswith("_STATS"):
    file = open(f)
    print f
    while 1:
        line = file.readline()

        if not line:
          break
        try:
          num = 0
          line = line.strip()
          print(line)
          num = line.split()[-1]
          print(num)
          if line.startswith("Number of pairs analyzed"):
              Number_of_pairs_analyzed += int(num)
              print('URA: Number_of_pairs_analyzed + %s') % Number_of_pairs_analyzed        
          elif line.startswith("Prefix failed in read 1"):
              Prefix_failed_in_read_1 += int(num)
          elif line.startswith("Prefix failed in read 2"):
              Prefix_failed_in_read_2 += int(num)
          elif line.startswith("Prefix failed in both"):
              Prefix_failed_in_both += int(num)
          elif line.startswith("Passed prefix total"):
              Passed_prefix_total += int(num)
          elif line.startswith("Failed prefix total"):
              Failed_prefix_total += int(num)
          elif line.startswith("Merged total"):
              Merged_total += int(num)
          elif line.startswith("Complete overlap forced total"):
              Complete_overlap_forced_total += int(num)
          elif line.startswith("Merge failed total"):
              Merge_failed_total += int(num)
          elif line.startswith("Merge discarded due to P"):
              Merge_discarded_due_to_P += int(num)
          elif line.startswith("Merge discarded due to Ns"):
              Merge_discarded_due_to_Ns += int(num)
          elif line.startswith("Merge discarded due to Q30"):
              Merge_discarded_due_to_Q30 += int(num)
          elif line.startswith("Pairs discarded due to min expected overlap"):
              Pairs_discarded_due_to_min_expected_overlap += int(num)
          elif line.startswith("Num mismatches found in merged reads"):
              Num_mismatches_found_in_merged_reads += int(num)
          elif line.startswith("Mismatches recovered from read 1"):
              Mismatches_recovered_from_read_1 += int(num)
          elif line.startswith("Mismatches recovered from read 2"):
              Mismatches_recovered_from_read_2 += int(num)
          elif line.startswith("Mismatches replaced with N"):
              Mismatches_replaced_with_N += int(num)
          
        except LookupError:
          pass

print "="*50    
print current_dir

print('Number_of_pairs_analyzed (in all files) = %s') % Number_of_pairs_analyzed        
print('Prefix_failed_in_read_1 (in all files) = %s') % Prefix_failed_in_read_1        
print('Prefix_failed_in_read_2 (in all files) = %s') % Prefix_failed_in_read_2        
print('Prefix_failed_in_both (in all files) = %s') % Prefix_failed_in_both        
print('Passed_prefix_total (in all files) = %s') % Passed_prefix_total        
print('Failed_prefix_total (in all files) = %s') % Failed_prefix_total        
print('Merged_total (in all files) = %s') % Merged_total        
print('Complete_overlap_forced_total (in all files) = %s') % Complete_overlap_forced_total        
print('Merge_failed_total (in all files) = %s') % Merge_failed_total        
print('Merge_discarded_due_to_P (in all files) = %s') % Merge_discarded_due_to_P        
print('Merge_discarded_due_to_Ns (in all files) = %s') % Merge_discarded_due_to_Ns        
print('Merge_discarded_due_to_Q30 (in all files) = %s') % Merge_discarded_due_to_Q30        
print('Pairs_discarded_due_to_min_expected_overlap (in all files) = %s') % Pairs_discarded_due_to_min_expected_overlap        
print('Num_mismatches_found_in_merged_reads (in all files) = %s') % Num_mismatches_found_in_merged_reads        
print('Mismatches_recovered_from_read_1 (in all files) = %s') % Mismatches_recovered_from_read_1        
print('Mismatches_recovered_from_read_2 (in all files) = %s') % Mismatches_recovered_from_read_2        
print('Mismatches_replaced_with_N (in all files) = %s') % Mismatches_replaced_with_N        

