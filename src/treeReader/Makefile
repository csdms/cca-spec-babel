
# the only production aspect of this makefile
# is to build the util target.
# anything else is experimental and probably cheesy.

# only the executable gets exported from this directory.
# no headers, library, etc.

include ../MakeIncl_CCA_Babel_Vars
VPATH=$(CCASPEC_SRC_ROOT)/src/treeReader
zeroth: first

CXX = $(CCASPEC_BABEL_CXX)
CXXFLAGS = $(CCASPEC_BABEL_CXXFLAGS)
HIDECOMPILE=$(CCASPEC_HIDECOMPILE)
HIDELIBTOOL=$(CCASPEC_HIDELIBTOOL)

LIBXML2_INC=$(XMLINC) -I.. -I.
LIBS=$(XMLLIB)
LIBTOOL=$(CCASPEC_BABEL_BABEL_LIBTOOL)
INC=-I$(CCASPEC_SRC_ROOT)/src -I$(CCASPEC_SRC_ROOT)/src/treeReader
LOCALFLAGS= $(OTHERFLAGS) $(INC) $(XMLFLAGS) $(LIBXML2_INC) -g


DRIVER= \
$(CCASPEC_SRC_ROOT)/src/treeReader/XMLCCAExtractor.cpp 

SRC= \
ComponentData.cpp \
PortData.cpp

XMLSRC = \
MetaDataParser.cpp \
Node.cpp \
Parser.cpp 

OBJ = $(SRC:%.cpp=%.lo)
XMLOBJ= $(XMLSRC:%.cpp=%.lo)


first all: all-$(HAVE_XML2)

all-0:
	@echo "configure did not detect libxml2"
	@echo "Skipping build of xml-dependent translators scripts."
	@echo "reconfigure --with-libxml2 option if translators needed."

all-1: util

xmlbuild: $(XMLOBJ)

test tcd tcd.x:	ComponentData.cpp
	$(LIBTOOL) --mode=link --tag=CXX $(HIDECOMPILE) $(CXX) -o tcd.x -DComponentData_MAIN $(CXXFLAGS) $(LOCALFLAGS) ComponentData.cpp
	./tcd.x

util extract.x: $(OBJ) $(XMLOBJ)
	-$(RM) XMLCCAExtractor.o
	$(LIBTOOL) --mode=link --tag=CXX $(HIDECOMPILE)  $(CXX) -o extract.x -DXMLCCAExtractor_MAIN \
		$(CXXFLAGS) $(LOCALFLAGS) $(DRIVER) \
		*.lo $(LIBS)
	 $(HIDELIBTOOL)$(LIBTOOL) --mode=install cp extract.x `pwd`/../cca-spec-babel-scanCCAxml.exe


clean: 
	-$(RM) -f *.o *.exe core.* a.out *.x
	$(LIBTOOL) --mode=clean $(RM) *.lo

%.i: %.cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $(LOCALFLAGS) $< | grep '[a-z]' |egrep -v '^# ' > $@

%.lo: %.cpp
	@echo "$@"
	$(HIDELIBTOOL)$(LIBTOOL) --mode=compile --tag=CXX $(HIDECOMPILE) $(CXX) -c $(CXXFLAGS) $(LOCALFLAGS) $<

%.cpp.ps : %.cpp
	-enscript -2rg --pretty-print=cpp --color $< -o $@

%.hpp.ps : %.hpp
	-enscript -2rg --pretty-print=cpp --color $< -o $@


include Makefile.depends
