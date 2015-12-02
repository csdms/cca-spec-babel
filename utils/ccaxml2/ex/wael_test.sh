../genccaxml.py --type=component \
--language=f90 \
--include-path=$TUTROOT/include/ \
--libpath=$TUTROOT/lib/ \
--shared-lib=libintegrators.MonteCarlo.so \
--static-lib=libintegrators.MonteCarlo.a \
--libtool-lib=libintegrators.MonteCarlo.la \
--c-client-lib=libintegrators.MonteCarlo-c.a \
--f77-client-lib=libintegrators.MonteCarlo-f77.a \
--f90-client-lib=libintegrators.MonteCarlo-f90.a \
--f90-client-headerpath=$TUTROOT/include/ \
--cxx-client-lib=libintegrators.MonteCarlo-cxx.a \
--useportlib=libfunction.FunctionPort-f90.a \
--provideportlib=libintegrator.IntegratorPort-f90.a \
integrators.MonteCarlo
