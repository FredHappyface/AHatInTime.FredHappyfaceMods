'''
Do translation. set at project root looks inside Localization/INT and produces
files for DEU german ESN spanish FRA french ITA italian. One side effect is that
effects and icons are stripped and must be added back in
'''

import os
from googletrans import Translator
translator = Translator()

translationTable = str.maketrans("éàèùâêîôûç", "eaeuaeiouc")


def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles



'''
Return the contents of a file as a string using a (relative) filepath
'''
def fileToTokens(filepath):
    tokens = []
    file = open(filepath, "r")
    for line in file:
        tokens.append(line)
    return tokens


'''
Write a string to a file defined with a (relative) path
'''
def stringToFile(filepath, string):
    tok = filepath.split('\\')
    checkfile = ''
    for x in tok[:-1]:
        checkfile += x + '\\'
    os.makedirs(checkfile, exist_ok=True)
    file = open(filepath, "w+")
    file.write(string)
    file.close()
    return

import unicodedata as ud

def get_ascii_char(c):
    s = ud.decomposition(c)
    if s == '': # for an indecomposable character, it returns ''
        return c
    code = int('0x' + s.split()[0], 0)
    return chr(code)

def get_translation(value, code):
    value = remove_text_inside_brackets(value)
    string =  translator.translate(value, dest= code).text
    out = ''
    for char in string:
        out += get_ascii_char(char)
    return out 


def remove_text_inside_brackets(text, brackets="()[]"):
    count = [0] * (len(brackets) // 2) # count open/close brackets
    saved_chars = []
    for character in text:
        for i, b in enumerate(brackets):
            if character == b: # found bracket
                kind, is_close = divmod(i, 2)
                count[kind] += (-1)**is_close # `+1`: open, `-1`: close
                if count[kind] < 0: # unbalanced bracket
                    count[kind] = 0  # keep it
                else:  # found bracket to remove
                    break
        else: # character is not a [balanced] bracket
            if not any(count): # outside brackets
                saved_chars.append(character)
    return ''.join(saved_chars)



files = getListOfFiles("Localization\\INT")
deu = ''
esn = ''
fra = ''
ita = ''
eng = ''

for file in files:
    tokens = fileToTokens(file)
    print(file)
    
    for token in tokens:

        if token[0] != '[':
            varname, value = token.split('=')

            print("Translating: " + value)

            # Translate value into deu esn fra ita
            deu += varname + '= ' + get_translation(value, 'de') + '\n'
            esn += varname + '= ' + get_translation(value, 'es') +'\n'
            fra += varname + '= ' + get_translation(value, 'fr') +'\n'
            ita += varname + '= ' + get_translation(value, 'it') +'\n'

            eng += varname + ' = ' + value
        else:
            deu += token 
            esn += token
            fra += token
            ita += token

            eng += token
            

    print("Writing output")
    stringToFile(file.replace("INT", "DEU", 1), deu)
    stringToFile(file.replace("INT", "ESN", 1), esn)
    stringToFile(file.replace("INT", "FRA", 1), fra)
    stringToFile(file.replace("INT", "ITA", 1), ita)
    stringToFile(file.replace("INT", "ENG", 1), eng)
    


        
