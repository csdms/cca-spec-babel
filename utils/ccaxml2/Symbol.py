from xml.dom import minidom, Node
import sys
import sets
import os
import socket
import datetime
from Deployment import Deployment, Port

##########################################################################3

class SymbolPropertyHelper:
    """ utils for parameters of typemaps. Note that sidl array doesn't work well
as xml attributes, so the enum names from cca.sidl are used."""
    def ccaType( utype):
        """convert some sidl,c, fortran primitives to cca enum Type"""
        cca = "UNKNOWNTYPE"
        if utype.lower() in ['bool', 'boolean', 'logical']:
            cca = 'Bool'
        elif utype.lower() in ['int', 'integer', 'integer*4']:
            cca = 'Int'
        elif utype.lower() in ['long', 'long integer', 'integer*8']:
            cca = 'Long'
        elif utype.lower() in ['float', 'real', 'real*4', 'single']:
            cca = 'Float'
        elif utype.lower() in ['double', 'long double', 'real*8', 'double precision']:
            cca = 'Double'
        elif utype.lower() in ['fcomplex','complex<float>']:
            cca = 'Fcomplex'
        elif utype.lower() in ['dcomplex','complex<double>']:
            cca = 'Dcomplex'
        elif utype.lower() in ['string']:
            cca = 'String'
        elif utype.lower() in ["array<bool>", "boolarray", "booleanarray"]:
            cca = 'BoolArray'
        elif utype.lower() in ["array<int>", "intarray"]:
            cca = 'IntArray'
        elif utype.lower() in ["array<long>", "longarray"]:
            cca = 'LongArray'
        elif utype.lower() in ["array<float>", "floatarray"]:
            cca = 'FloatArray'
        elif utype.lower() in ["array<double>", "doublearray"]:
            cca = 'DoubleArray'
        elif utype.lower() in ["array<dcomplex>", "dcomplexarray"]:
            cca = 'DcomplexArray'
        elif utype.lower() in ["array<fcomplex>", "fcomplexarray"]:
            cca = 'FcomplexArray'
        elif utype.lower() in ["array<string>", "stringarray"]:
            cca = 'StringArray'

        return cca

    ccaType = staticmethod(ccaType)

    def sidlType( utype):
        """convert assorted strings to sidl types"""
        sidl = "UNKNOWNTYPE"
        if utype.lower() in ['bool', 'boolean', 'logical']:
            sidl = 'bool'
        elif utype.lower() in ['int', 'integer', 'integer*4']:
            sidl = 'int'
        elif utype.lower() in ['long', 'long integer', 'integer*8']:
            sidl = 'long'
        elif utype.lower() in ['float', 'real', 'real*4', 'single']:
            sidl = 'float'
        elif utype.lower() in ['double', 'long double', 'real*8', 'double precision']:
            sidl = 'double'
        elif utype.lower() in ['fcomplex','complex<float>']:
            sidl = 'fcomplex'
        elif utype.lower() in ['dcomplex','complex<double>']:
            sidl = 'dcomplex'
        elif utype.lower() in ['string']:
            sidl = 'string'
        elif utype.lower() in ["array<bool>", "boolarray", "booleanarray"]:
            sidl = 'BoolArray'
        elif utype.lower() in ["array<int>", "intarray"]:
            sidl = 'array<int>'
        elif utype.lower() in ["array<long>", "longarray"]:
            sidl = 'array<long>'
        elif utype.lower() in ["array<float>", "floatarray"]:
            sidl = 'array<float>'
        elif utype.lower() in ["array<double>", "doublearray"]:
            sidl = 'array<double>'
        elif utype.lower() in ["array<dcomplex>", "dcomplexarray"]:
            sidl = 'array<dcomplex>'
        elif utype.lower() in ["array<fcomplex>", "fcomplexarray"]:
            sidl = 'array<fcomplex>'
        elif utype.lower() in ["array<string>", "stringarray"]:
            sidl = 'array<string>'

        return sidl

    sidlType = staticmethod(sidlType)

##########################################################################3

class Symbol:
    """This is the critter that knows most of the likely to change xml format details
and the definition methods. The to create non-cca-toolkit
symbols is to first define the nearest interface, class, port or component
and then use the set methods to change those elements which vary from the toolkit
defaults."""
    def __init__(self, filename, symbol=None, debug=False):
        self.filename = filename; # source
        self.debug = debug
        self.deployment = None	; # metadata
        self.symbol = symbol	; # full sidl name
        self.node = None	; # dom element

# handy constants
        self.binlangs = ["c", "cxx", "f77", "f90"]
        self.vmlangs = ["java", "python"]
        self.alllangs = []
        self.alllangs += self.binlangs
        self.alllangs += self.vmlangs

    def getFilename(self):
        """return name of the file this symbol comes from."""
        return self.filename

    def getSidlName(self):
        """return the sidl symbol."""
        return self.symbol

    def getSidlFile(self):
        """return the sidl file defining the symbol type."""
	return self.prefixExpand(self.deployment.getSidlSource())

    def getKind(self):
        """return the entity kind string."""
        return self.deployment.kind

    def getDependenceSymbols(self):
        x=self.deployment.getExtends()
        y=self.deployment.getRequiredSymbols()
        z=[]
        if len(x) > 0:
            z.extend(x)
        if len(y) > 0:
            z.extend(y)
        if len(z) > 0:
            w = list(sets.Set(z))
        else:
            w = []
        return w

    def getServerLib(self, linkage):
        """@param linkage  one of (static, shared, libtool).
@return full path of the lib or "unsupported" if server doesn't exist or empty string if
linkage makes no sense, as for python and java.
"""
        result = self.deployment.getServer().getLib(linkage)
        result2 = self.deployment.getServer().getImplLibFlags(linkage)
        if not result:
            result = ""
	result = self.prefixExpand(result)
        return result+result2

    def getClientLib(self, lang, linkage):
        """@param lang the client binding of interest.
@param linkage one of (static, shared, libtool).
@return full path of the lib or "unsupported" if the combination is unsupported.
"""
        return self.prefixExpand(self.deployment.getClient(lang).getLib(linkage))

    def getClientSymbolPath(self, lang):
        """Return pythonpath, classpath, or include dir for the client binding of the language given.
@param lang the given language.
@return directory or "unsupported" if that binding is not supported.
"""
        return self.prefixExpand(self.deployment.getClient(lang).getSymbolPath())

    def ia_internal(self):
        """All the methods with names starting a-h are the expected use 
methods. The methods named i-z are primarily internal use only.
"""

    def prefixExpand(self, val):
        if val and val[0] == '%':
            prefix=self.deployment.getPrefix()
            result = val.replace("%prefix%",prefix)
            return result
        return val

    ######## data creation routines for toolkit style.
    def intMakeUUID(self):
        """Generate a uuid default."""
        hostName="localhost.err"
        try:
           hostName = socket.gethostbyaddr(socket.gethostname())[0]
        except:
           pass
        userName = os.environ.get('USER')
        timeStamp = datetime.datetime.now().isoformat('|')
        result = userName+'@'+hostName+':'+self.symbol+':'+timeStamp 
        return result

    def intDefineImpl(self, impl, impall, imppart, libbasename, shared, static, libtool, include, libdir, classpath, pythonpath, extraShared, extraStatic, extraLibtool, extraCompiling, sharedSuffix):
        """Define things only impls have."""
        self.deployment.kind = "class"
        self.deployment.addImplementsAll(impall)
        self.deployment.addImplements(imppart)
        libstart = os.path.join(libdir,  "lib" + libbasename)
        desc = self.deployment.getServer()
        desc.setLang(impl)
        if impl in self.binlangs:
            if static:
               staticlib = libstart + ".a"
            else:
               staticlib = None
            if shared:
               sharedlib = libstart + sharedSuffix
            else:
               sharedlib = None
            if libtool:
               libtoollib = libstart + ".la"
            else:
               libtoollib = None
            desc.setLibs(impl, libtoollib, sharedlib, staticlib)
            desc.setSymbolPath(impl, include)
        if impl == "java":
            desc.setSymbolPath(impl, classpath)
        if impl == "python":
            desc.setSymbolPath(impl, pythonpath)
        desc.setExtraFlags(impl, extraShared, extraStatic, extraLibtool, extraCompiling)
        desc.finish()


    def intDefineCommon(self, sidlsource, libbasename, clients, shared, static, libtool, include, libdir, classpath, pythonpath, extends, requiredSymbols, prefix, babelbin, sharedSuffix):
        """ define the things common to class, interface, component, and port"""
        self.deployment.symbol = self.symbol
        self.deployment.sidlsource = sidlsource
        self.deployment.kind = "interface"
        self.deployment.uuid = self.intMakeUUID()
        self.deployment.setBabel(babelbin)
        self.deployment.setPrefix(prefix)
        
        self.deployment.addExtends(extends)
        self.deployment.addRequiredSymbols(requiredSymbols)
        libstart = os.path.join(libdir,  "lib" + libbasename + "-")
        for i in self.alllangs:
            if not i in clients:
                client = self.deployment.getClient(i)
                client.ignore = True
        for i in clients:
            client = self.deployment.getClient(i)
            if i in self.binlangs:
                if static:
                   staticlib = libstart + i + ".a"
                else:
                   staticlib = None

                if shared:
                   sharedlib = libstart + i + sharedSuffix
                else:
                   sharedlib = None

                if libtool:
                   libtoollib = libstart + i + ".la"
                else:
                   libtoollib = None

                client.setLibs(i, libtoollib, sharedlib, staticlib)
                client.setSymbolPath(i, include)

            if i == "java":
                client.setSymbolPath(i, classpath)
            if i == "python":
                client.setSymbolPath(i, pythonpath)
        for i in self.alllangs:
            self.deployment.clients[i].finish()
        for i in self.alllangs:
            if not self.deployment.clients[i].check(True):
                pass ; # could raise something here...

    def defineClass(self, impl, sidlsource, clients, libbasename, shared, static, libtool,
            include, libdir, classpath, pythonpath, requiredSymbols, impall, imppart, extends,
            extraShared, extraStatic, extraLibtool, extraCompiling, prefix, babelbin, sharedSuffix=".so"
    ):
        """convenience routine for defining a class in cca toolkit style"""
        self.deployment = Deployment()
        self.intDefineCommon(
            sidlsource=sidlsource,
            libbasename=libbasename,
            clients=clients,
            shared=shared,
            static=static,
            libtool=libtool,
            include=include,
            libdir=libdir,
            classpath=classpath,
            pythonpath=pythonpath,
            extends=extends,
            requiredSymbols=requiredSymbols,
            prefix=prefix,
            babelbin=babelbin,
            sharedSuffix=sharedSuffix)

        self.intDefineImpl(impl=impl,
            impall=impall,
            imppart=imppart,
            libbasename=libbasename,
            shared=shared, static=static, libtool=libtool,
            include=include,
            libdir=libdir,
            classpath=classpath,
            pythonpath=pythonpath,
            extraShared=extraShared,
            extraStatic=extraStatic,
            extraLibtool=extraLibtool,
            extraCompiling=extraCompiling,
            sharedSuffix=sharedSuffix)

    def defineInterface(self, sidlsource, clients, libbasename, shared, static, libtool,
            include, libdir, classpath, pythonpath, requiredSymbols, extends, prefix, babelbin,
            sharedSuffix=".so"
    ):
        """convenience routine for defining an interface in cca toolkit style"""
        self.deployment = Deployment()
        self.intDefineCommon(
            sidlsource=sidlsource,
            libbasename=libbasename,
            clients=clients,
            shared=shared,
            static=static,
            libtool=libtool,
            include=include,
            libdir=libdir,
            classpath=classpath,
            pythonpath=pythonpath,
            extends=extends,
            requiredSymbols=requiredSymbols,
            prefix=prefix,
            babelbin=babelbin,
            sharedSuffix=sharedSuffix)

    def definePort(self,
        babelbin,
        sidlsource,
        prefix,
        project,
        libbasename,
        clients,
        shared, static, libtool,
        requiredSymbols=[],
        extends=[],
        alias=None):
        """Wrapper for the common case of toolkit compliant Port install layout.
@param babelbin full path to babel-config this is generated from.
@param sidlsource location of symbol in sidl
@param prefix root of installation
@param project project name used in include path per cca toolkit.
@param libbasename name without lib prefix, language, or link style suffixes.
@param clients list of bindings supported.
@param shared True if shared is supported.
@param static True if static is supported.
@param libtool True if libtool is supported.
@param prefix Used to derive includedir, libdir, classpath, pythonpath
@param requiredSymbols List of extra sidl symbols required.
@param extends non-cca bases from which the symbol derives.
"""
        symlist = requiredSymbols
        defprefix="%prefix%"
        if not "gov.cca.Port" in extends:
            extends += ["gov.cca.Port"]
        pyver = sys.version[:3]
        pypath = os.path.join(defprefix, "lib","python"+pyver,"site-packages")
        self.defineInterface(sidlsource=sidlsource, clients=clients, libbasename=libbasename,
                    shared=shared, static=static, libtool=libtool,
                    include=os.path.join(defprefix,"include",project),
                    libdir=os.path.join(defprefix,"lib"),
                    classpath=os.path.join(defprefix,"lib","java"),
                    pythonpath=pypath,
                    requiredSymbols=symlist,
                    extends=extends,
                    prefix=prefix, babelbin=babelbin)
        if not alias:
            alias=self.symbol
        self.deployment.setAlias(alias)

    def defineToolkitComponent(self,
         impl,
         babelbin,
         sidlsource,
         prefix,
         project,
         libbasename,
         clients,
	 shared, static, libtool,
         usesports, 
         providesports,
         delegatesports,
         requiredSymbols=[],
         impall=[],
         imppart=[],
         extends=[],
         extraShared="",
         extraStatic="",
         extraLibtool="",
         extraCompiling="",
         alias=None):
        """Wrapper for the common case of toolkit compliant install layout.
@param impl language of the implementation
@param prefix root install dir.
@param project project name used in include path per cca toolkit.
@param libbasename name without lib prefix, language, or link style suffixes.
@param clients list of bindings supported.
@param shared True if shared is supported.
@param static True if static is supported.
@param libtool True if libtool is supported.
@param prefix Used to derive includedir, libdir, classpath, pythonpath
@param usesports List of (instancename, typename, [,optional property dict]) tuples
@param providesports List of (instancename, typename, [,optional property dict]) tuples
@param delegatesports List of (instancename, typename, delegate typename, [,optional property dict]) tuples
@param requiredSymbols List of extra sidl symbols required.
@param extends non-cca bases from which the symbol derives.
@param extraShared extra (non-sidl-based) shared libraries/flags needed privately.
@param extraStatic extra (non-sidl-based) static libraries/flags needed privately.
@param extraLibtool extra (non-sidl-based) libtool libraries/flags needed privately.
@param extraCompiling extra (non-sidl-based) include/D flags needed to digest headers.
"""
        symlist = requiredSymbols
        defprefix="%prefix%"
        if not "gov.cca.Component" in extends:
            extends += ["gov.cca.Component"]
        if not "gov.cca.ComponentRelease" in extends:
            extends += ["gov.cca.ComponentRelease"]
        if providesports:
            for i in providesports:
                symlist.append(i[1])
        if usesports:
            for i in usesports:
                symlist.append(i[1])
        if delegatesports:
            for i in delegatesports:
                print i
                symlist.append(i[1])
                if len(i) < 3 or not i[2]:
                    pass
                else:
                    symlist.append(i[2])
                    print "appended", i[2]
        pyver = sys.version[:3]
        pypath = os.path.join(defprefix,"lib","python"+pyver,"site-packages")
        self.defineClass(impl=impl, sidlsource=sidlsource, clients=clients, libbasename=libbasename,
                    shared=shared, static=static, libtool=libtool,
                    include=os.path.join(defprefix,"include",project),
                    libdir=os.path.join(defprefix,"lib"),
                    classpath=os.path.join(defprefix,"lib","java"),
                    pythonpath=pypath,
                    requiredSymbols=symlist,
                    impall=impall, imppart=imppart, 
                    extends=extends, 
                    extraShared=extraShared,
                    extraStatic=extraStatic,
                    extraLibtool=extraLibtool,
                    extraCompiling=extraCompiling,
                    prefix=prefix,
                    babelbin=babelbin)
        self.deployment.addPorts(usesports, providesports, delegatesports)
        if not alias:
            alias=self.symbol
        self.deployment.setAlias(alias)

    ######## routines to change items from their current or default values once defined.

    def changeClientLibs(self, lang, llib, dlib, slib):
        """ Change metadata for libs after entity is defined. """
        client = self.deployment.getClient(lang)
        if not client.ignore:
            if self.debug:
                print "CHANGE dlib:",dlib
            client.setLibs(lang, llib, dlib, slib)

    def changeClientSymbolPath(self, lang, path):
        """ Change metadata for include/pythonpath/classpath after class is defined. """
        client = self.deployment.getClient(lang)
        if not client.ignore:
                client.setSymbolPath(lang, path)

    def changeServerLibs(self, llib, dlib, slib):
        """ Change metadata for libs after class is defined. """
        client = self.deployment.getServer()
        if self.debug:
            print "CHANGE SVR dlib:",dlib
        client.setLibs(client.getLang(), llib, dlib, slib)

    def changeServerSymbolPath(self, path):
        """ Change the metadata for includes/pythonpath/javapath """
        client = self.deployment.getServer()
        client.setSymbolPath(client.getLang(), path)

    def changeUuid(self, id):
        """ Change metadata uuid after class is defined """
        self.deployment.setUuid(id)

    def changeBabel(self, babelbin):
        """ Change metadata babelbin after class is defined """
        self.deployment.setBabel(babelbin)

    def changePrefix(self, prefix):
        """ Change metadata prefix after class is defined (allowed if redundant) """
        self.deployment.setPrefix(prefix)

    def changeAlias(self, alias):
        """ Change metadata alias after class is defined """
        self.deployment.setAlias(alias)

    def changePorts(self, usesports, providesports, delegatesports):
        """add more ports.
@param usesports: list of tuples where each is (type, name) or
(type, name, propertydictionary)
@param providesports: as usesports.
@param delegatesports: (type, name, delegtype, propertydictionary)
"""
        self.deployment.addPorts(usesports, providesports, delegatesports)

    def changePortProperties(self, portprops, portpropsdelete):
        """@param portprops list of 4-tuples (port, prop, type, value)
@param portpropsdelete list of 2-tuples (port, prop)
"""
        self.deployment.setPortProperties(portprops, portpropsdelete)

    def deletePorts(self, names):
        """remove named ports from component"""
        self.deployment.removePorts(names)

    def changeSymbolDependences(self, impall, imppart, extends, required):
        """add to inheritance and interface/internally used dependence symbols."""
        self.deployment.addImplementsAll(impall)
        self.deployment.addImplements(imppart)
        self.deployment.addExtends(extends)
        self.deployment.addRequiredSymbols(required)

    def deleteSymbolDependences(self, impall, imppart, extends, required):
        """remove inheritance and interface/internally used symbols dependence."""
        self.deployment.removeExtends( impall, imppart, extends)
        self.deployment.removeRequiredSymbols(required)

    ######## DOM reading routines to load data structure

    def intReadUniqueChildElement(self, node, childname):
        """Find unique named child, and if it has a text value, its value.
@return (value, childnode), where (None , None) if child or text is missing.
@param node scope of search
@param childname unique tag to find
"""
        childlist = node.getElementsByTagName(childname)
        if len(childlist) == 0:
            return (None, None)
        if len(childlist) > 1:
            raise RuntimeError , "Extra " + childname + " in "+ self.filename
        child = childlist[0]
        if child.hasChildNodes():
            for n in child.childNodes:
                if n.nodeType == Node.TEXT_NODE:
                    value = n.data.strip()
                    return (value, child)
            return (None, child)
        return (None, None)

    def readSymbols(self,n,d):
        """Load base and required symbols from xml to deployment data.
@param n dom Node
@param d Deployment data"""
        if not n or not d:
            return

        basetag="sidlImplementsAll"
        (bstring, cn) = self.intReadUniqueChildElement(n, basetag)
        if bstring and len(bstring) > 0:
            extends = bstring.split(",")
            clean = []
            for i in extends:
                clean.append(i.strip())
            d.addImplementsAll(clean)

        basetag="sidlImplements"
        (bstring, cn) = self.intReadUniqueChildElement(n, basetag)
        if bstring and len(bstring) > 0:
            extends = bstring.split(",")
            clean = []
            for i in extends:
                clean.append(i.strip())
            d.addImplements(clean)

        basetag="sidlExtends"
        (bstring, cn) = self.intReadUniqueChildElement(n, basetag)
        if bstring and len(bstring) > 0:
            extends = bstring.split(",")
            clean = []
            for i in extends:
                clean.append(i.strip())
            d.addExtends(clean)

        basetag="sidlOtherSymbols"
        (rstring, cn) = self.intReadUniqueChildElement(n, basetag)
        if rstring and len(rstring) > 0:
            required = rstring.split(",")
            clean = []
            for i in required:
                clean.append(i.strip())
            d.addRequiredSymbols(clean)

        basetag="sidlsource"
        (sstring, cn) = self.intReadUniqueChildElement(n, basetag)
        if sstring:
            d.sidlsource = sstring

    def intReadPaths(self, node, lang, client):
        """load include/lib/class/python paths"""
        if lang in self.binlangs:
            (path, c) = self.intReadUniqueChildElement(node, "include")
            client.IncludePath = path
            (path, c) = self.intReadUniqueChildElement(node, "libtool")
            client.LibtoolLib = path
            (path, c) = self.intReadUniqueChildElement(node, "static")
            client.StaticLib = path
            (path, c) = self.intReadUniqueChildElement(node, "shared")
            client.SharedLib = path
        if lang == "java":
            (path, c) = self.intReadUniqueChildElement(node, "classpath")
            client.ClassPath = path
        if lang == "python":
            (path, c) = self.intReadUniqueChildElement(node, "pythonpath")
            client.PythonPath = path

    def intReadClient(self, node, lang, client):
        """Load client include/lib from xml info"""
        if not client or not node or not lang:
            return
        basetag = "client_" + lang
        (dummy, cn) = self.intReadUniqueChildElement(node, basetag)
        if cn and cn.getAttribute("unsupported") != "true":
            self.intReadPaths(cn, lang, client)

    def intReadServer(self, node, server):
        """update server from xml info"""
        if not server:
            return
        basetag = "server"
        (dummy, cn) = self.intReadUniqueChildElement(node, basetag)
        if not cn:
            return
        lang = cn.getAttribute("language")
        self.intReadPaths(cn, lang, server)
        (comp, c) = self.intReadUniqueChildElement(cn, "compilingDependenciesFlags")
        (shared, c) = self.intReadUniqueChildElement(cn, "sharedDependenciesLibs")
        (static, c) = self.intReadUniqueChildElement(cn, "staticDependenciesLibs")
        (libtool, c) = self.intReadUniqueChildElement(cn, "libtoolDependenciesLibs")
        server.setExtraFlags(lang, shared, static, libtool, comp)

    def intReadProperty(self, node):
        """update property from xml info"""
        pname = node.getAttribute("name")
        ptype = node.getAttribute("type")
        value = ""
        for n in node.childNodes:
            if n.nodeType == Node.TEXT_NODE:
                value = n.data.strip()
        return (pname, ptype, value)

    def intReadPort(self, node, direction):
        """update port from xml info"""
        if not node:
            return None
        nname = node.getAttribute("name")
        ntype = node.getAttribute("type")
        dtype = node.getAttribute("delegateType")
        childlist = node.getElementsByTagName("property")
        if len(dtype) < 3:
            dtype=None
        else:
            direction="delegates"
        p = Port(direction, nname, ntype, None, dtype)
        if childlist and len(childlist) > 0:
            for cn in childlist:
                (pname, ptype, value) = self.intReadProperty(cn)
                p.addProperty(pname, ptype, value)
        return p

    def intReadPortData(self, node, portdata):
        """update portdata from xml info"""
        if not portdata:
            return
        basetag = "ports"
        (dummy, pn) = self.intReadUniqueChildElement(node, basetag)
        if not pn:
            return
        for direction in ["provides", "uses","delegates"]:
            childlist = pn.getElementsByTagName(direction)
            for cn in childlist:
                p = self.intReadPort(cn, direction)
                portdata.addPort(p)

    def intReadBase(self,n,kind):
        """Read common bits from xml into data structures."""
        self.node = n
        d = Deployment()
        d.kind = kind
        self.deployment = d
        self.symbol = n.getAttribute("name")
        d.setAlias(n.getAttribute("paletteAlias"))
        d.setPrefix(n.getAttribute("prefix"))
        d.setUuid(n.getAttribute("uniqueID"))
        d.setBabel(n.getAttribute("babelConfig"))
        d.setSidlSource(n.getAttribute("sidlsource"))
        self.readSymbols(n,d)
        for i in self.alllangs:
            client = d.getClient(i)
            self.intReadClient(n, i, client)
        if d.kind == "class":
            server = d.getServer()
            self.intReadServer(n, server)
            if "gov.cca.Component" in self.deployment.extends:
                self.intReadPortData(n, d.getPortData())

    def readInterface(self,i, kind=None):
        """Reader of interfaceDeployment from xml into data structures"""
        if not i:
            return
        if not kind:
            kind = "interface"
        self.intReadBase(i,kind)
        if self.debug:
            print "found INTERFACE ", self.symbol

    def readPort(self,i):
        if not i:
            return
        """Reader of portDeployment from xml into data structures."""
        self.readInterface(i,"port")
        if self.debug:
            print "found PORT ", self.symbol

    def readClass(self,i, kind=None):
        if not i:
            return
        if not kind:
            kind = "class"
        self.intReadBase(i,kind)
        if self.debug:
            print "found CLASS ", self.symbol

    def readComponent(self,i):
        if not i:
            return
        self.readClass(i,"component")
        if self.debug:
            print "found COMPONENT ", self.symbol

    ######## DOM creation/update routines. used after all data is created/set.

    # private. here is where we should add in scl info when need be.
    def verifyNode(self, doc):
        """Create the named Deployment node under unique libInfo tag"""
        if not self.node:
            xmlkind = self.deployment.kind + "Deployment"
            elts = doc.getElementsByTagName(xmlkind)
            for i in elts:
                n = i.getAttribute("name")
                if n and n == self.symbol:
                    raise RuntimeError , "Unexpected " +xmlkind+ " found for "+self.symbol
            elts = doc.getElementsByTagName("libInfo")
            if len(elts) != 1:
                raise RuntimeError , "Unexpected libInfo in "+ self.filename
            li = elts[0]
            node = doc.createElement( xmlkind )
            node.setAttribute("name", self.symbol)
            self.node = li.appendChild(node)
            

    def verifyProperty(self, doc, node, key, vpair):
        """create or update key-typed_value pair in dom."""
        (ktype, kvalue) = vpair
        ktype = SymbolPropertyHelper.ccaType(ktype)
        kvalue = str(kvalue).strip()
        childlist = node.getElementsByTagName("property")
        child = None
        for i in childlist:
            if i.getAttribute("name") == key:
                child = i
                break
        if not child:
            child = doc.createElement("property")
            child = node.appendChild(child)
        child.setAttribute("name", key)
        child.setAttribute("type", ktype)
        stored = False
        for n in child.childNodes:
            if n.nodeType == Node.TEXT_NODE:
                n.data = kvalue
                stored = True
        if not stored:
            text = doc.createTextNode(kvalue)
            child.appendChild(text)
        return child
 

    def verifyPort(self, doc, n, port):
        """create or update uses or provides port in dom"""
        kind = port.getDirection()
        name = port.getName()
        if kind == "delegates":
            dtype = port.getDelegateType()
            kind="provides"
        else:
            dtype = None
        props =  port.getProperties()
        childlist = n.getElementsByTagName(kind)
        child = None
        for i in childlist:
            if i.getAttribute("name") == name:
                child = i
                break
        if not child:
            child = doc.createElement(kind)
            child = n.appendChild(child)
        child.setAttribute("name", name)
        child.setAttribute("type", port.getType())
        if dtype:
            child.setAttribute("delegateType", dtype)
        if len(props) > 0:
            for (key, value) in props.iteritems():
                # fixme: clear out old properties
                self.verifyProperty(doc, child, key, value)


    def verifyUniqueChildElement(self, doc, node, childname, value=None):
        """create or update tag and (if value given) text in dom"""
        childlist = node.getElementsByTagName(childname)
        if len(childlist) == 0:
            child = doc.createElement(childname)
            child = node.appendChild(child)
        else:
            if len(childlist) > 1:
                raise RuntimeError , "Extra " + childname + " in "+ self.filename
            child = childlist[0]
        if value:
            stored = False
            for n in child.childNodes:
                if n.nodeType == Node.TEXT_NODE:
                    n.data = value.strip()
                    stored = True
            if not stored:
                text = doc.createTextNode(value.strip())
                child.appendChild(text)
        return child

    def updateDomPaths(self, doc, lang, cn, client):
        """create or update include and lib paths in dom"""
        if lang in self.binlangs:
            self.verifyUniqueChildElement(doc, cn, "include", client.IncludePath)
            self.verifyUniqueChildElement(doc, cn, "libtool", client.LibtoolLib)
            self.verifyUniqueChildElement(doc, cn, "static", client.StaticLib)
            self.verifyUniqueChildElement(doc, cn, "shared", client.SharedLib)
        if lang == "java":
            self.verifyUniqueChildElement(doc, cn, "classpath", client.ClassPath)
        if lang == "python":
            self.verifyUniqueChildElement(doc, cn, "pythonpath", client.PythonPath)
            

    def updateDomSymbols(self, doc):
        """create or update base and required sidl dependency symbols in dom"""
        base = self.deployment.getExtends()
        required = self.deployment.getRequiredSymbols()
        ia = self.deployment.getImplementsAll()
        ip = self.deployment.getImplements()
        # print self.filename
        # print self.symbol
        # print "BASE",base
        # print "REQD",required
        rshort=[]
        for i in required:
            if not i in base and not i in ia and not i in ip:
                rshort.append(i)

        iastring=",".join(ia)
        #for i in ia:
        #    iastring += i+", "
        #iastring = iastring.strip(", ")

        ipstring=",".join(ip)
        #for i in ip:
        #    ipstring += i+", "
        #ipstring = ipstring.strip(", ")

        bstring=",".join(base)
        #for i in base:
        #    bstring += i+", "
        #bstring = bstring.strip(", ")

        rstring=",".join(rshort)
        #for i in rshort:
        #    rstring += i+", "
        #rstring = rstring.strip(", ")

        n = self.node
        if len(ipstring) > 0:
            basetag="sidlImplements"
            self.verifyUniqueChildElement(doc, n, basetag, ipstring)
        if len(iastring) > 0:
            basetag="sidlImplementsAll"
            self.verifyUniqueChildElement(doc, n, basetag, iastring)
        if len(bstring) > 0:
            basetag="sidlExtends"
            self.verifyUniqueChildElement(doc, n, basetag, bstring)
        if len(rstring) > 0:
            basetag="sidlOtherSymbols"
            self.verifyUniqueChildElement(doc, n, basetag, rstring)

        if self.deployment.sidlsource:
            self.verifyUniqueChildElement(doc, n, "sidlsource", self.deployment.sidlsource)

    def updateDomClient(self, doc, lang, client):
        """create or update client info in the dom"""
        if not client:
            return
        n = self.node
        basetag = "client_" + lang
        cn = self.verifyUniqueChildElement(doc, n, basetag)
        if not client.ignore:
            self.updateDomPaths(doc, lang, cn, client)
        else:
            cn.setAttribute("unsupported","true")

    def verifyScl(self, doc, server):
        pass
            
    def updateDomServer(self, doc, server):
        """create or update dom from server info"""
        if not server:
            return
        n = self.node
        basetag = "server"
        cn = self.verifyUniqueChildElement(doc, n, basetag)
        cn.setAttribute("language", server.getLang())
        self.updateDomPaths(doc, server.getLang(), cn, server)
        if server.nativeCompilingFlags:
            self.verifyUniqueChildElement(doc, cn, "compilingDependenciesFlags", server.nativeCompilingFlags)
        if server.nativeSharedFlags:
            self.verifyUniqueChildElement(doc, cn, "sharedDependenciesLibs", server.nativeSharedFlags)
        if server.nativeStaticFlags:
            self.verifyUniqueChildElement(doc, cn, "staticDependenciesLibs", server.nativeStaticFlags)
        if server.nativeLibtoolFlags:
            self.verifyUniqueChildElement(doc, cn, "libtoolDependenciesLibs", server.nativeLibtoolFlags)
        self.verifyScl(doc, server)

    def updateDomPorts(self, doc, ports):
        """create or update dom from uses/provides port info"""
        if not ports:
            return
        if ports.getCount() < 1:
            return
        plist = ports.getPorts()
        n = self.node
        basetag = "ports"
        cn = self.verifyUniqueChildElement(doc, n, basetag)
        # FIXME delete all uses/provides elements below cn, then add current
        for i in plist:
            self.verifyPort(doc, cn, i)

    def noneCheck(self):
        self.deployment.nonecheck()

    def domUpdate(self, doc):
        """Update or create all info under doc for the Symbol.
@param doc the dom root (a document node). 
"""
        self.verifyNode(doc)
        self.node.setAttribute("paletteAlias",self.deployment.getAlias())
        self.node.setAttribute("prefix",self.deployment.getPrefix())
        self.node.setAttribute("uniqueID", self.deployment.getUuid())
        self.node.setAttribute("babelConfig", self.deployment.getBabel())
        self.updateDomSymbols(doc)
        for i in self.alllangs:
            client = self.deployment.getClient(i)
            self.updateDomClient(doc, i, client)
        if self.deployment.kind == "class":
            server = self.deployment.getServer()
            self.updateDomServer(doc, server)
            if "gov.cca.Component" in self.deployment.extends:
                ports = self.deployment.getPortData()
                self.updateDomPorts(doc, ports)

