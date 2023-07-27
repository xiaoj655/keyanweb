#---2018-7 jxp roc1=0.9101
#resort the ranking list by jaccard distance

import os
import re
import sys
import subprocess
import xml.etree.ElementTree as ET
from multiprocessing import Pool
import multiprocessing as mp
import numpy as np
from scipy.spatial.distance import pdist
from Bio import SeqIO
import time
import methods

if __name__ == '__main__':
	# parameters
	#db_path_re1 = sys.argv[2]+'/webserver/model/linkDB/'+sys.argv[3]+'/4CBLS_extend_206-tmp'

	user_dir = '/home/www/PL-search/webserver/temp/user/223.73.111.107_1572315051.4'
	cutoff = 1
	methods.extract_results(user_dir, 2,  cutoff)	
