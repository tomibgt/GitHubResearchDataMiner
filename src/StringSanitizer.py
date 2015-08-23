'''
Created on Aug 23, 2015

@author: bgt

Non-printable character removal from Ants Aasma in Stackoverflow
http://stackoverflow.com/questions/92438/stripping-non-printable-characters-from-a-string-in-python

'''
import unicodedata, re

class StringSanitizer(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        control_chars = ''.join(map(unichr, range(0,32) + range(127,160)))
        self.control_char_re = re.compile('[%s]' % re.escape(control_chars))

    def stripNonPrintableCharactersFromString(self, string):
        '''
        Removes non-printable unicodecharacters
        '''
        return self.control_char_re.sub('', string)

    def stripSemicolonsFromString(self, string):
        '''
        Replaces semicolons (;) with a period and a comma (.,)
        '''
        return string.replace(';', '.,')
