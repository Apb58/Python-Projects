#~/usr/bin/python
# ver 0.1: 7/11/16
# Script to remove duplicate FASTA reads based on ID tag:
# Given a FASTA file with some duplicate reads that share the same identifier,
# produce a valid FASTA with the identifier removed

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
    #Input is a list of tags, output is the unique items from the list, with the order of the list maintained
    #This function can be replaced by use of just the set() method if the order of the tags/FASTA does not need to be maintained


path_to_file = raw_input("Enter path to FASTA:")
# e.g. /Users/User/Desktop/File.fas

File = open(path_to_file, 'r')
Text = File.read()

#Breaking FASTA into individual reads:
Lines = Text.split('>')
Lines = Lines[1:] #Removes the first empty item from the list
Tag_list = list()

for line in Lines:
    tags = line.split('\n')
    Tag_list.append(tags[0])

Sing_tags = f7(Tag_list)# Creates a list of all the unique tags

To_reconst = list()
for tag in Sing_tags:
    for line in Lines:
        if line.startswith(tag):
            To_reconst.append('>'+line)
            break
        else:
            pass

New_Fasta = ''.join(To_reconst)
File_2 = open('New_FASTA.fas','w')
File_2.write(str(New_Fasta))
File_2.close()

print "Length of FASTA: ",len(Lines)
print "Number of Unique Tags: ",len(Sing_tags)
print "Length of New FASTA",len(To_reconst)
