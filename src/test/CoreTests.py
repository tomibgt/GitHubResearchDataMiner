'''
Created on Oct 7, 2014

@author: bgt
'''
import unittest
from GitHubConnection import GitHubConnection


class Test(unittest.TestCase):

    #GHRDM can draw the commit log of a project in GitHub
    def testGitHubConnection(self):
        connection = GitHubConnection(user="tomibgt", repo="GitHubResearchDataMiner")
        commits = connection.getCommits()
        validFlag = commits.count('\n') > 2
        self.assertTrue(validFlag, "Cannot draw commit logs from GitHub")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()