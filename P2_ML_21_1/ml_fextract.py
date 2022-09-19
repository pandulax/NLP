#P2-20_8
import re
import os

from vocabulary import Closurevocab, Disclaimervocab

closure_list = Closurevocab.closure_list
disclaimer_list = Disclaimervocab.disclaimer_list


def column_namer(prefix= '', val_list=[]):
    col_names =''
    for i in range(len(val_list)):
        if i == 0:
            col_names += str(prefix)+str(i)
        else:
            col_names += ','+str(prefix)+ str(i)
    return col_names

#---- Line_Index_ratio ------------------------------------------------------------------
def line_index_ratio(line_index, string_index={}):
    if string_index:
        temp_index=[]
        for os_i in string_index:
            temp_index.append(os_i)
        
        max_index = max(temp_index)
        index_ratio = line_index/max_index
        
        return index_ratio
#---------------------------------------------------------------------------------------- 

#---- Line_word_count -------------------------------------------------------------------
def line_word_count(string_line):
    words_list = string_line.split()
    words_count = len(words_list)
    return words_count
#----------------------------------------------------------------------------------------

#---- Line_str_len ----------------------------------------------------------------------
def line_str_len(string_line):
    str_length = len(string_line)
    return str_length
#----------------------------------------------------------------------------------------

#---- Title_Case ------------------------------------------------------------------------
def title_case(string_line):
    
    shortwords_list = ['Hi', 'Pfa', 'Fyi', 'Asap', 'Aka' , 'Dear']
    Lastname_pattern = re.compile( '^[A-Z][a-z][A-Z]{0,1}[a-z]+$' )
    
    string_line = string_line.strip().replace('.', ' ')
    string_line = string_line.strip().rstrip(',')
    
    nst_line_list = string_line.split()
    fnames_correct = ''
    lname_correct = ''
    
    for nst in nst_line_list:
        if not nst.isalpha():
            nst_line_list = ''
    
    if string_line:
        if 1 < len(nst_line_list) and nst_line_list[0] not in shortwords_list:
            fnames_correct = ' '.join( nst_line_list[:-1] ).istitle()
            lname_correct  = Lastname_pattern.match(nst_line_list[-1:][0])
        
        elif len(nst_line_list) == 1  and  nst_line_list[0] not in shortwords_list :
            fnames_correct = nst_line_list[0].istitle()
            lname_correct = True
    
    if fnames_correct  and  lname_correct:
        return 1
    else:
        return 0
#----------------------------------------------------------------------------------------

#---- Upper_Case ------------------------------------------------------------------------
def upper_case(string_line):
    if string_line.isupper():
        return 1
    else:
        return 0
#----------------------------------------------------------------------------------------

#---- Numeric_Count ---------------------------------------------------------------------
def numeric_count(string_line):
    ncount = 0
    for num_i in string_line:
        if num_i.isnumeric():
            ncount += 1
    return ncount
#----------------------------------------------------------------------------------------

#---- Numeric_ratio ---------------------------------------------------------------------
def numeric_ratio(numeric_count, line_str_len):
    nratio = 0
    if numeric_count != 0:
        nratio = numeric_count/line_str_len
    return nratio
#----------------------------------------------------------------------------------------

#---- email_count -----------------------------------------------------------------------
def email_count(string_line):
    email_pattern = re.compile( '([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)' )
    emailcount = 0
    for mail in email_pattern.finditer( string_line ):
        emailcount += 1
    return emailcount
#----------------------------------------------------------------------------------------

#---- email_ratio -----------------------------------------------------------------------
def email_ratio(email_count, line_word_count):
    emailratio = 0
    if email_count != 0:
        emailratio = email_count/line_word_count
    return emailratio
#----------------------------------------------------------------------------------------

#----- Line ngram count to a list--------------------------------------------------------
def ngramcount(string_line ='', nglist = []):
    string_line = string_line.lower()
    string_line = string_line.replace(',', ' ')
    string_line = string_line.replace('.', ' ')
    string_line = string_line.replace(':', ' ')
    
    string_line = ' '.join(string_line.split())
    
    wc_list=[]
    for ngram in nglist:
        html_tag = re.compile(ngram)
        count=0
        for found in html_tag.finditer(string_line):
            count += 1
        wc_list.append(count)
    return wc_list
#----------------------------------------------------------------------------------------


#----- Single-Line ngram count to a list--------------------------------------------------------
def ngram_count(string_line ='', nglist = []):
    string_line = string_line.lower()
    string_line = string_line.replace(',', ' ')
    string_line = string_line.replace('.', ' ')
    string_line = string_line.replace(':', ' ')
    string_line = string_line.replace('-', ' ')
    
    string_list = string_line.split()
    
    wc_list=[]
    for ngram in nglist:
        count = string_list.count(ngram)
        wc_list.append(count)
    return wc_list
#----------------------------------------------------------------------------------------

def fextract(index, string_index = {}):
    
    
    v1 = line_index_ratio(index, string_index)
    
    v2 = line_word_count(string_index[index])
    
    v3 = line_str_len(string_index[index])
    
    v4 = title_case( string_index[index])
    
    v5 = upper_case( string_index[index])
    
    v6 = numeric_count( string_index[index])
    
    v7 = numeric_ratio( v6, v3)
    
    v8 = email_count(string_index[index])
    
    v9 = email_ratio( v8, v2)
    
    v10 = ngram_count( string_index[index], closure_list)
    
    v11 = ngram_count(string_index[index], disclaimer_list)
    
    
    dataset_arr_list = [v1] + [v2] + [v3] + [v4] + [v5] + [v6] + [v7] + [v8] + [v9] + v10 + v11
    
    
    return dataset_arr_list


#s_index = {2:'Hi', 3:'How are you doing', 5: 'Latest update can be found in the updated info', 9:'Thanks', 11:' Eric James'}

#if __name__ == '__main__':
    #fextract(9, s_index)


