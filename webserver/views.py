from flask import render_template, request, redirect, url_for, jsonify
from webserver import app
from conf import *
import methods
import os
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from threading import Thread
import socket


@app.route('/')
@app.route('/home')
@app.route('/home/')
def home():
    return render_template('home.html')


@app.route('/server', methods=['GET', 'POST'])
def server():
    if request.method == 'POST':
        email_sended = 0
        user_ip_time = request.access_route[0] + '_' + str(time.time())
        user_dir = os.path.join(USER_FOLD, user_ip_time)
        user_file = os.path.join(user_dir, 'result.txt')
        receive_seq = request.form['sequence']
        user_email = request.form['Email']
        cutoff = int(request.form['cutoff'])
        recutoff = int(request.form['recutoff'])
        #cutoff = float(request.form['type_select'])
        #cutoff = int(16)
        if receive_seq:
            sequences = receive_seq.replace('\r\n', '\n').split('\n')
        else:
            sequences = request.files['file']
        methods.create_fold(user_dir)
        check_result = methods.check_and_write(sequences, user_dir)
        if not check_result[0]:
            return render_template('error.html', error=check_result[1])
        else:
            methods.predict(user_ip_time, user_email, cutoff, recutoff,  CON_FOLD)
            return redirect(url_for('result', uip=user_ip_time, cutoff=cutoff, recutoff=recutoff))
    elif request.method == 'GET':
        return render_template('server.html')

@app.route('/serverhmmer', methods=['GET', 'POST'])
def serverhmmer():
    if request.method == 'POST':
        email_sended = 0
        user_ip_time = request.access_route[0] + '_' + str(time.time())
        user_dir     = os.path.join(USER_FOLD, user_ip_time)
        user_file    = os.path.join(user_dir, 'result.txt')
        receive_seq  = request.form['sequence']
        user_email   = request.form['Email']
        cutoff       = int(request.form['cutoff'])
        recutoff     = int(request.form['recutoff'])
        #cutoff = float(request.form['type_select'])
        #cutoff = int(16)
        if receive_seq:
            sequences = receive_seq.replace('\r\n', '\n').split('\n')
        else:
            sequences = request.files['file']
        methods.create_fold(user_dir)
        check_result = methods.check_and_write(sequences, user_dir)
        if not check_result[0]:
            return render_template('error.html', error=check_result[1])
        else:
            methods.predicthmmer(user_ip_time, user_email, cutoff, CON_FOLD)
            return redirect(url_for('resulthmmer', uip=user_ip_time, cutoff=cutoff, recutoff=recutoff))
    elif request.method == 'GET':
        return render_template('serverhmmer.html')

@app.route('/serverdeltablast', methods=['GET', 'POST'])
def serverdeltablast():
    if request.method == 'POST':
        email_sended = 0
        user_ip_time = request.access_route[0] + '_' + str(time.time())
        user_dir     = os.path.join(USER_FOLD, user_ip_time)
        user_file    = os.path.join(user_dir, 'result.txt')
        receive_seq  = request.form['sequence']
        user_email   = request.form['Email']
        cutoff       = int(request.form['cutoff'])
        recutoff     = int(request.form['recutoff'])
        #cutoff = float(request.form['type_select'])
        #cutoff = int(16)
        if receive_seq:
            sequences = receive_seq.replace('\r\n', '\n').split('\n')
        else:
            sequences = request.files['file']
        methods.create_fold(user_dir)
        check_result = methods.check_and_write(sequences, user_dir)
        if not check_result[0]:
            return render_template('error.html', error=check_result[1])
        else:
            methods.predictdeltablast(user_ip_time, user_email, cutoff, CON_FOLD)
            return redirect(url_for('resultdeltablast', uip=user_ip_time, cutoff=cutoff, recutoff=recutoff))
    elif request.method == 'GET':
        return render_template('serverdeltablast.html')

@app.route('/serverpsiblastexb', methods=['GET', 'POST'])
def serverpsiblastexb():
    if request.method == 'POST':
        email_sended = 0
        user_ip_time = request.access_route[0] + '_' + str(time.time())
        user_dir     = os.path.join(USER_FOLD, user_ip_time)
        user_file    = os.path.join(user_dir, 'result.txt')
        receive_seq  = request.form['sequence']
        user_email   = request.form['Email']
        cutoff       = int(request.form['cutoff'])
        recutoff     = int(request.form['recutoff'])
        #cutoff = float(request.form['type_select'])
        #cutoff = int(16)
        if receive_seq:
            sequences = receive_seq.replace('\r\n', '\n').split('\n')
        else:
            sequences = request.files['file']
        methods.create_fold(user_dir)
        check_result = methods.check_and_write(sequences, user_dir)
        if not check_result[0]:
            return render_template('error.html', error=check_result[1])
        else:
            methods.predictpsiblastexb(user_ip_time, user_email, cutoff, CON_FOLD)
            return redirect(url_for('resultpsiblastexb', uip=user_ip_time, cutoff=cutoff, recutoff=recutoff))
    elif request.method == 'GET':
        return render_template('serverpsiblastexb.html')

@app.route('/citation')
@app.route('/citation/')
def citation():
    return render_template('citation.html')

@app.route('/download')
@app.route('/download/')
def download():
    return render_template('download.html')

@app.route('/document')
@app.route('/document/')
def document():
    return render_template('document.html')

@app.route('/ISHERROR')
@app.route('/ISHERROR/')
def isherror():
    return render_template('ISHERROR.html')

@app.route('/tutorial')
@app.route('/tutorial/')
def tutorial():
    return render_template('tutorial.html')


@app.route('/<user_dir>/<cutoff>')
def user_result(user_dir, cutoff):
    res = methods.extract_results(user_dir, float(cutoff))
    return render_template('result.html', result=res)

@app.route('/<user_dir>/<cutoff>')
def user_resulthmmer(user_dir, cutoff):
    res = methods.extract_resultshmmer(user_dir, float(cutoff))
    return render_template('resulthmmer.html', result=res)

@app.route('/resulthmmer/<uip>', methods=['GET', 'POST'])
def resulthmmer(uip):
    user_dir = os.path.join(USER_FOLD, uip)    
    if request.method == 'POST':
        print 'result post'
        s_option = request.form.getlist("selected")
        print s_option[0].split('&&')[0]
      
        cutoff = float(request.args.get('cutoff'))
        #print '1'
           
        clustal_file= os.path.join(WORK_FOLD, 'static/clustal/' + uip + '_' + s_option[0].split('&&')[0] + '.txt') 
        
        methods.generate_msahmmer(uip, s_option, cutoff)
        #print '2'
        # with open(post_seq_file,'w') as writer:
        clustal_result = []        
        with open(clustal_file, 'r') as fp: 
            #print '7'
            clustal_result = fp.readlines()
            #print '8'
    #    return 0 
        return render_template('clustal.html', uip=uip, query=s_option[0].split('&&')[0], clustal_result=clustal_result)

    elif request.method == 'GET':
        #cutoff = int(request.args.get('cutoff'))
        cutoff = 5

        result_score = user_dir + '/hmmer/score/LTR_score_iter5'
        recutoff = float(request.args.get('recutoff'))
        query_name = request.args.get('query')
        #query_name = "d1cxca_"
        if os.path.isfile(result_score):
            res = methods.extract_resultshmmer(user_dir, cutoff, recutoff)
            query_names = [i[0] for i in res]
            # download_path = os.path.join(WORK_FOLD, 'static/result/' + uip + '.txt')
            # methods.write_res(download_path, res)
            if query_name:
                for i in range(len(res)):
                    if res[i][0] == query_name:
                        res = res[i]
                        break
            else:
                res = res[0]
            #print 'result return!'
            return render_template('resulthmmer.html', result=res, uip=uip, cutoff=cutoff, query_names=query_names, recutoff=recutoff)
        else:
            # return render_template('running.html', uip=uip)
            return render_template('processinghmmer.html', uip=uip, cutoff=cutoff, recutoff=recutoff)


@app.route('/result/<uip>', methods=['GET', 'POST'])
def result(uip):
    user_dir = os.path.join(USER_FOLD, uip)    
    if request.method == 'POST':
        print 'result post'
        s_option = request.form.getlist("selected")
        print s_option[0].split('&&')[0]
      
        cutoff = float(request.args.get('cutoff'))
        #print '1'
           
        clustal_file= os.path.join(WORK_FOLD, 'static/clustal/' + uip + '_' + s_option[0].split('&&')[0] + '.txt') 
        
        methods.generate_msa(uip, s_option, cutoff)
        #print '2'
        # with open(post_seq_file,'w') as writer:
        clustal_result = []        
        with open(clustal_file, 'r') as fp: 
            #print '7'
            clustal_result = fp.readlines()
            #print '8'
        
        return render_template('clustal.html', uip=uip, query=s_option[0].split('&&')[0], clustal_result=clustal_result)

    elif request.method == 'GET':
        cutoff = int(request.args.get('cutoff'))
        recutoff = float(request.args.get('recutoff'))
        iternumber = 1 
        if int(cutoff) == 2:
            iternumber=2
        elif int(cutoff)==3:
            iternumber=5
        elif int(cutoff)==4:
            iternumber=10

	result_cutoff = int(recutoff)
#	if int(recutoff) == 2:
#		result_cutoff = -5 
#	if int(recutoff) == 3:
#		result_cutoff = 0 
#	if int(recutoff) == 4:
#		result_cutoff = 1 
#	if int(recutoff) == 5:
#		result_cutoff = 2 
#	if int(recutoff) == 6:
#		result_cutoff = 3 
#	if int(recutoff) == 7:
#		result_cutoff = 4 
#	if int(recutoff) == 8:
#		result_cutoff = 5 
#
        result_score = user_dir + '/score/LTR_score_iter'+str(iternumber)
#        cutoff = float(request.args.get('cutoff'))
        query_name = request.args.get('query')
        if os.path.isfile(result_score):
            res = methods.extract_results(user_dir, cutoff, result_cutoff)
            query_names = [i[0] for i in res]
            # download_path = os.path.join(WORK_FOLD, 'static/result/' + uip + '.txt')
            # methods.write_res(download_path, res)
            if query_name:
                for i in range(len(res)):
                    if res[i][0] == query_name:
                        res = res[i]
                        break
            else:
                res = res[0]
            #print 'result return!'
            return render_template('result.html', result=res, uip=uip, cutoff=cutoff, recutoff=recutoff, query_names=query_names)
        else:
            # return render_template('running.html', uip=uip)
            return render_template('processing.html', uip=uip, cutoff=cutoff, recutoff=recutoff)

@app.route('/resultdeltablast/<uip>', methods=['GET', 'POST'])
def resultdeltablast(uip):
    user_dir = os.path.join(USER_FOLD, uip)    
    if request.method == 'POST':
        print 'result post'
        s_option = request.form.getlist("selected")
        print s_option[0].split('&&')[0]
      
        cutoff = float(request.args.get('cutoff'))
        #print '1'
           
        clustal_file= os.path.join(WORK_FOLD, 'static/clustal/' + uip + '_' + s_option[0].split('&&')[0] + '.txt') 
        
        methods.generate_msadeltablast(uip, s_option, cutoff)
        #print '2'
        # with open(post_seq_file,'w') as writer:
        clustal_result = []        
        with open(clustal_file, 'r') as fp: 
            #print '7'
            clustal_result = fp.readlines()
            #print '8'
    #    return 0 
        return render_template('clustal.html', uip=uip, query=s_option[0].split('&&')[0], clustal_result=clustal_result)

    elif request.method == 'GET':
        #cutoff = int(request.args.get('cutoff'))
        cutoff = 5

        result_score = user_dir + '/deltablast/score/LTR_score_iter5'
        recutoff = float(request.args.get('recutoff'))
        query_name = request.args.get('query')
        #query_name = "d1cxca_"
        if os.path.isfile(result_score):
            res = methods.extract_resultsdeltablast(user_dir, cutoff, recutoff)
            query_names = [i[0] for i in res]
            # download_path = os.path.join(WORK_FOLD, 'static/result/' + uip + '.txt')
            # methods.write_res(download_path, res)
            if query_name:
                for i in range(len(res)):
                    if res[i][0] == query_name:
                        res = res[i]
                        break
            else:
                res = res[0]
            #print 'result return!'
            return render_template('resultdeltablast.html', result=res, uip=uip, cutoff=cutoff, query_names=query_names, recutoff=recutoff)
        else:
            # return render_template('running.html', uip=uip)
            return render_template('processingdeltablast.html', uip=uip, cutoff=cutoff, recutoff=recutoff)
@app.route('/resultpsiblastexb/<uip>', methods=['GET', 'POST'])
def resultpsiblastexb(uip):
    user_dir = os.path.join(USER_FOLD, uip)    
    if request.method == 'POST':
        print 'result post'
        s_option = request.form.getlist("selected")
        print s_option[0].split('&&')[0]
      
        cutoff = float(request.args.get('cutoff'))
        #print '1'
           
        clustal_file= os.path.join(WORK_FOLD, 'static/clustal/' + uip + '_' + s_option[0].split('&&')[0] + '.txt') 
        
        methods.generate_msapsiblastexb(uip, s_option, cutoff)
        #print '2'
        # with open(post_seq_file,'w') as writer:
        clustal_result = []        
        with open(clustal_file, 'r') as fp: 
            #print '7'
            clustal_result = fp.readlines()
            #print '8'
    #    return 0 
        return render_template('clustal.html', uip=uip, query=s_option[0].split('&&')[0], clustal_result=clustal_result)

    elif request.method == 'GET':
        #cutoff = int(request.args.get('cutoff'))
        cutoff = 5

        result_score = user_dir + '/psiblastexb/score/LTR_score_iter5'
        recutoff = float(request.args.get('recutoff'))
        query_name = request.args.get('query')
        #query_name = "d1cxca_"
        if os.path.isfile(result_score):
            res = methods.extract_resultspsiblastexb(user_dir, cutoff, recutoff)
            query_names = [i[0] for i in res]
            # download_path = os.path.join(WORK_FOLD, 'static/result/' + uip + '.txt')
            # methods.write_res(download_path, res)
            if query_name:
                for i in range(len(res)):
                    if res[i][0] == query_name:
                        res = res[i]
                        break
            else:
                res = res[0]
            #print 'result return!'
            return render_template('resultpsiblastexb.html', result=res, uip=uip, cutoff=cutoff, query_names=query_names, recutoff=recutoff)
        else:
            # return render_template('running.html', uip=uip)
            return render_template('processingpsiblastexb.html', uip=uip, cutoff=cutoff, recutoff=recutoff)

