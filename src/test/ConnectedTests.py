'''
Created on Oct 7, 2014

@author: bgt
'''

import datetime
import os
import unittest
from GitHubConnection import GitHubConnection
import HelperFunctions


class ConnectedTest(unittest.TestCase):

    def setUp(self):
        self.connection = GitHubConnection(user="tomibgt", repo="GitHubResearchDataMiner")

    def testChoke(self):
        self.connection._GitHubConnection__choke()
        alpha = HelperFunctions.millitimestamp()
        self.connection._GitHubConnection__choke()
        delta = HelperFunctions.millitimestamp()
        self.assertGreater(delta, alpha+79, "The choke delay is less than 0.08 seconds: "+str((delta-alpha)/1000)+" ("+str(delta)+")")
        self.assertLess(delta, alpha+90, "The choke delay is too much over 0.08 seconds: "+str((delta-alpha)/1000)+" ("+str(delta)+")")
                
    # issue #2 Draw commit logs for a repository in GitHub
    def testGitHubConnection(self):
        commits = self.connection.getCommitMessages()
        validFlag = commits.count('\n') > 2
        self.assertTrue(validFlag, "Cannot draw commit logs from GitHub")

    # issue #1 Produce CSV file of all commit data of a given repository
    def testProduceCSVfile(self):
        filepath = self.connection.getCsv()
        fileh = open(filepath, 'r')
        for line in fileh:
            self.assertGreater(line.count(';'), 1, "Produced file is not CSV: "+line)
        fileh.close()
        os.remove(filepath)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()