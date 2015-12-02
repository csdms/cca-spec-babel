from optparse import OptionParser, Values
from xml.dom import minidom
import sys
import os


class Devnull:
    """ The do nothing writer to replace sys.stderr when we want to see
    no spew.
    """
    def write(self, msg): pass
    def flush(self): pass



WarnFatal=False

if 'BOCCA_DEBUG' in os.environ.keys():
    if os.environ['BOCCA_DEBUG'] == "1":
        DEBUGSTREAM = sys.stderr
        WARN = True

class CCAXMLQuery:
    """Class to support querying for a sidl symbol installation."""

    def process(self, opts, args):

        for i in args:
            if len(i) < 3 or not "." in i:
                self.parser.print_help()
                print "SIDL symbol requested appears to be incomplete:", i
                return 1

        import Index, Symbol, File
        self.index = Index.Index()
        self.debug = opts.debug
        if self.debug:
            self.DEBUGSTREAM = sys.stderr
            print >> self.DEBUGSTREAM, sys.argv
        if opts.debugDepl:
            self.index.debug=True

        self.pathcheck = opts.pathcheck
        # fixme pathcheck impl?
        if opts.warnFatal:
            WarnFatal=True

        deplpath = opts.deplpath
        if not deplpath:
            deplpath=[]
        if not opts.nodeplpath:
            deplpath.append(os.environ.get("CCA_COMPONENT_PATH"))
            deplpath.append(os.environ.get("SIDL_DLL_PATH"))
        for i in deplpath:
            print >> self.DEBUGSTREAM, "### Search path includes:"
            self.index.appendpath(i)
        print >> self.DEBUGSTREAM, "### Loading data"
        self.index.scanpath()
        print >> self.DEBUGSTREAM, "### Done loading data"

        status=1
        value="Invalid output format specified: "+opts.outstyle
        # the below should return status of 0 or 1 only:
        if opts.outstyle == "text":
            (status, value) = self.process_text(opts,args[0])
        if opts.outstyle == "gmake":
            (status, value) = self.process_gmake(opts,args)
        if opts.outstyle == "shellvars":
            (status, value) = self.process_shell(opts,args)
           
        if status != 0:
            print >> sys.stderr, value
            return status

        if opts.outfile:
            self.OUT = open(opts.outfile,"w")
        
        if self.OUT:
            print >> self.OUT, value
            return 0
        else:
            print >> sys.stderr, "Unable to open " +opts.outfile + " for writing."
            return 1

    def process_gmake(self, opts, sidlname):
        pass

    def process_shell(self, opts, sidlname):
        pass

    def process_text(self, opts, sidlname):

        result=""
        index = self.index
        s = index.getSymbol(sidlname)
        d = s.deployment
        if not s:
            return (1, "Symbol "+sidlname+" is not found in path: "+self.index.getPath())
        kind = s.getKind()
        # filename = s.getFilename()
        
        if self.debug:
            s.deployment.nonecheck()

        if opts.sidlKmode:
            return (0, kind)
        if opts.sidlImode:
            ilist = index.findSidlFileDependencies(sidlname)
            result=""
            for i in ilist:
                result += "-I"+i+" "
            return (0, result)
        if opts.sidlSmode:
            ilist = index.findSidlSymbolDependencies(sidlname)
            result=" ".join(ilist)
            return (0, result)
        if opts.sidlFmode:
            ilist = index.findSidlFileDependencies(sidlname)
            result=" ".join(ilist)
            return (0, result)
        if opts.requiresmode:
            result=" ".join(d.getRequiredSymbols())
            return (0, result)
        if opts.extendsmode:
            result=" ".join(d.getExtends())
            return (0, result)
        if opts.prefixmode:
            result=d.getPrefix()
            return (0, result)
        if opts.sharedSuffixmode:
            pass; # fixme
        if opts.sharedmode:
            pass; # fixme
        if opts.staticmode:
            pass; # fixme
        if opts.libtoolmode:
            pass; # fixme
        if opts.aliasmode:
            result=d.getAlias()
            return (0, result)
        if opts.id:
            result=d.getUuid()
            return (0, result)
        if opts.clientsmode:
            pass; # fixme
        if opts.babelbin:
            result=d.getBabel()
            return (0, result)

        if kind == "interface" or kind == "enum" or kind == "port":
            return (1, "no queries found for an enum/interface/port ("+ sidlname  +")" )

        if opts.impallmode:
            result=" ".join(d.getImplementsAll())
            return (0, result)
        if opts.imppartmode:
            result=" ".join(d.getImplements())
            return (0, result)
        if opts.serverIncludemode:
            ds = d.getServer()
            result = ds.getSymbolPath(ds.getLang())
            return (0, result)
        if opts.compilingDependFlagsmode:
            pass; # fixme
        if opts.sharedDependLibsmode:
            pass; # fixme
        if opts.staticDependLibsmode:
            pass; # fixme
        if opts.libtoolDependLibsmode:
            pass; # fixme
        if opts.providesPortsmode:
            pl = d.getPortInfo("provides")
            pl2=[]
            for i in pl:
                pl2.append("@".join(i))
            result=" ".join(pl2)
            return (0, result)
        if opts.usesPortsmode:
            pl = d.getPortInfo("uses")
            pl2=[]
            for i in pl:
                pl2.append("@".join(i))
            result=" ".join(pl2)
            return (0, result)
        if opts.delegatesPortsmode:
            pl = d.getPortInfo("delegates")
            pl2=[]
            for i in pl:
                pl2.append("@".join(i))
            result=" ".join(pl2)
            return (0, result)

        if opts.liblang:
            pass; # fixme: give all libs needed to resolve sidlname for client liblang
        if opts.classpath:
            includelang="java"
        if opts.pythonpath:
            includelang="python"
        if opts.includelang:
            pass; # fixme: give all includes needed to resolve sidlname for client liblang
        if opts.includedirslang:
            pass; # fixme: as includelang, but no -I,etc flags added.
#lang=None

        if opts.portPropertiesmode and len(opts.portPropertiesmode) >0:
            port=opts.portPropertiesmode
            pnames = d.getPortPropertyNames(port)
            if pnames:
                return (0,  " ".join(pnames))
                return result
            return (0, "")

        if opts.portPropValues and len(opts.portPropValues) > 0:
            # only 1st in text mode
            for i in opts.portPropValues:
                if i.contains(","):
                    pplist = i.split(",")
                else:
                    pplist = [i]
                for p in pplist:
                    (port, key) = p.split("@")
                    t = d.getPortPropertyValue(port, key)
                    if t:
                        return (0, "@".join(t) )
            return (1, "No port/property defined for "+opts.portPropValues[0])
        
        return (2, "Unrecognized or unimplemented query: "+ str(sys.argv))

        
    def optionsDict(self, options):
        """return a dict of the options set (including defaults) which makes it easier
to tell if we were given an option."""
        classattrs = dir(Values)
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
        if WarnFatal:
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

    def initParser(self, pusage):
        self.parser = OptionParser(usage=pusage)
        self.DEBUGSTREAM = Devnull()
        parser = self.parser

        # options for tool managing.
        parser.add_option("--general-options",
                  dest="     ======== search, output, and debugging options  ========")

        parser.add_option("-c", "--no-default-path", action="store_true", dest = "nodeplpath",
              help="Ignore the default search path for deployment xml files.")
        parser.add_option("-D", "--dpath", action="append", dest = "deplpath",
              help="extend the search path for deployment xml files. (Default is $CCA_COMPONENT_PATH:$SIDL_DLL_PATH:.)")
        parser.add_option("-o", "--output", dest = "outfile",
              help="name of output file. Default is stdout")
        parser.add_option("-m", "--mode", dest = "outstyle",
              help="format of output. Valid formats are text, shellvars, and gmake; text mode answers only one query, while shellvars and gmake allow multiple outputs and multiple symbols",
              metavar="FORMAT_NAME")
        parser.add_option( "--debug", action="store_true", dest = "debug",
              help="turn on debugging")
        parser.add_option( "--debug-depl", action="store_true", dest = "debugDepl",
              help="turn on debugging for deployment xml parser.")
        parser.add_option( "--path-check", action="store_true", dest = "pathcheck",
              help="Check all paths found for correctness and warn if not.")
        parser.add_option("-W", "--warnings-fatal", action="store_true", dest = "warnFatal", 
              help="Treat warnings as errors")

        parser.add_option("--query-options",
                  dest="     ======== sidl symbol query options  ========")

        parser.add_option("-k","--kind", dest = "sidlKmode", action="store_true",
              help = "List kind of sidlname (enum, interface, class, port, component)")
        parser.add_option("-s","--sidl-symbols", dest = "sidlSmode", action="store_true",
              help = "List of all other sidl symbols needed to resolve sidlname")
        parser.add_option("--sidl-includes", dest = "sidlImode", action="store_true",
              help = "List of -Ifile arguments babel needs to resolve sidlname")
        parser.add_option("--sidl-files", dest = "sidlFmode", action="store_true",
              help = "List of sidl files required to process sidlname")
        parser.add_option("--libs", dest = "liblang", action="store",
              help = "List of libraries needed to resolve sidlname", metavar = "CLIENT_LANGUAGE")
        parser.add_option("-r","--requires", dest = "requiresmode", action="store_true",
              help = "List of sidl symbols used directly in sidlname.")
        parser.add_option("-e","--extends", dest = "extendsmode", action="store_true",
              help = "List of sidl symbols which sidlname extends.")
        parser.add_option("--prefix", dest = "prefixmode",
              help = "Show root directory for installation.")
        parser.add_option("--includes", dest = "includelang",  action="store",
              help = "Show path argument for headers/mod/etc files needed to use sidlname client in the given language",
              metavar = "CLIENT_LANGUAGE")
        parser.add_option("--classpath", dest="classpath", help = "alias for --includes=java")
        parser.add_option("--pythonpath", dest="pythonpath", help = "alias for --includes=python")
        parser.add_option("--include-dirs", dest = "includedirslang", action="store",
              help = "List header and mod directories needed for sidlname client in the given language",
              metavar = "CLIENT_LANGUAGE")
        parser.add_option("--shared-suffix", dest = "sharedSuffixmode", action="store_true",
              help = "Extension used on dynamic loading files.")

        parser.add_option("--shared", dest = "sharedmode", action="store_true",
              help = "List shared libraries for libs query.")

        parser.add_option("--static", dest = "staticmode", action="store_true",
              help = "List static libraries for libs query.")

        parser.add_option("--libtool", dest = "libtoolmode", action="store_true",
              help = "List libtool libraries for libs query.")

        parser.add_option("-a", "--alias", dest = "aliasmode",
              help = "Return ias to be used in GUI's palletes for sidlname")
        
        parser.add_option("-i", "--uuid", dest = "id",
              help = "Return Universally unique id for this installation of sidlname")

        parser.add_option("--clients", dest="clientsmode",
              help = "List languages that are supported by the complete dependency chain of sidlname")
        
        parser.add_option("--with-babel-config", dest = "babelbin", action="store_true",
              help = "Show full path of babel-config of the babel used for building the symbol")
        #
        # the following items apply only to sidl classes.
        #
        parser.add_option("--server-query-options",
                  dest="     ======== options for classes/components ========")

        parser.add_option("--implements-all", dest = "impallmode", action="store_true",
              help = "List of sidl symbols on the implements-all list for sidlname.")

        parser.add_option("--implements-part", dest = "imppartmode", action="store_true",
              help = "List of sidl symbols to on the implements-part list of sidlname")

        # parser.add_option("-l", "--language", dest = "lang",
        #           help = "Implementation language for sidlname")
        
        parser.add_option("--impl-includes", dest = "serverIncludemode", action="store_true",
               help = "Show path to server header files for sidlname")

        parser.add_option("--compiling-depend-flags", dest = "compilingDependFlagsmode", action = "store_true",
               help = "Includes/Defines/etc needed to digest external things in the server headers.")

        parser.add_option("--shared-depend-libs", dest = "sharedDependLibsmode", action = "store_true",
               help = "External shared libraries on which this implementation depends.")

        parser.add_option("--static-depend-libs", dest = "staticDependLibsmode", action = "store_true",
               help = "External static libraries on which this implementation depends.")

        parser.add_option("--libtool-depend-libs", dest = "libtoolDependLibsmode", action = "store_true",
               help = "External libtool libraries on which this implementation depends.")


        #
        # the following items apply only to components
        #
        parser.add_option("--component-opts",
                  dest="     ======== options for cca component classes ========")

        parser.add_option("-p", "--provides", dest="providesPortsmode", action="store_true",
        help="List ports provided by the component.")

        parser.add_option("-u", "--uses", dest="usesPortsmode", action="store_true",
        help="List ports used by the component.")

        parser.add_option("-d", "--delegates", dest="delegatesPortsmode", action="store_true",
        help="List ports provided by the component via delegation.")

        parser.add_option("--port-property-names", dest="portPropertiesmode", 
        help="List of properties on a port. ",
        metavar="PORT_NAME")

        parser.add_option("--port-property-value", dest="portPropValues", action="append",
        help="List TYPE@VALUE for the property name(s) given",
        metavar="PORT_NAME@PROPERTY_NAME[,NAME...]")

        parser.set_defaults(nodeplpath=False,
                deplpath=[],
                outfile=None,
                outstyle="text",
                debug=False,
                debugDepl=False,
                pathcheck=False,
                warnFatal=False,
                sidlSmode=False,
                sidlKmode=False,
                sidlImode=False,
                sidlFmode=False,
                liblang=None,
                classpath=False,
                pythonpath=False,
                requiresmode=False,
                extendsmode=False,
                prefixmode=False,
                includelang=None,
                includedirslang=None,
                sharedSuffixmode=False,
                sharedmode=False,
                staticmode=False,
                libtoolmode=False,
                aliasmode=False,
                id=False,
                clientsmode=False,
                babelbin=False,
                impallmode=False,
                imppartmode=False,
                lang=None,
                serverIncludemode=False,
                compilingDependFlagsmode=False,
                sharedDependLibsmode=False,
                staticDependLibsmode=False,
                libtoolDependLibsmode=False,
                providesPortsmode=False,
                usesPortsmode=False,
                delegatesPortsmode=False,
                portPropertiesmode=None ,
                portPropValues=[]
                   )
        return parser
