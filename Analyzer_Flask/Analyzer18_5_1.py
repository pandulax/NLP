#Analyzer - 18.5.1
import sys
import re


class Analyzer:
    
    def __init__(self, *argv, **kwargs):
        
        self.selfclose_tags = ['area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr']
        
        self.chars_list = [',', '.', '&amp;', '&#38;', '!', '&nbsp;', '&#160;']
        self.cword_list = ['thank', 'thanks', 'thanking', 'b','regard', 'regards', 'sincere', 'sincerely', 'gratitude', 'gratitudes', 'cheers', 'appreciation', 'you', 'your', 'yours', 'kind', 'best', 'many' , 'and', 'with', 'again' , 'fond ', 'all', 'the']
        
        self.disclaimer_intercept_list = ['IMPORTANT', 'legal','construe', 'solicit', 'warrant', 'disseminate', 'contain','disclose', 'virus', 'liable' ,'liability', 'confidential', 'privilege', 'email', 'warning', 'proprietary']
        self.disclaimer_startword_list = ['important', 'notice', 'warning']
        
        
    def file_reader(self, file):
        with open(file, 'r') as f:
            return f.read() #list of sentences
    
    
    def drop_char(self, str_line='' , char_list=[] ):
        string = str(str_line)
        for ci in char_list:
            string = string.replace( ci, '')
            
        return string
    
    
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
    
    
    
    def execute(self, page):
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
        
        #-----  Mail Border-line identifier ---------------------------------------------
        border_index = None
        
        pattern1 = re.compile('<div[ ]+style=.*?\Wborder\W.*?>')
        pattern2 = re.compile('<hr.*?>')
        
        for pbi in range( len(pre_body_list) ):
            if re.search( pattern1, pre_body_list[pbi] ):
                border_index = pbi
                break
            
            if re.search( pattern2, pre_body_list[pbi] ):
                border_index = pbi
                break
        
        
        Ori_body_list = pre_body_list[:border_index]  # Preserving original format (No stripping)
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
        for si in range( len(body_list) ):
            if not re.search(html_tag, body_list[si]) and body_list[si] != '':
                #--Removing white spaces, and appendung to a dictionary
                String_index[si] = body_list[si].strip()
                Ori_String_index[si] = body_list[si].strip()
        
        #--------------------------------------------------------------------------------
        
        
        #----- Drop Chars ---------------------------------------------------------------
        for i in String_index:
            str_line = String_index[i]
            new_str_line = self.drop_char( str_line , char_list= self.chars_list  )
            
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
        
        
        #---- Closing (Mail-close greet) open tags --------------------------------------------------------- 
        if mail_close_index:
            cnew_tag_close = self.tag_closer( mail_close_index, Ori_body_list )
            
            mail_close_index = cnew_tag_close[0]
            top_new_bottom   = cnew_tag_close[1]
        #--------------------------------------------------------------------------------
        
        
        #----- Signature Contennt Removal -----------------------------------------------
        title_index = None
        email_index = None
        email_pattern = re.compile('([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)')
        name_pattern = re.compile( '(?:[A-Z][a-z]*\s?)+' )
        
        if not mail_close_index:
            
            for bl_i in Ori_String_index:
                bstring_line = Ori_String_index[bl_i]
                
                if email_pattern.search( bstring_line ):
                    email_index = bl_i
                
                st_line_len   = len( bstring_line.replace('.', ' ').split() )
                st_line_isalpha = ''.join(bstring_line.split()).isalpha()
                
                if st_line_len == 1  and  len( bstring_line.replace('.', ' ').split()[0] ) < 2: # If string = 'Single letter' set it to 0
                    st_line_len = 0
                
                if name_pattern.search(bstring_line)  and  0 < st_line_len < 5  and  st_line_isalpha:
                    title_index = bl_i
            
            if title_index  and  email_index  and  title_index < email_index:
                mail_close_index = title_index
            
            elif title_index  and  email_index  and  email_index < title_index:
                mail_close_index = email_index   
            
            #----- Closing (Signature) open tags --------------------------------------------
            if mail_close_index:
                snew_tag_close = self.tag_closer( mail_close_index, Ori_body_list )
                
                mail_close_index = snew_tag_close[0]
                top_new_bottom   = snew_tag_close[1]
        #------------------------------------------------------------------------------------
        
        
        #----- Disclaimer identifier---------------------------------------------------------
        if not mail_close_index and not email_index:
            
            disclaimer_found = False
            disclaimer_list = []
            found_dword_count = 0
            intercept_prob = 0
            sword_prob = 0
            
            for disc_i in String_index:
                if self.word_count(String_index[disc_i], min= 80, max= 400):
                    disclaimer_list.append(disc_i)
            
            if disclaimer_list:
                #-- Validating probability - intercepting key word ------
                for d_word in self.disclaimer_intercept_list:
                    if d_word in Ori_body_list[ max(disclaimer_list) ]:
                        found_dword_count += 1
                
                intercept_prob =  (found_dword_count/len(self.disclaimer_intercept_list) ) * 100
                
                
                #-- Validating probability - Starting key word ----------
                disclaimer_string = body_list[ max(disclaimer_list) ]
                
                disclaimer_start_string = disclaimer_string.split()[0]  #First word of the string
                
                for d_sword in self.disclaimer_startword_list:
                    if  d_sword in disclaimer_start_string.lower():# If disclaimer startword found increase the proberbility.
                        sword_prob = 2.0
                
                
                if found_dword_count > 0 and  intercept_prob + sword_prob >= 0.2 :
                    
                    Ori_body_list[max(disclaimer_list)] = ''    # Cleaning disclaimer string from (Ori_body_list)
                    body_list[max(disclaimer_list)] = ''
                    
                    disclaimer_found = True
                    mail_close_index = max(disclaimer_list)
                    
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
        
        return Page_FIlTERED
