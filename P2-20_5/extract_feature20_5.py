#P2-20_4
import re
import os
import csv

#closure_list = ['all the best', 'b Regards', 'best', 'best regards', 'best wishes', 'cheers', 'cordially', 'cordially yours', 'faithfully', 'fond regards', 'kind regards', 'many thanks', 'regards', 'respectfully', 'respectfully yours', 'sincerely', 'sincerely yours', 'thank you', 'thanks again', 'thanks regards', 'thanks and regards', 'thanks b regards', 'thanks and b regards', 'warmly', 'warm regards', 'with appreciation', 'with gratitude', 'with sincere appreciation', 'with sincere thanks', 'yours truly', 'yours sincerely', 'yours faithfully']
#closure_list = ['all best', 'all the best', 'b regards', 'best', 'bests', 'best regards', 'best wishes', 'ciao', 'cheers', 'cordially', 'cordially yours', 'faithfully', 'fond regards', 'kind regards', 'thanks', 'many thanks', 'my best to you', 'rgds', 'regards', 'respectfully', 'respectfully yours', 'sincerely', 'sincerely yours', 'see you around', 'take care', 'thank you', 'thank you best regards', 'thank you and best regards', 'thank you b regards', 'thank you and b regards', 'thanks again', 'thanks regards', 'thanks and regards', 'thanks b regards', 'thanks and b regards', 'thanks so much', 'warmly', 'warmest', 'warm gratitude', 'warm regards', 'warmest regards', 'with appreciation', 'with gratitude', 'with sincere appreciation', 'with sincere thanks', 'yours truly', 'yours sincerely', 'yours faithfully']

closure_list = ['see', 'cordially', 'many', 'respectfully', 'cheers', 'wishes', 'with', 'my', 'truly', 'much', 'best', 'thanks', 'thanking', 'kind', 'appreciation', 'take', 'bests', 'regard', 'regards', 'all', 'so', 'sincere', 'sincerely', 'warm', 'ciao', 'faithfully', 'fond', 'thank', 'again', 'the', 'to', 'and', 'rgds', 'care', 'yours', 'warmly', 'around', 'gratitude', 'b', 'you', 'very', 'warmest']

disclaimer_list = ['disclaimer', 'important', 'disseminate', 'contain', 'disclose', 'virus', 'liable', 'liability', 'confidential', 'privileged', 'email', 'mail', 'warning', 'content', 'message', 'notice', 'transmit', 'individual', 'entity', 'immediate', 'distribute', 'prohibit', 'damage', 'authori', 'conclude', 'organization', 'attorney', 'protect']


def column_namer(slef, prefix= '', val_list=[]):
    col_names =''
    for i in range(len(val_list)):
        if i == 0:
            col_names += str(prefix)+str(i)
        else:
            col_names += ','+str(prefix)+ str(i)
    return col_names

#---- Line_Index_ratio ------------------------------------------------------------------
def line_index_ratio(self, line_index, string_index={}):
    if string_index:
        temp_index=[]
        for os_i in string_index:
            temp_index.append(os_i)
        
        max_index = max(temp_index)
        index_ratio = line_index/max_index
        
        return index_ratio
#---------------------------------------------------------------------------------------- 

#---- Line_word_count -------------------------------------------------------------------
def line_word_count(self, string_line):
    words_list = string_line.split()
    words_count = len(words_list)
    return words_count
#----------------------------------------------------------------------------------------

#---- Line_str_len ----------------------------------------------------------------------
def line_str_len(self, string_line):
    str_length = len(string_line)
    return str_length
#----------------------------------------------------------------------------------------

#---- Title_Case ------------------------------------------------------------------------
def title_case(self, string_line):
    
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
def upper_case(self, string_line):
    if string_line.isupper():
        return 1
    else:
        return 0
#----------------------------------------------------------------------------------------

#---- Numeric_Count ---------------------------------------------------------------------
def numeric_count(self, string_line):
    ncount = 0
    for num_i in string_line:
        if num_i.isnumeric():
            ncount += 1
    return ncount
#----------------------------------------------------------------------------------------

#---- Numeric_ratio ---------------------------------------------------------------------
def numeric_ratio(self, numeric_count, line_str_len):
    nratio = 0
    if numeric_count != 0:
        nratio = numeric_count/line_str_len
    return nratio
#----------------------------------------------------------------------------------------

#---- email_count -----------------------------------------------------------------------
def email_count(self, string_line):
    email_pattern = re.compile( '([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)' )
    emailcount = 0
    for mail in email_pattern.finditer( string_line ):
        emailcount += 1
    return emailcount
#----------------------------------------------------------------------------------------

#---- email_ratio -----------------------------------------------------------------------
def email_ratio(self, email_count, line_word_count):
    emailratio = 0
    if email_count != 0:
        emailratio = email_count/line_word_count
    return emailratio
#----------------------------------------------------------------------------------------

#----- Line ngram count to a list--------------------------------------------------------
def ngramcount(self, string_line ='', nglist = []):
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

directory = 'label'

labeled_list = os.listdir(directory)

closure_cols = column_namer(0, 'C', closure_list)
disclaimer_cols = column_namer(0, 'D', disclaimer_list)


with open('debug_dataset.csv', 'w') as outfile:
    #outfile.write('')
    outfile.write('fname, line, class, v1, v2, v3, v4, v5, v6, v7, v8, v9,' + closure_cols + ',' + disclaimer_cols + '\n')


with open('dataset.csv', 'w') as outfile:
    #outfile.write('')
    outfile.write('class, v1, v2, v3, v4, v5, v6, v7, v8, v9,' + closure_cols + ',' + disclaimer_cols + '\n')


for labeled_f in labeled_list:
    #print(labeled_f)
    file_index = {}
    
    with open(directory + '\\' + labeled_f) as csvfile:
        readCSV = csv.reader(csvfile, delimiter='>')
        for row in readCSV:
            #print(row)
            file_index[int(row[1])] = [row[0], row[2], row[3]] # Index_no = File_name, label, String
            
    #print(file_index)
    
    for index in file_index:
        
        Y = file_index[index][1]
        
        v1 = line_index_ratio(0, index, file_index)
        
        v2 = line_word_count(0, file_index[index][2])
        
        v3 = line_str_len(0, file_index[index][2])
        
        v4 = title_case(0, file_index[index][2])
        
        v5 = upper_case(0, file_index[index][2])
        
        v6 = numeric_count(0, file_index[index][2])
        
        v7 = numeric_ratio(0, v6, v3)
        
        v8 = email_count(0, file_index[index][2])
        
        v9 = email_ratio(0, v8, v2)
        
        v10 = ngramcount(0, file_index[index][2], closure_list)
        
        v11 = ngramcount(0, file_index[index][2], disclaimer_list)
        
        #print(Y, str(v1)[:5], v2, v3, v4, v5, v6, v7, v8, v9, v10)
        
        full_arr = [ file_index[index][0] ] + [index] + [Y] + [v1] + [v2] + [v3] + [v4] + [v5] + [v6] + [v7] + [v8] + [v9] + v10 + v11
        
        #print(full_arr)
        
        
        if Y =='CC' and 1 not in v10:
            print (Y, file_index[index][0], index )
        
        if Y =='DD' and 1 not in v11:
            print (Y, file_index[index][0], index )
        
        
        csv_string = ''
        for item_i in range( len(full_arr) ):
            if item_i == 0:
                csv_string += str(full_arr[item_i])
            else:
                csv_string += ',' + str(full_arr[item_i])
        
        #print(csv_string)
        
        with open('debug_dataset.csv', 'a') as outfile:
            outfile.write(csv_string+'\n')
        
        
        
        dataset_arr =  [Y] + [v1] + [v2] + [v3] + [v4] + [v5] + [v6] + [v7] + [v8] + [v9] + v10 + v11
        
        dataset_string = ''
        
        for item_i in range( len(dataset_arr) ):
            if item_i == 0:
                dataset_string += str(dataset_arr[item_i])
            else:
                dataset_string += ',' + str(dataset_arr[item_i])
        
        
        with open('dataset.csv', 'a') as outfile:
            outfile.write(dataset_string+'\n')




