'''
Created on Oct 7, 2014

@author: bgt
'''
import os
import unittest
from GitHubConnection import GitHubConnection


class Test(unittest.TestCase):

    # issue #2 Draw commit logs for a repository in GitHub
    def testGitHubConnection(self):
        connection = GitHubConnection(user="tomibgt", repo="GitHubResearchDataMiner")
        commits = connection.getCommits()
        validFlag = commits.count('\n') > 2
        self.assertTrue(validFlag, "Cannot draw commit logs from GitHub")

    # issue #1 Produce CSV file of all commit data of a given repository
    def testProduceCSVfile(self):
        connection = GitHubConnection(user="tomibgt", repo="GitHubResearchDataMiner")
        filepath = connection.getCsv()
        fileh = open(filepath, 'r')
        for line in fileh:
            self.assertGreater(line.count(';'), 4, "Produced file is not CSV")
        fileh.close()
        os.remove(filepath)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()