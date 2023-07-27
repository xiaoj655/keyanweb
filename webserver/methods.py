import os
import shlex
import subprocess
from conf import *
import pickle
import time
from Bio import SeqIO



def write_res(user_file, result):
    with open(user_file, 'w') as f:
        for i in result:
            f.write(
                '---------------------------------------------------------------------------------------\n')
            f.write('The results of query protein ' + i[0] + ' are:')
            f.write(
                '\n---------------------------------------------------------------------------------------\n')
            for j in i[1]:
                f.write('>' + j[0] + ' ' + j[1] +
                        ' ' + j[2] + '\n' + j[3] + '\n')
            f.write('\n')


def cmd(command):
    cmd_args = shlex.split(command)
    # subprocess.Popen(cmd_args).wait()
    subprocess.Popen(cmd_args)


def is_protein(s):
    for i in s:
        if i not in ALPHABET:
            return False
    return True


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


'''
def scop_info(scop_file):
    info = {}
    last_name = ''
    fasta_sequences = SeqIO.parse(open(scop_file), 'fasta')
    for fasta in fasta_sequences:
        i = fasta.description.split(' ', 2)
        last_name = i[0].replace('.', '_')
        info[last_name] = i[1:]
        info[last_name].append(str(fasta.seq).upper())
    return info
'''

def check_and_write(data, path, max_num_of_sequences=MAX_NUM_OF_SEQUENCES):
    with open(os.path.join(path, 'test.fasta'), 'w') as fp:
        line_num, sequence_num = 0, 0
        id_name = []
        first_is_name, need_line = False, False
        for i in data:
            line_num += 1
            i = i.strip()
            if len(i) == 0:
                continue
            if i[0] == '>':
                # check duplicted id
                if i in id_name:
                    return False, 'Duplicated ID: ' + i + '\nTwo sequences cannot share the same identifier!'
                else:
                    id_name.append(i)

                # check name
                if len(i.strip()) == 1:
                    return False, 'Line ' + str(line_num) + ' is wrong, it should be a name of protein sequence!'
                first_is_name = True
                sequence_num += 1

                # check standard amino acids
                if need_line:
                    return False, 'Line ' + str(line_num) + ' is wrong, it should be a protein sequence!'

                # check sequence number
                if sequence_num > max_num_of_sequences:
                    return False, 'No more than ' + str(max_num_of_sequences) + ' protein sequences!'
                need_line = True
                if sequence_num != 1:
                    fp.write('\n')
                i = i.replace('|', ' ')
                i = i.replace('/', ' ')
                i = i.replace('.', ' ')
                fp.write(i + '\n')
            else:
                i = i.upper()
                if not first_is_name:
                    return False, 'Line 1 is wrong, it should be a name of protein sequence!'
                if not is_protein(i):
                    return False, 'Line ' + str(line_num) + ' is wrong, it is not a protein sequence!'
                need_line = False
                fp.write(i)
        if need_line:
            return False, 'Line ' + str(line_num) + ' is wrong, it should be a protein sequence!'
        if not first_is_name:
            return False, 'There is no query protein sequences!'
    return True, None

'''
def predict(user_fold, detect_method='Com-ProtDec-LTR'):
    if detect_method=='Com-ProtDec-LTR':
        cmd('webserver/model/code/run_Com-ProtDec-LTR.sh ' + user_fold)
    elif detect_method=='Pse-ProtDec-LTR':
        cmd('webserver/model/code/run_Pse-ProtDec-LTR.sh ' + user_fold)
    else:
        cmd('webserver/model/code/run_Ori-ProtDec-LTR.sh ' + user_fold)
'''


def predict(uip, user_email, cutoff, recutoff, CON_FOLD):
    user_dir = os.path.join(USER_FOLD, uip)
    if user_email == '':
        cmd('webserver/model/code/run.sh ' + user_dir +
            ' ' + 'no_email' + ' ' + str(cutoff) + ' ' + str(recutoff)  +' ' + uip+ ' ' +CON_FOLD)
    else:
        cmd('webserver/model/code/run.sh ' + user_dir +
            ' ' + user_email + ' ' + str(cutoff) + ' ' + str(recutoff) + ' ' + uip+ ' ' +CON_FOLD)

def predictpsiblastexb(uip, user_email, cutoff, CON_FOLD):
    user_dir = os.path.join(USER_FOLD, uip)
    if user_email == '':
        cmd('webserver/model/code/runpsiblastexb.sh ' + user_dir +
            ' ' + 'no_email' + ' ' + str(cutoff) + ' '  + uip+ ' ' +CON_FOLD)
    else:
        cmd('webserver/model/code/runpsiblastexb.sh ' + user_dir +
            ' ' + user_email + ' ' + str(cutoff) + ' '  + uip+ ' ' +CON_FOLD)

def predictdeltablast(uip, user_email, cutoff, CON_FOLD):
    user_dir = os.path.join(USER_FOLD, uip)
    if user_email == '':
        cmd('webserver/model/code/rundeltablast.sh ' + user_dir +
            ' ' + 'no_email' + ' ' + str(cutoff) + ' '  + uip+ ' ' +CON_FOLD)
    else:
        cmd('webserver/model/code/rundeltablast.sh ' + user_dir +
            ' ' + user_email + ' ' + str(cutoff) + ' '  + uip+ ' ' +CON_FOLD)

def predicthmmer(uip, user_email, cutoff, CON_FOLD):
    user_dir = os.path.join(USER_FOLD, uip)
    if user_email == '':
        cmd('webserver/model/code/runhmmer.sh ' + user_dir +
            ' ' + 'no_email' + ' ' + str(cutoff) + ' ' + uip+ ' ' +CON_FOLD)
    else:
        cmd('webserver/model/code/runhmmer.sh ' + user_dir +
            ' ' + user_email + ' ' + str(cutoff) + ' ' + uip+ ' ' +CON_FOLD)

def extract_resultshmmer(user_fold, cutoff=1, recutoff=-1000):
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
            if score < float(recutoff):
                continue
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

            hits = [[j[0], scop_decription[j[0].replace('.', '_')][0], scop_decription[j[0].replace('.', '_')][1], scop_decription[j[0].replace('.', '_')][2], j[
                1], "images/" + j[0][1:5] + ".bio.jpg", "images/" + j[0][1:5] + ".asym.jpg", len(scop_decription[j[0].replace('.', '_')][2])] for j in hits]
        res_html.append([i, hits])
    # query_name [hit_name scop_decriptrion scop_decriptrion scop_decriptrion
    # score images images]
    return res_html

def extract_resultsdeltablast(user_fold, cutoff=1, recutoff=-1000):
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
    with open(os.path.join(user_fold, 'deltablast/LTR_input_iter5')) as seq_list, open(os.path.join(user_fold, 'deltablast/score/LTR_score_iter5')) as seq_score:
    #with open(os.path.join(user_fold, 'LTR_input_iter'+str(cutoff))) as seq_list, open(os.path.join(user_fold, 'score', 'LTR_score_iter'+str(cutoff))) as seq_score:
        for i, j in zip(seq_list, seq_score):
            query = i.strip().split()[-3]
            hit = i.strip().split()[-1]
            score = float('%.2f' % float(j.strip().split()[2]))
            #if score < float(recutoff):
            if score < recutoff:
                continue
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
        #    for hittt in hits:
    #            print hittt
   #             print hittt[0][1:5] 
#                print scop_decription[ hittt[0].replace('.', '_')][0] 
 #               print scop_decription[ hittt[0].replace('.', '_')][1] 
  #              print scop_decription[ hittt[0].replace('.', '_')][2] 
    #        print 'xxxxxxxxxxxxxxxxxxxx'
            hits = [[j[0], scop_decription[j[0].replace('.', '_')][0], scop_decription[j[0].replace('.', '_')][1], scop_decription[j[0].replace('.', '_')][2], j[
                1], "images/" + j[0][1:5] + ".bio.jpg", "images/" + j[0][1:5] + ".asym.jpg", len(scop_decription[j[0].replace('.', '_')][2])] for j in hits]
        res_html.append([i, hits])
    # query_name [hit_name scop_decriptrion scop_decriptrion scop_decriptrion
    # score images images]
    return res_html

def extract_resultspsiblastexb(user_fold, cutoff=1, recutoff=-1000):
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
    with open(os.path.join(user_fold, 'psiblastexb/LTR_input_iter5')) as seq_list, open(os.path.join(user_fold, 'psiblastexb/score/LTR_score_iter5')) as seq_score:
    #with open(os.path.join(user_fold, 'LTR_input_iter'+str(cutoff))) as seq_list, open(os.path.join(user_fold, 'score', 'LTR_score_iter'+str(cutoff))) as seq_score:
        for i, j in zip(seq_list, seq_score):
            query = i.strip().split()[-3]
            hit = i.strip().split()[-1]
            score = float('%.2f' % float(j.strip().split()[2]))
            if score < float(recutoff):
                continue
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

            hits = [[j[0], scop_decription[j[0].replace('.', '_')][0], scop_decription[j[0].replace('.', '_')][1], scop_decription[j[0].replace('.', '_')][2], j[
                1], "images/" + j[0][1:5] + ".bio.jpg", "images/" + j[0][1:5] + ".asym.jpg", len(scop_decription[j[0].replace('.', '_')][2])] for j in hits]
        res_html.append([i, hits])
    # query_name [hit_name scop_decriptrion scop_decriptrion scop_decriptrion
    # score images images]
    return res_html


def extract_results(user_fold, cutoff=1, recutoff=-1000):
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
    with open(os.path.join(user_fold, 'LTR_input_iter'+str(iternumber))) as seq_list, open(os.path.join(user_fold, 'score', 'LTR_score_iter'+str(iternumber))) as seq_score:
        for i, j in zip(seq_list, seq_score):
            query = i.strip().split()[-3]
            hit = i.strip().split()[-1].replace('.', '_')
            score = float('%.2f' % float(j.strip().split()[2]))
            if score < float(recutoff):
                continue
            if query in res:
                res[query].append([hit, score])
            else:
                res[query] = [[hit, score]]

   # LAST result is null
    with open(os.path.join(user_fold, 'LTR_input_iter1')) as seq_list, open(os.path.join(user_fold, 'score', 'LTR_score_iter1')) as seq_score:
        for q in query_name:
            if not res.has_key(q):
                for i, j in zip(seq_list, seq_score):
                    query = i.strip().split()[-3]
                    hit = i.strip().split()[-1].replace('.', '_')
                    score = float('%.2f' % float(j.strip().split()[2]))
                    if query == q:
                        if query in res:
                            res[query].append([hit, score])
                        else:
                            res[query] =[[hit,score]]
                     

 #   print res
    res_html = []
    for i in query_name:
        hits = []
        if not res.has_key(i):
            hits = []
        else:
            hits = sorted(res[i], key=lambda d: d[1], reverse=True)
#            print hits
 #           for jjj in hits:
                #print jjj[0][1:5]
            hits = [[j[0], scop_decription[j[0].replace('.', '_')][0], scop_decription[j[0].replace('.', '_')][1], scop_decription[j[0].replace('.', '_')][2], j[
                1], "images/" + j[0][1:5] + ".bio.jpg", "images/" + j[0][1:5] + ".asym.jpg", len(scop_decription[j[0].replace('.', '_')][2])] for j in hits]
        res_html.append([i, hits])
    # query_name [hit_name scop_decriptrion scop_decriptrion scop_decriptrion
    # score images images]
    return res_html

def generate_msahmmer(uip, s_option, cutoff=0.0):

    # print '3'
    user_fold = os.path.join(USER_FOLD, uip)
    #res = extract_results(user_fold, cutoff)
    # print 'ccc'
    with open(os.path.join(user_fold, 'hmmer/query', s_option[0].split('&&')[0] + '.seq'), 'r') as f:
        query = f.readlines()

    user_file = os.path.join(user_fold, 'hmmer/query', s_option[
                             0].split('&&')[0] + '_' + '.res')
    clustal_file = os.path.join(
        WORK_FOLD, 'static/clustal/' + uip + '_' + s_option[0].split('&&')[0] + '.txt')

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
    # print '6'
    subprocess.Popen(cmd_args).wait()
def generate_msadeltablast(uip, s_option, cutoff=0.0):

    # print '3'
    user_fold = os.path.join(USER_FOLD, uip)
    #res = extract_results(user_fold, cutoff)
    # print 'ccc'
    with open(os.path.join(user_fold, 'deltablast/query', s_option[0].split('&&')[0] + '.seq'), 'r') as f:
        query = f.readlines()

    user_file = os.path.join(user_fold, 'deltablast/query', s_option[
                             0].split('&&')[0] + '_' + '.res')
    clustal_file = os.path.join(
        WORK_FOLD, 'static/clustal/' + uip + '_' + s_option[0].split('&&')[0] + '.txt')

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
    # print '6'
    subprocess.Popen(cmd_args).wait()


def generate_msapsiblastexb(uip, s_option, cutoff=0.0):

    # print '3'
    user_fold = os.path.join(USER_FOLD, uip)
    #res = extract_results(user_fold, cutoff)
    # print 'ccc'
    with open(os.path.join(user_fold, 'psiblastexb/query', s_option[0].split('&&')[0] + '.seq'), 'r') as f:
        query = f.readlines()

    user_file = os.path.join(user_fold, 'psiblastexb/query', s_option[
                             0].split('&&')[0] + '_' + '.res')
    clustal_file = os.path.join(
        WORK_FOLD, 'static/clustal/' + uip + '_' + s_option[0].split('&&')[0] + '.txt')

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
    # print '6'
    subprocess.Popen(cmd_args).wait()

def generate_msadeltablast(uip, s_option, cutoff=0.0):

    # print '3'
    user_fold = os.path.join(USER_FOLD, uip)
    #res = extract_results(user_fold, cutoff)
    # print 'ccc'
    with open(os.path.join(user_fold, 'deltablast/query', s_option[0].split('&&')[0] + '.seq'), 'r') as f:
        query = f.readlines()

    user_file = os.path.join(user_fold, 'deltablast/query', s_option[
                             0].split('&&')[0] + '_' + '.res')
    clustal_file = os.path.join(
        WORK_FOLD, 'static/clustal/' + uip + '_' + s_option[0].split('&&')[0] + '.txt')

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
    # print '6'
    subprocess.Popen(cmd_args).wait()



def generate_msa(uip, s_option, cutoff=0.0):

    # print '3'
    user_fold = os.path.join(USER_FOLD, uip)
    #res = extract_results(user_fold, cutoff)
    # print 'ccc'
    with open(os.path.join(user_fold, 'query', s_option[0].split('&&')[0] + '.seq'), 'r') as f:
        query = f.readlines()

    user_file = os.path.join(user_fold, 'query', s_option[
                             0].split('&&')[0] + '_' + '.res')
    clustal_file = os.path.join(
        WORK_FOLD, 'static/clustal/' + uip + '_' + s_option[0].split('&&')[0] + '.txt')

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
    # print '6'
    subprocess.Popen(cmd_args).wait()

    '''
    res = extract_results(user_fold, cutoff)    
    for i in res:
        with open(os.path.join(user_fold, 'query', i[0] + '.seq'), 'a') as fp:
            fp.write('\n')
            for j in i[1]:
                fp.write('>' + ' '.join(j[:3]) + '\n')
                fp.write(j[3] + '\n')
        cmd_args = shlex.split('./webserver/model/Clustal_Omega/clustalo-1.2.3-Ubuntu-x86_64 -i ' + os.path.join(user_fold, 'query', i[0] + '.seq') + ' --threads 5 --outfmt clustal -o ' + os.path.join(WORK_FOLD, 'static/clustal/' + uip + '_' + i[0:7] + '.txt'))
        subprocess.Popen(cmd_args).wait()
    '''


def create_fold(path):
    cmd_args = shlex.split('mkdir -m 777 ' + path)
    subprocess.Popen(cmd_args).wait()
