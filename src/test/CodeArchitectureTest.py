'''
Created on Oct 10, 2014

@author: bgt
'''
import unittest
import GitHubResearchDataMiner

class CodeArchitectureTest(unittest.TestCase):


    def testConfiguration(self):
        self.assertIsNotNone(GitHubResearchDataMiner.config.get('authentication', 'ghusername'), "Configuration failed")
        self.assertIsNotNone(GitHubResearchDataMiner.config.get('authentication', 'ghpassword'), "Configuration failed")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testConfiguration']
    unittest.main()