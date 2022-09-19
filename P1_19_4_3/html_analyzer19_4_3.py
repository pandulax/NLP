#Analyzer - 19.4.2
import sys
import re
#from bs4 import BeautifulSoup

#import nltk
#pos_tag = nltk.pos_tag
#WNL = nltk.stem.WordNetLemmatizer()
#lemt = WNL.lemmatize

class Analyzer:
    
    def __init__(self, *argv, **kwargs):
        
        self.file_name = argv[0]
        
        self.selfclose_tags = ['area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr']
        
        self.chars_list = [',', '.', '&amp;', '&#38;', '!', '&nbsp;', '&#169;', '&copy;', '&#174;', '&reg;', '&#8471;', '&#8482;', '&trade;', '&#8480;', '&#160;', '&bull;', '&#8219;', '&quot;', '&#34;', '&lsquo;', '&#8216;', '&rsquo;', '&#8217;', '&ldquo;', '&#8220;', '&rdquo;', '&#8221;', '&#09;', '&#10;', '&#13;', '&#8226;', '&deg;', '&#176;', '&infin;', '&#8734;', '&#36;' , '&#8364;' , '&euro;' , '&#163;' , '&pound;' , '&#165;' , '&yen;' , '&#162;' , '&cent;' , '&#8377;', '&#9702;', '&#8729;', '&#8227;' , '&#8259;', '&#43;', '&#150;', '&#151;']
        
        self.stopw_list = ['and', 'all', 'the', 'b']
        self.cword_list = ['thank', 'thanks', 'thanking', 'regard', 'regards', 'sincere', 'sincerely', 'gratitude', 'gratitudes', 'cheers', 'appreciation', 'you', 'your', 'yours', 'kind', 'best', 'many' , 'with', 'again' , 'fond' ]
        
        self.disclaimer_intercept_list = ['disseminate', 'contain', 'disclose', 'virus', 'liable', 'liability', 'confidential', 'privileged', 'mail', 'warning', 'content', 'message', 'notice', 'transmit', 'individual', 'entity', 'immediate', 'distribute', 'prohibit', 'damage', 'authori', 'conclude', 'organization', 'attorney', 'protect']
        self.disclaimer_startword_list = ['important', 'notice', 'warning']
        self.shortwords_list = ['Hi', 'Pfa', 'Fyi', 'Asap', 'Aka' , 'Dear']
        
        self.stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
        
    def file_reader(self, file):
        with open(file, 'r') as f:
            return f.read() #list of sentences
    
    
    def drop_char(self, str_line='' , char_list=[] ):
        string = str(str_line)
        for ci in char_list:
            string = string.replace( ci, '')
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
        uni_chars = re.compile('&#[0-9]+?;')
        if uni_chars.search(string_line):
            string_line = string_line.replace( uni_chars.search(string_line)[0], ' ' )
        
        #--- Cleaning Unicode String ----------------------------------------------------
        uni_str = re.compile('&[a-z]+;')
        if uni_str.search(string_line):
            string_line = string_line.replace( uni_str.search(string_line)[0], ' ' )
        
        return string_line
    
    
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
                #sc_tag = re.compile('<[^/].*?>').search(body_top[index])[0].replace('>', '').replace('<', '').split()[0]
                sc_tag = re.search("[a-zA-Z]+", re.compile('<[^/].*?>').search(body_top[index])[0] )[0]
            
            if start_tag  and  sc_tag not in self.selfclose_tags:
                count -= 1
                #print(index, body_top[index])
            
            elif close_tag:
                count += 1
                #print(index, body_top[index])
            
            elif body_top[index] != ''  and  sc_tag not in self.selfclose_tags:
                top_strings_list.append(index)
                #print(index, 'String - ', body_top[index])
            
            if count == -1:
                top_open_tags_list.append(index)
                #top_new_bottom += body_top[index].replace('>','').replace('<', '</').split()[0] + '>'
                top_new_bottom += '</' + re.search("[a-zA-Z]+", body_top[index] )[0] + '>'
                count=0
                #print(index, '>>>> ', body_top[index])
        
        #print('Before - ', mail_close_index)
        
        #if top_open_tags_list  and  top_strings_list  and  min(top_open_tags_list)  >  max(top_strings_list):
            #mail_close_index = min(top_open_tags_list)
            #top_new_bottom = ''
        
        #print('After - ', mail_close_index)
        #print('top_new_bottom : ', top_new_bottom)
        
        return mail_close_index, top_new_bottom
    
    
    
    def execute(self):
        page = self.file_reader(self.file_name)
        #print(page)
        page = re.compile(r'[\t]').sub(' ', page)
        page = re.compile(r'[\n\r]').sub('', page)
        page = str(page)
        
        
        #----- HTML <body> </body> tag identifier ---------------------------------------
        #body_start = re.compile('<body.*?>')
        #body_end   = re.compile('</body>')
        
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
        
        #-----  Mail Border-line identifier ---------------------------------------------
        border_index = None
        #pat_index_list = []
        #pat1_index, pat2_index = None, None
        
        pattern1 = re.compile('<div[ ]+style=.*?\Wborder\W.*?>')
        pattern2 = re.compile('<hr.*?>')
        
        for pbi in range( len(pre_body_list) ):
            if re.search( pattern1, pre_body_list[pbi] ):
                border_index = pbi
                break
            
            if re.search( pattern2, pre_body_list[pbi] ):
                border_index = pbi
                break
        
        #----- Validating border Indices -------------------
        #if pat_index_list:
            #border_index = min(pat_index_list)
        
        #--------------------------------------------------------------------------------
        
        Ori_body_list = pre_body_list[:border_index]  # Preserving original format
        body_list = pre_body_list[:border_index]
        
        pre_body_list = None #Flushing pre_body_list
        
        
        #----- Removing White spaces ----------------------------------------------------
        for list_i in range( len(body_list) ):
            body_list[list_i] = body_list[list_i].strip()  # Striped
        
        #print(body_list)
        #--------------------------------------------------------------------------------
        
        #----- Filtering Strings by '<' -------------------------------------------------
        #String_index = {}
        #for si in range( len(body_list) ):
            #if body_list[si][0] != "<":
                #String_index[si] = body_list[si]
                #print(si, body_list[si])
        #--------------------------------------------------------------------------------
        
        #----- Identify Strings by ignoring '<tag>' -------------------------------------
        html_tag = re.compile('<.*?>')
        String_index = {}
        Ori_String_index = {}
        String_index_list = []
        
        for si in range( len(body_list) ):
            if not re.search(html_tag, body_list[si]) and body_list[si] != '':
                #--Removing white spaces, and appendung to a dictionary
                String_index[si] = body_list[si].strip()
                Ori_String_index[si] = body_list[si].strip()
                String_index_list.append(si)
                #print(si, body_list[si])
        #--------------------------------------------------------------------------------
        
        #----- Drop Chars/Words ---------------------------------------------------------------
        for i in String_index:
            str_line = String_index[i]
            
            new_str_line = self.drop_char( str_line , char_list = self.chars_list  )
            new_str_line = self.drop_words( new_str_line, word_list = self.stopw_list )
            
            String_index[i] = new_str_line
        
        #[print (i, String_index[i]) for i in String_index]
        #--------------------------------------------------------------------------------
        
        mail_close_index = None
        top_new_bottom = ''
        
        ###----- Greet closure ----------------------------------------------------------
        close_index = self.word_ount_index( String_index , min= 1, max= 4)  #For Greet ending
        cAlpha_index = self.alpha_index(close_index)
        
        #[print (i, cAlpha_index[i]) for i in cAlpha_index]
        
        
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
            #print(cgreet_index, Ori_body_list[cgreet_index]) ##
        
        #print(mail_close_index) #Mail close index.
        
        #---- Closing (Mail-close greet) open tags ---------------------------------------
        if mail_close_index:
            cnew_tag_close = self.tag_closer( mail_close_index, Ori_body_list )
            
            mail_close_index = cnew_tag_close[0]
            top_new_bottom   = cnew_tag_close[1]
        #--------------------------------------------------------------------------------
        
        
        #----- Signature Contennt Removal -----------------------------------------------
        sig_string_index = {}
        
        line_gap_ratio = 0.78
        sig_guess=False
        sig_guess_list = []
        title_index = None
        email_index = None
        phone_index = None
        signature = False
        MailPhone_list =[]
        title_index_list = []
        sig_valid_string_list = []
        
        email_pattern = re.compile( '([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)' )
        Lastname_pattern = re.compile( '^[A-Z][a-z][A-Z]{0,1}[a-z]+$' )
        #name_pattern = re.compile( '(?:[A-Z][a-z]*\s?)+' )
        
        if not mail_close_index:
            
            for bl_i in String_index_list[::-1]:
                
                bstring_line = Ori_String_index[bl_i]
                
                #--- Cleaning Unicode Chars -------------------------
                bstring_line = self.clean_unicode_chars(bstring_line)
                
                sig_string_index[bl_i] = bstring_line.strip()
                
                ##--- Cleaning Unicode Chars --------------------------------------------------------------------------
                #uni_chars = re.compile('&#[0-9]+?;')
                #if uni_chars.search(bstring_line):
                #    bstring_line = bstring_line.replace( uni_chars.search(bstring_line)[0], ' ' )
                ##-----------------------------------------------------------------------------------------------------
                #
                ##--- Cleaning Unicode String -------------------------------------------------------------------------
                #uni_str = re.compile('&[a-z]+;')
                #if uni_str.search(bstring_line):
                #    bstring_line = bstring_line.replace( uni_str.search(bstring_line)[0], ' ' )
                ##-----------------------------------------------------------------------------------------------------
                
                st_line_list = bstring_line.split()
                st_line_len  = len( st_line_list )
                
                ##--- validating for 'Single letter' string -----------------------------------
                #bsrt_line = bstring_line.strip()
                #single_char = False
                #if bsrt_line != '':
                    #for syn_i in ['.', ',', '|']:
                        #bsrt_line = bsrt_line.replace(syn_i, '' )
                    #if len( bsrt_line.split()[0] ) < 2 : # If string, set single_char = True
                        #single_char = True
                ##------------------------------------------------------------------------------
                
                if 0 < st_line_len < 6 : #and  not single_char:
                    
                    #--- Validating e-mail --------------------
                    if email_pattern.search( bstring_line ):
                        email_index = bl_i
                        print('e-mail : ', bstring_line)
                        #continue
                    #------------------------------------------
                    
                    #--- Validating Phone -----------------
                    tphone =''
                    for num_i in bstring_line:
                        if num_i.isnumeric():
                            tphone += num_i
                    
                    if tphone and  8 <= len(tphone) <= 11 :
                        phone_index = bl_i
                        print('Phone : ', bstring_line)
                        #continue
                    #--------------------------------------
                    
                    #--- Validating Name --------------------------------------------------------------------
                    bstring_line = bstring_line.strip().replace('.', ' ')
                    bstring_line = bstring_line.strip().replace(',', '')
                    
                    nst_line_list = bstring_line.split()
                    fnames_correct = ''
                    lname_correct = ''
                    
                    for nst in nst_line_list:
                        if not nst.isalpha():
                            nst_line_list = ''
                    
                    if bstring_line:
                        if 1 < len(nst_line_list) and nst_line_list[0] not in self.shortwords_list:
                            fnames_correct = ' '.join( nst_line_list[:-1] ).istitle()
                            lname_correct  = Lastname_pattern.match(nst_line_list[-1:][0])
                        
                        elif len(nst_line_list) == 1  and  nst_line_list[0] not in self.shortwords_list :
                            fnames_correct = nst_line_list[0].istitle()
                            lname_correct = True
                        
                    if fnames_correct  and  lname_correct:
                        #title_index = bl_i
                        title_index_list.append(bl_i)
                        print('Name : ', bstring_line)
                        break
                    #----------------------------------------------------------------------------------------
            
            #----- Updating MailPhone_list if mai/phone found -----------
            if email_index or phone_index:
                if email_index:
                    MailPhone_list.append(email_index)
                if phone_index:
                    MailPhone_list.append(phone_index)
            #------------------------------------------------------------
            
            if title_index_list:
                title_index = max(title_index_list)
                #----- Finding most-valid title_index -----------------------------
                #for tti in range(len(title_index_list)):
                #    if tti+1 < len(title_index_list):
                #        if title_index_list[tti+1]/title_index_list[tti] >= 0.72:
                #            title_index = title_index_list[tti+1]
                #------------------------------------------------------------------
            
            for ss_i in sig_string_index:
                if sig_string_index[ss_i] != '':
                    sig_valid_string_list.append(ss_i)
            
            
            if sig_valid_string_list:
                for vstr_i in range(len(sig_valid_string_list)):
                    if vstr_i+1 < len(sig_valid_string_list):
                        if sig_valid_string_list[vstr_i+1]/sig_valid_string_list[vstr_i] >= line_gap_ratio:
                            sig_guess = True
                            sig_guess_list.append(sig_valid_string_list[vstr_i+1])
                        elif sig_valid_string_list[vstr_i+1]/sig_valid_string_list[vstr_i] < line_gap_ratio  and  sig_guess == True:
                            break
            
            #if max(top_sig_string)/title_index  <  0.72:
                #signature = True
            if MailPhone_list and sig_guess_list and title_index:
                if ( max(MailPhone_list) in sig_guess_list) and ( title_index in sig_guess_list) and title_index < min(MailPhone_list):
                    mail_close_index = min(sig_guess_list)
                    
                else:
                    mail_close_index = min(MailPhone_list)
            #if signature and title_index  and  MailPhone_list and  title_index < max(MailPhone_list):
                #mail_close_index = min(MailPhone_list)
            
            #elif not title_index  and  MailPhone_list:
                #mail_close_index = max(MailPhone_list)
            
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
            found_dword_count = 0
            intercept_prob = 0
            sword_prob = 0
            
            for disc_i in String_index:
                if self.word_count(String_index[disc_i], min= 55, max= 400):
                    disclaimer_list.append(disc_i)
                    #print(String_index[disc_i])
            
            if disclaimer_list:
                #print( 'Disclaimer: ' + str( max(disclaimer_list) ) )
                
                #-- Validating probability - intercepting key word ------
                for d_word in self.disclaimer_intercept_list:
                    if d_word in Ori_body_list[ max(disclaimer_list) ].lower():
                        found_dword_count += 1
                
                intercept_prob =  (found_dword_count/len(self.disclaimer_intercept_list) ) * 100
                
                
                #-- Validating probability - Starting key word ----------
                disclaimer_string = body_list[ max(disclaimer_list) ]
                #disclaimer_string = disclaimer_string.strip() #Removing white spaces
                disclaimer_start_string = disclaimer_string.split()[0]  #First word of the string
                
                for d_sword in self.disclaimer_startword_list:
                    if  d_sword in disclaimer_start_string.lower():# If disclaimer startword found increase the proberbility.
                        sword_prob = 2.0
                
                
                if found_dword_count > 0 and  intercept_prob + sword_prob >= 0.13 :
                    
                    Ori_body_list[max(disclaimer_list)] = ''    # Cleaning disclaimer string from (Ori_body_list)
                    
                    disclaimer_found = True
                    mail_close_index = max(disclaimer_list)
                    
            #----- Closing (Disclaimer) open tags --------------------------------------------
            if disclaimer_found:
                
                if mail_close_index:
                    dnew_tag_close = self.tag_closer( mail_close_index, Ori_body_list )
                    
                    mail_close_index = dnew_tag_close[0]
                    top_new_bottom   = dnew_tag_close[1]
        #------------------------------------------------------------------------------------
        
        
        #print (mail_close_index)
        #print (body_list)
        
        #print(body_list[:mail_close_index])
        
        
        #--------------------------------------------------------------------------------
        
        #[ print (i) for i in Ori_body_list[:mail_close_index] ]
        body_top = ''
        for bt_item in Ori_body_list[:mail_close_index] :
            body_top += bt_item
        #--------------------------------------------------------------------------------
        
        
        #print(top_new_bottom)
        
        ##html_close_tag = re.compile('<[^/].*?>')
        
        body_FIlTERED = body_top + top_new_bottom
        
        Page_FIlTERED = page_TOP + body_FIlTERED + page_BOTTOM      ### Filtered FINAL HTML STRING
        
        #return Page_FIlTERED
        
        #print('--------page_TOP\n', page_TOP)
        #print('--------page_BOTTOM\n', page_BOTTOM)
        
        #print(Page_FIlTERED)  #######
        
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



##############----- Name closure ------------------------------------------------------------------
#            
#            cname_index = self.word_ount_index( String_index , min= 1, max= 7)  #for Name ending
#            nAlpha_index = self.alpha_index(cname_index)
#            #[print (i, nAlpha_index[i]) for i in nAlpha_index]
#            
#            name_match_list=[]
#            
#            for nw_key in nAlpha_index:
#                
#                nw_list = nltk.pos_tag( nAlpha_index[nw_key].split() )
#                
#                n_count = 0
#                for nw in nw_list:
#                    if nw[1] == 'NNP':
#                        n_count += 1
#                
#                if n_count == len(nw_list):
#                    name_match_list.append(nw_key)
#            
#            if name_match_list:
#                name_index = max(name_match_list)
#                mail_close_index = name_index
#                print('Name index', name_index, Ori_body_list[name_index])  ##
#            else:
#                #print('Name index: ' + mail_close_index)
#                pass
#
#############-------------------------------------------------------------------------------
#
#########print(Ori_body_list[mail_close_index])
#
#
##----- Cleaning body_new_bottom-------------------
#html_tag = re.compile('<.*?>')
#div_sp = re.compile('<div.*?>')
#div_ep = re.compile('</div>')

##body_new_bottom list concatenate
#for ob_str in Ori_body_list[mail_close_index: ] :          # Ori_body_list 
#    if re.search(html_tag, ob_str):                        # if ob_str[0] ==  '<':
#        body_new_bottom += ob_str
#        #print(tmpstr[found.start() : found.end()])
#        
#div_s = re.search(div_sp, body_new_bottom)
#div_e = re.search(div_ep, body_new_bottom)

#if div_e.end() <= div_s.start():
#    body_new_bottom = body_new_bottom[ :div_e.end() ]
##-----------------------------------------------------
#
#
#----- Mail Border-line identifier-----------------------------------------------
#border_t1 = re.compile("<div[ ]+style='border.*?>")
#border_t2 = re.compile('<div[ ]+style="border.*?>')
#border_t3 = re.compile('<hr.*?border-style.*?>')
#
#btype_1 = re.search(border_t1, body)
#btype_2 = re.search(border_t2, body)
#btype_3 = re.search(border_t3, body)
#
#if btype_1 != None:
#    body = body[:btype_1.start()]
#    print ('t1', btype_1.start())
#
#elif btype_2 != None:
#    body = body[:btype_2.start()]
#    print ('t2', btype_2.start())
#
#elif btype_3 != None:
#    body = body[:btype_3.start()]
#    print ('t3', btype_3.start())
#
#print(body)
#--------------------------------------------------------------------------------
#
#
#----- Prettify body-------------------------------------------------------------
#BSoup = BeautifulSoup(body, features='lxml').encode_contents(formatter='html')
#prettify_body = BeautifulSoup(body, features='lxml').prettify(formatter="html") #BeautifulSoup(body, features='lxml')
#print(prettify_body)
#
#prettify_list = prettify_body.splitlines()    #Converting to list
#list = prettify_list
#--------------------------------------------------------------------------------
#
#
##-------------------------------------------------------------------------------
#top_new_bottom = ''
#top_open_tags_list = []
#top_strings_list = []
#start_tag = False
#close_tag = False
#sc_tag = False
#
#if mail_close_index:
#    body_top = body_list[ : mail_close_index ]
#    
#    count=0
#    for index in range( len(body_top)-1, 0, -1 ):
#        
#        start_tag = re.compile('<[^/].*?>').search(body_top[index])
#        close_tag = re.compile('</.*?>').search(body_top[index])
#        
#        if start_tag:
#            #sc_tag = re.compile('<[^/].*?>').search(body_top[index])[0].replace('>', '').replace('<', '').split()[0]
#            sc_tag = re.search("[a-zA-Z]+", re.compile('<[^/].*?>').search(body_top[index])[0] )[0]
#        
#        if start_tag  and  sc_tag not in self.selfclose_tags:
#            count -= 1
#            print(index, body_top[index])
#        
#        elif close_tag:
#            count += 1
#            print(index, body_top[index])
#        
#        elif body_top[index] != ''  and  sc_tag not in self.selfclose_tags:
#            top_strings_list.append(index)
#            print(index, 'String - ', body_top[index])
#        
#        if count == -1:
#            top_open_tags_list.append(index)
#            #top_new_bottom += body_top[index].replace('>','').replace('<', '</').split()[0] + '>'
#            top_new_bottom += '</' + re.search("[a-zA-Z]+", body_top[index] )[0] + '>'
#            count=0
#            print(index, '>>>> ', body_top[index])
#    
#    
#    print('Before - ', mail_close_index)
#    
#    if top_open_tags_list  and  top_strings_list  and  min(top_open_tags_list)  >  max(top_strings_list):
#        mail_close_index = min(top_open_tags_list)
#        top_new_bottom = ''
#    
#    print('After - ', mail_close_index)
##-------------------------------------------------------------------------------
