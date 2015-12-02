
GEN_FILES=\
CCA_Babel_Vars.sh \
MakeIncl_CCA_Babel_Vars \
test-babel-config \
cca-spec-babel-config \
test-babel-config-* \
cca-spec-babel-config-* \
cca-spec-babel-scanCCAxml.exe

all: subdirs
	@echo $(GEN_FILES)

subdirs:
	(cd treeReader; $(MAKE) util)
	cp treeReader/extract.x ./cca-spec-babel-scanCCAxml.exe

clean: clean-subdirs
	(cd treeReader; $(MAKE) clean)

clean-subdirs:
	(cd treeReader; $(MAKE) clean)

distclean:
	$(RM) $(GEN_FILES)

install:
	(cd ..; $(MAKE) install)
