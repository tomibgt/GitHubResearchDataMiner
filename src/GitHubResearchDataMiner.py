'''
Created on Oct 10, 2014

@author: bgt
'''

import ConfigParser
import os
import sys
import GitHubConnection

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.dirname(__file__)+'/config.cfg'))

if __name__ == '__main__':
    user = sys.argv[1]
    repo = sys.argv[2]
    connection = GitHubConnection.GitHubConnection(user=user, repo=repo)
    connection.getCsv()
    