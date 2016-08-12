import csv
import codecs

class CsvTools():

    def __init__(self, args):
      
      # print args
      
      self.from_file_name = args.from_file_name
      self.to_file_name   = args.to_file_name
      # self.from_file_content = []
      # self.to_file_content = []

      self.delimiter = args.delimiter
      print "delimiter = '%s'" % (self.delimiter)

      self.quotechar = args.quotechar
      print "quotechar = '%s'" % (self.quotechar)

    
    def read_in_file(self):
      input_reader = self.get_reader(self.from_file_name)
      self.from_file_content = self.parce_csv(input_reader)
      print "=" * 10        
      
      # for x in self.from_file_content:
      #     print "for x in self.from_file_content:"
          # print (x)
      
    def read_out_file(self):
      out_reader = self.get_reader(self.to_file_name)
      self.to_file_content = self.parce_csv(out_reader)
      
      # for x in self.to_file_content:
      #     print "for x in self.to_file_content:"
      #     print (x)
      

    def make_out_dict(self):
      print "in make_out_dict"
      # print self.to_file_content
      # for x in self.to_file_content:
      #     print "for x in self.to_file_content:"
      #     print (x)
      
      print "1" * 10        
      for o_row in self.to_file_content:
        combined_row = o_row
        print combined_row
        for i_row in self.from_file_content:
          if i_row['Query'] == o_row['Name']:
            # print(i_row['Query'], i_row['Annotation'])
            combined_row['Annotation'] = i_row['Annotation']
            print "2" * 10        
            print "combined_row = "
            print combined_row
            
        

      
    def write_to_out_file(self):
      self.make_out_dict()
      
    #
    # def import_from_file(self):
    #     self.from_file_name
    #     print "self.from_file_name"
    #     print self.from_file_name
    #
    #     self.get_reader()
    #     # print "LLL self.reader"
    #     # print self.reader
    #
    #     # self.csv_headers, self.csv_content =
    #     self.parce_csv()
    #
    #     # print "=" * 10
    #     # print self.csv_headers
    #     # print "=" * 10
    #
    #     print "SSS self.csv_content: "
    #     print self.from_file_content
    #     print "=" * 10
    #
    #     for x in self.from_file_content:
    #         print "for x in self.from_file_content:"
    #         print (x)
    #     #
    #     # self.check_headers_presence()
    #     #
    #     # self.get_csv_by_header_uniqued()
    #

    def get_reader(self, file_name):
        try:
            infile = open(file_name, mode = 'r')
            return csv.DictReader(codecs.EncodedFile(infile, "utf-8"), delimiter = self.delimiter, quotechar = self.quotechar)
        except csv.Error as e:
            self.errors.append('%s is not a valid CSV file: %s' % (infile, e))
        except:
            raise


    def parce_csv(self, reader):
      file_content = []
      for row in reader:
        file_content.append(row)
        
        
      return file_content
        
      # print row
      """
      {'Min Sequence Length': '', 'Hit end': '448855', 'Ref Seq Name': '', 'Molecule Type': 'DNA', 'Query end': '507', 'dash': '-', 'strain': 'NEG-M', '# Nucleotide Sequences With Mates': '', 'Genetic Code': 'Standard', 'Query start': '40', 'E Value': '2.52E-144', 'Ref Seq Length': '', 'Description': 'Naegleria gruberi strain NEG-M genomic NAEGRscaffold_22, whole genome shotgun sequence', 'Bit-Score': '323.188', 'SequenceListOrderingRevisionNumber': '', 'db_xref': 'taxon:744533', '# Nucleotide Sequences With Quality': '0', '% Pairwise Identity': '', 'Annotation': '26S proteasome CDS', 'Hit start': '449322', 'Topology': 'linear', 'Sequence Length': '156', 'Query coverage': '50.16%', 'Name': 'NW_003163305', 'Database': 'Naegleria gruberi NZ ACER00000000', 'Max Sequence Length': '', 'URN': 'urn:local:.:gak-6gx1c49', 'Modified': 'Mon Mar 29 00:00:00 EDT 2010', 'Created Date': 'Wed Aug 10 09:40:22 EDT 2016', '# Sequences': '', 'GID': '290990065', 'Organism': 'Naegleria gruberi strain NEG-M', '% Identical Sites': '', 'Sequence': 'GGGGMQGDQPLPDTAETVTISSLALLKMLKHGRAGVPMEVMGLMLGEFIDDYTVRCIDVFAMPQSGTGVSVEAVDPVFQTKMLELLKQTGRPEMVVGWYHSHPGFGCWLSSVDINTQQSFESLTKRSVAVVVDPIQSVKGKVVIDAFRTINPQLAM', 'Grade': '67.70%', 'Taxonomy': 'Eukaryota; Heterolobosea; Schizopyrenida; Vahlkampfiidae; Naegleria', 'Mean Coverage': '', 'Ref Seq Index': '', 'Accession': 'NW_003163305', 'Free end gaps': '', '# Nucleotides': '', 'country': 'USA', 'Query': '55387_Solumitrus_QUALITY_PASSED_R1_paired_contig_1705_7110_8043f', 'Original Query Frame': '1', 'Size': '8 KB'}
      
      """
        # print(row['Name'], row['Annotation'])
      
      
      # for y_index, row in enumerate(self.reader):


          # print "parce_csv row"
          # print row

          # if y_index == 0:
          #     self.csv_headers = [header_name.lower() for header_name in row if header_name]
          #     # continue
          # else:
          #     self.csv_content.append(row)
                       
      # return self.csv_headers, self.csv_content



if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description = 'Adds a column from one csv file to another. Two files should have a common column (a common key).',     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-f", "--from_file_name",
                required = True, action = "store", dest = "from_file_name", default = "in_file.csv",
                help = "From CSV file name")

    parser.add_argument("-t", "--to_file_name",
                required = True, action = "store", dest = "to_file_name", default = "out_file.csv",
                help = "Destination CSV file name")
                
    parser.add_argument("-d", "--delimiter",
                required = False, action = "store", dest = "delimiter", default = ',',
                help = "CSV delimeter: comma, tab, space etc")
                
    parser.add_argument("-q", "--quotechar",
                required = False, action = "store", dest = "quotechar", default = '"',
                help = "CSV quote character: single or double quote")                

    args = parser.parse_args()

    csv_tools = CsvTools(args)
    csv_tools.read_in_file()
    csv_tools.read_out_file()
    csv_tools.make_out_dict()
    

