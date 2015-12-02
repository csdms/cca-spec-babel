#!/usr/bin/env python                                                           

#-----------------------------------                                            
# Debugging support for subcommands                                             

import sys, os

class Devnull:
    """ The do nothing writer to replace sys.stderr when we want to see         
    no spew.                                                                    
    """
    def write(self, msg): pass
    def flush(self): pass

DEBUGSTREAM = Devnull()

if 'BOCCA_DEBUG' in os.environ.keys():
    if os.environ['BOCCA_DEBUG'] == "1":
        DEBUGSTREAM = sys.stderr


