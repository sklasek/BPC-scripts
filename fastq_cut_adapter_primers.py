import os
import sys
import re

class Utils():
  def __init__(self, args):
    self.verbatim  = args.verbatim
    
  def check_if_verb(self):
    try:
      if self.verbatim:
        return True
    except IndexError:
      return False
    except:
      raise
      # print("Unexpected error:", sys.exc_info()[0])
      # return False
    return False
  
class Files():
    def __init__(self, args):
      self.start_dir   = self.get_start_dir(args) 
      self.compressed  = args.compressed
      if args.ext is None and self.compressed == True:
          self.ext     = "1_R1.fastq.gz"
      elif args.ext is not None:
          self.ext     = args.ext
      else:
          self.ext     = "1_R1.fastq"
      print("extension = %s" % self.ext)

    def open_write_close(file_name, text):
        file = open(file_name, "w")
        file.write(text)
        file.close()

    def get_start_dir(self, args):
      if not os.path.exists(args.start_dir):
          # try:
          print("Input fastq file with the '%s' extension does not exist in %s" % (reads.ext, reads.start_dir))
          # except AttributeError:
          #     print("Input fastq file with a '%s' extension does not exist in ." % (args.ext))
          sys.exit()
      print("Start from %s" % args.start_dir)
      return args.start_dir

    def get_dirs(self, fq_files):
      # all_dirs = set()
      # all_dirs.add(fq_files[file_name][0])
      return [file_name[0] for file_name in fq_files]
        
    def get_fq_files_info(self):
      #fq_files = get_files("/xraid2-2/sequencing/Illumina", ".fastq.gz")
      # "/xraid2-2/sequencing/Illumina/20151014ns"
      print("Getting file names")
      fq_files = self.get_files()
      print("Found %s %s" % (len(fq_files), self.ext))
      return fq_files
        
    def get_files(self):
        files = {}
        filenames = []
        for dirname, dirnames, filenames in os.walk(self.start_dir, followlinks=True):
            if self.ext:
                filenames = [f for f in filenames if f.endswith(self.ext)]

            for file_name in filenames:
                full_name = os.path.join(dirname, file_name)
                (file_base, file_extension) = os.path.splitext(os.path.join(dirname, file_name))
                files[full_name] = (dirname, file_base, file_extension)
        return files        
        
class Reads():
    def __init__(self, args):
        self.quality_len = args.quality_len

    def get_adapter(self, file_name):
      file_name_arr = file_name.split("_")
      try:
        adapter = file_name_arr[1]
        if any(ch not in 'ACGTN' for ch in adapter): 
          print("File name should have INDEX_ADAPTER at the beginning. This file name (%s) is not valid for removing adapters" % file_name)
          sys.exit()
      except IndexError:
        print("File name should have INDEX_ADAPTER at the beginning. This file name (%s) is not valid for removing adapters" % file_name)
        sys.exit()
      return adapter
        
    def remove_adapters(self, f_input_entry, file_name, output):

        # cnt = 1
      
      # while f_input.next():
        # f_input.next(raw = True)
        e = f_input_entry
        print("e.header_line: %s" % e.header_line)
        print("e.sequence: %s" % e.sequence)
        print("e.optional: %s" % e.optional)
        print("e.qual_scores: %s" % e.qual_scores)
        adapter = self.get_adapter(file_name)
        print("adapter: %s" % adapter)
        adapter_len = len(adapter)
        seq_no_adapter = e.sequence[adapter_len:]
        qual_scores_short = e.qual_scores[adapter_len:]
        
        e.sequence = seq_no_adapter
        e.qual_scores = qual_scores_short
        
        output.store_entry(e)
        # cnt += 1
        # print(cnt)

    def remove_adapters_n_primers(self, f_input, file_name):
      output_file_name = file_name + '_adapters_n_primers_trimmed.fastq'
      output = open(output_file_name, 'a')
      B_forward_primer_re = "^CCAGCAGC[CT]GCGGTAA."
      
      while f_input.next():
        f_input.next(raw = True)
        e = f_input.entry
        adapter = self.get_adapter(file_name)
        print(adapter)        
        
        adapter_len = len(adapter)
        seq_no_adapter = e.sequence[adapter_len:]
        print("seq_no_adapter:")
        print(seq_no_adapter)
        
        m = re.search(B_forward_primer_re, seq_no_adapter)
        forward_primer = m.group(0)
        print("forward_primer:")
        print(forward_primer)
        
        primer_len = len(forward_primer)
        
        
        # m.group(0):
        # CCAGCAGCTGCGGTAAC
        seq_no_primer = seq_no_adapter[primer_len:]
        print("seq_no_primer:")
        print(seq_no_primer)
        
        e.sequence = seq_no_primer
        # print("e.sequence:")
        # print(e.sequence)
        
        output.store_entry(e)
        
        # TODO: fix
        # TODO cut other lines (score etc.)
        # print("adapter_len = ")
        # print(adapter_len)
        # print(e.sequence)
        # print("seq_no_adapter:")
        # print(seq_no_adapter)
        # print("---")
        
        
    def compare_w_score(self, f_input, file_name, all_dirs):
      for _ in range(50):
        f_input.next(raw = True)
        e = f_input.entry
        
        print(e)
        
        seq_len = len(e.sequence)
        qual_scores_len = len(e.qual_scores)
        try:
            if self.quality_len:
                print("\n=======\nCOMPARE_W_SCORE")
                print("seq_len = %s" % (seq_len))
                print("qual_scores_len = %s" % (qual_scores_len))
        except IndexError:
            pass
        except:
            raise
        # print(e.header_line)
        if (seq_len != qual_scores_len):
          print("WARNING, sequence and qual_scores_line have different length in %s for %s" % (file_name, e.header_line))
          print("seq_len = %s" % (seq_len))
          print("qual_scores_len = %s" % (qual_scores_len))
          
          all_dirs.add(fq_files[file_name][0])

    def get_seq_len(self, f_input, file_name, all_dirs):
      seq_lens = []
      for _ in range(50):
        f_input.next(raw = True)
        e = f_input.entry
        seq_len = len(e.sequence)
        seq_lens.append(seq_len)
        # print(seq_len)
      print("sorted seq_lens:")
      print(sorted(set(seq_lens)))

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='''Check fastq files reads and quality lines length.
    Command line example: python %(prog)s -d/--dir DIRNAME -e/--extension -v --compressed/-c
    ''')
    # todo: add user_config
    # parser.add_argument('--user_config', metavar = 'CONFIG_FILE',
    #                                     help = 'User configuration to run')
    parser.add_argument('--dir', '-d', required = True, action='store', dest='start_dir',
                        help = 'A start directory path.')
    parser.add_argument('--extension', '-e', required = False, action='store', dest='ext',
                        help = 'An extension to look for. Default is a "1_R1.fastq".')
    parser.add_argument('--compressed', '-c', action = "store_true", default = False,
                        help = 'Use if fastq compressed. Default is a %(default)s.')
    parser.add_argument('--quality_len', '-q', action = "store_true", default = False,
                        help = 'Print out the quality and read length. Default is a %(default)s.')
    parser.add_argument('--verbatim', '-v', action = "store_true", default = False,
                        help = 'Print outs.')

    args = parser.parse_args()
    print(args)

    files = Files(args)
    reads = Reads(args)
    utils = Utils(args)
    check_if_verb = utils.check_if_verb()
    
    fq_files = files.get_fq_files_info()
    all_dirs = files.get_dirs(fq_files)
    print(all_dirs)

    # for file_name in fq_files:
    #     file = open(f)
    #     if (verbose):
    #       print f
    #     while 1:
    #         line = file.readline()
    #
    #         if not line:
    #           break
    #         try:
    print(fq_files)

    for file_name in fq_files:
      file = open(file_name)
      # if (check_if_verb):
      # print(file_name)

      output_file_name = file_name + '_adapters_trimmed.fastq'
      output = open(output_file_name, "a")
        
      cnt = 0
      content = []
      temp_d = {}
      while 1:
        cnt += 1
        if cnt == 5:
          cnt = 1

        line = file.readline()
        print("cnt %s, line %s" % (cnt, line))
        # print(line)
        print("---\n")       
        if cnt == 1:
          temp_d["header"] = line
        if cnt == 2:
          temp_d["sequence"]  = line
        if cnt == 3:
          temp_d["optional"]  = line
        if cnt == 4:
          temp_d["qscore"]  = line

          print(temp_d)

        

        if not line:
          break
        try:

          # print("file_name")
          # print(file_name)
          print("---\n")       


          # reads.remove_adapters(f_input.entry, file_name, output)
          # input  = fq.FastQSource(in_file_name, compressed = True)
          #         output = fq.FastQOutput('unknown_good_runkey.fastq')
          #
          # reads.remove_adapters_n_primers(f_input, file_name)
          # reads.compare_w_score(f_input.entry, file_name, all_dirs)
          # reads.get_seq_len(f_input, file_name, all_dirs)
        except RuntimeError:
          if (check_if_verb):
            print(sys.exc_info()[0])
        except:
          raise
        # print("Unexpected error:", sys.exc_info()[0])
        # next

      
    print("Directories: %s" % all_dirs)
    