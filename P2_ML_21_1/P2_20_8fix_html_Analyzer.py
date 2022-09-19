#Analyzer - 19.4.2

import sys
import re
from ml_fextract import fextract
from ml_predict  import predict


class Analyzer:
    
    def __init__(self, *argv, **kwargs):
        
        self.file_name = argv[0]
        
        self.selfclose_tags = ['area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr']
        
        self.chars_list = [',', '.', '&amp;', '&#38;', '&nbsp;', '&#160;' , '!',]
        self.stopw_list = ['and', 'all', 'the', 'b']
        
        self.cword_list = ['thank', 'thanks', 'thanking', 'regard', 'regards', 'sincere', 'sincerely', 'gratitude', 'gratitudes', 'cheers', 'appreciation', 'you', 'your', 'yours', 'kind', 'best', 'many' , 'with', 'again' , 'fond', 'b' ]
        
        self.disclaimer_intercept_list = ['IMPORTANT', 'legal','construe', 'solicit', 'warrant', 'disseminate', 'contain','disclose', 'virus', 'liable' ,'liability', 'private', 'confidential', 'privilege', 'mail', 'warning', 'proprietary']
        self.disclaimer_startword_list = ['important', 'notice', 'warning']
        self.shortwords_list = ['Hi', 'Pfa', 'Fyi', 'Asap', 'Aka' ]
    
    
    def file_reader(self, file):
        with open(file, 'r') as f:
            return f.read() #list of sentences
    
    
    def drop_char(self, str_line='' , char_list=[] ):
        string = str(str_line)
        for ci in char_list:
            string = string.replace( ci, ' ')
        return string
    
    
    def drop_words(self, wstr_line='' , word_list=[]):
        wstring = str(wstr_line)
        wstring = wstring.lower()
        wstring_list = wstring.split()
        for wrd in word_list:
            for wi in range( wstring_list.count(wrd) ):
                wstring_list.remove(wrd)
        dwstring = ' '.join(wstring_list)
        return dwstring
    
    
    def word_count(self, str_line = '', min=1, max= 4):
        '''Returns True/False, if specified string of words are in specified min/max parameters.
        min: Minimum word length(default : 1), max: Maximum word length(default : 4)'''
        
        str_line  = str_line.strip()   # Removing spaces from Begining/End of string
        list_line = str_line.split()   # Splitting string to list of words
        
        if len(list_line) >= min and len(list_line) <= max:   #Filter by number of words
            return True
        else:
            return False
    
    
    def word_ount_index(self, string_index = {}, min= 1, max= 4 ):
        #----- Filter words by Count ----------------------------------------------------
        wCount_index = {}
        for Si in string_index:
            line = string_index[Si]
            
            if self.word_count(line, min= 1, max= 4) == True:
                wCount_index[Si] = line
        
        return wCount_index
    
    
    def alpha_index(self, w_index = {}):
        #----- Filter words by Alpha ----------------------------------------------------
        wAlpha_index = {}
        for Ci in w_index:
            merged_str = w_index[Ci].replace(' ', '')
            
            if merged_str.isalpha() == True:
                wAlpha_index[Ci] = w_index[Ci]
        
        return wAlpha_index
    
    
    def clean_unicode_chars(self, string_line=''):
        #--- Cleaning Unicode Chars -----------------------------------------------------
        uni_chars = re.compile('&#[0-9]+;')
        for unichar in uni_chars.finditer(string_line):
            string_line = string_line.replace( unichar[0], ' ' )
       
        #--- Cleaning Unicode String ----------------------------------------------------
        uni_str = re.compile('&[a-z]+;')
        for unistr in uni_str.finditer(string_line):
            string_line = string_line.replace( unistr[0], ' ' )
       
        return string_line
    
    
    
    def mailborder(self, pre_body_list=[]):
        border_index = None
        from_taglist=[]
        sent_taglist=[]
        to_taglist=[]
        
        for indx in range( len(pre_body_list) ):
            pbline = pre_body_list[indx].split()
            if pbline and pbline[0] == 'From:':
                from_taglist.append(indx)
            
            if pbline and pbline[0] == 'Sent:':
                sent_taglist.append(indx)
            
            if pbline and pbline[0] == 'To:':
                to_taglist.append(indx)
        
        if from_taglist and sent_taglist and to_taglist:
            from_tag = min(from_taglist)
            sent_tag = min(sent_taglist)
            to_tag   = min(to_taglist)
        
            if (from_tag/sent_tag) > 0.8 and (sent_tag/to_tag) > 0.8 :
                border_index = from_tag
        
        return border_index
    
    
    def tag_closer(self, mail_close_index = None, body_list = []):
        ''' Tag closer  '''
        top_new_bottom = ''
        top_open_tags_list = []
        top_strings_list = []
        start_tag = False
        close_tag = False
        sc_tag = False
        
        body_top = body_list[ : mail_close_index ]
        
        count=0
        for index in range( len(body_top)-1, 0, -1 ):
            
            start_tag = re.compile('<[^/].*?>').search(body_top[index])
            close_tag = re.compile('</.*?>').search(body_top[index])
            
            if start_tag:
                sc_tag = re.search("[a-zA-Z]+", re.compile('<[^/].*?>').search(body_top[index])[0] )[0]
            
            if start_tag  and  sc_tag not in self.selfclose_tags:
                count -= 1
            
            elif close_tag:
                count += 1
            
            elif body_top[index] != ''  and  sc_tag not in self.selfclose_tags:
                top_strings_list.append(index)
            
            if count == -1:
                top_open_tags_list.append(index)
                top_new_bottom += '</' + re.search("[a-zA-Z]+", body_top[index] )[0] + '>'
                count=0
        
        return mail_close_index, top_new_bottom
    
    
    def execute(self):
        page = self.file_reader(self.file_name)
        page = re.compile(r'[\t]').sub(' ', page)
        page = re.compile(r'[\n\r]').sub('', page)
        page = str(page)
        
        bs_tag = re.compile('<body.*?>').search(page)
        be_tag = re.compile('</body>').search(page)
        
        if bs_tag != None:
            body = page[ bs_tag.end() : be_tag.start() ]
            
            page_TOP = page[ :bs_tag.end() ]
            page_BOTTOM = page[ be_tag.start(): ]
        else:
            body = page
            page_TOP, page_BOTTOM = '', ''
        #--------------------------------------------------------------------------------       
        
        
        #----- Body content to a list----------------------------------------------------
        html_tag = re.compile('<.*?>')
        
        pre_body_list =[]
        pre=0
        for i in html_tag.finditer(body):
            s,e = i.start(), i.end()
            if s == 0 or pre == s:
                pre_body_list.append(body[s:e])
            else:
                pre_body_list.append(body[pre:s])
                pre_body_list.append(body[s:e])
            pre=i.end()
        
        #--------------------------------------------------------------------------------
        
        #----- If no tags ---------------------------------------------------------------
        if not pre_body_list:
            pre_body_list.append(body)
        
        #----- Validating Mail Border ----------------------------------------------
        border_index = self.mailborder(pre_body_list)
        #----------------------------------------------------------------------------
        
        #-----  Mail Border-line identifier ---------------------------------------------
        
        border_index_list = []
        
        pattern1 = re.compile('<div[ ]+style=.*?\Wborder\W.*?>')
        pattern2 = re.compile('<hr.*?>')
        
        for pbi in range( len(pre_body_list) ):
            if re.search( pattern1, pre_body_list[pbi] ):
                border_index_list.append(pbi)
            
            if re.search( pattern2, pre_body_list[pbi] ):
                border_index_list.append(pbi)
            
        #--------------------------------------------------------------------------------
        
        if border_index  and border_index_list:
            for bil_i in border_index_list:
                if 0.8 <= (bil_i/border_index) < 1:
                    border_index = bil_i
        
        Ori_body_list = pre_body_list[:border_index]  # Preserving original format
        body_list = pre_body_list[:border_index]
        
        pre_body_list = None #Flushing pre_body_list
        
        
        #----- Removing White spaces ----------------------------------------------------
        for list_i in range( len(body_list) ):
            body_list[list_i] = body_list[list_i].strip()  # Striped
        #--------------------------------------------------------------------------------
        
        #----- Identify Strings by ignoring '<tag>' -------------------------------------
        html_tag = re.compile('<.*?>')
        String_index = {}
        Ori_String_index = {}
        String_index_list = []
        
        for si in range( len(body_list) ):
            if not re.search(html_tag, body_list[si]) and body_list[si] != '':
                String_index[si] = body_list[si].strip()
                Ori_String_index[si] = body_list[si].strip()
                String_index_list.append(si)
        #--------------------------------------------------------------------------------
        
        #----- Drop Chars/Words ---------------------------------------------------------------
        for i in String_index:
            str_line = String_index[i]
            
            new_str_line = self.clean_unicode_chars(str_line)
            new_str_line = self.drop_char( new_str_line , char_list = self.chars_list  )
            new_str_line = self.drop_words( new_str_line, word_list = self.stopw_list )
            
            String_index[i] = new_str_line
        #--------------------------------------------------------------------------------
        
        mail_close_index = None
        top_new_bottom = ''
        
        ###----- Greet closure ----------------------------------------------------------
        close_index = self.word_ount_index( String_index , min= 1, max= 4)  #For Greet ending
        cAlpha_index = self.alpha_index(close_index)
        
        close_match_list=[]
        
        for cw_key in cAlpha_index:
            
            cw_list = cAlpha_index[cw_key].lower().split()
            
            c_count = 0
            for cw in cw_list:
                if cw in self.cword_list:
                    c_count += 1
            
            if c_count == len(cw_list):
                close_match_list.append(cw_key)
        
        
        if close_match_list:
            cgreet_index = max(close_match_list)
            mail_close_index = cgreet_index            #Final Mail-Closing Index
            
        
        #---- Closing (Mail-close greet) open tags ---------------------------------------
        if mail_close_index:
            cnew_tag_close = self.tag_closer( mail_close_index, Ori_body_list )
            
            mail_close_index = cnew_tag_close[0]
            top_new_bottom   = cnew_tag_close[1]
        #--------------------------------------------------------------------------------
        
        
        #----- Signature Contennt Removal -----------------------------------------------
        title_index = None
        email_index = None
        phone_index = None
        MailPhone_list =[]
        
        email_pattern = re.compile( '([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)' )
        Lastname_pattern = re.compile( '^[A-Z][a-z][A-Z]{0,1}[a-z]+$' )
        
        if not mail_close_index:
            
            for bl_i in String_index_list[::-1]:
                
                bstring_line = Ori_String_index[bl_i]
                
                #--- Cleaning Unicode Chars --------------------------------------------------------------------------
                uni_chars = re.compile('#[0-9]+;')
                if uni_chars.search(Ori_String_index[bl_i]):
                    bstring_line = Ori_String_index[bl_i].replace( uni_chars.search(Ori_String_index[bl_i])[0], ' ' )
                #-----------------------------------------------------------------------------------------------------
                
                st_line_list = bstring_line.split()
                st_line_len  = len( st_line_list )
                
                #--- validating for 'Single letter' string -----------------------------------
                bsrt_line = bstring_line
                single_char = False
                if st_line_len == 1:
                    for syn_i in ['.', ',', ':', ';', '!']:
                        bsrt_line = bsrt_line.replace(syn_i, '' )
                    if len( bsrt_line.split()[0] ) < 2: # If string, set single_char = True
                        single_char = True
                #------------------------------------------------------------------------------
                
                if 0 < st_line_len < 6  and  not single_char:
                    
                    #--- Validating e-mail --------------------
                    if email_pattern.search( bstring_line ):
                        email_index = bl_i
                    #------------------------------------------
                    
                    #--- Validating Phone -----------------
                    tphone =''
                    for num_i in bstring_line:
                        if num_i.isnumeric():
                            tphone += num_i
                    
                    if tphone and  8 <= len(tphone) <= 11 :
                        phone_index = bl_i
                    #--------------------------------------
                    
                    #--- Validating Name --------------------------------------------------------------------
                    bstring_line = bstring_line.strip().replace('.', ' ')
                    bstring_line = bstring_line.strip().replace(',', '')
                    
                    nst_line_list = bstring_line.split()
                    fnames_correct = ''
                    lname_correct = ''
                    
                    if bstring_line:
                        if 1 < len(nst_line_list):
                            fnames_correct = ' '.join( nst_line_list[:-1] ).istitle()
                            lname_correct  = Lastname_pattern.match(nst_line_list[-1:][0])
                            
                        elif len(nst_line_list) == 1  and  nst_line_list[0] not in self.shortwords_list :
                            fnames_correct = nst_line_list[0].istitle()
                            lname_correct = True
                    
                    if fnames_correct  and  lname_correct:
                        title_index = bl_i
                        break
                    #----------------------------------------------------------------------------------------
            
            #----- Updating MailPhone_list if mai/phone found -----------
            if email_index or phone_index:
                if email_index:
                    MailPhone_list.append(email_index)
                if phone_index:
                    MailPhone_list.append(phone_index)
            #------------------------------------------------------------
            
            if title_index  and  MailPhone_list and  title_index < min(MailPhone_list):
                mail_close_index = min(MailPhone_list)
            
            #----- Closing (Signature) open tags --------------------------------------------
            if mail_close_index:
                snew_tag_close = self.tag_closer( mail_close_index, Ori_body_list )
                
                mail_close_index = snew_tag_close[0]
                top_new_bottom   = snew_tag_close[1]
        #------------------------------------------------------------------------------------
        
        
        #----- Disclaimer identifier---------------------------------------------------------
        if not mail_close_index :
            
            disclaimer_found = False
            disclaimer_list = []
            predicted_disclaimer_list = []
            
            #found_dword_count = 0
            #intercept_prob = 0
            #sword_prob = 0
            
            for disc_i in String_index:
                if self.word_count(String_index[disc_i], min= 50, max= 400):
                    disclaimer_list.append(disc_i)
            
            if disclaimer_list:
                for dl_i in disclaimer_list:
                    line_feature_list = fextract(dl_i, String_index)
                    predicted = predict([line_feature_list])[0]
                    
                    if predicted == 'DD':
                        predicted_disclaimer_list.append(dl_i)
            
            if predicted_disclaimer_list:
                disclaimer_found = True
                mail_close_index = min(predicted_disclaimer_list)
                
                
                ##-- Validating probability - intercepting key word ------
                #for d_word in self.disclaimer_intercept_list:
                    #if d_word in Ori_body_list[ max(disclaimer_list) ]:
                        #found_dword_count += 1
                
                #intercept_prob =  (found_dword_count/len(self.disclaimer_intercept_list) ) * 100
                
                
                ##-- Validating probability - Starting key word ----------
                #disclaimer_string = body_list[ max(disclaimer_list) ]
                #disclaimer_start_string = disclaimer_string.split()[0]  #First word of the string
                
                #for d_sword in self.disclaimer_startword_list:
                    #if  d_sword in disclaimer_start_string.lower():# If disclaimer startword found increase the proberbility.
                        #sword_prob = 2.0
                
                
                #if found_dword_count > 0 and  intercept_prob + sword_prob >= 0.2 :
                    
                    #Ori_body_list[max(disclaimer_list)] = ''    # Cleaning disclaimer string from (Ori_body_list)
                    
                    #disclaimer_found = True
                    #mail_close_index = max(disclaimer_list)
                    
            #----- Closing (Disclaimer) open tags --------------------------------------------
            if disclaimer_found:
                
                if mail_close_index:
                    dnew_tag_close = self.tag_closer( mail_close_index, Ori_body_list )
                    
                    mail_close_index = dnew_tag_close[0]
                    top_new_bottom   = dnew_tag_close[1]
        #------------------------------------------------------------------------------------
        
        
        #--------------------------------------------------------------------------------
        body_top = ''
        for bt_item in Ori_body_list[:mail_close_index] :
            body_top += bt_item
        #--------------------------------------------------------------------------------
        
        
        body_FIlTERED = body_top + top_new_bottom
        
        Page_FIlTERED = page_TOP + body_FIlTERED + page_BOTTOM      ### Filtered FINAL HTML STRING
        
        #return Page_FIlTERED
        ######------------------------------------------------
        out_file = self.file_name.split('\\')[-1] 
        outfile_path = '' 
        if len( self.file_name.split('\\') ) > 1 : 
            for i in self.file_name.split('\\')[:-1]: 
                outfile_path += i + '\\' 
        
        with open(outfile_path + 'FILTERED_' + out_file, 'w') as fw: 
            fw.write(Page_FIlTERED) 
        
        print('\nFiltered file : ' +outfile_path + 'FILTERED_' + out_file)
    
    
if __name__ == "__main__":
   
    ##file = 'htf.html'
    file = sys.argv[1] 
   
    A = Analyzer(file) 
    A.execute() 