'''
Created on Aug 20, 2015
A class that reads configuration from a configuration file and command line parameters,
and gives out this information.

@author: bgt
'''

import ConfigParser

class BgtConfiguration(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.fileConfig = None

        self.outputfile = "output.csv"
        self.repo = ""
        self.user = ""
    
    def get(self, section, option):
        return self.fileConfig.get(section, option)
    
    def parseCommandLine(self, argv):
        if len(argv) < 4:
            raise BadCommandLineException("Too few commandline parameters.")
        self.user = argv[1]
        self.repo = argv[2]
        if len(argv) > 3:
            self.outputfile = argv[3]

    def readConfigfile(self, configFilePathName):
        self.fileConfig = ConfigParser.ConfigParser()
        self.fileConfig.readfp(open(configFilePathName))

class BadCommandLineException(Exception):
    pass

        