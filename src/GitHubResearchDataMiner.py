'''
Created on Oct 10, 2014

@author: bgt
'''

import ConfigParser
import os
import sys
import GitHubConnection
from BgtConfiguration import BgtConfiguration
from BgtConfiguration import BadCommandLineException

def printHowToUse():
    print "Usage: python GitHubResearchDataMiner.py githubUserName githubProjectName [outputfilepath.csv]"

if __name__ == '__main__':
    config = BgtConfiguration()
    try:
        config.readConfigfile(os.path.dirname(__file__)+'/config.cfg')
        config.parseCommandLine(sys.argv)
    except BadCommandLineException as e:
        print e.message
        printHowToUse()
        sys.exit()
    
    connection = GitHubConnection.GitHubConnection(config)
    connection.getCsv(config.outputfile)

    