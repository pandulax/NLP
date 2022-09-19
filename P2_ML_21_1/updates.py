
from ml_fextract import fextract
from ml_predict  import predict


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
            
            
            #----- Closing (Disclaimer) open tags --------------------------------------------
            if disclaimer_found:
                
                if mail_close_index:
                    dnew_tag_close = self.tag_closer( mail_close_index, Ori_body_list )
                    
                    mail_close_index = dnew_tag_close[0]
                    top_new_bottom   = dnew_tag_close[1]
        #------------------------------------------------------------------------------------
        
        
##================================================================================================
        
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
        
        
        
        #----- Drop Chars/Words ---------------------------------------------------------------
        for i in String_index:
            str_line = String_index[i]
            
            new_str_line = self.clean_unicode_chars(str_line)
            new_str_line = self.drop_char( new_str_line , char_list = self.chars_list  )
            new_str_line = self.drop_words( new_str_line, word_list = self.stopw_list )
    
    