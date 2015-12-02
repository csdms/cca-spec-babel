#!/usr/bin/env python
from xml.dom import minidom
import os, sys
import getopt
import imp

def usage():
    print "Create XML deployment file for a CCA entity.\n"
    print "Usage:"
    print os.path.basename(sys.argv[0]), "< --type=component | class | interface | port > [options]"
    print "for help on options for type T, use the command"
    print "  ", os.path.basename(sys.argv[0]), "--type=T --help"
    return

def dispatch(className, argv):
    (file, filename, description) = imp.find_module(className)
    mod = imp.load_module(className, file, filename, description)
    targetClass = getattr(mod, className)
    newObject = targetClass()
    newObject.processArgs(argv)
    newObject.generateXML()
    print newObject.getXMLRep()
    return

    
if __name__ == '__main__':
    longOptions =["type=", "help"]
    shortOptions = 't:h'
    askHelp = False
    hasType = False
    typeGiven=''
    typeClassMap = {'component':'CCAComponentXML', 
                    'port':'CCAPortXML', 
                    'class':'CCAClassXML', 
                    'interface':'CCAInterfaceXML'}
    
    # Parse only first argument to decide where to dispatch the command
    try:
        opts1, args1 = getopt.getopt(sys.argv[1:2], shortOptions, longOptions)
    except getopt.error, e :
        usage()
        sys.exit(1)
        
    for o, a in opts1:
        if o in ("-h", "--help"):
            askHelp = True
        if o in ("-t", "--type"):
            hasType = True
            typeGiven = a
    
    if (not hasType or typeGiven not in typeClassMap.keys()):
        usage()
        sys.exit(0)
#    print "Dispatching to class ", typeClassMap[typeGiven]
    dispatch(typeClassMap[typeGiven], sys.argv[2:])
    sys.exit(0)