import os
import shlex
import subprocess
from conf import *
import pickle
import time
from Bio import SeqIO




def scop_info(scop_file):
    info = {}
    last_name = ''
    with open(scop_file) as fp:
        for i in fp:
            if i[0] == '>':
                i = i[1:].strip().split(' ', 2)
                last_name = i[0].replace('.', '_')
                info[last_name] = i[1:]
            else:
                info[last_name].append(i.strip())
    return info


def extract_resultshmmer(user_fold, cutoff=1):
    scop_decription = scop_info('/home/www/SMI-BLAST/webserver/model/scope-95-2.06.upper2.fa')
    query_name = []
    with open(os.path.join(user_fold, 'test.fasta'), 'r') as fp:
        for i in fp:
            if i[0] == '>':
                i = i[1:].strip().split()[0]
                query_name.append(i)
    res = {}
    iternumber = 1
    if int(cutoff) == 2:
        iternumber=2
    elif int(cutoff)==3:
        iternumber=5
    elif int(cutoff)==4:
        iternumber=10
    with open(os.path.join(user_fold, 'hmmer/LTR_input_iter5')) as seq_list, open(os.path.join(user_fold, 'hmmer/score/LTR_score_iter5')) as seq_score:
    #with open(os.path.join(user_fold, 'LTR_input_iter'+str(cutoff))) as seq_list, open(os.path.join(user_fold, 'score', 'LTR_score_iter'+str(cutoff))) as seq_score:
        for i, j in zip(seq_list, seq_score):
            query = i.strip().split()[-3]
            hit = i.strip().split()[-1]
            score = float('%.2f' % float(j.strip().split()[2]))
#            if score < cutoff:
 #               continue
            if query in res:
                res[query].append([hit, score])
            else:
                res[query] = [[hit, score]]

    res_html = []
    for i in query_name:
        hits = []
        if not res.has_key(i):
            hits = []
        else:
            hits = sorted(res[i], key=lambda d: d[1], reverse=True)

            hits = [[j[0], scop_decription[j[0]][0], scop_decription[j[0]][1], scop_decription[j[0]][2], j[
                1], "images/" + j[0][1:5] + ".bio.jpg", "images/" + j[0][1:5] + ".asym.jpg", len(scop_decription[j[0]][2])] for j in hits]
        res_html.append([i, hits])
    # query_name [hit_name scop_decriptrion scop_decriptrion scop_decriptrion
    # score images images]
    return res_html

def resulthmmer(uip):
    user_dir = os.path.join("/home/www/SMI-BLAST/webserver/temp/user", uip)    

    result_score = user_dir + '/hmmer/score/LTR_score_iter5'
    print result_score
    #query_name = request.args.get('query')
    query_name = "d1cxca_"
    if os.path.isfile(result_score):
        res = extract_resultshmmer("/home/www/SMI-BLAST/webserver/temp/user/223.73.111.136_1567500183.87", 5)
    #    print res
        query_names = [i[0] for i in res]
        if query_name:
            for i in range(len(res)):
                print i
                if res[i][0] == query_name:
                    res = res[i]
                    break
                else:
                    res = res[0]
    #    print res

if __name__ == '__main__':
    print 'werw'
    resulthmmer("223.73.111.136_1567500183.87")
#    xxx= extract_resultshmmer("/home/www/SMI-BLAST/webserver/temp/user/10.249.148.207_1567439192.97",5)
    print 'sss'
    #print xxx
