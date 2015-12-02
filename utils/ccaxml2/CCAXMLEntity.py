import optparse
from xml.dom import minidom
import sys
import os
from ccagm import which

class CCAXMLEntity:
    """Class to support defining or modifying the metadata file
for a sidl symbol installation."""

    def __init__(self, kind, sidlname, opts):
        import Index, Symbol, File
        self.debug = opts.debug
        if self.debug:
            print sys.argv
        self.pathcheck = opts.pathcheck
        self.options = opts
        self.sidlname = sidlname
        self.kind = kind.lower()
        self.index = Index.Index()

        # missing feature-- need to check that symbol is not already in the
        # search path in another file and whine if it is there.
        deplpath = self.options.deplpath
        if not deplpath:
            deplpath=[]
        deplpath.append(os.environ.get("CCA_COMPONENT_PATH"))
        deplpath.append(os.environ.get("SIDL_DLL_PATH"))
        for i in deplpath:
            self.index.appendpath(i)
        self.index.scanpath()

        symnew=False
        if kind == "change":
            s = self.index.getSymbol(sidlname)
            if not s:
                self.fatalError("Symbol "+sidlname+" is not found in path: "+self.index.getPath())
            kind = s.getKind()
            self.filename = s.getFilename()
        else:
            if not opts.outfile or len(opts.outfile) < 1:
                self.filename = "./"+sidlname+"_depl.xml"
            else:
                self.filename = opts.outfile

            if not os.path.isfile(self.filename):
                self.file = File.File(self.filename, "new")
            else:
                self.file = File.File(self.filename)
                self.file.setChanged()
            self.index.addFile(self.filename, self.file)
            s = self.index.getSymbol(sidlname)
            if not s:
                self.file.insertSymbol(sidlname)
                s = Symbol.Symbol(self.filename, sidlname, self.debug)
                symnew=True

        self.process_opts(s, symnew)
        if self.debug:
            s.deployment.nonecheck()
        self.index.updateSymbol(s, self.pathcheck)

    def write(self):
        
        self.index.closeAll()
        
    def process_port_props(self):
        ptuples = []
        dtuples = []
        if self.options.portProperties:
            ptuples=[]
            for i in self.options.portProperties:
                 x= i.split("@")
                 if len(x) != 4:
                     self.fatalError("Expected PORTNAME@PROPNAME@TYPE@VALUE for --port-property. Got instead "+i)
                 ptuples.append(x)
        if self.options.deletePortProperties:
            for i in self.options.deletePortProperties:
                 x= i.split("@")
                 if len(x) != 2:
                     self.fatalError("Expected PORTNAME@PROPNAME for --delete-port-property. Got instead "+i)
                 dtuples.append(x)
        return (ptuples, dtuples)
                                      
    def process_ports(self, portinput, direction):
        result=[]
        if portinput:
            for i in portinput:
                plist=i.split("@")
                if len(plist) < 2:
                    self.fatalError(direction+ " port incorrectly defined: " + i)
                if len(plist) > 2 and direction != "Delegates":
                    self.warning(direction+" port extra modifiers ignored: " + "@".join(plist[2:]))
                if not "." in plist[0]:
                    self.warning(direction+" port type " + plist[0] + " does not appear to be a sidl type.")
                if direction == "Delegates" and len(plist) > 2 and not "." in plist[2]:
                    self.warning(direction+" port type " + plist[2] + " does not appear to be a sidl type.")
                if direction == "Delegates":
                    if len(plist) > 2:
                        result.append((plist[1], plist[0], plist[2]))
                    else:
                        result.append((plist[1], plist[0], plist[0]))
                else:
                    result.append((plist[1], plist[0]) )
        if self.debug:
            print "PORTS", result
        return result

    def process_deletes(self):
        """return names of ports to be removed"""
        names=[]
        if self.options.deletePorts:
            for i in self.options.deletePorts:
                for j in i.split(","):
                    names.append(j)
        return names

    def process_symbols(self):
        """return various bases and other symbols as lists."""
        impall=[]
        if self.options.impall:
            b=self.options.impall
            for i in b:
                for j in i.split(","):
                    impall.append(j)
        imppart=[]
        if self.options.imppart:
            b=self.options.imppart
            for i in b:
                for j in i.split(","):
                    imppart.append(j)
        extends=[]
        if self.options.extends:
            b=self.options.extends
            for i in b:
                for j in i.split(","):
                    extends.append(j)
        others=[]
        if self.options.othersymbols:
            # print "SOOS:", self.options.othersymbols
            b=self.options.othersymbols
            for i in b:
                for j in i.split(","):
                    others.append(j)
                    # print "FOUNDSYM_OTHER:", j
        return (impall, imppart, extends, others)

    def resolve_babel(self, babelconfig):
        if babelconfig:
            if not os.path.exists(babelconfig):
                print >> sys.stderr, "Warning: Unable to verify babel-config path given: "+babelconfig
            return babelconfig
        else:
           babelconfig="/fixme/babel-config"
           try:
               babelconfig=which.which("babel-config")
           except Exception, e:
               print >> sys.stderr, "Warning: Unable to find babel-config in path. Assuming bogus value."
               print >> sys.stderr, e
               pass
           return babelconfig

    def process_opts(self, s, symnew ):
        impl = self.options.lang
        if self.kind in ["class","component"] and not impl:
            self.fatalError("--language=SERVERLANG must be specified with class or component")
        prefix = self.options.prefix 
        babelbin = self.resolve_babel(self.options.babelbin)
        sidlsource = self.options.sidlsource
        defprefix="%prefix%"
        if not sidlsource or sidlsource == os.path.join(prefix, "share", "cca", self.sidlname + ".sidl"):
            sidlsource = os.path.join(defprefix, "share", "cca", self.sidlname + ".sidl")
        alias = self.options.alias
        if not alias:
            alias = self.sidlname
        include = self.options.includePath
        if not include:
            include = os.path.join(defprefix,"include")
        if self.options.project and len(self.options.project) > 0:
            include = os.path.join(include, self.options.project)
        else:
            if symnew and self.kind in ["port","component"]:
                self.warning("--project=PROJECT expected for CCA toolkit header packaging conformance.")
        libdir = self.options.libPath
        # we have a little weirdness here:
        if not libdir or libdir == os.path.join(prefix,"lib"):
            libdir = os.path.join(defprefix,"lib")
                
        classpath = self.options.classpath
        if not classpath:
            classpath = os.path.join(libdir,"java")
        pythonpath = self.options.pythonpath
        shared = self.options.shared
        static = self.options.static
        libtool = self.options.libtool
        libbasename = self.sidlname
        if self.options.basename:
            libbasename = self.options.basename
        clients = self.options.clients.split(",")
        usesports = self.process_ports(self.options.usesPorts,"Uses")
        providesports = self.process_ports(self.options.providesPorts,"Provides")
        delegatesports = self.process_ports(self.options.delegatesPorts,"Delegates")
        deleteports = self.process_deletes()
        (portprops, portpropsdelete) = self.process_port_props()

        if self.debug:
            if usesports and len(usesports) > 0:
                print "OPTUSES:", usesports
            if providesports and len(providesports) > 0:
                print "OPTPROV:", providesports
            if delegatesports and len(delegatesports) > 0:
                print "OPTDELEG:", delegatesports
        extraShared = self.options.sharedDependLibs
        extraStatic = self.options.staticDependLibs
        extraLibtool = self.options.libtoolDependLibs
        extraCompiling = self.options.compilingDependFlags
        sharedSuffix = self.options.sharedSuffix
        
        if symnew:
            project = self.options.project
            (impall, imppart, extends, requiredSymbols) = self.process_symbols()
            # This is where we get all the sensible defaults if the
            # user specifies only symbol.
            if self.kind == "component":
                s.defineToolkitComponent(impl,
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
                                     requiredSymbols,
                                     impall, imppart, extends,
                                     extraShared,
                                     extraStatic,
                                     extraLibtool,
                                     extraCompiling,
                                     alias
                ); # missing sharedSuffix... 
            if self.kind == "class":
                s.defineClass(impl,
                          sidlsource,
                          clients,
                          libbasename,
                          shared, static, libtool,
                          include,
                          libdir,
                          classpath,
                          pythonpath,
                          requiredSymbols,
                          impall, imppart, extends, 
                          extraShared,
                          extraStatic,
                          extraLibtool,
                          extraCompiling,
                          prefix,
                          babelbin,
                          sharedSuffix
                )
            if self.kind == "port":
                s.definePort(babelbin, 
                         sidlsource,
                         prefix,
                         project,
                         libbasename,
                         clients, 
                         shared, static, libtool,
                         requiredSymbols,
                         extends, 
                         alias
                )
            if self.kind == "interface":
                if self.debug:
                    print "DEFINING interface ",self.sidlname
                s.defineInterface(sidlsource,
                              clients,
                              libbasename,
                              shared, static, libtool,
                              include,
                              libdir,
                              classpath,
                              pythonpath,
                              requiredSymbols,
                              extends,
                              prefix,
                              babelbin,
                              sharedSuffix
                )
   
        optsdict = self.optionsDict(self.options)
        if self.debug:
            print "OPLIST", optsdict
        if optsdict.has_key("alias") and optsdict["alias"] != None:
            s.changeAlias(optsdict["alias"])
        if optsdict.has_key("id") and optsdict["id"] != None:
            s.changeUuid(optsdict["id"])
        if optsdict.has_key("prefix") and optsdict["prefix"] != None:
            s.changePrefix(optsdict["prefix"])
        for i in clients:
            if self.debug:
                print "UPDATING client", i
            self.updateSymbolClient(i, s, optsdict)
        if self.kind in ["component","class"]:
            self.updateSymbolServer(s, optsdict)
        if self.kind == "component":
            self.updateSymbolPorts(s, usesports, providesports, delegatesports, deleteports)
            s.changePortProperties(portprops, portpropsdelete)
        self.updateSymbolDepends(s)
        


    def updateSymbolDepends(self, s):
        """process options to add/remove base and required symbols."""
        (newimpall, newimppart, newextends, requiredSymbols) = self.process_symbols()
        s.changeSymbolDependences(newimpall, newimppart, newextends, requiredSymbols)
        killimpall=[]
        if self.options.impalldelete:
            b=self.options.impalldelete
            for i in b:
                for j in i.split(","):
                    killimpall.append(j)
        killimppart=[]
        if self.options.imppartdelete:
            b=self.options.imppartdelete
            for i in b:
                for j in i.split(","):
                    killimppart.append(j)
        killextends=[]
        if self.options.extendsdelete:
            b=self.options.extendsdelete
            for i in b:
                for j in i.split(","):
                    killextends.append(j)
        killrequired=[]
        if self.options.othersymbolsdelete:
            b=self.options.othersymbolsdelete
            for i in b:
                for j in i.split(","):
                    killrequired.append(j)
        s.deleteSymbolDependences(killimpall, killimppart, killextends, killrequired)

    def optionsDict(self, options):
        """return a dict of the options set (including defaults) which makes it easier
to tell if we were given an option."""
        classattrs = dir(optparse.Values)
        opts = dict()
        for name in [_ for _ in dir(options) if _ not in classattrs]:
            try:
                if not "=" in name:
                    opts[name] = getattr(options, name)
            except:
                pass
        return opts

    def updateSymbolPorts(self, sym, usesports, providesports, delegatesports, deleteports):
        """Update the ports of the component."""
	sym.changePorts(usesports, providesports, delegatesports)
        sym.deletePorts(deleteports)
   

    def updateSymbolServer(self, sym, dopts):
        """ update impl details based on dictionary made from opts. """
        inc = None
        lang = dopts["lang"]
        if lang in ["c","cxx","f90","f77"]:
            iname="ServerIncludePath"
            lname="LibtoolLib"
            dname="SharedLib"
            sname="StaticLib"
            slib=None
            dlib=None
            llib=None
            if dopts.has_key(iname):
                inc = dopts[iname]
            if dopts.has_key(lname):
                llib = dopts[lname]
            if dopts.has_key(dname):
                dlib = dopts[dname]
            if dopts.has_key(sname):
                slib = dopts[sname]
            sym.changeServerLibs(llib, dlib, slib)
        if lang == "java":
            if dopts.has_key("classpathServer"):
                inc = dopts["classpathServer"]
        if lang == "pythonpath":
            if dopts.has_key("pythonpathServer"):
                inc = dopts["pythonpathServer"]
        if inc:
            sym.changeServerSymbolPath(lang,inc)

    def updateSymbolClient(self, lang, sym, dopts):
        """ update clients based on dictionary made from opts. """
        inc = None
        if lang in ["c","cxx","f90","f77"]:
            iname=lang+"ClientIncludePath"
            lname=lang+"LibtoolLib"
            dname=lang+"SharedLib"
            sname=lang+"StaticLib"
            slib=None
            dlib=None
            llib=None
            if dopts.has_key(iname):
                if self.debug:
                    print "FOUND include option for", iname
                inc = dopts[iname]
            if dopts.has_key(lname):
                llib = dopts[lname]
            if dopts.has_key(dname):
                dlib = dopts[dname]
            if dopts.has_key(sname):
                slib = dopts[sname]
            sym.changeClientLibs(lang, llib, dlib, slib)
        if lang == "java":
            if dopts.has_key("classpath"):
                inc = dopts["classpath"]
        if lang == "pythonpath":
            if dopts.has_key("pythonpath"):
                inc = dopts["pythonpath"]
        if inc:
            if self.debug:
                print "SETTING include option ",inc
            sym.changeClientSymbolPath(lang,inc)
            
        
    
    def fatalError(self, msg = ""):
        print >> sys.stderr, "Error:", msg
        sys.exit(1)

    def warning(self, msg=""):
        print >> sys.stderr, "Warning:", msg
        if self.options.warnFatal:
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
        
################################################################################

def clientSwitches(parser, lang, langname):
    parser.add_option("--shared-"+lang, dest = lang+"SharedLib",
               help = "Libtool "+langname+" client library name. Full path overrides directory in --lib",
               metavar = "LIBNAME")
    parser.add_option("--static-"+lang, dest = lang+"StaticLib",
               help = "Static "+langname+" client library name. Full path overrides directory in --lib",
               metavar = "LIBNAME")
    parser.add_option("--libtool-"+lang, dest = lang+"LibtoolLib",
               help = "Libtool "+langname+" client library name. Full path overrides directory in --lib",
               metavar = "LIBNAME")
    parser.add_option("--include-"+lang, dest = lang+"ClientIncludePath",
               help = "Path to "+langname+" client header files (overrides value specified using --include)",
               metavar = "INCLUDEDIR")
    
################################################################################

def initParser(parser):
    # options for tool managing.
    parser.add_option("-o", "--output", dest = "outfile",
              help="name of output file. Default is ./symbol_depl.xml")
    parser.add_option("-D", "--debug", action="store_true", dest = "debug",
              help="Debug the xml generator")
    parser.add_option( "--path-check", action="store_true", dest = "pathcheck",
              help="Check paths found or generated into xml.")
    parser.add_option("-W", "--warnings-fatal", action="store_true", dest = "warnFatal", 
              help="Treat warnings as errors")
    parser.add_option("--deployment-path", action="append", dest = "deplpath", 
              help="Path to search for other deployment xml files. (Default is $CCA_COMPONENT_PATH:$SIDL_DLL_PATH:.)")

    parser.add_option("--general-options",
                      dest="    ======== OPTIONS FOR ALL INSTALLS ========")

    parser.add_option("--with-babel-config", dest = "babelbin", action="store",
              help = "Full path of babel-config of the babel used for building the symbol",
              metavar = "BIN_BABEL_CONFIG")
    parser.add_option("--extends", dest = "extends", action="append",
              help = "List of sidl symbols which this one extends eg --extends='pkg.x,pkg.y'. Classes can extend only one, interfaces can extend many",
              metavar = "EXTENDS_SYMLIST")
    parser.add_option("--implements-all", dest = "impall", action="append",
              help = "List of sidl interfaces which this class implements fully eg --implements-all='pkg.x,pkg.y'.",
              metavar = "IMPL_ALL_SYMLIST")
    parser.add_option("--implements-part", dest = "imppart", action="append",
              help = "List of sidl interfaces which this class implements partially eg --implements-part='pkg.x,pkg.y'.",
              metavar = "IMPL_PART_SYMLIST")
    parser.add_option("--base-symbols", dest = "basesymbols", action="append",
              help = "No longer supported. See --[extends,implements-all,implements-part")
    parser.add_option("--requires", dest = "othersymbols", action="append",
              help = "List of sidl symbols used directly in the implementation or sidl description.",
              metavar = "REQUIRES_SYMLIST")
    parser.add_option("--remove-extends", dest = "extendsdelete", action="append",
              help = "List of sidl symbols to remove from extends list. E.g. --remove-extends='pkg.x,pkg.y'.",
              metavar = "EXTENDS_SYMLIST")
    parser.add_option("--remove-implements-all", dest = "impalldelete", action="append",
              help = "List of sidl symbols to remove from implements-all list. E.g. --remove-implements-all='pkg.x,pkg.y'.",
              metavar = "IMPL_ALL_SYMLIST")
    parser.add_option("--remove-implements-part", dest = "imppartdelete", action="append",
              help = "List of sidl symbols to remove from implements-part list. E.g. --remove-implements-part='pkg.x,pkg.y'.",
              metavar = "IMPL_PART_SYMLIST")
    parser.add_option("--remove-requires", dest = "othersymbolsdelete", action="append",
              help = "List of sidl symbols to remove from requires list.",
              metavar = "REQUIRES_SYMLIST")
    parser.add_option("--sidl", dest = "sidlsource",
              help = "Location of sidl file for this interface or class.",
              metavar = "INSTALLED_SIDL")
    parser.add_option("--prefix", dest = "prefix",
              help = "Root directory for installation. Used to generate any other paths not specified.",
              metavar = "PREFIX")
    parser.add_option("-I", "--include", dest = "includePath",
              help = "Path to headers and mod files. Overrides PREFIX/include",
              metavar = "INCLUDEDIR")
    parser.add_option("-L", "--lib", dest = "libPath",
              help = "Path default to server and client libraries. Overrides PREFIX/lib.",
              metavar = "LIBDIR")
    parser.add_option("--shared-suffix", dest = "sharedSuffix",
              help = "Extension of dynamic loading files. Defaults to .so",
              metavar = "SUFFIX")

    parser.add_option("--no-shared", dest = "shared", action="store_false",
              help = "Shared libraries are unsupported.")

    parser.add_option("--no-static", dest = "static", action="store_false",
              help = "Static libraries are unsupported.")

    parser.add_option("--no-libtool", dest = "libtool", action="store_false",
              help = "Libtool libraries are unsupported.")

    parser.add_option("--basename", dest="basename",
              help = "Base name for archives. (default is sidl symbol name)")

    parser.add_option("-a", "--alias", dest = "alias",
              help = "Component alias to be used in GUI's palletes (default is component name)",
              metavar = "ALIAS")
    
    parser.add_option("-i", "--uuid", dest = "id",
              help = "Universally unique id \n(default is USER@HOST:component_name:time_stamp)", 
              metavar="UUID")

    parser.add_option("--client-options", 
                      dest="     ======== OPTIONS FOR CLIENT INSTALLS ========")

    parser.add_option("--clients", dest="clients",
              help = "Client languages that are supported. Default is 'c,cxx,f77,f90,java,python'",
              metavar = "LANGLIST")

    clientSwitches(parser,"c","C")
    clientSwitches(parser,"f77","F77")
    clientSwitches(parser,"f90","F90")
    clientSwitches(parser,"cxx","C++")
    
    parser.add_option("--classpath", dest="classpath",
              help = "Path to root where client java bits will be installed", metavar="JAVADIR")
    
    parser.add_option("--pythonpath", dest="pythonpath",
              help = "Path to root where client python bits will be installed", metavar="PYTHONDIR")
    
    #
    # the following items apply only to sidl classes.
    #
    parser.add_option("--server-options",
                      dest="     ======== OPTIONS FOR SERVER INSTALLS ========")


    parser.add_option("-l", "--language", dest = "lang",
              help = "Implementation language for class (valid values are c, cxx, f77, f90, python, java)")
    
    parser.add_option("--shared-lib", dest = "sharedLib",
              help = "Shared library archive for the implementation. Library must be located in directory specified using --lib",
              metavar = "LIBNAME")
    parser.add_option("--static-lib", dest = "staticLib",
              help = "Static library archive for the implementation. Library must be located in directory specified using --lib",
              metavar = "LIBNAME")
    parser.add_option("--libtool-lib", dest = "libtoolLib",
              help = "libtool-generated library archive for the implementation. Library must be located in directory specified using --lib",
              metavar = "LIBNAME")

    parser.add_option("--include-impl", dest = "ServerIncludePath",
               help = "Path to server header files (overrides value specified using --include)",
               metavar = "INCLUDEDIR")

    parser.add_option("--impl-classpath", dest="classpathServer",
              help = "Path to root where impl java bits will be installed", metavar="JAVADIR")
    
    parser.add_option("--impl-pythonpath", dest="pythonpathServer",
              help = "Path to root where impl python bits will be installed", metavar="PYTHONDIR")
    
    
    parser.add_option("--compiling-depend-flags", dest = "compilingDependFlags", action = "append",
               help = """Includes/Defines/etc needed to digest external things in the server headers""",
               metavar = "FLAGS")

    parser.add_option("--shared-depend-libs", dest = "sharedDependLibs", action = "append",
               help = """External libraries on which this implementation depends.""",
               metavar = "LIBFLAGS")

    parser.add_option("--static-depend-libs", dest = "staticDependLibs", action = "append",
               help = """External libraries on which this implementation depends.""",
               metavar = "LIBFLAGS")

    parser.add_option("--libtool-depend-libs", dest = "libtoolDependLibs", action = "append",
               help = """External libraries on which this implementation depends.""",
               metavar = "LIBFLAGS")


    #
    # the following items apply only to components
    #
    parser.add_option("--component-opts",
                      dest="     ======== OPTIONS FOR CCA INSTALLS ========")

    parser.add_option("--project", dest="project", 
        help="Define project name used as $prefix/include/$PROJECT/ per CCA toolkit guidelines. Default is none.",
        metavar = "PROJECT")

    parser.add_option("-p", "--provides", dest="providesPorts", action="append",
        help="ports PROVIDED by the component. A port is specified as "
        + "PORT_TYPE@PORT_NAME, where PORT_TYPE is the fully qualified SIDL type of the provided port, "
        + "and PORT_NAME is the name given to the provided port instance in the component code. "
        + "Multiple ports can be specified using multiple --provides options."
        + "Multiple ports of the same type can only be specified with the --delegates option.")

    parser.add_option("-u", "--uses", dest="usesPorts", action="append",
        help="ports USED by the component. A port is specified as "
        + "PORT_TYPE@PORT_NAME, where PORT_TYPE is the fully qualified SIDL type of the used port, "
        + "and PORT_NAME is the name given to the used port instance in the component code. "
        + "Multiple ports can be specified using multiple --uses options.")

    parser.add_option("-d", "--delegates", dest="delegatesPorts", action="append",
        help="ports PROVIDED by the component by delegation. A port is specified as "
        + "PORT_TYPE@PORT_NAME@DELEGATE_TYPE, where PORT_TYPE is the fully qualified SIDL type of the provided port, "
        + "PORT_NAME is the name given to the provided port instance in the component code, and. " 
        + "DELEGATE_TYPE is the class of the delegate instance."
        + "Multiple provides ports of the same type are implemented with delegation.")

    # remember to strip anything after 2nd @ when processing ports.

    parser.add_option("--delete", dest="deletePorts", action="append",
        help="Delete a port.", metavar = "PORT_NAME")

    parser.add_option("--port-property", dest="portProperties", action="append",
        help="Add a property to a port. ",
        metavar="PORT_NAME@PROPERTY_NAME@TYPE@VALUE")

    parser.add_option("--delete-port-property", dest="deletePortProperties",
        action="append",
        help="Remove a property from a port.",
        metavar = "PORT_NAME@PROPERTY_NAME")

    parser.set_defaults(providesPorts=None,
                        babelbin=None,
                        usesPorts=None,
                        delegatesPorts=None,
                        deletePorts=None,
                        uuid=None,
                        sidlsource=None,
                        basename=None,
                        othersymbolsdelete=None,
                        othersymbols=None,
                        extends=None,
                        extendsdelete=None,
                        impall=None,
                        impalldelete=None,
                        imppart=None,
                        imppartdelete=None,
                        deplpath=None,
                        prefix="/UNSPECIFIED_PREFIX",
                        project="",
                        clients="c,cxx,f77,f90,java,python",
                        shared=True,
                        static=True,
                        libtool=True,
                        pathcheck=False,
                        debug=False,
                        warnFatal=False,
                        sharedSuffix=".so"
                       )
