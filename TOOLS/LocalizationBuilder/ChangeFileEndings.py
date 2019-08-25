'''
Changes the file extensions to the correct ones for DEU german ESN
spanish FRA french ITA italian
'''

import os

def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles

languages = ['DEU', 'ESN', 'FRA', 'ITA', 'PTB']
extensions = ['.deu', '.esn', '.fra', '.ita', '.ptb']

for language in range(len(languages)):
    files = getListOfFiles("Localization\\" + languages[language])
    print(files)
    for file in files:
        pre, ext = os.path.splitext(file)
        os.rename(file, pre + extensions[language])
