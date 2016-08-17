"""
Get more levels from
release11_2_Archaea_unaligned.fa.gz
release11_2_Bacteria_unaligned.fa.gz
and make taxonomy.map

S000871964	Acidimicrobium_ferrooxidans	Acidimicrobium	NA
should be
S000871964	Acidimicrobium_ferrooxidans	Acidimicrobium  Acidimicrobiaceae	NA

"""
import gzip
from itertools import tee, izip

class Spingo_Taxonomy():
    def __init__(self):
        # self.arc_filename = "/users/ashipunova/spingo/database/release11_2_Archaea_unaligned.fa.gz"
        # self.bact_filename = "/users/ashipunova/spingo/database/release11_2_Bacteria_unaligned.fa.gz"
        """
        cut -f1 taxonomy.map > mapped_ind.txt
        gzip -dc release11_2_Archaea_unaligned.fa.gz | grep -F -f mapped_ind.txt >mapped_arc_headers.txt
        time gzip -dc release11_2_Bacteria_unaligned.fa.gz | grep -F -f mapped_ind.txt >mapped_bact_headers.txt

        """
        self.tax_map_filename = "/users/ashipunova/spingo/database/taxonomy.map"
        self.arc_filename = "/users/ashipunova/spingo/database/mapped_arc_headers.txt"
        self.bact_filename = "/users/ashipunova/spingo/database/mapped_bact_headers.txt"

        self.tax_map_file_content = []
        self.arc_file_content = []
        self.bact_file_content = []
        self.taxmap_dict = {}
        self.maped_taxonomy_arr = []
        self.new_map_text = []

    def get_file_content(self, in_filename):
        with open(in_filename, 'rb') as f:
            return f.readlines()

    def get_taxmap_dict(self):
        for line in self.tax_map_file_content:
            self.taxmap_dict[line.split("\t")[0]] = line.split("\t")[1:]


    def pairwise(self, iterable):
        tax_array = iterable[0].strip().split(";")
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        # print "tax_array = %s" % (tax_array)
        a = iter(tax_array)
        return izip(a, a)
        
    def make_taxonomy_by_rank(self, i_dict):
        for k, v in i_dict.items():
            print "=" * 10
            
            print k
            # spingo_tax.make_taxonomy_by_rank(v[1])
            # print v[1]
            for x, y in spingo_tax.pairwise(v[1]):
               print "%s: %s" % (y, x)
        

        # l = 'Lineage=Root;rootrank;Bacteria;domain;"Actinobacteria";phylum;Actinobacteria;class;Acidimicrobidae;subclass;Acidimicrobiales;order;"Acidimicrobineae";suborder;Acidimicrobiaceae;family;Ferrimicrobium;genus'
        # l_arr = l.split(";")
        # my_dict['S001416053'][l_arr[3]] = l_arr[2] 
        # my_dict['S001416053'][l_arr[5]] = l_arr[4] 
        # my_dict['S001416053'][l_arr[7]] = l_arr[2] 
        # my_dict['S001416053'][l_arr[9]] = l_arr[2] 
        # my_dict['S001416053'][l_arr[3]] = l_arr[2] 

    def get_mapped_dict(self, arr):
        m_d = {}
        for line in arr:
            # print "line = %s" % line
            
            # S003805392 Ferrimicrobium acidiphilum; PS130, ['Lineage=Root;rootrank;Bacteria;domain;"Actinobacteria";phylum;Actinobacteria;class;Acidimicrobidae;subclass;Acidimicrobiales;order;"Acidimicrobineae";suborder;Acidimicrobiaceae;family;Ferrimicrobium;genus\n']
            l     = line.split("\t")
            # print "l = %s" % l
            
            first_part = l[0].split(" ")
            ind   = first_part[0].strip(">")
            binom = first_part[1:]
            tax   = l[1:]
            
            # print "ind = %s; binom = %s; tax = %s" % (ind, binom, tax)
            m_d[ind] = (binom, tax)
        return m_d


if __name__ == '__main__':
    spingo_tax = Spingo_Taxonomy()

    spingo_tax.tax_map_file_content = spingo_tax.get_file_content(spingo_tax.tax_map_filename)
    print spingo_tax.tax_map_file_content[0]
    spingo_tax.get_taxmap_dict()
    # arc_maped_taxonomy_arr  = spingo_tax.get_maped_taxonomy_arr(spingo_tax.arc_filename)
    # bact_maped_taxonomy_arr = spingo_tax.get_maped_taxonomy_arr(spingo_tax.bact_filename)

    spingo_tax.arc_file_content  = spingo_tax.get_file_content(spingo_tax.arc_filename)
    spingo_tax.bact_file_content = spingo_tax.get_file_content(spingo_tax.bact_filename)

    print "spingo_tax.bact_file_content[0]"
    print spingo_tax.bact_file_content[0]

    test = spingo_tax.bact_file_content[0:3]
    # a = spingo_tax.get_mapped_dict(spingo_tax.bact_file_content)
    a = spingo_tax.get_mapped_dict(test)
    spingo_tax.make_taxonomy_by_rank(a)
    # for k, v in a.items():
    #     print k, v
        
    # for k, v in a.items():
    #     # spingo_tax.make_taxonomy_by_rank(v[1])
    #     # print v[1]
    #     for x, y in spingo_tax.pairwise(v[1]):
    #        print "%s: %s" % (y, x)
    #     