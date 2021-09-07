from xml.etree import ElementTree
import xml.etree.ElementTree as ET
from os import listdir
from os.path import isfile, join
import re
import os
from xml.dom.minidom import parse
import xml.dom.minidom
#Searches files in specific directory and opens one file with specified extension
for filename in os.listdir(r"C:\Users\Tuğrul\PycharmProjects\Ravi"):
    if filename.endswith(".pdb"):
        with open(os.path.join(r"C:\Users\Tuğrul\PycharmProjects\Ravi", filename)) as f:
            content = f.readlines()
#print(f)
#Function that splits a string every 3 characters
def split_every_3(seq):
    return [seq[i:i+3] for i in range(0, len(seq), 3)]

#Function that reads a file with 3_letter and 1_letter code correspondance and returns a dictionary
def read_res_table_to_dictionary (aa_table):
	#Open correspondance file
	res_table_file= open('aa_table.txt');
	three_letter_code = [];
	one_letter_code = [];
	#Read the file and makes 2 lists, one for each type of code
	for line in res_table_file:
		three_letter_code.append(line.split()[1].upper());
		one_letter_code.append(line.split()[2].upper());
	#Pairs the lists
	paired_list = zip(three_letter_code, one_letter_code);
	#Returns a dictionary from the paired lists
	return dict (paired_list);



#Start of the code
SEQ = ET.Element("SEQ")
sequence_from_pdb = [];
chain_from_pdb = [];
n_residues_on_chain = [];
last_res = "";
resolution_found=False;
seq3_to_seq1_dictionary = read_res_table_to_dictionary ("aa_table");
#print (seq3_to_seq1_dictionary);


#Read PDB file
for line in content:
	if 'RESOLUTION' in line:
		if (resolution_found==False):
			my_resolution = line.split()[3];
			resolution_found=True;
	if line.split()[0] == 'ATOM':
		if (last_res!=line.split()[5]):
			#print(line);
			sequence_from_pdb.append(line.split()[3]);
			chain_from_pdb.append(line.split()[4]);
			last_res=line.split()[5];

#Count how many residues on each chain
count=1;
i = 1;
while i < len(sequence_from_pdb):
	if chain_from_pdb[i] == chain_from_pdb[i-1]:
		count=count+1;
	else:
		n_residues_on_chain.append(count);
		count=1;
	i=i+1;
n_residues_on_chain.append(count);

#Generate XML tree structure
res_pos=1;
for i in range (len(n_residues_on_chain)):
    CHAIN = ET.SubElement(SEQ, "CHAIN")
    CHAIN_ID = ET.SubElement(CHAIN, "CHAIN_ID")
    CHAIN_ID.text = str(chain_from_pdb[res_pos])
    for j in range (n_residues_on_chain[i]):
        RESIDUE = ET.SubElement(CHAIN, "RESIDUE")
        RES_POSITION = ET.SubElement(RESIDUE, "RES_POSITION")
        RES_POSITION.text = str(res_pos)
        AA_CODE = ET.SubElement(RESIDUE, "AA_CODE")
        AA_CODE.text = str(seq3_to_seq1_dictionary[sequence_from_pdb[res_pos-1]])
        res_pos=res_pos+1;
tree = ET.ElementTree(SEQ)
SEQ = tree.getroot()

#Print tree structure to file
ET.tostring(SEQ, encoding='utf8').decode('utf8')
tree.write("pdb_one_letter.xml")
from xml.dom import minidom
pdbtoxml = minidom.parseString(ET.tostring(SEQ)).toprettyxml(indent="   ")
with open("pdb_one_letter.xml", "w") as pdb:
    pdb.write(pdbtoxml)


tree = ET.parse('pdb_one_letter.xml')
ET.fromstring(open('pdb_one_letter.xml').read())

chain = [seq for seq in SEQ.findall('.//CHAIN') if seq.findtext('.//CHAIN_ID') == "A"]
print(chain)
sequence = [res for res in SEQ.findall('.//RESIDUE') if res.findtext('.//RES_POSITION') == "456"]
print(sequence)
for seq in chain:
		for res in sequence:
			if res in seq:
				print(res.findtext('.//AA_CODE'))
			else:
				print("WRONG!!!!!!!!!!")
