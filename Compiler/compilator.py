# -*- coding: utf-8 -*-
"""
Compilator
"""
import pandas as pd

_NULL_STR = "*_*"

PIF = dict()

TA = dict()
reserved_words=['identifier','const','int',
 'double',
 'char',
 'bool',
 'void',
 'struct',
 'if',
 'else',
 'else if',
 'for',
 'while',
 'break',
 'return',
 'read',
 'write',
 'in',
 'continue']

for i,res_word in enumerate(reserved_words):
    TA[res_word] = i


system_separators = [' ', ';', ':', '']
system_operators = ['+', '-', '*', '/', '>', '<', '==', '=', '>=', '<=', '!=', '%', '++', '--']

def is_identifier(token):
    cond_one = ord(token[0]) < ord('a') or ord(token[0]) > ord('z')
    cond_two = ord(token[0]) < ord('A') or ord(token[0]) > ord('B')
    cond_three = ord(token[0]) < ord('0') or ord(token[0]) > ord('9')
	#If it starts with anything other than a letter or '_'
    if cond_one:
        if cond_two:
            if (token[0] != '_'):
                return False
    #If it's a single letter
    if (len(token)==1 and (not cond_one or not cond_two)):
        return True
    
    for i in range(1,len(token)):
        if (cond_one and cond_two and cond_three and (token[i]!='_')):
            return False
        return True
                    
def is_constant(token):
    digit_cond = ((token[0] >= ord('0')) and (token[0] <= ord('9')))
    if (digit_cond and len(token) == 1):
        return True
    
    elif (digit_cond):
        for i in range(1,len(token)):
            #it's not a number
            if (not((token[0] >= ord('0')) and (token[0] <= ord('9')))):
                return False
        #it's a number
        return True
    #We check if it's constant string
    if ((token[0] == '"') and token[-1] == '"'):
        for i in range(1,len(token)-1):
            if token[i] == '"':
                return False
        return True
    return False       

def is_comment(line):
    for i in range(0,len(line)):
        if(line[i] in system_separators):
            continue
        elif(line[i]=='#'):
            return True
    return False

class SymbolTable():
    def __init__(self,num_of_codes):
        self.num_of_codes = num_of_codes
        null_list = [_NULL_STR]*5
        self.tokens = list()
        for i in range(0,num_of_codes):
            self.tokens.append(null_list[:])
    def search_or_add(self, token):
        byte_value = 0
        for character in token:
            byte_value += ord(character)
        hash_code = byte_value % self.num_of_codes
        for i in range(5):
            if self.tokens[hash_code][i] == token:
                return hash_code
            elif self.tokens[hash_code][i] == _NULL_STR:
                self.tokens[hash_code][i] = token
                return hash_code
        #If we got here it means we are out of space
        print("No more space, what can you do?")
    
    def to_csv(self):
        df = pd.DataFrame()
        counter = 0
        for i in range(len(self.tokens)):
            if self.tokens[i][0] != _NULL_STR:
                df[counter] = self.tokens[i]
                counter += 1
        df.replace( to_replace=_NULL_STR, value=pd.NA, inplace=True)
        df.dropna(inplace=True)
        df.to_csv('ST.csv')
        
        
ST = SymbolTable(97)

def detect_token(line):
    if(len(line)==1):
        copy_line = line[:]
        line = _NULL_STR[:]
        return copy_line
    for i in range(len(line)):
        if(line[i] in system_separators):
            to_return = line[0:i]
            line = line[i:]
            return to_return
        elif(i==len(line)-1):
            to_return = line[:i]
            line = _NULL_STR[:]
            return to_return

def genPIF(token, TA_index, ST_index):
    PIF[token] = (TA_index, ST_index)
    
def dict_to_csv(table):
    if 'identifier' in table:
        df = pd.DataFrame(table, index=[0])
        df.to_csv('TA.csv')
    else:
        df = pd.DataFrame(table, index=[0,1])
        df.to_csv('PIF.csv')

def scanning(file_name):
    lines = list()
    with open(file_name) as f:
        lines = f.readlines()
        
    for i in range(len(lines)):
        if(is_comment(lines[i])):
            continue
        while lines[i] != _NULL_STR:
            copy_line = lines[i][:]
            token = detect_token(lines[i])
            if lines[i] == copy_line:
                lines[i] = lines[i][len(token):]
            if(len(token) == 0):
                break
            if(token in TA):
                genPIF(token, TA[token], -1)
            elif(is_identifier(token)):
                index = ST.search_or_add(token)
                ta_index = TA['identifier']
                genPIF(token,ta_index,index)
            elif(is_constant(token)):
                index = ST.search_or_add(token)
                ta_index = TA['constant']
                genPIF(token,ta_index,index)
            else:###########
                print(f"Lexical error: Line {i} -> unidentified token: {token}")
    
    dict_to_csv(PIF)
    dict_to_csv(TA)
    ST.to_csv()


scanning('./program.txt')
                
                
        
        

