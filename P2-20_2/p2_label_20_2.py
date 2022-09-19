#Analyzer - 19.4.6
import os
import sys
import re
import csv
#from bs4 import BeautifulSoup

#import nltk
#pos_tag = nltk.pos_tag
#WNL = nltk.stem.WordNetLemmatizer()
#lemt = WNL.lemmatize

class Analyzer:
    
    def __init__(self, *argv, **kwargs):
        
        self.file_name = argv[0]
        
        #self.selfclose_tags = ['area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr']
        
        #self.chars_list = [',', '.', '&amp;', '&#38;', '!', '&nbsp;', '&#169;', '&copy;', '&#174;', '&reg;', '&#8471;', '&#8482;', '&trade;', '&#8480;', '&#160;', '&bull;', '&#8219;', '&quot;', '&#34;', '&lsquo;', '&#8216;', '&rsquo;', '&#8217;', '&ldquo;', '&#8220;', '&rdquo;', '&#8221;', '&#09;', '&#10;', '&#13;', '&#8226;', '&deg;', '&#176;', '&infin;', '&#8734;', '&#36;' , '&#8364;' , '&euro;' , '&#163;' , '&pound;' , '&#165;' , '&yen;' , '&#162;' , '&cent;' , '&#8377;', '&#9702;', '&#8729;', '&#8227;' , '&#8259;', '&#43;', '&#150;', '&#151;']
        
        #self.stopw_list = ['and', 'all', 'the', 'b']
        #self.cword_list = ['thank', 'thanks', 'thanking', 'regard', 'regards', 'sincere', 'sincerely', 'gratitude', 'gratitudes', 'cheers', 'appreciation', 'you', 'your', 'yours', 'kind', 'best', 'many' , 'with', 'again' , 'fond' ]
        
        #self.disclaimer_intercept_list = ['disseminate', 'contain', 'disclose', 'virus', 'liable', 'liability', 'confidential', 'privileged', 'mail', 'warning', 'content', 'message', 'notice', 'transmit', 'individual', 'entity', 'immediate', 'distribute', 'prohibit', 'damage', 'authori', 'conclude', 'organization', 'attorney', 'protect']
        #self.disclaimer_startword_list = ['important', 'notice', 'warning']
        #self.shortwords_list = ['Hi', 'Pfa', 'Fyi', 'Asap', 'Aka' , 'Dear']
        
        #self.stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
        
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
                #print( (from_tag/sent_tag) )
                #print( (sent_tag/to_tag) )
                #print('')
                #print( from_tag, pre_body_list[from_tag])
                #print('')
                border_index = from_tag        
        
        return border_index
    
    
    def lineindex_ratio(self, string_index={}):
        if string_index:
            temp_index=[]
            for os_i in string_index:
                temp_index.append(os_i)
            
            max_index = max(temp_index)
            
            stringratio_index = {}
            for os_i in string_index:
                stringratio_index[os_i] = os_i/max_index
            
        return stringratio_index
    
    
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
        page = str(page)
        page = re.compile(r'[\t]').sub(' ', page)
        page = re.compile(r'[\n]').sub('', page)
        page = re.compile(r'[\r]').sub('', page)
        
        
        #----- HTML <body> </body> tag identifier ---------------------------------------
        
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
        #--------------------------------------------------------------------------------
        
        #----- Validating Mail Border ----------------------------------------------
        
        border_index = None
        border_index = self.mailborder(pre_body_list)
        
        #---------------------------------------------------------------------------
        
        #-----  Mail Border-line identifier ---------------------------------------------
        border_index_list = []
        
        pattern1 = re.compile('<div[ ]+style=.*?\Wborder\W.*?>')
        pattern2 = re.compile('<hr.*?>')
        
        for pbi in range( len(pre_body_list) ):
            if re.search( pattern1, pre_body_list[pbi] ):
                border_index_list.append(pbi)
            
            if re.search( pattern2, pre_body_list[pbi] ):
                border_index_list.append(pbi)
                
        ##--------------------------------------------------------------------------------
        
        topborder_index_list=[]
        if border_index  and border_index_list:
            for bil_i in border_index_list:
                if 0.8 <= (bil_i/border_index) < 1:
                    #print('Border_line', bil_i/border_index)
                    border_index = bil_i
        
        
        Ori_body_list = pre_body_list[:border_index]  # Preserving original format
        body_list = pre_body_list[:border_index]
        
        #pre_body_list = None #Flushing pre_body_list
        
        
        #----- Removing White spaces ----------------------------------------------------
        for list_i in range( len(body_list) ):
            body_list[list_i] = body_list[list_i].strip()  # Striped
        
        #print(body_list)
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
        
        property_list = []
        cleanded_string_index = {}
        
        for line_i in Ori_String_index:
            
            cleanded_str = self.clean_unicode_chars(Ori_String_index[line_i])
            cleanded_str = cleanded_str.strip()
            #print(cleanded_str)
            if cleanded_str != '':
                cleanded_string_index[line_i] = cleanded_str
                print(line_i)
        
        for cs_i in cleanded_string_index:
            index_ratio = self.line_index_ratio(cs_i, cleanded_string_index)
            
            property_list.append([ cs_i, cleanded_string_index[cs_i] ])
        
        
        outfile_path = 'label'  #label
        
        out_file = self.file_name.split('\\')[-1]
        out_file = out_file.split('.')[0]
        
        out_file_name = 'LABEL_' + out_file + '.txt'
        
        with open(outfile_path+ '/' + out_file_name , 'w') as fw:
            for pl_i in property_list:
                #print( '<T>' , pl_i[0], '<T>' , pl_i[1], '<T>' , pl_i[2] )
                outfile_str =  out_file + '>' + str(pl_i[0]) + '>' + '>'+ str(pl_i[1]) 
                fw.write(outfile_str + '\n')
            
        print('\nFile (To be labeled) : ' +outfile_path + '/' + out_file_name)
        
        
        #print(top_new_bottom)
        
        ##html_close_tag = re.compile('<[^/].*?>')
        
        #body_FIlTERED = body_top + top_new_bottom
        
        #Page_FIlTERED = page_TOP + body_FIlTERED + page_BOTTOM      ### Filtered FINAL HTML STRING
        
        #return Page_FIlTERED
        
        #print('--------page_TOP\n', page_TOP)
        #print('--------page_BOTTOM\n', page_BOTTOM)
        
        #print(Page_FIlTERED)  #######
        
        ######------------------------------------------------
        #out_file = self.file_name.split('\\')[-1] 
        #outfile_path = '' 
        #if len( self.file_name.split('\\') ) > 1 : 
            #for i in self.file_name.split('\\')[:-1]: 
                #outfile_path += i + '\\' 
       
        #with open(outfile_path + 'FILTERED_' + out_file, 'w') as fw: 
            #fw.write(Page_FIlTERED) 
       
        #print('\nFiltered file : ' +outfile_path + 'FILTERED_' + out_file) 


if __name__ == "__main__":
   
    #file = 'htf.html'
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

#with open('LABEL_h1.txt') as csvfile:
#    readCSV = csv.reader(csvfile, delimiter='<')
#    for row in readCSV:
#        #print(row)
#        print(row[0],row[1],row[2],row[3])

