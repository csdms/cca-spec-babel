import sys
import os
import sets

# This file abstracts binary deployment metadata for sidl symbols.
# It knows nothing of xml and shouldn't.
#
# A deployment description encapsulates data:
#- boolean isFinished: no more data should be added.
#- prefix of expected installation
#- sidl symbol
#- sidl basetype (interface, class, enum, struct)
#- language of implementation if appropriate.
#- sidl symbols on which symbol depends as extends or implements.
#- sidl symbols on which symbol depends publically (i.e. in sidl, but not derived from)
#- sidl symbols on which symbol depends privately (i.e. in impl but not sidl)
#- full path of sidl file describing class (may be shared with other sidl entities).
#- SUPPORTS-static (TRUE/FALSE)
#- SUPPORTS-dynamic (TRUE/FALSE)
#- SUPPORTS-libtool (TRUE/FALSE)
#- list of non-xml-supported,nonlibtool dependencies of impl.
#- directory,name of libtool library of impl
#- libtool-link list of non-xml-supported dependencies of impl.
#- directory,name of shared library of impl
#- shared-link list of non-xml-supported dependencies of impl.
#- directory,name of static library of impl
#- static-link list of non-xml-supported dependencies of impl.
#- directory name of headers for impl
#- foreach client in cxx,c,f77,f90
#-- directory,name of libtool library of client
#-- directory,name of shared library of client
#-- directory,name of static library of client
#-- directory name of headers for client
#- foreach client in java
#-- CLASSPATH elements
#- foreach client in python
#-- PYTHONPATH elements

##########################################################################3

class Client:
    """Container representing what we need to know about a generated binding.
The fields will be populated according to the language type in proper use.
This container exists in the context of an interface, class, struct, or enum
description that includes knowledge of the sidl symbol.
The fields have the special value 'unsupported' if the installation
does not support them."""
    def  __init__(self,lang,debug=False):
        self.finished = False
        self.ccaSpecBinding = "babel"
        self.uns = "unsupported"
        self.ignore = False
        self.debug = debug

        # babel binding language
        self.lang = lang

        # header/mod install directory
        self.IncludePath = None

        # classpath/jar if java
        self.ClassPath = None

        # pythonpath if python
        self.PythonPath = None

        # path-free full name of static library if c,cxx,f77,f90
        # e.g. name-c.a
        self.StaticLib = None

        # path-free full name of shared library if c,cxx,f77,f90
        # e.g. name-cxx.so.2
        self.SharedLib = None

        # path-free full name of libtool library if c,cxx,f77,f90
        # e.g. name-cxx.la
        self.LibtoolLib = None

    def nonecheck(self, name):
        if not self.finished:
            print "UNSET finished " + name
        if not self.ccaSpecBinding:
            print "missing ccaSpecBinding" +name
        if not self.lang:
            print "missing lang" +name
        if not self.IncludePath:
            print "missing IncludePath" +name
        if not self.PythonPath:
            print "missing PythonPath" +name
        if not self.ClassPath:
            print "missing ClassPath" +name
        if not self.SharedLib:
            print "missing sharedlib" +name
        if not self.StaticLib:
            print "missing staticlib" +name
        if not self.LibtoolLib:
            print "missing LibtoolLib" +name

    def getLang(self):
        return self.lang

    def setLang(self, lang):
        if self.debug:
            print "LANG=", lang
        self.lang = lang

    def setLibs(self, lang, libtoollib, sharedlib, staticlib):
        """ give complete pathname of each lib or None for those not supported.
This is not clever about libtool libs pointing at static, shared because the
install being documented may no have occured yet.
"""
        if not lang in ['cxx', 'c', 'f77', 'f90', 'ior']:
            return
        if libtoollib:
            self.LibtoolLib = libtoollib
        if sharedlib:
            self.SharedLib = sharedlib
        if staticlib:
            self.StaticLib = staticlib

    def setSymbolPath(self, lang, path):
        if lang == "java":
            self.ClassPath = path
        if lang == "python":
            self.PythonPath = path
        if lang in ['cxx', 'c', 'f77', 'f90', 'ior']:
            self.IncludePath = path

    def getSymbolPath(self):
        if self.lang == "java":
            return self.ClassPath
        if self.lang == "python":
            return self.PythonPath
        if self.lang in ['cxx', 'c', 'f77', 'f90', 'ior']:
            return self.IncludePath

    def getLib(self, linkage):
        if linkage == "libtool":
            return self.LibtoolLib
        if linkage == "shared":
            return self.SharedLib
        if linkage == "static":
            return self.StaticLib

    def setSpec(self, spec):
        self.ccaSpecBinding = spec

    def unsupported(self, lang):
        self.lang = lang
        self.finish()
   
    def finish(self):
        """ set all None entities to unsupported. Not for error checking. """
        if not self.lang:
            raise RuntimeError, "Client lang unspecified. Cannot be finished."
        if not self.IncludePath:
            self.IncludePath = self.uns
        if not self.ClassPath:
            self.ClassPath = self.uns
        if not self.PythonPath:
            self.PythonPath = self.uns
        if not self.StaticLib:
            self.StaticLib = self.uns
        if not self.SharedLib:
            self.SharedLib = self.uns
        if not self.LibtoolLib:
            self.LibtoolLib = self.uns
        self.finished = True
   
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
        
    def warnUnset(self, msg, verbose):
        if verbose:
            print  sys.stderr, "Unset member ", msg, " in client description for ", self.lang

    def check(self, verbose):
        """Self consistency check. Does not verify against filesystem.
@param verbose. If verbose, then spew detected errors.
@return true if ok, false if a problem found."""
        ok = False
        if not self.lang:
            if verbose:
                print  sys.stderr, "lang undefined in client description"
            return False

        # all branches must fall out to final return here.
        if self.lang == "java":
            if self.ClassPath and self.ClassPath != "":
                ok = True
            else:
                self.warnUnset("ClassPath", verbose)

        if self.lang == "python":
            if self.PythonPath and self.PythonPath != "":
                ok = True
            else:
                self.warnUnset("PythonPath", verbose)

        if self.lang in ["c","cxx","f77","f90","ior"]:
            score=0

            if self.StaticLib:
                score += 1
            else:
                self.warnUnset("StaticLib", verbose) 

            if self.SharedLib:
                score += 1
            else:
                self.warnUnset("SharedLib", verbose) 

            if self.LibtoolLib:
                score += 1
            else:
                self.warnUnset("LibtoolLib", verbose) 

            if score == 3:
                ok = True

        return ok

##########################################################################3

class Server(Client):
    def __init__(self,debug=False):
        Client.__init__(self,None,debug)

        # babel server language
        # self.lang

        # private native (non-babel) link dependencies. 
        self.nativeCompilingFlags = ""
        self.nativeSharedFlags = None
        self.nativeStaticFlags = None
        self.nativeLibtoolFlags = None

    def nonecheck(self, dummy=None):
        Client.nonecheck(self,"server")
        if not self.nativeLibtoolFlags:
            print "missing nativeLibtoolFlags"
        if not self.nativeCompilingFlags:
            print "missing nativeCompilingFlags"
        if not self.nativeSharedFlags:
            print "missing nativeSharedFlags"
        if not self.nativeStaticFlags:
            print "missing nativeStaticFlags"

    def finish(self):
        Client.finish(self)
        if not self.nativeLibtoolFlags:
            self.LibtoolFlags = self.uns
        if not self.nativeStaticFlags:
            self.nativeStaticFlags = self.uns
        if not self.nativeSharedFlags:
            self.SharedFlags = self.uns

    def setExtraFlags(self, lang, extraShared, extraStatic, extraLibtool, extraCompiling):
        self.lang = lang
        if self.debug:
            print "SEF LANG=", lang
        if extraCompiling:
            self.nativeCompilingFlags = extraCompiling
        else:
            self.nativeCompilingFlags = ""
        if extraShared:
            self.nativeSharedFlags = extraShared
        else:
            self.nativeSharedFlags = ""
        if extraStatic:
            self.nativeStaticFlags = extraStatic
        else:
            self.nativeStaticFlags = ""
        if extraLibtool:
            self.nativeLibtoolFlags = extraLibtool
        else:
            self.nativeLibtoolFlags = ""
        
    def getImplLibFlags(self, linkage):
        if linkage == "libtool":
            return self.nativeLibtoolFlags
        if linkage == "shared":
            return self.nativeSharedFlags
        if linkage == "static":
            return self.nativeStaticFlags
        return ""

##########################################################################3
class PortData:
    def __init__(self):
        self.ports = dict()

    def getSymbolsRequired(self):
        out = []
        for i in self.ports.keys():
            out.append(self.ports[i].getType())
            dt = self.ports[i].getDelegateType()
            if dt:
                out.append(dt)
        return out
    
    def setProperties(self, padd, pdelete):
        for i in padd:
            if self.ports.has_key(i[0]):
                self.ports[i[0]].addProperty(i[1], i[2], i[3])
        for i in pdelete:
            if self.ports.has_key(i[0]):
                self.ports[i[0]].removeProperty(i[1])
        
    def getCount(self):
        return len(self.ports)

    def addPort(self, port):
        if not port:
            return
        self.ports[port.getName] = port

    def removePort(self, name):
        if not name:
            return
        if self.ports.has_key(name):
            del self.ports[name]
 
    def getPorts(self):
        return self.ports.values()

    def getPort(self, name):
        if self.ports.has_key(name):
            return self.ports[name]
        return None

    def getPortInfoByKind(self, direction):
        """direction is uses, provides, or delegates.
           @return tuples of type, instance [,delegate]."""
        result=[]
        for i in self.ports.keys():
            p = self.ports[i]
            if p.usesOrProvides == direction:
                if direction == "delegates":
                    t = ( p.getType(), p.getName(), p.getDelegateType())
                else:
                    t= (p.getType(), p.getName())
                result.append(t)
        return result
 
    def getPortPropByName(self, portname, key):
        if self.ports.has_key(portname):
            port = self.ports[portname]
            return port.getProp(key)
        else:
            return None

    def nonecheck(self):
        for i in self.ports.keys():
            if self.ports[i] == None:
                print "missing portdata value for", i
            else:
                self.ports[i].nonecheck(i)
        
##########################################################################3

class Port:
    def __init__(self, direction, portname, porttype, properties=None, delegatetype=None):
        """ Metadata for a port. This object should know nothing of xml.
        In our representation, "delegates" makes some things easier to code, but
        the representation is handled in xml files as "provides" with an optional attribute
        delegateType.
@param portname port instance name
@param porttype interface type of port
@param properties optional dictionary of (primitiveType, value) tuples.
@param dtype optional delegate instance sidl type.
"""
        
        if not direction in ["uses", "provides", "delegates"]:
            raise RuntimeError , "Unexpected direction ("+direction+") to Port"
        self.usesOrProvides = direction
        self.instanceName = portname
        self.sidlSymbol = porttype
        if not delegatetype:
           self.sidlDelegate = porttype
        else:
           self.sidlDelegate = delegatetype
        self.props = dict()
        if properties:
            for i in properties.keys():
                (ptype, pvalue) = properties[i]
                self.props[i] = (ptype, pvalue)

    def nonecheck(self, name):
        if not self.usesOrProvides:
            print "missing direction in", name
        if not self.instanceName:
            print "missing instanceName in", name
        if not self.sidlSymbol:
            print "missing sidlSymbol in", name
        if not self.props:
            print "missing props in", name
       
    def addProperty(self, pname, ptype, pvalue):
        self.props[pname] = (ptype, pvalue)

    def removeProperty(self, pname):
        del self.props[pname]

    def getProperties(self):
        return self.props

    def getProp(self, name):
        if self.props.has_key(name):
            return self.props[name]
        else:
            return None

    def getName(self):
        return self.instanceName

    def getType(self):
        return self.sidlSymbol

    def getDelegateType(self):
        return self.sidlDelegate

    def getDirection(self):
        """Direction is uses, provides, or delegates (a type of providing)"""
        return self.usesOrProvides

##########################################################################3

class Deployment:
    """This is the union of all deployment types."""
    def nonecheck(self):
        print "DEPL CHECK"
        if not self.symbol:
            print "missing symbol"
        if not self.kind:
            print "missing kind"
        if not self.filename:
            print "missing xml filename"
        if not self.uuid or self.uuid=="fixmeuuid":
            print "missing uuid"
        if not self.babelbin or self.babelbin=="/fixme/babel-config":
            print "missing babelbin (babel-config)"
        if not self.paletteAlias:
            print "paletteAlias missing"
        if not self.prefix:
            print "prefix missing"
        if not self.impall:
            print "missing impall"
        if not self.imppart:
            print "missing imppart"
        if not self.extends:
            print "missing extends"
        if not self.requiredSymbols:
            print "missing requiredSymbols"
        if not self.alias:
            print "missing alias"
        if not self.sidlsource:
            print "missing sidlsource"
        if not self.clients:
            print "missing clients"
        else:
            for i in self.clients.keys():
                self.clients[i].nonecheck(i)
        if not self.impl:
            print "missing impl"
        else:
            if self.kind in ["class","component"]:
                self.impl.nonecheck()
        if not self.ports:
            print "missing ports"
        else:
            if self.kind in ["component"]:
                self.ports.nonecheck()
        print "DEPL COMPLETED"
      
         
    def __init__(self):
        self.symbol = None # sidl symbol
        self.kind = None; # one of enum, struct, class, interface
        self.babelbin = "/fixme/babel-config"
        self.filename = None ; # must always be set for a readable/writable symbol xml description
        self.uuid = "fixmeuuid"
        self.paletteAlias = None
        self.prefix = None
        self.sidlsource = None

# library description
        self.impall = []		; # anything appearing in implements-all in sidl
        self.imppart = []		; # anything appearing in implements in sidl
        self.extends = []		; # anything appearing in extends in sidl
        self.requiredSymbols = []	; # any other nonprimitive symbol anywhere in the sidl or impl
        self.clients = dict()		; # binding details
        for i in ["ior", "c", "cxx", "java", "python", "f90", "f77"]:
            self.clients[i] = Client(i)	

        # component/port  only
        self.alias = None


        # [] in component subclass. symbols used but not visible to sidl.
        # this is the union of anything used privately and everything
        # found in ports.
        # self.allSymbols = None

        # impl only
        self.impl = Server()

        # component impl only
        self.ports = PortData()

        # dom subtree
        self.dom = None

        # options handling. doesn'tbelonghere.
        self.debug = False
        self.warnFatal = False
        self.options = None
        self.args = None
        self.parser = None

        return

    def getPrefix(self):
        return self.prefix

    def setPrefix(self,prefix):
        # if self.prefix and prefix != self.prefix:
        #     raise RuntimeError, "prefix cannot be redefined from "+self.prefix +" to " + prefix
        self.prefix = prefix

    def getPortData(self):
        return self.ports

    def getPortInfo(self, direction):
        """return list of tuples containing info about ports (type, name [,delegatetype])
           given the direction (uses, provides, delegates)."""
        if self.ports:
            return self.ports.getPortInfoByKind(direction)

    def getPortPropertyNames(self, portname):
        p = self.ports.getPort(portname)
        if p:
            plist = p.properties.keys()
            return plist
        return None
            
    def getPortPropertyValue(self, portname, key):
        """@return type, value for a given propertykey and port instance name, or None"""
        if self.ports:
            return self.ports.getPortPropByName(portname, key)
        return None

    def getServer(self):
        return self.impl

    def getClient(self, lang):
        return self.clients[lang]

    def setAlias(self, alias):
        self.alias = alias

    def getAlias(self):
        if not self.alias:
            return self.symbol
        return self.alias

    def getUuid(self):
        return self.uuid

    def setUuid(self, id):
        self.uuid = id

    def getBabel(self):
        return self.babelbin

    def setBabel(self, b):
        self.babelbin = b

    def setSidlSource(self, src):
        self.sidlsource = src

    def getSidlSource(self):
        return self.sidlsource

    def removePorts(self, names):
        if names:
            for i in names:
                self.ports.removePort(i)

    def addImplements(self, slist):
        """Add implements bases of a class"""
        self.imppart.extend(slist)
        x = list(sets.Set(self.imppart))
        self.imppart = x

    def addImplementsAll(self, slist):
        """Add implements-all bases of a class"""
        self.impall.extend(slist)
        x = list(sets.Set(self.impall))
        self.impall = x

    def addExtends(self, slist):
        """Add extends bases of a class or interface"""
        self.extends.extend(slist)
        x = list(sets.Set(self.extends))
        self.extends = x

    def addRequiredSymbols(self, slist):
        """Add other dependencies for methods"""
        if None in slist:
             raise RuntimeError, "none on slist in ARS"
        self.requiredSymbols.extend(slist)
        x = list(sets.Set(self.requiredSymbols))
        self.requiredSymbols = x

    def removeRequiredSymbols(self, slist):
        if not slist:
            return
        x=[]
        for i in self.requiredSymbols:
            if not i in slist:
                x.append(i)
        self.requiredSymbols = x
    
    def removeExtends(self, impall, imppart, extendslist):
        if extendslist:
            x=[]
            for i in self.extends:
                if not i in extendslist:
                    x.append(i)
            self.extends = x
        if imppart:
            x=[]
            for i in self.imppart:
                if not i in imppart:
                    x.append(i)
            self.imppart = x
        if impall:
            x=[]
            for i in self.impall:
                if not i in impall:
                    x.append(i)
            self.impall = x
    
    def getExtends(self):
        x= []
        x.extend(self.extends)
        return x
 
    def getImplementsAll(self):
        x= []
        x.extend(self.impall)
        return x
 
    def getImplements(self):
        x= []
        x.extend(self.imppart)
        return x
 
    def getRequiredSymbols(self):
        """Get all required symbols given + the port-required symbols."""
# This is computed result is needed because ports can be deleted and they
# must take their required types with them when deleted.
        a = self.ports.getSymbolsRequired()
        x= []
        x.extend(self.requiredSymbols)
        if a and len(a) > 0:
            x.extend(a)
        y = list(sets.Set(x))
        return y

    def addPorts(self, uses, provides, delegates):
        if self.debug:
            print "DEFINING PORTS", uses , provides, delegates
        if provides:
            for i in provides:
                pprops = None
                if len(i) == 2:
                    (pname , ptype) = i
                if len(i) == 3:
                    (pname , ptype, pprops) = i
                p = Port("provides", pname, ptype, pprops)
                self.ports.addPort(p)
        if uses:
            for i in uses:
                pprops = None
                if len(i) == 2:
                    (pname , ptype) = i
                if len(i) == 3:
                    (pname , ptype, pprops) = i
                p = Port("uses", pname, ptype, pprops)
                self.ports.addPort(p)
        if delegates:
            for i in delegates:
                pprops = None
                if len(i) == 3:
                    (pname , ptype, dtype) = i
                if len(i) == 4:
                    (pname , ptype, dtype, pprops) = i
                p = Port("delegates", pname, ptype, pprops, dtype)
                self.ports.addPort(p)

    def setPortProperties(self, padd, pdelete):
        self.ports.setProperties(padd, pdelete)
     
    def fatalError(self, msg = ""):
        print >> sys.stderr, "Error:", msg
        sys.exit(1)

    def usageError(self, msg = ""):
        print >> sys.stderr, "Error:", msg
        self.parser.print_help(sys.stderr)
        print >> sys.stderr, "Error:", msg
        sys.exit(1)

    def warning(self, msg=""):
        print >> sys.stderr, "Warning:", msg
        if self.warnFatal:
            sys.exit(1)

