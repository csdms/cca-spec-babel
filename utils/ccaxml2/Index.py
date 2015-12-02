import os
from File import File

class Index:
    """The expected use of this class is by:
1) setting the path
2) scanpath (or addFile for file creation)
3) getSymbol
4) modify Symbol
5) closeAll-- writes any files that were changed.
"""
    def __init__(self):
        self.pathlist = []
        self.symtab = dict()
        self.filelist = dict()
        self.debug=False

    def getPath(self):
        path=":".join(self.pathlist)
        return path

    def getSymbol(self, sidlname):
        """Lookup a sidl symbol. None returned if unknown."""
        if self.symtab.has_key(sidlname):
            return self.symtab[sidlname]
        return None

    def updateSymbol(self, sym, pathcheck):
        if not sym:
            return
        sfile = self.filelist[sym.getFilename()]
        sfile.domFromSymbol(sym)
        sfile.setChanged()
        if pathcheck:
            sfile.pathCheck(sym.node)

    def addFile(self, filename, file):
        """Load all data from .cca File object given into our symbol table"""
        self.filelist[filename] = file
        file.domToSymtab(self. symtab)

    def scanfile(self, filename):
        """Open a named file into symbol table"""
        if self.debug:
            print "INDEXING", filename
        rfile = File(filename)
        self.filelist[filename] = rfile
        rfile.domToSymtab(self. symtab)
        self.printIndex()

    def setpath(self, path):
        """set the search path """
        self.pathlist = path.split(os.pathsep)

    def appendpath(self, path):
        """ append path to search path """
        if path:
            newelts = path.split(os.pathsep)
            self.pathlist.extend(newelts)

    def prependpath(self, path):
        """ insert path before search path """
        if path:
            old = self.pathlist
            self.setpath(path)
            self.pathlist.extend(old)

    def clear(self):
        """ forget all data except path"""
        self.symtab = dict()
        for i in self.filelist:
            i.clear()

    def scanpath(self, suffix=None):
        """for all dirs in path load all files in dirs named *.cca"""
        if self.debug:
            print "SCANPATH", suffix
        self.clear()
        for i in self.pathlist:
            if i:
                if os.path.isdir(i):
                    self.scandir(i, suffix)
                elif os.path.isfile(i):
                    self.scanfile(i)
                elif self.debug:
                    print "scanpath found nonexistent element: ", i
                else:
                    pass

    def scandir(self, dirname, suffix=None):
        """load all files in dir named *.cca"""
        import glob
        if self.debug:
            print "SCANDIR", dirname, suffix
        sdir = os.path.expanduser(dirname)
        if not suffix:
            suffix = "*.cca"
        else:
            suffix = "*" + suffix
        files = glob.glob(os.path.join(sdir,suffix))
        if files:
            for i in files:
                self.scanfile(i)

    def closeAll(self):
        """write all files that have been changed"""
        for i in self.filelist.values():
            i.writeChanges()
            i.clear()

    def printIndex(self):
        """list symbols and locations found"""
        for i in self.symtab.keys():
            print i+" in file "+ self.symtab[i].getFilename()


    def intFindSymbolDependencies(self, symbol, slist, warn=False, withFiles=False):
       """recursive implementation detail of findSymbolDependencies"""
       if not symbol:
           if warn:
               print "null symbol to visitor"
           return

       childlist = symbol.getDependenceSymbols()

       if withFiles:
           # append source location to each before continuing
           newlist = []
           for childname in childlist:
               child = self.getSymbol(childname)
               if not child:
                   if warn:
                       print "unindexed dependence:", childname
                   newlist.append(childname)
               else:
                   loc = child.getSidlFile()
                   newlist.append(childname +"@"+ loc)

           childlist = newlist

       for i in childlist:
           if not i in slist:
               childname=""
               if withFiles:
                   childname = i.split("@")[0]
               else:
                   childname = i
               child = self.getSymbol(childname)
               if not child:
                   if warn:
                       print "unindexed dependence:", i
               else:
                   self.intFindSymbolDependencies(child, slist, warn, withFiles)
               slist.append(i)


    def findSymbolDependenciesLocations(self, sidlname, warn=False):
        """Return a list of all the symbols this one depends on where each symbol as its defining sidl file appended with an @ (eg sym@filname). List will be ordered from least complex dependence to most, reverse of the typical ordering used by linux ld. List ends with name given."""
        root = self.getSymbol(sidlname)
        dlist = []
        self.intFindSymbolDependencies(root, dlist, warn, True)
        dlist.append(sidlname + "@"+ root.getSidlFile())
        return dlist
       
    def findSymbolDependencies(self, sidlname, warn=False):
        """Return a list of all the symbols this one depends on. List will be ordered from least complex dependence to most, reverse of the typical ordering used by linux ld. List ends with name given."""
        root = self.getSymbol(sidlname)
        dlist = []
        self.intFindSymbolDependencies(root, dlist, warn, False)
        dlist.append(sidlname)
        return dlist
       

    def findLinkFlags(self, sidlname, lang, linkage):
        """determine and return the linker options needed to include symbol and all its
dependencies.
@param the symbol of interest
@param lang language of the client needed.
"""
        symlist = self.findSymbolDependencies(sidlname)
        llist=[]
        for i in symlist:
            s = self.getSymbol(i)
            if not s:
                print "WARNING: Symbol dependence", i, "has no xml definition. skipping."
                continue
            clib = s.getClientLib(lang, linkage)
            if clib == "unsupported":
                raise RuntimeError, "Unsupported linkage and binding:"+linkage+", "+lang+" for "+i
            llist.append(clib)
            if s.getKind() in ["class", "component"]:
                slib = s.getServerLib(linkage)
                if slib == "unsupported":
                    raise RuntimeError, "Unsupported linkage "+linkage+" for server of "+i
                if slib != "":
                    llist.append(slib)
        rlist = []
        for i in llist:
            if not i in rlist:
                rlist.append(i)
        rlist.reverse() 
        return rlist       

    def findIncludeDirs(self, sidlname, lang):
        """Determine and return the directories needed to include symbol and all its
dependencies. For java and python, returns an appropriate archive path.
@param lang language of the client needed.
"""
        symlist = self.findSymbolDependencies(sidlname)
        llist=[]
        for i in symlist:
            s = self.getSymbol(i)
            if not s:
                print "WARNING: Symbol dependence", i, "has no xml definition. skipping."
                continue
            idir = s.getClientSymbolPath(lang)
            if idir == "unsupported":
                raise RuntimeError, "Unsupported binding:"+lang+" for "+i + " needed by " + sidlname
            llist.append(idir)
        rlist = []
        for i in llist:
            if not i in rlist:
                rlist.append(i)
        rlist.reverse() 
        return rlist
        

    def findSidlFileDependencies(self, sidlname):
        """Determine and return the list of installed sidl files required to process the
sidlname given and all its dependencies. Note that if the xml files lie, so will this
function. A common lie is that a symbol does not depend on sidl.sidl; most likely
build systems will be constructed to work around this particular lie even if babel isn't.
"""
        symlist = self.findSymbolDependencies(sidlname)
        llist=[]
        for i in symlist:
            s = self.getSymbol(i)
            if not s:
                print "WARNING: Symbol dependence", i, "has no xml definition. skipping."
                continue
            src = s.getSidlFile()
            if not src or src == "unsupported" or src == "":
                raise RuntimeError, "Undefined sidl source for " + i + " needed by " + sidlname
            llist.append(src)
        rlist = []
        for i in llist:
            if not i in rlist:
                rlist.append(i)
        rlist.reverse() 
        return rlist       
        pass

