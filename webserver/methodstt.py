import os
import shlex
import subprocess
from conf import *
import pickle
import time
import methods
from Bio import SeqIO

def generate_msahmmer(uip, s_option, cutoff=0.0):

    # print '3'
    USER_FOLD = "/home/www/SMI-BLAST/webserver/temp/user"
    user_fold = os.path.join(USER_FOLD, uip)
    #res = extract_results(user_fold, cutoff)
    # print 'ccc'
    #with open(os.path.join(user_fold, 'hmmer/query', s_option[0].split('&&')[0] + '.seq'), 'r') as f:
    with open(os.path.join(user_fold, 'hmmer/query', 'd1cxca_.seq'), 'r') as f:
        query = f.readlines()

    #user_file = os.path.join(user_fold, 'hmmer/query', s_option[
    user_file = os.path.join(user_fold, 'hmmer/query/d1cxca_.res')
                             #0].split('&&')[0] + '_' + '.res')
                             #0].split('&&')[0] + '_' + '.res')
    clustal_file = os.path.join(
        WORK_FOLD, 'static/clustal/' + uip + '_d1cxca_.txt')

    with open(user_file, 'w') as fp:
        fp.write(query[0].rstrip() + '\n')
        fp.write(query[1].rstrip() + '\n')
        # fp.write('\n')
        # print '4'

        for s in s_option:
            j = s.split('&&')
            print j[2]
            fp.write('>' + ' '.join(j[1:4]) + '\n')  # test
            #fp.write('>' + j[9:16] + '\n')
            # print j[4]
            fp.write(j[4] + '\n')
        # print '5'
    cmd_args = shlex.split('./webserver/model/Clustal_Omega/clustalo-1.2.3-Ubuntu-x86_64 -i ' +
                           user_file + ' --threads 5 --outfmt clustal -o ' + clustal_file + ' --force')
    print cmd_args
    subprocess.Popen(cmd_args).wait()
def resulthmmer(uip):
    print 'sdfa'
    cutoff = 5
    USER_FOLD = "/home/www/SMI-BLAST/webserver/temp/user"
    user_dir = os.path.join(USER_FOLD, uip)
    result_score = user_dir + '/hmmer/score/LTR_score_iter5'
#       cutoff = float(request.args.get('cutoff'))
    #query_name = request.args.get('query')
    print result_score
    query_name = "d1cxca_"
    if os.path.isfile(result_score):
        print 'werwer'
        res = extract_resultshmmer(user_dir, cutoff)
        query_names = [i[0] for i in res]
        # download_path = os.path.join(WORK_FOLD, 'static/result/' + uip + '.txt')
        # methods.write_res(download_path, res)
        if query_name:
            print query_name
            for i in range(len(res)):
                if res[i][0] == query_name:
                    res = res[i]
                    break
        else:
            res = res[0]
        print res

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
if __name__ == '__main__':
#    resulthmmer("223.73.111.136_1567500183.87")
#    generate_msahmmer("223.73.111.136_1567501733.68",'' ,'5')
    res = methods.extract_results("/home/www/SMI-BLAST/webserver/temp/user/223.73.111.136_1567514550.29", 2)
