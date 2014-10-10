'''
Created on Oct 10, 2014

@author: bgt
'''

import ConfigParser
import os

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.dirname(__file__)+'/config.cfg'))

if __name__ == '__main__':
    pass