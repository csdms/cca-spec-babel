from CCAXMLEntity import CCAXMLEntity
from optparse import OptionParser
from xml.dom import minidom
import socket
import sys
import os
import datetime

class CCAComponentXML(CCAXMLEntity):
    def __init__(self):
        CCAXMLEntity.__init__(self)
        self.kind = 'component'
        self.libInfoXML = None
        self.options = None
        self.args = None
        self.parser = None
        self.symbol = ''
        self.lang = ''
        self.name = ''
        self.id = ''
        self.palletAlias = ''
        self.includePath = ''
        self.libPath = ''
        self.staticLib = ''
        self.sharedLib = ''
        self.libtoolLib = ''
        self.cClientLib=''
        self.cClientHeaderPath = ''
        self.f77ClientLib=''
        self.f90ClientLib=''
        self.f90ClientHeaderPath = ''
        self.cxxClientLib = ''
        self.cxxClientHeaderPath = ''
        self.portLibPath = ''
        self.usePortLibList = []
        self.providePortLibList = []
        self.dependLibList = []
        
        usage = "usage: %prog --type=component [options] SIDL_SYMBOL"
        parser = OptionParser(usage=usage)
        parser.add_option("-n", "--name", dest = "name",
                  help="Component name (default is component SIDL symbol)")
        parser.add_option("-i", "--id", dest = "id",
                  help = "Component unique id \n(default is USER@HOST:component_name:time_stamp)", 
                  metavar="COMPONENT_ID")
        parser.add_option("-l", "--language", dest = "lang",
                  help = "Component implementation language (valid values are c, cxx, f77, f90, python, java)")
        parser.add_option("-a", "--alias", dest = "palletAlias",
                  help = "Component alias to be used in GUI's palletes (default is component name)",
                  metavar = "PALLET_ALIAS")
        
        parser.add_option("-I", "--include-path", dest = "includePath",
                  help = "Path to headers and mod files for the component and its client libraries",
                  metavar = "DIR")
        parser.add_option("-L", "--libpath", dest = "libPath",
                  help = "Path to component and client libraries",
                  metavar = "LIB")
        
        parser.add_option("--shared-lib", dest = "sharedLib",
                  help = "Shared library archive for the component. Library must be located in directory specified using --libpath",
                  metavar = "LIB")
        parser.add_option("--static-lib", dest = "staticLib",
                  help = "Static library archive for the component. Library must be located in directory specified using --libpath",
                  metavar = "LIB")
        parser.add_option("--libtool-lib", dest = "libtoolLib",
                  help = "libtool-generated library archive for the component. Library must be located in directory specified using --libpath",
                  metavar = "LIB")
        
        parser.add_option("--c-client-lib", dest = "cClientLib",
                   help = "Component C client library name. Specifying full path overrides directory specified in --libpath",
                   metavar = "LIB")
        parser.add_option("--c-client-headerpath", dest = "cClientHeaderPath",
                   help = "Path to component C client header files (overrides value specified using --include-path)",
                   metavar = "DIR")
        
        parser.add_option("--f77-client-lib", dest = "f77ClientLib",
                   help = "Component F77 client library name. Specifying full path overrides directory specified in --libpath",
                   metavar = "LIB")
        
        parser.add_option("--f90-client-lib", dest = "f90ClientLib",
                   help = "Component C client library name. Specifying full path overrides directory specified in --libpath",
                   metavar = "LIB")
        parser.add_option("--f90-client-headerpath", dest = "f90ClientHeaderPath",
                   help = "Path to component F90 client header and mod files (overrides value specified using --include-path)",
                   metavar = "DIR")
        
        parser.add_option("--cxx-client-lib", dest = "cxxClientLib",
                   help = "Component CXX client library name. Specifying full path overrides directory specified in --libpath",
                   metavar = "LIB")
        parser.add_option("--cxx-client-headerpath", dest = "cxxClientHeaderPath",
                   help = "Path to component CXX client header files (overrides value specified using --include-path)",
                   metavar = "DIR")
        
        parser.add_option("--port-libpath", dest = "portLibPath",
                   help = "Path to libraries representing ports used or provided by the component. Default is the same as --libpath",
                   metavar = "DIR")
        parser.add_option("-u", "--useportlib", dest = "usePortLibList", action = "append",
                   help = """Static library corresponding to port used by the component. The library is expected to be located
                             in the directory specified using --port-libpath. Full path to the library is also accepted. This option may be repeated.""",
                   metavar = "LIB")
        parser.add_option("-p", "--provideportlib", dest = "providePortLibList", action = "append", 
                   help = """Static library corresponding to port provided by the component. The library is expected to be located
                             in the directory specified using --port-libpath. Full path to the library is also accepted. 
                             This option may be repeated.""",
                   metavar = "LIB")
        parser.add_option("-d", "--depend-lib", dest = "dependLibList", action = "append",
                   help = """Full path to external libraries on which this component depends. This option may be repeated.""",
                   metavar = "LIB")
        
        parser.set_default('usePortLibList', [])
        parser.set_default('providePortLibList', [])
        parser.set_default('dependLibList', [])
        self.parser = parser
        return
    
    def usageError(self, msg = ""):
        print >> sys.stderr, "Error:", msg
        self.parser.print_help(sys.stderr)
        sys.exit(1)

    def checkPath(self, path):
        
        ''' Checks if path points to an existing directory. 
        
            Returns a tuple (state, abspath). 
            state = True and abspath = absolute_path, when path is a valid directory.
            state = False and abspath = None, when path is not a valid directory
        '''
        if (os.path.isdir(path)):
            abspath = os.path.abspath(path)
            return (True, abspath)
        else:
            return (False, None)
        
    def checkFile(self, fname):
        
        ''' Checks if fname points to an existing file. 
        
            Returns a tuple (state, abspath). 
            state = True and abspath = absolute_filename, when path is a valid file name.
            state = False and abspath = None, when fname is not a valid file name
        '''
        if (os.path.isfile(fname)):
            abspath = os.path.abspath(fname)
            return (True, abspath)
        else:
            return (False, None)
        
    def checkLib(self, libName, defaultLibPath):
        
        ''' Checks if libname points to an existing library file. If libname doesn't
            contain path specification, the library is assumed to be located in the 
            defaultLibPath.

            Returns a tuple (state, abspath). 
            state = True and abspath = absolute_filename, when libName is a valid file name.
            state = False and abspath = None, when libName is not a valid file name
        '''
        if ('/' not in libName):
            lib = os.path.join(defaultLibPath, libName)
        else:
            lib = libName
        return self.checkFile(lib)
        
   
    def processArgs(self, argv):
        (self.options, self.args) = self.parser.parse_args(argv)
        if (len(self.args) != 1):
            self.usageError("Missing SIDL_SYMBOL specification")
        self.symbol = self.args[0]
        # Simple check for full SIDL symbol
        if (len(self.symbol.split('.')) < 2):
            self.usageError("Incomplete specification of SIDL_SYMBOL (possibly missing package name(s))")
            
        # Check for component name (and use default if not specified)
        if (self.options.name != None):
            self.name = self.options.name
        else:
            self.name = self.symbol

        # Check for component id (and use default if not specified)
        if( self.options.id != None):
            self.id = self.options.id
        else:
            hostName = socket.gethostbyaddr(socket.gethostname())[0]
            userName = os.environ.get('USER')
            timeStamp = datetime.datetime.now().isoformat('|')
            self.id = userName+'@'+hostName+':'+self.name+':'+timeStamp 
        
        # Check for component alias (and use default if not specified)
        if(self.options.palletAlias != None):
            self.palletAlias = self.options.palletAlias
        else:
            self.palletAlias = self.name
        
        if (self.options.lang == None):
            self.usageError("Missing required specification for --lang")
        validLangs = ['c', 'cxx', 'f77', 'f90', 'python', 'java']
        if (self.options.lang.lower() not in validLangs):
            print >> sys.stderr, "Error: invalid language specification ", self.options.lang
            sys.exit(1)
        self.lang = self.options.lang
        
        if (self.options.includePath == None):
            self.usageError("Missing required specification for --include-path")
        state, self.includePath = self.checkPath(self.options.includePath)
        if (state == False):
            print >> sys.stderr, "Error: Invalid path ", self.options.includePath
            sys.exit(1)
        
        if (self.options.libPath == None):
            self.usageError("Missing required specification for --libpath")
        state, self.libPath = self.checkPath(self.options.libPath)
        if (state == False):
            print >> sys.stderr, "Error: Invalid path ", self.options.libPath
            sys.exit(1)
        
        if (self.options.staticLib == None and 
            self.options.sharedLib == None and
            self.options.libtoolLib == None):
            print >> sys.stderr, "Error: Must specify at least one of --shared-lib, --static-lib or  --libtool-lib"
            sys.exit(1)
        
# Checking libraries ONLY in self.libPath
        if (self.options.staticLib != None):
            state, self.staticLib = self.checkLib(os.path.join(self.libPath, self.options.staticLib), '')
            if (state == False):
                print >> sys.stderr, "Error: Missing library file", self.options.staticLib
                sys.exit(1)
        
        if (self.options.sharedLib != None):
            state, self.sharedLib = self.checkLib(os.path.join(self.libPath, self.options.sharedLib), '')
            if (state == False):
                print >> sys.stderr, "Error: Missing library file", self.options.sharedLib
                sys.exit(1)
        
        if (self.options.libtoolLib != None):
            state, self.libtoolLib = self.checkLib(os.path.join(self.libPath, self.options.libtoolLib), '')
            if (state == False):
                print >> sys.stderr, "Error: Missing library file", self.options.libtoolLib
                sys.exit(1)
               
        if (self.options.cClientLib != None):
            state, self.cClientLib = self.checkLib(self.options.cClientLib, self.libPath)
            if (state == False):
                print >> sys.stderr, "Error: Missing library file", self.options.cClientLib
                sys.exit(1)
            self.cClientHeaderPath = self.includePath
            
        if (self.options.cClientHeaderPath != None):
            state, self.cClientHeaderPath = self.checkPath(self.options.cClientHeaderPath)
            if (state == False):
                print >> sys.stderr, "Error: Invalid path ", self.options.cClientHeaderPath
                sys.exit(1)
        
        if (self.options.f77ClientLib != None):
            state, self.f77ClientLib = self.checkLib(self.options.f77ClientLib, self.libPath)
            if (state == False):
                print >> sys.stderr, "Error: Missing library file", self.options.f77ClientLib
                sys.exit(1)
        
        if (self.options.f90ClientLib != None):
            state, self.f90ClientLib = self.checkLib(self.options.f90ClientLib, self.libPath)
            if (state == False):
                print >> sys.stderr, "Error: Missing library file", self.options.f90ClientLib
                sys.exit(1)
            self.f90ClientHeaderPath = self.includePath
            
        if (self.options.f90ClientHeaderPath != None):
            state, self.f90ClientHeaderPath = self.checkPath(self.options.f90ClientHeaderPath)
            if (state == False):
                print >> sys.stderr, "Error: Invalid path ", self.options.f90ClientHeaderPath
                sys.exit(1)
        
        if (self.options.cxxClientLib != None):
            state, self.cxxClientLib = self.checkLib(self.options.cxxClientLib, self.libPath)
            if (state == False):
                print >> sys.stderr, "Error: Missing library file", self.options.cxxClientLib
                sys.exit(1)
            self.cxxClientHeaderPath = self.includePath
            
        if (self.options.cxxClientHeaderPath != None):
            state, self.cxxClientHeaderPath = self.checkPath(self.options.cxxClientHeaderPath)
            if (state == False):
                print >> sys.stderr, "Error: Invalid path ", self.options.cxxClientHeaderPath
                sys.exit(1)
                
# FIXME : How do we want to handle python and java clients?
        
        if (self.options.portLibPath == None):
            self.portLibPath = self.libPath
        else:
            state, self.portLibPath = self.checkPath(self.options.portLibPath)
            if (state == False):
                print >> sys.stderr, "Error: Invalid path ", self.options.portLibPath
                sys.exit(1)
                
        for ulib in self.options.usePortLibList :
            state, lib = self.checkLib(ulib, self.portLibPath)
            if (state == False):
                print >> sys.stderr, "Error: invalid use port library file ", ulib
                sys.exit(1)
            else:
                self.usePortLibList.append(lib)
        
        for plib in self.options.providePortLibList :
            state, lib = self.checkLib(plib, self.portLibPath)
            if (state == False):
                print >> sys.stderr, "Error: invalid use port library file ", plib
                sys.exit(1)
            else:
                self.providePortLibList.append(lib)
        
        for plib in self.options.dependLibList :
            state, lib = self.checkLib(plib, '')
            if (state == False):
                print >> sys.stderr, "Error: invalid use port library file ", plib
                sys.exit(1)
            else:
                self.dependLibList.append(lib)
        
        return

    def generateXML(self):

        impl = minidom.getDOMImplementation()
        self.deploymentXML = impl.createDocument(None, "componentDeployment", None)
        top_element = self.deploymentXML.documentElement
        top_element.setAttribute("name", self.name)
        top_element.setAttribute("uniqueID", self.id)
        top_element.setAttribute("palletClassAlias", self.palletAlias)
        top_element.setAttribute("language", self.lang)
        
        envNode = self.deploymentXML.createElement("environment")
        top_element.appendChild(envNode)
        
        libNode = self.deploymentXML.createElement("library")
        envNode.appendChild(libNode)
        
        # FIXME : What is exactly supposed to go into library's name attribute?
        libNode.setAttribute("name", self.name)
        
        # FIXME : Are we dis-allowing locating different archives in different directories ?
        libNode.setAttribute("location", self.libPath)
        if(self.sharedLib != ''):
            libNode.setAttribute("shared-archive",os.path.basename(self.sharedLib))
            libNode.setAttribute("loading", "dynamic")
        if(self.libtoolLib != ''):
            libNode.setAttribute("libtool-archive",os.path.basename(self.libtoolLib))
            libNode.setAttribute("loading", "dynamic")
        if(self.staticLib != ''):
            libNode.setAttribute("static-archive",os.path.basename(self.staticLib))
            libNode.setAttribute("loading", "static")
        # FIXME : How do we decide on the value of loading attribute if we have both static and shared archives ?
        # FIXME : For now, static loading overrides dynamic loading
        
        # FIXME : How do we define headers for python and java ?
        # FIXME : What header files should go here, and what files should go in the clients section?
        if (self.lang in ['c', 'cxx', 'f90']):
            headerNode = self.deploymentXML.createElement("headers")
            envNode.appendChild(headerNode)
            headerNode.setAttribute('path', self.includePath)
            headerFiles = ''
            symbolUbar = self.symbol.replace('.', '_')
            if (self.lang == 'c'):
                headerFiles = symbolUbar +'.h'
            elif (self.lang == 'cxx'):
                headerFiles = symbolUbar + '.hxx'
            else:
            # FIXME : Is this good enough for F90 ?
                headerFiles = symbolUbar + '.mod ' + symbolUbar + '_type.mod' 
            headerNode.setAttribute('files', headerFiles)
        
        clientListNode = self.deploymentXML.createElement("clientList")
        envNode.appendChild(clientListNode)
        if (self.cClientLib != ''):
            cClientNode =  self.deploymentXML.createElement("client")
            clientListNode.appendChild(cClientNode)
            cClientNode.setAttribute("language" , "c")
            cClientNode.setAttribute("library", os.path.basename(self.cClientLib))
            cClientNode.setAttribute("libpath" , os.path.dirname(self.cClientLib))
            cClientNode.setAttribute("headerpath", self.cClientHeaderPath)
                                     
        if (self.cxxClientLib != ''):
            cxxClientNode =  self.deploymentXML.createElement("client")
            clientListNode.appendChild(cxxClientNode)
            cxxClientNode.setAttribute("language" , "cxx")
            cxxClientNode.setAttribute("library", os.path.basename(self.cxxClientLib))
            cxxClientNode.setAttribute("libpath" , os.path.dirname(self.cxxClientLib))
            cxxClientNode.setAttribute("headerpath", self.cxxClientHeaderPath)
                                     
        if (self.f90ClientLib != ''):
            f90ClientNode =  self.deploymentXML.createElement("client")
            clientListNode.appendChild(f90ClientNode)
            f90ClientNode.setAttribute("language" , "f90")
            f90ClientNode.setAttribute("library", os.path.basename(self.f90ClientLib))
            f90ClientNode.setAttribute("libpath" , os.path.dirname(self.f90ClientLib))
            f90ClientNode.setAttribute("headerpath", self.f90ClientHeaderPath)
                                     
        # FIXME: Do we need header path for F77 clients? 
        if (self.f77ClientLib != ''):
            f77ClientNode =  self.deploymentXML.createElement("client")
            clientListNode.appendChild(f77ClientNode)
            f77ClientNode.setAttribute("language" , "f77")
            f77ClientNode.setAttribute("library", os.path.basename(self.f77ClientLib))
            f77ClientNode.setAttribute("libpath" , os.path.dirname(self.f77ClientLib))
#            f77ClientNode.setAttribute("headerpath", self.f77ClientHeaderPath)
                     
        usePortListNode = self.deploymentXML.createElement("usePortLibList")
        envNode.appendChild(usePortListNode)
        # FIXME: Do we only need and assume port libs only in the language of the component ?
        for ulib in self.usePortLibList:
            usePortNode = self.deploymentXML.createElement("usePortLib")
            usePortNode.setAttribute("path", os.path.dirname(ulib))
            usePortNode.setAttribute("library", os.path.basename(ulib))
            usePortListNode.appendChild(usePortNode)
            
        providePortListNode = self.deploymentXML.createElement("providePortLibList")
        envNode.appendChild(providePortListNode)
        # FIXME: Do we only need and assume port libs only in the language of the component ?
        for plib in self.providePortLibList:
            providePortNode = self.deploymentXML.createElement("providePortLib")
            providePortNode.setAttribute("path", os.path.dirname(plib))
            providePortNode.setAttribute("library", os.path.basename(plib))
            providePortListNode.appendChild(providePortNode)
            
        dependListNode = self.deploymentXML.createElement("dependLibList")
        envNode.appendChild(dependListNode)
        for lib in self.dependLibList:
            dependNode = self.deploymentXML.createElement("dependLib")
            dependNode.setAttribute("path", os.path.dirname(lib))
            dependNode.setAttribute("library", os.path.basename(lib))
            dependListNode.appendChild(dependNode)
        
#       FIXME: Proper selection for scl library (.la or .so ?) 
        sclLib = ''
        if (self.libtoolLib != ''):
            sclLib = self.libtoolLib
        elif (self.sharedLib != ''):
            sclLib = self.sharedLib
        if (sclLib != ''):
            sclNode = self.deploymentXML.createElement("scl")
            top_element.appendChild(sclNode)
            libNode = self.deploymentXML.createElement("library")
            sclNode.appendChild(libNode)
            libNode.setAttribute("uri", sclLib)
            libNode.setAttribute("scope", "global")
            libNode.setAttribute("resolution", "now")
            classNode = self.deploymentXML.createElement("class")
            sclNode.appendChild(classNode)
            classNode.setAttribute("name", self.symbol)
            classNode.setAttribute("desc", "ior/impl")
            if (self.lang == 'python'):
                pyClassNode = self.deploymentXML.createElement("class")
                sclNode.appendChild(pyClassNode)
                pyClassNode.setAttribute("name", self.symbol)
                pyClassNode.setAttribute("desc", "python/impl")
            
#        print self.deploymentXML.toprettyxml(indent="   ")
        
#        text = newdoc.createTextNode('Some textual content.')
#        top_element.appendChild(text)

#        pass
    