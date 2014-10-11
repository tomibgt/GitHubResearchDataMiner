'''
Created on Oct 10, 2014

@author: bgt
'''

import time
import unittest
import GitHubResearchDataMiner
import HelperFunctions

class CodeArchitectureTest(unittest.TestCase):


    def testConfiguration(self):
        self.assertIsNotNone(GitHubResearchDataMiner.config.get('authentication', 'ghusername'), "Configuration failed")
        self.assertIsNotNone(GitHubResearchDataMiner.config.get('authentication', 'ghpassword'), "Configuration failed")

    def testMilliTimeStamp(self):
        alpha = HelperFunctions.millitimestamp()
        time.sleep(1)
        beta = HelperFunctions.millitimestamp()
        self.assertGreater(beta-alpha, 900, "millitimestamp counts units smaller than milliseconds")
        self.assertLess(beta-alpha, 1500, "millitimestamp counts units greater than milliseconds")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testConfiguration']
    unittest.main()