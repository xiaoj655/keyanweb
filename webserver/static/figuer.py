import os
from Bio import SeqIO
import urllib 


if __name__ == '__main__':
    name =[]
    i=0
    fasta_159 = '/var/www/ProtDec-LTR3.0/webserver/static/astral-scop-1.59.fasta'
    fasta_sequences = SeqIO.parse(open(fasta_159), 'fasta')
    for fasta in fasta_sequences:
        name.append(str(fasta.id))    
    print len(name)
    for item in name[1398:]: 
        print item[1:5]
        imgurl_1 = 'http://www.rcsb.org/pdb/image/' + item[1:5] + '_bio_r_500.jpg?bioNum=1'
        imgurl_2 = 'http://www.rcsb.org/pdb/image/' + item[1:5] + '_asym_r_500.jpg '
    
        file1='/var/www/ProtDec-LTR3.0/webserver/static/image/' + item[1:5] + '_bio_r_500'
        file2='/var/www/ProtDec-LTR3.0/webserver/static/image/' + item[1:5] + '_asym_r_500'
        if not (os.path.isfile(file1) and os.path.isfile(file1)):
            urllib.urlretrieve(imgurl_1,'%s.jpg' % file1)
            urllib.urlretrieve(imgurl_2,'%s.jpg' % file2) 
        
    