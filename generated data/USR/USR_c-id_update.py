import pandas as pd
import re
import wxconv
import glob
from wxconv import WXC
import codecs
import numpy as np
import os,subprocess,shutil

###INPUTS
#1. path to the directory containing the individual USR files
usr_dir_path = '/mnt/ubuntu/e/META/ltrc/Corpus/Hin_Geo_ncert_11stnd-bk3_USR'
#2. path to the xlsx file having the parallel sentence corpus data (directory delimiter : '/')
parellel_corpus_excel_path = '/mnt/ubuntu/e/META/ltrc/Corpus/Parallel Corpus Excel/ParallelCorpus_geo_ncert_11stnd-bk3.xlsx'
#3. name of the mrs dictionary data file
mrs_dictionary_filename = 'H_concept-to-mrs-rels.dat'
#4. file format of the usr files (txt/xlsx)
usr_ff = 'txt'
#5. combined USR file name
result_comb_usr = 'combined_Hin_Geo_ncert_11stnd-bk3_modv2.xlsx'

def getLines(file,splitby):
    with codecs.open(file, 'r', encoding="utf-8") as filer:
                    data = filer.read()
                    data = re.sub('\t+', '\t', data)
                    data = data.strip('\n')
    lines = data.split(splitby)
    return lines
#helper function to generate dataframe from .txt usr files
def get_txt_df(dir_path):
    d = {'sent_id':[],'hin_sent':[],'og_conc':[]}
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            
                fpath = dir_path.split('/')[-1] + '/' + path
                lines = getLines(fpath,'\n')

                if len(lines) >= 10:
                    d['sent_id'].append(path.split('.')[0])
                    d['hin_sent'].append(lines[0])
                    d['og_conc'].append(lines[1])
            
    usr_d = pd.DataFrame.from_dict(d)
    return usr_d

#helper function to generate dataframe from '.xlsx' usr files
def get_xlsx_df(dir_path):
    d = {'sent_id':[],'hin_sent':[],'og_conc':[]}
    res = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
                fpath = dir_path.split('/')[-1] + '/' + path
                #fpath = 'Hin_Geo_ncert_8stnd_USR\\' + path
                df1 = pd.read_excel(fpath ,header =None)
                d['sent_id'].append(path.split('.')[0])
                d['hin_sent'].append(df1.iloc[0][0])
                conc = []
                for i in range(len(list(df1))):
                    conc.append(str(df1.iloc[1][i]))

                d['og_conc'].append(','.join(conc))

    usr_d = pd.DataFrame.from_dict(d)
    return usr_d

usr_d = get_txt_df(usr_dir_path) if usr_ff == 'txt' else get_xlsx_df(usr_dir_path)

def get_pc_df(filepath):
    pc_6_df = pd.read_excel(filepath,header=None)
    pc_6_df. columns = ['hin_id', 'hin_sent', 'eng_id', 'eng_sent']
    pc_6_df['hin_sent'] = pc_6_df['hin_sent'].astype(str)
    pc_6_df['hin_sent'] = pc_6_df.hin_sent.apply(lambda x: x.replace('  ',' '))
    pc_6_df['hin_sent'] = pc_6_df.hin_sent.apply(lambda x: x.replace('|','।'))
    pc_6_df['hin_sent'] = pc_6_df.hin_sent.apply(lambda x: x.replace(' ।','।'))
    pc_6_df['eng_sent'] = pc_6_df.eng_sent.apply(lambda x : re.sub("[\(\[].*?[\)\]]", "", x))
    pc_6_df['eng_sent'] = pc_6_df.eng_sent.apply(lambda x : x.replace('"',''))
    pc_6_df['eng_sent'] = pc_6_df.eng_sent.apply(lambda x : x.replace("n't",' not'))
    pc_6_df['eng_sent'] = pc_6_df.eng_sent.apply(lambda x : x.replace("'s'",''))
    pc_6_df['eng_sent'] = pc_6_df.eng_sent.apply(lambda x : x.strip('\n'))
    pc_6_df['eng_sent'] = pc_6_df.eng_sent.apply(lambda x : x.strip(' '))
    pc_6_df['hin_sent'] = pc_6_df.hin_sent.apply(lambda x: x.replace(' ?','?'))
    return pc_6_df

pc_6_df = get_pc_df(parellel_corpus_excel_path)
pc_6_df.to_csv('pc_v1.txt', sep ='\t')


def gen_root_txt(input_filename,output_filename):
    fw = open(output_filename, 'w')
    f = open(input_filename, 'r', encoding="utf8")
    fr = f.readlines()
    fw.write('hin_id'+'\t'+'hin_sent'+'\t''eng_id' + '\t' +'eng_sent' +'\t'+'eng_roots\n')

    for i in range(len(fr)):
        try:
            lst = fr[i].split('\t')
            hin_id = lst[1]
            hin_sent = lst[2]
            eng_id = lst[3]
            engsent = lst[4].replace('\n','')
            engsent = engsent.replace("'s",'')
            engsent = engsent.replace(';','')
            engsent = engsent.replace('°','')
            engsent = engsent.replace("'",'')
            engsent = engsent.replace(")",'')
            cmd = "echo "+engsent+" | lt-proc eng.bin"
            result1 = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE)
            engroots = str(result1.communicate()[0])
            entry = hin_id + '\t' + hin_sent + '\t' + eng_id + '\t' + engsent + '\t' + engroots
            fw.write(entry)
            fw.write('\n')
        except:
            fw.write('OOPs' + engsent)
            fw.write('\n')
    fw.close()

gen_root_txt("pc_v1.txt",'pc_root_v1.txt')
pc_conc_root_6_df = pd.read_csv('pc_root_v1.txt',sep = '\t')
#pc_conc_root_6_df2 = pc_conc_root_6_df.dropna()
pc_conc_root_6_df = pc_conc_root_6_df[1:]
#print(pc_conc_root_6_df)
pc_conc_root_6_df.to_csv('pc_debug.txt',sep = '\t')
def get_rootlist(roots):
    roots = str(roots['eng_roots'])
    roots = roots[2:] if roots[:2] == "b'" else roots
    sp1 = roots.split('^')
    lt = []
    for i in sp1:
        sp2 = i.split('/')
        for j in sp2[1:]:
            sp3 = j.split('<')[0]
            if sp3 not in lt and sp3 != '.':
                lt.append(sp3)
    return lt
pc_conc_root_6_df['eng_root_l'] = pc_conc_root_6_df.apply(lambda x : get_rootlist(x),axis=1)
#print(pc_conc_root_6_df)
pc_conc_root_6_df.to_csv('pc_debug2.txt',sep = '\t')
def get_rootlist2(row):
    sent_id = row['sent_id'].split('-')[0]
    #print(sent_id)
    cross = pc_conc_root_6_df.apply(lambda x : x['hin_id'].strip(' ') == sent_id,axis=1)
    if pc_conc_root_6_df[cross].empty == False:
        return pc_conc_root_6_df[cross]['eng_root_l'].values[0]
    else:
        return ''
usr_d.to_csv('usr_debug.txt',sep = '\t')
usr_d['eng_roots'] = usr_d.apply(lambda x: get_rootlist2(x),axis =1)
def handle_comp_usr(row):
    hin_sent = row['hin_sent']
    sent_splt = hin_sent.split(' ')
    og_conc = row['og_conc'].split(',')
    con2 = WXC(order='utf2wx')
    comps = []
    for i in sent_splt:
        if '-' in i:
            i = i.replace(',','')
            i = i.replace(':','')
            i = i.replace(';','')
            comps.append(con2.convert(i.replace('#','')))
    
    d = {}
    for j in range(len(og_conc)):
        el = og_conc[j]
        el = el.split('_')[0]
        if el in comps:
            j_s = el.split('-') 
            j_s = [k+'_1' for k in j_s]
            el = '+'.join(j_s)
            d[j] = el
    for i in d.keys():
        og_conc[i] = d[i]
    return (',').join(og_conc)
usr_d['og_conc'] = usr_d.apply(lambda x:handle_comp_usr(x),axis=1)

def get_mrs_df(filename):
    d ={'conc_label_wx':[],'conc_label_utf':[],'conc_in_eng':[],'mrs_conc':[]}
    con = WXC(order='wx2utf', lang='hin')
    for line in getLines(filename,'\n'):
        internal_lines = line.split('\t')
        if len(internal_lines)>=4:
            d['conc_label_wx'].append(internal_lines[1])
            d['conc_label_utf'].append(con.convert(internal_lines[1]).replace('+',' '))
            d['conc_in_eng'].append(internal_lines[2])
            d['mrs_conc'].append(internal_lines[3])
        else:
            #print(internal_lines[2])
            d['conc_label_wx'].append(internal_lines[1])
            d['conc_label_utf'].append(con.convert(internal_lines[1]).replace('+',' '))
            if len(internal_lines[2])>20:
                d['conc_in_eng'].append(internal_lines[2].split(' ')[0])
                d['mrs_conc'].append(internal_lines[2].split(' ')[1])
            else:
                d['conc_in_eng'].append(internal_lines[2][0:7])
                d['mrs_conc'].append(internal_lines[2][8:])
    mrs_df = pd.DataFrame.from_dict(d)
    return mrs_df

mrs_df = get_mrs_df(mrs_dictionary_filename)

def get_comp_word_usr(word):
    if '-' in word:
        split_dsh = word.split('-')
        #if len(split_dsh)>2:
            #print(word)
        wordlist = [split_dsh[0].split('_')[0].replace('+',' ')]
        wordlist.append('-'+'-'.join(split_dsh[1:]))
        return ' '.join(wordlist)
    else:
        split_pls = word.split('+')
        wordlist = []
        for i in split_pls:
            wordlist.append(i.split('_')[0])
        return ' '.join(wordlist)
def get_comp_word_mrs(word):
    if '-' in word:
        split_dsh = word.split('-')
        wordlist = [i.split('_')[0] for i in split_dsh]
    elif '+' in word:
        split_pls = word.split('+')
        wordlist = [i.split('_')[0] for i in split_pls]
    else:
        return word.split('_')[0]
    return ' '.join(wordlist)
def get_ft(df,eng_root_l,suffix,i):
    condit2 = df.conc_in_eng.apply(lambda x : x.split('_')[0].lower() in eng_root_l)
    cross2 = df[condit2]
    if cross2.empty != True:
        #print('11111')
        if len(cross2)>1:
            y = [k.split('_')[0] for k in cross2['conc_in_eng']]
            x=np.array(y)

            eng_uq = np.unique(x)
            if len(eng_uq)>1:
                for v in cross2['conc_label_wx'].values:
                    return v if suffix == '' else v + suffix
            else:
                return cross2['conc_label_wx'].values[0] if suffix == '' else cross2['conc_label_wx'].values[0] + suffix
        else:
            return cross2['conc_label_wx'].values[0] if suffix == '' else cross2['conc_label_wx'].values[0] + suffix
    else:
        return i if suffix == '' else i + suffix


def get_correct(row):
    og_conc = row['og_conc'].split(',')
    eng_root_l = [s.lower() for s in row['eng_roots']]
    ft = []
    for i in og_conc:
        hinword = get_comp_word_usr(i)
        suffix = ''
        if '-' in hinword:
            split_spc = hinword.split('-')
            hinword = hinword.split('-')[0].strip(' ')
            suffix ='-'+ '-'.join(split_spc[1:])
        
                    
        condit1 = mrs_df.conc_label_wx.apply(lambda x : get_comp_word_mrs(x)==hinword)
        cross1 = mrs_df[condit1]
        if cross1.empty != True:
            ft.append(get_ft(cross1,eng_root_l,suffix,i))
        else:
            if ' ' in hinword:
                if suffix == '':
                    #print(hinword)
                    split_spc = hinword.split(' ')
                    ft1 = []
                    for j in split_spc:
                        condit2 = mrs_df.conc_label_wx.apply(lambda x : get_comp_word_mrs(x)==j)
                        cross2 = mrs_df[condit2]
                        if cross2.empty != True:

                            ft1.append(get_ft(cross2,eng_root_l,suffix,j+'_1'))
                        else:
                            ft1.append(j+'_1***')
                    ft.append('+'.join(ft1))
                else:

                    ft.append(hinword.replace(' ','+')+'***'+suffix)
            else:
                app = i if suffix == '' else i+suffix
                ft.append(app+'***')
    return ft


usr_d_1 = usr_d
usr_d_1['mod_conc'] = usr_d_1.apply(lambda x : get_correct(x),axis=1)

def get_warn(row):
    conc = row['mod_conc']
    
    nfound = []
    rej = ['main','nan']
    for i in conc:
        if '***' in i and i.replace('***','') not in rej:
            if '+' in i and '-' not in i:
                splt_pls = i.split('+')
                for j in splt_pls:
                    if '***' in j:
                        nfound.append(j)
            elif '-' in i:
                #print(i.split('-')[0])
                nfound.append(i.split('-')[0])
            else:
                nfound.append(i)
    nfound = [i.replace('***','') for i in nfound]
    return ','.join(nfound) +" not found in dictionary."

usr_d_1['warning'] = usr_d_1.apply(lambda x:get_warn(x),axis =1)
usr_d_1['mod_conc'] = usr_d_1.mod_conc.apply(lambda x: [y.replace('***','') for y in x] )
usr_d_1['warning'] = usr_d_1.warning.apply(lambda x : '' if x == ' not found in dictionary.' else x)

def modify_excel_USRs(dir_path):
    
    ndir = dir_path+'_mod'
    if os.path.isdir(ndir):
        shutil.rmtree(ndir)
    os.mkdir(dir_path+'_mod')
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            try:
                fpath = dir_path.split('/')[-1] + '/' + path
                #fpath = 'Hin_Geo_ncert_8stnd_USR\\' + path
                df1 = pd.read_excel(fpath ,header =None)
                sent_id = path.split('.')[0]
                mod_conc= usr_d_1[usr_d_1['sent_id'] == sent_id]['mod_conc'].values[0]
                #print(mod_conc)
                if len(mod_conc) != len(list(df1)):
                    print(sent_id)
                else:
                    for i in range(len(list(df1))):
                        df1.iloc[1][i] = mod_conc[i]
                df1.loc[len(df1.index)] = ['']*len(list(df1))
                df1.iloc[len(df1.index)-1][0] = usr_d_1[usr_d_1['sent_id'] == sent_id]['warning'].values[0]
                full_path = ndir+'/' + path
                df1.to_excel(full_path,header=False,index=False)
            except:
                print('Invalid file content:'  + fpath)
def modify_txt_USRs(dir_path):
    
    ndir = dir_path+'_mod'
    if os.path.isdir(ndir):
        shutil.rmtree(ndir)
    os.mkdir(dir_path+'_mod')
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            try:
                fpath = dir_path.split('/')[-1] + '/' + path
                #fpath = 'Hin_Geo_ncert_8stnd_USR\\' + path
                lines = getLines(fpath,'\n')
                sent_id = path.split('.')[0]
                mod_conc= usr_d_1[usr_d_1['sent_id'] == sent_id]['mod_conc'].values[0]
                #print(mod_conc)
                if len(mod_conc) != len(lines[1].split(',')):
                    print(sent_id)
                lines[1] = ','.join(mod_conc)
                
                if len(lines) == 11:
                    lines[10] = usr_d_1[usr_d_1['sent_id'] == sent_id]['warning'].values[0]
                elif len(lines)<11:
                    lines.append(usr_d_1[usr_d_1['sent_id'] == sent_id]['warning'].values[0])
                
                full_path = ndir+'/' + path
                fw = open(full_path, 'w')
                for line in lines:
                    fw.write(line)
                    fw.write('\n')
                fw.close()
                #df1.to_excel(path,header=False,index=False)
            except:
                print('Invalid file content:'  + fpath)
                

if usr_ff == 'txt':
    modify_txt_USRs(usr_dir_path)
else:
    modify_excel_USRs(usr_dir_path)
def gen_combined_txtUSR(dir_path):
    d = {'sent_id':[],'hin_sent':[],'og_conc':[],'num':[],'col4':[],'pos':[],'deprel':[],'col7':[],'col8':[],'col9':[],'type':[],'warning':[]}
    res = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            fpath = dir_path.split('/')[-1] + '/' + path
            lines = getLines(fpath,'\n')
            sent_id = path.split('.')[0]
            if len(lines)>=10:
                d['sent_id'].append(path.split('.')[0])
                d['hin_sent'].append(lines[0])
                d['og_conc'].append(lines[1])
                d['num'].append(lines[2])
                d['col4'].append(lines[3])
                d['pos'].append(lines[4])
                d['deprel'].append(lines[5])
                d['col7'].append(lines[6])
                d['col8'].append(lines[7])
                d['col9'].append(lines[8])
                d['type'].append(lines[9])
                if len(lines) == 11:
                    d['warning'].append(lines[10])
                else:
                    d['warning'].append('')

            else:
                print(path)

                

    combined_usr_dd = pd.DataFrame.from_dict(d)
    return combined_usr_dd
def gen_combined_USR(dir_path):
    d = {'sent_id':[],'hin_sent':[],'og_conc':[],'num':[],'col4':[],'pos':[],'deprel':[],'col7':[],'col8':[],'col9':[],'type':[],'warning':[]}
    res = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
                fpath = dir_path.split('/')[-1] + '/' + path
                df1 = pd.read_excel(fpath ,header =None)
                sent_id = path.split('.')[0]
                df1 = df1.fillna('')
                d['sent_id'].append(path.split('.')[0])
                d['hin_sent'].append(df1.iloc[0][0])
                if len(df1.index)<10:
                    print(path)
                    for i in range(len(df1.index),10):
                        df1.loc[i] = ['']*len(list(df1))

                conc,num,col4,pos,deprel,col7,col8,col9,type1,warning = [],[],[],[],[],[],[],[],[],[]
                for i in range(len(list(df1))):
                    conc.append(str(df1.iloc[1][i]))
                    num.append(str(df1.iloc[2][i]))
                    col4.append(str(df1.iloc[3][i]))
                    pos.append(str(df1.iloc[4][i]))
                    deprel.append(str(df1.iloc[5][i]))
                    col7.append(str(df1.iloc[6][i]))
                    col8.append(str(df1.iloc[7][i]))
                    col9.append(str(df1.iloc[8][i]))            
                    type1.append(str(df1.iloc[9][i]))
                    if len(df1) == 11:
                        warning.append(str(df1.iloc[10][i]))
                    else:
                        warning.append('')

                d['og_conc'].append(','.join(conc))
                d['num'].append(','.join(num))
                d['col4'].append(','.join(col4))
                d['pos'].append(','.join(pos))
                d['deprel'].append(','.join(deprel))
                d['col7'].append(','.join(col7))
                d['col8'].append(','.join(col8))
                d['col9'].append(','.join(col9))
                d['type'].append(','.join(type1))
                d['warning'].append(','.join(warning))

    combined_usr_dd = pd.DataFrame.from_dict(d)
    return combined_usr_dd
combined_usr_dd = gen_combined_txtUSR(usr_dir_path + '_mod') if usr_ff == 'txt' else gen_combined_USR(usr_dir_path + '_mod')
combined_usr_dd['type'] = combined_usr_dd.type.apply(lambda x: x.replace(',',''))
combined_usr_dd['warning'] = combined_usr_dd.warning.apply(lambda x: x.strip(','))
combined_usr_dd.to_excel(result_comb_usr,header=False,index=False)




