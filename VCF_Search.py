# Program to Search extremely large VCFs for variants at specific genomic positions/specific variant types
# 04/12/17
# Adrian Bubie

# This script reads in a VCF and breaks down each line of the VCF to determine if the search criteria are met for a
# particular line; this is meant to be a faster search than just grep-ing the file (regex)

def brk_line_positions(Lines, chr_coordinate, pos_coordinate):

    coor = chr_coordinate+'\t'+pos_coordinate

    matching_lines = list()

    for line in Lines:
        if line.startswith('#') or line.startswith(' '):
            pass

        elif line.startswith(chr_coordinate):
            line_parts = line.split('\t')
            comp_pos = str(line_parts[0])+'\t'+str(line_parts[1])

            if coor == comp_pos:
                matching_lines.append(line)

        else:
            pass


    return matching_lines


chr_2_search = input('Chromosome to search: ')
pos_2_search = input('Position to search: ')

VCF_File = open('/path/to/vcf.vcf','r')
VCF_Lines = VCF_File.readlines()

Search_results = brk_line_positions(VCF_Lines, chr_2_search, pos_2_search)
Output_Lines = open('/path/to/outputfile/file.txt','w')
Output_Lines.write(''.join(Search_results))
Output_Lines.close()
