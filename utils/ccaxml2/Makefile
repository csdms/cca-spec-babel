
all:
	python check1

doc:
	(cd doc ; env PYTHONPATH=.. pydoc -w ../*.py)

clean:
	$(RM) -r *.pyc *.v2 *.v3 t.ccomp_depl.xml t.type4_depl.xml cca_depl.xml testtk.out
	-(cd doc; $(RM) *)

.PHONY: doc
