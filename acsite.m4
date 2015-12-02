dnl    CCAFE_PATH_TO_FILE(VARIABLE, TEST_FILES, PATH, 
dnl	 [ RUN_IF_FOUND, [RUN_IF_NOT_FOUND)

dnl    Test for the presence of file(s) (TEST_FILES) in the given colon
dnl    separated list of directory paths (PATH).  If all of the files for a
dnl    given path element are present, it sets VARIABLE to the matching PATH
dnl    element and calls AC_SUBST on it.  The files appear in TEST_FILES as a
dnl    space separated list.  The last two arguments are run if a path to the
dnl    files is found or not found respectively.
AC_DEFUN(CCAFE_PATH_TO_FILE,
[
var="$1"
testFiles="$2"
path="$3"

result=_searching
paths=`echo $path|tr ":" " "`
for chome in $paths ; do
    for testFile in $testFiles ; do
	    if ! test -f $chome/$testFile ; then
		    result=_searching
		    break
	    fi	
	    result=$chome	
    done
    if test "$result" = "$chome" ; then
	    $1=$result
	    if test -n '$4' ; then
		# if found
		  $4 
	    fi
	    echo "       found: $result"
	    break;
    fi
done
if test "$result" = _searching ; then
	if test -n '$5' ; then
	      #if not found
		$5
	fi
fi
]
)

AC_DEFUN(CCAFE_CHECK_BABEL,
[
#--------------------------------------------------------------------
# See if we can find Babel
#--------------------------------------------------------------------
AC_MSG_CHECKING([ Babel stuff])
echo
echo -n "   "

AC_ARG_WITH(babel,
    [  --with-babel=BABEL_ROOT     The full path to the babel install dir.],
    , [with_babel=yes] )
case $with_babel in 
    no)
        BABEL_ROOT=
	AC_MSG_WARN(
    [Building CCAFFEINE without Babel 
     will cause babel components to be non-operable. 
     To specify a location for the Babel; run
     configure again with the argument: --with-babel=BABEL_ROOT where
     BABEL_ROOT is the full path to the Babel install.]
		   )
        ;;
    yes)
        #  The user didn't give the --with-babel
        #  option or didn't give the library's location.
        #  If that fails, disable and print a warning.
	BABEL_ROOT="yes"
        ;;
    *)
        #  The user gave us --with-babel=BABEL_ROOT, use that as the
        #  location.
        BABEL_ROOT="$with_babel"
        ;;
esac

# test for success

if test "$BABEL_ROOT" = "yes"; then
    ccafe_babel_dirs="$BABEL_HOME:/usr/local/babel:/usr/babel:$HOME/babel"
    BABEL_ROOT=
    CCAFE_PATH_TO_FILE(BABEL_ROOT, bin/babel, $ccafe_babel_dirs, 
	    AC_MSG_RESULT(Babel root found.),
	    AC_MSG_WARN(
	[Cannot find babel root directory.  Building CCAFFEINE without Babel 
	 will cause babel components to be non-operable. 
	 To specify a location for the Babel; run
	 configure again with the argument: --with-babel=BABEL_ROOT where
	 BABEL_ROOT is the full path to the Babel install.]
                        )
			)
fi
AC_SUBST(BABEL_ROOT)
]
)

dnl
dnl Search for babel CONFIG_INSTALL_NOTES installed tree 
dnl in $BABEL_ROOT
dnl
dnl Requires:
dnl   variable BABEL_ROOT to be defined.
dnl
dnl If found, set variable BABEL_NOTES.
dnl If not found, unset variable BABEL_NOTES.
dnl
dnl bugs: could be more clever about checking for versions
dnl after v0.7.4, by extracting babel-config --version
dnl instead of betting on ls.
dnl
AC_DEFUN(CCA_BABEL_NOTES,
[
#--------------------------------------------------------------------
# See if we can find Babel CONFIG_INSTALL_NOTES
#--------------------------------------------------------------------
AC_MSG_CHECKING([ Babel installation notes ])
echo
echo -n "   "

if test -d $BABEL_ROOT ; then
  if test -f $BABEL_ROOT/CONFIG_INSTALL_NOTES ; then
    BABEL_NOTES=$BABEL_ROOT/CONFIG_INSTALL_NOTES
    AC_MSG_RESULT([ $BABEL_NOTES. ])
  fi
  if test -x $BABEL_ROOT/bin/babel-config; then
    BABEL_NOTES=`ls $BABEL_ROOT/babel-*/CONFIG_INSTALL_NOTES`
    AC_MSG_RESULT([ $BABEL_NOTES. ])
  fi
  if test -z $BABEL_NOTES ; then
    AC_MSG_WARN([ Cannot find CONFIG_INSTALL_NOTES in $BABEL_ROOT tree. ])
  fi
else
  AC_MSG_WARN([ BABEL_ROOT not defined. No Babel config notes found.])
fi
]
)

dnl 
dnl CCAFE_EXTRACT_VAR( VARNAME, INPUT-FILE, INPUT-VARNAME, [ DEFAULT-VALUE ] )
dnl grep for lines of form INPUT-VARNAME = rest of line
dnl and set VARNAME to be the value found.
dnl If var is not found and default-value is supplied, var takes that value.
dnl misfeatures: follows the autoconf convention that there should not
dnl be sideeffects perpetrated on the output files -- only variables get 
dnl defined.
AC_DEFUN(CCAFE_EXTRACT_VAR,
[
	AC_MSG_CHECKING([for $3])
	cevDefault=
	cev1=`grep "^$3 " $2`
	if test -z "$cev1"; then
		cev1=`grep "^$3	" $2`
	fi
	if test -z "$cev1"; then
		cev1=`grep "^$3=" $2`
	fi
changequote(, )dnl
	cev2=`echo "$cev1" | sed 's/^[[:alnum:],[:space:],_,-,.]*=//'`
	cev3=`echo "$cev2" | sed 's/^[[:space:]]*//'`
changequote([, ])dnl
	if test -z "$cev3" ; then
		ifelse([$4], , : , [ cev3="$4" ])
	fi
	if test -z "$cev3" ; then
		AC_MSG_RESULT(no)
	else
		[$1]=$cev3
		AC_MSG_RESULT([$cev3])
	fi
]
)

dnl
dnl CCAFE_ENV_CHECK( VAR, [MESSAGE-IF-FOUND], [MESSAGE-IF-NOT-FOUND] )
dnl checks that VARNAME is or isn't defined.
dnl When no MESSAGE-IFs are supplied, defaults to printing yes/no.
dnl Side-effects: none, other than message output.
dnl internally used variables are all prefixed cec_.
dnl Internal variables (less prefix):
dnl yes, no, var_eval, var_val, empty_eval, empty_test, there.
dnl on normal completion: 
dnl cec_there == 1 if the variable is set (includes empty value)
dnl cec_there == 0 if not set.
dnl Bugs: 
dnl This macro would be 3 lines if we could assume bash syntax is portable.
dnl It even works when checking for environment variables with the
dnl value cec_not_there.
AC_DEFUN(CCAFE_ENV_CHECK,
[
	if test -z "$1"  ; then
		AC_MSG_RESULT(CCAFE env_check called with empty VAR argument)
	else
		AC_MSG_CHECKING(environment for $1)
# build a line which echos the name in $1
# get the value of that var
		cec_var_eval="echo $"`echo $1`
		cec_var_val=`eval $cec_var_eval`
		if test -z "$cec_var_val" ; then
# either its there, not there or 0 len
# 0 len may be meaningful so we need to distinguish.
# at this point we don't need to worry about overwriting its value
# temporarily since it's at most empty.
			cec_empty_eval="echo \${"`echo $1`"-cec_not_there}"
			cec_empty_test=`eval $cec_empty_eval`
			if test "X$cec_empty_test" = "Xcec_not_there" ; then
				cec_there=0
			else
				cec_there=1
			fi
		else
			cec_there=1
		fi
		cec_yes=yes
		cec_no=no
		ifelse([$2], , : , [cec_yes="$2"])
		ifelse([$3], , : , [cec_no="$3"])
		if test $cec_there -eq 1 ; then
			AC_MSG_RESULT($cec_yes)
		else
			AC_MSG_RESULT($cec_no)
		fi
	fi
]
)

AC_DEFUN(CSB_CHECK_BOOST,
[
#--------------------------------------------------------------------
# See if we can find Boost
#--------------------------------------------------------------------
AC_MSG_CHECKING([ BOOST smart pointers ])
echo 
echo -n "    "


AC_ARG_WITH(boost,
    [  --with-boost=BOOST_ROOT     The full path to the BOOST install dir.
    of, give --with-boost=yes and the default],
    , [with_boost=yes] )
case $with_boost in 
    no)
	# can't live without BOOST
       AC_MSG_WARN(
       [
	We must use boost to build a translator utility. This
	does not affect compiling normal cca-dependent code, but
        the bld2babel-cpp and similar translators won't operate.
	])
        ;;
    yes)
        #  The user didn't give the --with-boost
        #  option or didn't give the library's location.
        #  If that fails, disable and print a warning.
	BOOST_ROOT="yes"
        ;;
    *)
        #  The user gave us --with-boost=BOOST_ROOT, use that as the
        #  location of the BOOST library.
        BOOST_ROOT="$with_boost"
        ;;
esac

# test for success

if test "x$BOOST_ROOT" = "xyes" ; then
    ccafe_boost_dirs="$fullpathsrcdir/src/treeReader"
    BOOST_ROOT=
    CCAFE_PATH_TO_FILE(BOOST_ROOT, boost/shared_ptr.hpp, "$ccafe_boost_dirs", 
	AC_MSG_RESULT([Using treeReader version of boost headers.]),
	AC_MSG_WARN(
	   [Cannot find BOOST headers.
	    Make sure that the specified path has the directory \"boost\"
	    in it and does not have it *included* in the path.  
	    bld2babel-cpp cannot be built without BOOST smart pointers
	    To specify a location for the BOOST smart pointer library run
	    configure again with the argument:
	    --with-boost=BOOST_ROOT
	    where BOOST_ROOT is the full path to the boost headers. 
	    See http://www.boost.org for more details.])
		      )
elif test "x$BOOST_ROOT" = "xno"; then 
    ccafe_boost_dirs="/usr:/usr/local:/usr/local/include:/usr/include:$HOME:$HOME/include:/opt/include:/usr/local/packages/boost"
    BOOST_ROOT=
    CCAFE_PATH_TO_FILE(BOOST_ROOT, boost/shared_ptr.hpp, "$ccafe_boost_dirs", 
	AC_MSG_RESULT([BOOST root dir found.]),
	AC_MSG_WARN(
	   [Cannot find BOOST headers.
	    Make sure that the specified path has the directory \"boost\"
	    in it and does not have it *included* in the path.  
	    bld2babel-cpp cannot be built without BOOST smart pointers.
	    To specify a location for the BOOST smart pointer library run
	    configure again with the argument:
	    --with-boost=BOOST_ROOT
	    where BOOST_ROOT is the full path to the boost headers. 
	    See http://www.boost.org for more details.])
		      )
else
    CCAFE_PATH_TO_FILE(BOOST_ROOT, boost/shared_ptr.hpp, "$BOOST_ROOT",
	v=1,
	AC_MSG_WARN(
	   [Cannot find BOOST headers.
	    Make sure that the specified path has the directory \"boost\"
	    in it and does not have it *included* in the path.  
	    bld2babel-cpp cannot be built without BOOST smart pointers.
	    To specify a location for the BOOST smart pointer library run
	    configure again with the argument:
	    --with-boost=BOOST_ROOT
	    where BOOST_ROOT is the full path to the boost headers. 
	    See http://www.boost.org for more details.])
		      )
	
fi
AC_SUBST(BOOST_ROOT)
]
)

# Checks for unix programs
AC_DEFUN(CCATUT_UNIX_PROGRAMS,
[
AC_CANONICAL_SYSTEM
AC_HEADER_STDC
AC_CHECK_HEADERS(fcntl.h strings.h sys/file.h sys/time.h unistd.h)

AC_PROG_LN_S
AC_SUBST(LN_S)

AC_PROG_MAKE_SET
AC_SUBST(SET_MAKE)

AC_PROG_RANLIB
AC_SUBST(RANLIB)
#AC_CHECK_LIB(blas, saxpy_)
#AC_CHECK_LIB(lapack, lsame_)

# source tree vars
CURRDIR=`pwd`
# The next two lines entirely quoted to keep autoconf/m4 
# from messing with the [] in the regex.
[CURRDIR_PARENT=`echo $CURRDIR | sed 's%[^/][^/]*$%%' | sed 's%\/$%%'`]
[CURRDIR_GRANDPARENT=`echo $CURRDIR_PARENT | sed 's%[^/][^/]*$%%' | sed 's%\/$%%'`]
[CURRDIR_GREATGRANDPARENT=`echo $CURRDIR_GRANDPARENT | sed 's%[^/][^/]*$%%' | sed 's%\/$%%'`]
[CURRDIR_ANCESTOR=`echo $CURRDIR_GREATGRANDPARENT | sed 's%[^/][^/]*$%%' | sed 's%\/$%%'`]
]
)

## end of paths to search collection

AC_DEFUN(CCATUT_COMPILER,
[
#AC_LANG_CPLUSPLUS

# FIND C compiler
#------------------------------------------------------------------------------
#  see if the user gave us the location of the c compiler
#------------------------------------------------------------------------------
AC_ARG_WITH(cc,
    [Location of alternative c compiler:
  --with-cc=EXECUTABLE
                          The location of C.
                          Give the full path:
                              --with-cc='/usr/local/gcc/bin/gcc' ],
    , [with_cc=yes])

case "$with_cc" in
    no)
        #  User specified --without-cc
        #  print a warning.
        AC_MSG_WARN([Option '--without-cc' Causes demo to be suppressed.])
        AC_MSG_ERROR([A c compiler is required; demo has a c code.])
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_cc=_searching
        ;;
    *)
        CC="$with_cc"
        ;;
esac

if test "$with_cc" = _searching ; then
    AC_PROG_CC
fi
AC_SUBST(CC)

# FIND c++ compiler
#------------------------------------------------------------------------------
#  see if the user gave us the location of the c++ compiler
#------------------------------------------------------------------------------
AC_ARG_WITH(cPP,
    [Location of alternative c++ compiler:
  --with-c++=EXECUTABLE
                          The location of C++.
                          Give the full path:
                              --with-c++='/usr/local/gcc/bin/g++' ],
    , [with_cPP=yes])

case "$with_cPP" in
    no)
        #  User specified --without-c++
        #  print a warning.
        AC_MSG_WARN([Option '--without-c++' Causes compilation to be suppressed.])
        AC_MSG_ERROR([A c++ compiler is required; current code is a c++ code.])
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_cPP=_searching
        ;;
    *)
        CXX="$with_cPP"
        cca_have_cpp=yes
        ;;
esac

if test "$with_cPP" = _searching ; then
    AC_PROG_CXX
fi


# set the warning flags depending on whether or not we are using gcc
if test "${GCC}" = "yes" ; then
    CFLAGS_WARNING="-Wall -Wconversion"
else
    CFLAGS_WARNING=""
fi
AC_SUBST(CFLAGS_WARNING)

#------------------------------------------------------------------------------
# If we're using GCC, see if the compiler understands -pipe.  If so, use it.
# It makes compiling go faster.  (This is only a performance feature.)
#------------------------------------------------------------------------------

if test -z "$no_pipe"; then
if test -n "$GCC"; then
  AC_MSG_CHECKING([if c++ compiler understands -pipe])
  OLDCXX="$CXX"
  CXX="$CXX -pipe"
  AC_TRY_COMPILE(,,
    AC_MSG_RESULT(yes),
    CXX="$OLDCXX"
    AC_MSG_RESULT(no))
fi
fi

AC_SUBST(CXX)
AC_SUBST(CXXFLAGS)
AC_SUBST(CXX_TEMPLATES)

# FIND c++ preprocessor
AC_PROG_CXXCPP
AC_SUBST(CXXCPP)
]
)

#------------------------------------------------------------------------------
#
# Some folklore is keyed to hostname, which is probably a very bad
# idea in the long run, but provides examples for frustrated alpha users.
# Most of it is keyed to the answers supplied by AC_CANONICAL_SYSTEM.
#
# We wish MPICH was adapted to use autoconf 2.x so we could steal
# conveniently everything they deduce about fortran, mpi, threads,
# etc in their configure scripts and extend it to our compilers.
#
# Find the mpi dujour if not suppressed.
# Setup pll build targets if available.
# Always:
# MPI, MPI_ARCH, MPICC, MPICXX, MPIRUN
# When mpicc and mpiCC are broken, as is frequently the case
# MPI_LDFLAGS, MPILIB
# Note that we need to finish the failure cases and expand folklore
# to cope with broken mpiCC. Or we need mpich to just work in every
# single release. Or we need MPI forum to standardize on a
# "configuration variables" sh includable file to live in
# $MPI_HOME/lib/config.vars so we don't need mpiCC,
# or ... insert your favorite solution to the vagaries of mpi builds
# here.
#--------------------------------------------------------------------
AC_DEFUN(CCATUT_LIB_MPI,
[
# MPICH search paths 
ccatut_mpich_dirs="
	$MPI_HOME
    	$CCATUT_HOME/mpich
    	$CCATUT_HOME/mpich-1.2.2.3
    	$CCATUT_HOME/mpi
    	$TOP/mpich
    	$TOP/mpich-1.2.2.3
    	$TOP/mpi
	$CCAFE_PARENT/mpi
	$CCAFE_ANCESTOR/mpi
	$CCAFE_PARENT/mpich
	$CCAFE_ANCESTOR/mpich
	$prefix/mpi
	$prefix/mpich
	$HOME/mpi
	$HOME/mpich
    	/home/local/mpich-1.2.2
    	/home/petsc/software/mpich-1.2.0/linux
    	/usr/local/mpi
    	/usr/local/mpich
"

AC_ARG_WITH(mpi,
    [Location of mpi:
  --with-mpi=MPI_HOME
                          The location of mpich used in your framework.
                          Give the full path, e.g.:
                              --with-mpi='/share/bizarre/mpich1.1.2' ],
    , [with_mpi=yes])

case "$with_mpi" in
    no)
        ccatut_have_mpi=no
        ;;
    yes)
        with_mpi=_searching
        ;;
    *)
        MPI="$with_mpi"
        ;;
esac

if test "$with_mpi" = _searching ; then
    ccatut_have_mpi=no
    AC_MSG_CHECKING([for mpi])
    for mhome in $ccatut_mpich_dirs ; do
  echo checking for mpi in $mhome ...
        if test -f $mhome/include/mpi.h -a -x $mhome/bin/tarch -a -x $mhome/bin/mpirun; then
            MPI=$mhome
            MPIRUN=$MPI/bin/mpirun
            MPI_ARCH=`$mhome/bin/tarch`
	    MPI_INCLUDE="-I$mhome/include"
            AC_MSG_RESULT([$mhome ($MPI_ARCH) found.])
            ccatut_have_mpi=yes
            break
        fi
    done
    if test -z "$MPI" ; then
        ccatut_have_mpi=no
        AC_MSG_RESULT([mpi not found. mpi-based components and tests disabled.
           --with-mpi=/path/of/mpi(ch) to enable them.])
    fi
fi

# we think we have something. check that it runs
# and if not, sigh and go to folklore.
ccatut_try_mpi_folklore=no
if test ! "X$ccatut_have_mpi" = Xno ; then
    if test -x $MPI/bin/mpirun -a "X$ccatut_try_mpi_folklore" = Xno ; then
        MPIRUN=$MPI/bin/mpirun
    else
    MPIRUN=broken
        ccatut_try_mpi_folklore=yes
    fi
    if test -x $MPI/bin/tarch -a "X$ccatut_try_mpi_folklore" = Xno ; then
        MPI_ARCH=`$MPI/bin/tarch`
    else
        MPI_ARCH="Set_MPI_ARCH_in_Makefile.Vars_manually"
        ccatut_try_mpi_folklore=yes
    fi
    if test -x $MPI/bin/mpicc -a "X$ccatut_try_mpi_folklore" = Xno ; then
        AC_MSG_CHECKING([mpicc])
        $MPI/bin/mpicc -o config.cpi.exe config/cpi.c
        if test -x config.cpi.exe ; then
            AC_MSG_RESULT(yes)
            MPICC=$MPI/bin/mpicc
        else
            MPICC=broken
            BROKEN_MPICC=$MPI/bin/mpicc
            AC_MSG_RESULT(broken.)
        fi
        rm -f config.cpi.exe cpi.o
    fi
    if test -x $MPI/bin/mpiCC -a "X$ccatut_try_mpi_folklore" = Xno ; then
        AC_MSG_CHECKING([mpiCC])
        $MPI/bin/mpiCC -o config.cppi.exe config/cpi.cpp
        if test -x config.cppi.exe ; then
            AC_MSG_RESULT(yes)
            MPICXX=$MPI/bin/mpiCC
        else
            MPICXX=broken
            BROKEN_MPICXX=$MPI/bin/mpiCC
            AC_MSG_RESULT(broken.)
        fi
        rm -f config.cppi.exe cpi.o
    fi
    if test "X$ccatut_try_mpi_folklore" = Xno ; then
        MPI_HOME=$MPI
    fi
fi
if test "X$ccatut_try_mpi_folklore" = Xyes ; then
    echo "SIGH! rummaging about in history for mpi."
    CCAFE_MPI_HUNT=yes
    . config/mpi.folklore
fi
if test -d "$MPI/build/$MPI_ARCH/ch_p4/include" ; then
    MPI_INCLUDE="-I$MPI/build/$MPI_ARCH/ch_p4/include $MPI_INCLUDE"
fi
if test -s "$MPI/build/$MPI_ARCH/ch_p4/lib/libmpich.a" ; then
    MPILIB="$MPI/build/$MPI_ARCH/ch_p4/lib/libmpich.a"
    MPI_LIBDIR="$MPI/build/$MPI_ARCH/ch_p4/lib"
fi
if test -d "$MPI/include/mpi2c++" ; then
    MPI_INCLUDE="-I$MPI/include/mpi2c++ $MPI_INCLUDE"
fi
if test -s "$MPI/lib/libmpich.a" ; then
    MPILIB="$MPI/lib/libmpich.a"
    MPI_LIBDIR="$MPI/lib"
fi
AC_SUBST(MPI)
AC_SUBST(MPIRUN)
AC_SUBST(MPI_ARCH)
AC_SUBST(MPI_HOME)
AC_SUBST(BROKEN_MPICC)
AC_SUBST(BROKEN_MPICXX)
AC_SUBST(MPICC)
AC_SUBST(MPICXX)
AC_SUBST(MPI_LDFLAGS)
AC_SUBST(MPILIB)
AC_SUBST(MPI_LIBDIR)
AC_SUBST(MPI_INCLUDE)
]
)

#------------------------------------------------------------------------------
# CCA_ROOT: See if the user gave us the location of cca-spec
# then search $ccatut_cca_spec_dirs.
# One of these directories must be
# present and contain the correct files, or else the user
# must give the directory that contains the correct files.
#------------------------------------------------------------------------------
# cca spec (must contain java and cxx binding subdirs)

AC_DEFUN(CCATUT_SPEC_CCA,
[
ccatut_cca_spec_dirs="
    $CCATUT_HOME/cca-spec
    $TOP/cca-spec
    $CURRDIR_PARENT/cca-spec
    $CURRDIR_GRANDPARENT/cca-spec
    $CURRDIR_GREATGRANDPARENT/cca-spec
    $CURRDIR_ANCESTOR/cca-spec
    /home/alice/CCA/cca-spec
    $prefix/cca-spec
    $HOME/cca-spec
    $HOME/cca/cca-spec
    /usr/local/cca-spec
    $prefix/cca
    /usr/local/cca
    $HOME/cca
"
AC_ARG_WITH(cca, 
    [Location of cca:
  --with-cca=SPEC_TREE
                          The location of CCA java and cxx specifications. 
                          Give the full path:
                              --with-cca='/usr/local/cca-spec'
                          or check out the spec from Sandia in a directory
                          next to CCAFFEINE. ] ,
    , [with_cca=no])

case "$with_cca" in
    no)
        # lUser input error
        with_cca=_searching
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_cca=_searching
        ;;
    *)
        CCA_ROOT="$with_cca"
        ;;
esac

if test "$with_cca" = _searching ; then
    AC_MSG_CHECKING([for REQUIRED cca-spec])
    for chome in $ccatut_cca_spec_dirs ; do
        if test -d $chome ; then
            with_cca=$chome
            AC_MSG_RESULT([found $chome.])
            break
        fi
    done
fi
if test "$with_cca" = _searching ; then
    AC_MSG_RESULT([Cannot find CCA specification root directory.])
    AC_MSG_ERROR([Please install it and/or use --with-cca=CCA_ROOT.])
fi
if test ! -f "$with_cca/cxx/include/cca.h"  ; then
    AC_MSG_RESULT([No cxx/include/cca.h in $with_cca.])
    AC_MSG_ERROR([Please install a correct CCA specification directory.])
fi
CCA_ROOT="$with_cca"
EG_ROOT="$with_cca/cxx/eg"
AC_SUBST(CCA_ROOT)
AC_SUBST(EG_ROOT)
]
)

#------------------------------------------------------------------------------
# CCAFE_ROOT: See if the user gave us the location of ccaffeine
# then search $ccatut_ccafe_spec_dirs.
# One of these directories must be
# present and contain the correct files, or else the user
# must give the directory that contains the correct files.
#------------------------------------------------------------------------------
AC_DEFUN(CCATUT_LIB_CCAFE,
[
#  CCAFEINE search paths
ccatut_ccafe_dirs="
    $CCATUT_HOME/dccafe
    $TOP/dccafe
    $CURRDIR_PARENT/dccafe
    $CURRDIR_GRANDPARENT/dccafe
    $CURRDIR_GREATGRANDPARENT/dccafe
    $CURRDIR_ANCESTOR/dccafe
    $prefix/dccafe
    $HOME/dccafe
    $HOME/cca/dccafe
    /home/alice/CCA/dccafe
    /usr/local/dccafe
"

AC_ARG_WITH(dccafe, 
    [Location of dccafe:
  --with-dccafe=CCAFFEINE_TREE
                          The location of dccafe
                          Give the full path: e.g.
                              --with-dccafe=/usr/local/dccafe ] ,
    , [with_dccafe=yes])

case "$with_dccafe" in
    no)
        # lUser input error
        with_dccafe=_searching
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_dccafe=_searching
        ;;
    *)
        CCAFE_ROOT="$with_dccafe"
        ;;
esac

if test "$with_dccafe" = _searching ; then
    AC_MSG_CHECKING([for REQUIRED ccaffeine distribution])
    for chome in $ccatut_ccafe_dirs ; do
        if test -d $chome ; then
            with_dccafe=$chome
            AC_MSG_RESULT([found $chome.])
            break
        fi
    done
fi
if test "$with_dccafe" = _searching ; then
    AC_MSG_RESULT([Cannot find dccafe root directory.])
    AC_MSG_ERROR([Please install it and/or use --with-dccafe=CCAFE_ROOT.])
fi
if test ! -f "$with_dccafe/cxx/port/supportInterfaces.h"  ; then
    AC_MSG_RESULT([No cxx/port/supportInterfaces.h in $with_dccafe.])
    AC_MSG_ERROR([Please install a correct ccaffeine-0.3.x distribution.])
fi
CCAFE_ROOT="$with_dccafe"
CCAFE_CXX_ROOT="$CCAFE_ROOT/cxx"
AC_SUBST(CCAFE_ROOT)
AC_SUBST(CCAFE_CXX_ROOT)
]
)

#------------------------------------------------------------------------------
# ESI_ROOT: See if the user gave us the location of esi
# then search $ccatut_esi_dirs.
# One of these directories must be
# present and contain the correct files, or else the user
# must give the directory that contains the correct files.
#------------------------------------------------------------------------------
AC_DEFUN(CCATUT_SPEC_ESI,
[
# ESI search paths
ccatut_esi_dirs="
    $ESI_DIR
    $ESI_HOME
    $CCATUT_HOME/esi
    $CCATUT_HOME/esi-1.0.0
    $TOP/esi
    $TOP/esi-1.0.0
    $CCATUT_HOME/software/esi
    $CCATUT_HOME/software/esi-1.0.0
    /home/alice/CCA/esi
    /home/alice/CCA/esi-1.0.0
    $prefix/esi
    $prefix/esi-1.0.0
    /usr/local/esi
    /usr/local/esi-1.0.0
    /home/local/esi
    /home/local/esi-1.0.0
    $HOME/esi
    $HOME/esi-1.0.0
    $CURRDIR_PARENT/esi
    $CURRDIR_PARENT/esi-1.0.0
    $CURRDIR_GRANDPARENT/esi
    $CURRDIR_GRANDPARENT/esi-1.0.0
    $CURRDIR_GREATGRANDPARENT/esi
    $CURRDIR_GREATGRANDPARENT/esi-1.0.0
    $CURRDIR_ANSCESTOR/esi
    $CURRDIR_ANSCESTOR/esi-1.0.0
    /home/alice/CCA/esi-1.0.0
"
AC_ARG_WITH(esi,
    [Location of esi:	
  --with-esi=ESI_ROOT	
                          The location of esi
                          Give the full path: e.g.
                              --with-esi=/usr/local/esi ] ,
    , [with_esi=yes])

case "$with_esi" in
    no)
        # lUser input error
        with_esi=_searching
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_esi=_searching
        ;;
    *)
        ESI_ROOT="$with_esi"
        ;;
esac

if test "$with_esi" = _searching ; then
    AC_MSG_CHECKING([for REQUIRED esi header distribution])
    for chome in $ccatut_esi_dirs ; do
        if test -d $chome ; then
            with_esi=$chome
            AC_MSG_RESULT([found $chome.])
            break
        fi
    done
fi
if test "$with_esi" = _searching ; then
    AC_MSG_RESULT([Cannot find ESI specification root directory.])
    AC_MSG_ERROR([Please install it and/or use --with-esi=ESI_ROOT.])
fi
if test ! -f "$with_esi/cxx/include/esi/IndexSpace.h"  ; then
    AC_MSG_RESULT([No cxx/include/esi/IndexSpace.h in $with_esi.])
    AC_MSG_ERROR([Please install esi-1.0.0 or later.])
fi
ESI_ROOT="$with_esi"
AC_SUBST(ESI_ROOT)
]
)

#------------------------------------------------------------------------------
# BLASLAPACK_LIB: See if the user gave us the location of libblas.a AND liblapack.a 
# in the case when they are in the same directory.
# then search $ccatut_blaslapack_dirs.
# One of these directories must be
# present and contain the correct files, or else the user
# must give the directory that contains the correct files.
#------------------------------------------------------------------------------
AC_DEFUN(CCATUT_LIB_BLASLAPACK,
[

# BLAS and LAPACK search paths
ccatut_blaslapack_dirs="
    /home/alice/CCA/blaslapack
    $CCATUT_HOME/blaslapack
    $TOP/blaslapack
    /usr/lib
    /usr/local/lib
    /home/local/lib
    $prefix/lib
    $HOME/lib
"
# BLAS
ccatut_blas_dirs="$ccatut_blaslapack_dirs"
# LAPACK
ccatut_lapack_dirs="$ccatut_blaslapack_dirs"

AC_ARG_WITH(blaslapack,
    [Location of blas and lapack libraries:   
  --with-blaslapack=BLASLAPACK_LIB
                          The location of BLAS and LAPACK libraries
                          Give the full path: e.g.
                              --with-blaslapack=/usr/local/lib ] ,
    , [with_blaslapack=yes])

case "$with_blaslapack" in 
    no)
        # lUser input error
        with_blaslapack=_searching
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_blaslapack=_searching
        ;;
    *)
        BLASLAPACK_LIB="$with_blaslapack"
        ;;
esac

if test "$with_blaslapack" = _searching ; then
    AC_MSG_CHECKING([for BLAS and LAPACK libraries ])
    for chome in $ccatut_blaslapack_dirs ; do
        if test -d $chome -a -f $chome/libblas.a -a -f $chome/liblapack.a ; then
            with_blaslapack=$chome
            AC_MSG_RESULT([found $chome.])
            break
        fi
    done
fi
if test "$with_blaslapack" = _searching ; then
    AC_MSG_RESULT([Cannot find BLAS and LAPACK directory.])
    AC_MSG_ERROR([Please install it and/or use --with-blaslapack=BLASLAPACK_LIB.])
fi
if test ! -f "$with_blaslapack/libblas.a"  ; then
    AC_MSG_RESULT([No libblas.a in $with_blaslapack.])
    AC_MSG_ERROR([Please specify the localtion of libblas.a.])
fi
if test ! -f "$with_blaslapack/liblapack.a"  ; then
    AC_MSG_RESULT([No liblapack.a in $with_blaslapack.])
    AC_MSG_ERROR([Please specify the localtion of liblapack.a.])
fi

BLASLAPACK_LIB="$with_blaslapack"
AC_SUBST(BLASLAPACK_LIB)

#------------------------------------------------------------------------------
# BLAS_LIB: See if the user gave us the location of libblas.a
# then search $ccatut_blas_dirs.
# One of these directories must be
# present and contain the correct files, or else the user
# must give the directory that contains the correct files.
#------------------------------------------------------------------------------
AC_ARG_WITH(blas,
    [Location of blas libraries:   
  --with-blas=BLAS_LIB
                          The location of BLAS libraries
                          Give the full path: e.g.
                              --with-blas=/usr/local/lib ] ,
    , [with_blas=yes])

case "$with_blas" in 
    no)
        # lUser input error
        with_blas=_searching
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_blas=_searching
        ;;
    *)
        BLAS_LIB="$with_blas"
        ;;
esac

if test "$with_blas" = _searching ; then
    AC_MSG_CHECKING([for BLAS libraries ])
    for chome in $ccatut_blas_dirs ; do
        if test -d $chome -a -f $chome/libblas.a; then
            with_blas=$chome
            AC_MSG_RESULT([found $chome.])
            break
        fi
    done
fi
if test "$with_blas" = _searching ; then
    AC_MSG_RESULT([Cannot find BLAS directory.])
    AC_MSG_ERROR([Please install it and/or use --with-blas=BLAS_LIB.])
fi
if test ! -f "$with_blas/libblas.a" -a ! -f "$BLASLAPACK_LIB/libblas.a" ; then
    AC_MSG_RESULT([No libblas.a in $with_blas.])
    AC_MSG_ERROR([Please specify the localtion of libblas.a.])
fi

BLAS_LIB="$with_blas"
AC_SUBST(BLAS_LIB)

#------------------------------------------------------------------------------
# LAPACK_LIB: See if the user gave us the location of liblapack.a
# then search $ccatut_lapack_dirs.
# One of these directories must be
# present and contain the correct files, or else the user
# must give the directory that contains the correct files.
#------------------------------------------------------------------------------
AC_ARG_WITH(lapack,
    [Location of blas and lapack libraries:   
  --with-lapack=LAPACK_LIB
                          The location of LAPACK libraries
                          Give the full path: e.g.
                              --with-lapack=/usr/local/lib ] ,
    , [with_lapack=yes])

case "$with_lapack" in 
    no)
        # lUser input error
        with_lapack=_searching
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_lapack=_searching
        ;;
    *)
        LAPACK_LIB="$with_lapack"
        ;;
esac

if test "$with_lapack" = _searching ; then
    AC_MSG_CHECKING([for LAPACK libraries ])
    for chome in $ccatut_lapack_dirs ; do
        if test -d $chome -a -f "$chome/liblapack.a" ; then
            with_lapack=$chome
            AC_MSG_RESULT([found $chome.])
            break
        fi
    done
fi
if test "$with_lapack" = _searching ; then
    AC_MSG_RESULT([Cannot find LAPACK directory.])
    AC_MSG_ERROR([Please install it and/or use --with-lapack=LAPACK_LIB.])
fi
if test ! -f "$with_lapack/liblapack.a" -a ! -f "$BLASLAPACK_LIB/libblas.a" ; then
    AC_MSG_RESULT([No liblapack.a in $with_lapack.])
    AC_MSG_ERROR([Please specify the localtion of liblapack.a.])
fi
LAPACK_LIB="$with_lapack"
AC_SUBST(LAPACK_LIB)
]
)


#------------------------------------------------------------------------------
#  Find CUMULVS libraries
#------------------------------------------------------------------------------

AC_DEFUN(CCATUT_LIB_CUMULVS,
[
#  CUMULVS search paths
ccatut_cumulvs_dirs="
    $STV_ROOT
    $CCATUT_HOME/CUMULVS
    $TOP/CUMULVS
    $CURRDIR_PARENT/CUMULVS
    $CURRDIR_GRANDPARENT/CUMULVS
    $CURRDIR_GREATGRANDPARENT/CUMULVS
    $CURRDIR_ANCESTOR/CUMULVS
    $prefix/CUMULVS
    $HOME/CUMULVS
    $HOME/cca/CUMULVS
    /home/alice/CCA/CUMULVS
    /usr/local/CUMULVS
"

AC_ARG_WITH(cumulvs, 
    [Location of CUMULVS:
  --with-cumulvs=CUMULVS_TREE
                          The location of CUMULVS
                          Give the full path: e.g.
                              --with-cumulvs=/usr/local/CUMULVS ] ,
    , [with_cumulvs=yes])

case "$with_cumulvs" in
    no)
        # lUser input error
        with_cumulvs=_searching
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_cumulvs=_searching
        ;;
    *)
        STV_ROOT="$with_cumulvs"
        ;;
esac

if test "$with_cumulvs" = _searching ; then
    AC_MSG_CHECKING([for REQUIRED CUMULVS])
    for chome in $ccatut_cumulvs_dirs ; do
        if test -d $chome ; then
            with_cumulvs=$chome
            AC_MSG_RESULT([found $chome.])
            break
        fi
    done
fi
if test "$with_cumulvs" = _searching ; then
    AC_MSG_RESULT([Cannot find CUMULVS root directory.])
    AC_MSG_ERROR([Please install it and/or use --with-cumulvs=STV_ROOT.])
fi
if test ! -f "$with_cumulvs/include/stv.h"  ; then
    AC_MSG_RESULT([No include/stv.h in $with_cumulvs.])
    AC_MSG_ERROR([Please install a correct CUMULVS 1.2.x distribution.])
fi
STV_ROOT="$with_cumulvs"
AC_SUBST(STV_ROOT)
]
)


#------------------------------------------------------------------------------
#  Find PVM libraries
#------------------------------------------------------------------------------

AC_DEFUN(CCATUT_LIB_PVM,
[
#  PVM search paths
ccatut_pvm_dirs="
    $PVM_ROOT
    $CCATUT_HOME/pvm3
    $TOP/pvm3
    $CURRDIR_PARENT/pvm3
    $CURRDIR_GRANDPARENT/pvm3
    $CURRDIR_GREATGRANDPARENT/pvm3
    $CURRDIR_ANCESTOR/pvm3
    $prefix/pvm3
    $HOME/pvm3
    $HOME/cca/pvm3
    /home/alice/CCA/pvm3
    /usr/local/pvm3
"

AC_ARG_WITH(pvm, 
    [Location of PVM:
  --with-pvm=PVM_TREE
                          The location of PVM
                          Give the full path: e.g.
                              --with-pvm=/usr/local/pvm3 ] ,
    , [with_pvm=yes])

case "$with_pvm" in
    no)
        # lUser input error
        with_pvm=_searching
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_pvm=_searching
        ;;
    *)
        PVM_ROOT="$with_pvm"
        ;;
esac

if test "$with_pvm" = _searching ; then
    AC_MSG_CHECKING([for REQUIRED PVM])
    for chome in $ccatut_pvm_dirs ; do
        if test -d $chome ; then
            with_pvm=$chome
            AC_MSG_RESULT([found $chome.])
            break
        fi
    done
fi
if test "$with_pvm" = _searching ; then
    AC_MSG_RESULT([Cannot find PVM root directory.])
    AC_MSG_ERROR([Please install it and/or use --with-pvm=PVM_ROOT.])
fi

PVM_ROOT="$with_pvm"

# Make sure $PVM_ARCH is set...
if test -z "$PVM_ARCH" ; then
	# Make sure pvmgetarch exists...
	if test -x $PVM_ROOT/lib/pvmgetarch ; then
		PVM_ARCH=`$PVM_ROOT/lib/pvmgetarch`
	else
		AC_MSG_WARN([\$PVM_ROOT/lib/pvmgetarch script not found!])
		AC_MSG_ERROR([Please set PVM_ARCH env var.])
	fi
fi

PVM_XDIR="$PVM_ROOT/bin/$PVM_ARCH"

# Now check for (writable) PVM bin directory...
AC_MSG_CHECKING([for writable PVM bin directory ($PVM_XDIR)])
xdirck="aok"
if test ! -e $PVM_XDIR ; then
	# Hmmm... nothing there - try to create it...
	AC_MSG_WARN([PVM bin directory $PVM_XDIR doesn't exist - trying to create...])
	mkdir -p $PVM_XDIR
	if test $? != 0 ; then
		# Damn, can't create that directory...
		AC_MSG_WARN([Cannot create PVM bin directory $PVM_XDIR !])
		xdirck="notok"
	else
		AC_MSG_RESULT([$PVM_XDIR successfully created.])
	fi
else
	if test ! -d $PVM_XDIR ; then
		# Hmmm... not a directory...!
		# Rather than delete it and make a directory,
		# we'll just defer to alternate $HOME/pvm3 soln...
		AC_MSG_WARN([$PVM_XDIR is *not* a directory!])
		xdirck="notok"
	else
		if test ! -w $PVM_XDIR ; then
			# Hmmm... not writable - system-wide install?
			AC_MSG_WARN([PVM bin directory $PVM_XDIR is not writable!])
			xdirck="notok"
		fi
	fi
fi

# If not O.K., try using $HOME/pvm3/bin/$PVM_ARCH...
if test $xdirck = "notok" ; then
	# First, see if $PVM_ROOT is already $HOME/pvm3...
	homepvm="$HOME/pvm3"
	if test "$PVM_ROOT" = "$homepvm" ; then
		# We're screwwwwed, PVM already *is* in $HOME...
    	AC_MSG_RESULT([Cannot write to PVM bin directory in $PVM_XDIR.])
    	AC_MSG_ERROR([Please make $PVM_XDIR a writable directory.])
	else
		# Try to make bin directory in $HOME/pvm3...
		PVM_XDIR="$homepvm/bin/$PVM_ARCH"
		mkdir -p $PVM_XDIR
		if test $? != 0 ; then
			# Damn, can't create directory...
			AC_MSG_RESULT([Cannot create PVM bin directory $PVM_XDIR.])
    		AC_MSG_ERROR([Please make $PVM_XDIR a writable directory.])
		else
			AC_MSG_RESULT([$PVM_XDIR successfully created.])
		fi
	fi
else
   	AC_MSG_RESULT([$PVM_XDIR is O.K.])
fi

AC_SUBST(PVM_ROOT)
AC_SUBST(PVM_ARCH)
AC_SUBST(PVM_XDIR)
]
)


#------------------------------------------------------------------------------
#  see if the user gave us the location of clueful make
#------------------------------------------------------------------------------
AC_DEFUN(CCATUT_PROG_GMAKE,
[
AC_ARG_WITH(gmake, 
    [Location of gmake:
  --with-gmake=EXECUTABLE
                          The location of gmake.  Give the full path:
                              --with-gmake='/share/bizarre/bin/gmake' ] ,
    , [with_gmake=yes])

case "$with_gmake" in
    no)
        ccatut_have_gmake=no
        ;;
    yes)
        #  User didn't give the option or didn't give useful
       #  information, search for it ourselves
        with_gmake=_searching
        ;;
    *)
        #  Only the library was specified
        GMAKE="$with_gmake"
        ;;
esac

if test "$with_gmake" = _searching ; then
    AC_CHECK_PROG(gmake_1, gmake, gmake, NONE)
    if test ! "$gmake_1" = NONE ; then
        GMAKE="$gmake_1"
    fi
fi
AC_SUBST(GMAKE)
]
)

#------------------------------------------------------------------------------
#  see if the user gave us the location of the tclsh
#------------------------------------------------------------------------------
AC_DEFUN(CCATUT_PROG_TCLSH,
[
TCLSH=/usr/local/bin/tclsh
AC_ARG_WITH(tclsh, 
    [Location of tclsh:
  --with-tclsh=EXECUTABLE
                          The location of the Tcl8.x or later tclsh.
                          Give the full path:
                              --with-tclsh='/share/bizarre/bin/tclsh' ],
    , [with_tclsh=no])

case "$with_tclsh" in
    no)
        #  User specified --without-tclsh; this makes no sense,
        #  print a warning and search for it ourselves
        AC_MSG_WARN([Option '--without-tclsh'
        Causes some convenience scripts to be unusable.])
        ccatut_have_tclsh=no
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_tclsh=_searching
        ;;
    *)
        TCLSH="$with_tclsh"
        ccatut_have_tclsh=yes
        ;;
esac

if test "$with_tclsh" = _searching ; then
    AC_CHECK_PROG(tclsh_1, tclsh, tclsh, NONE)
    if test ! "$tclsh_1" = NONE ; then
        TCLSH=`which $tclsh_1`
        ccatut_have_tclsh=yes
    fi
fi
if test "$ccatut_have_tclsh" = "no"; then
TCLSH=":"
fi
AC_SUBST(TCLSH)

]
)

#------------------------------------------------------------------------------
#  see if the user gave us the location of the tclsh
#------------------------------------------------------------------------------
AC_DEFUN(PROG_PYTHON,
[
AC_ARG_WITH(util-python, 
    [Location of python:
  --with-util-python=PYTHON_EXECUTABLE
                          The location of the python interpreter used for
                          non-babel utilities.
                          Give the full path:
                              --with-util-python='/usr/bin/python' ],
    , [with_util_python=yes])

case "$with_util_python" in
    no)
        #  User specified --without-tclsh; this makes no sense,
        #  print a warning and search for it ourselves
        AC_MSG_WARN([Option '--without-util-python'
        Causes some convenience scripts to be unusable.])
        have_util_python=no
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_util_python=_searching
        ;;
    *)
        UTIL_PYTHON="$with_util_python"
        have_util_python=yes
        ;;
esac

if test "$with_util_python" = _searching ; then
    AC_CHECK_PROG(python_1, python, python, NONE)
    if test ! "$python_1" = NONE ; then
        UTIL_PYTHON=`which $python_1`
        have_util_python=yes
    fi
fi
if test "x$have_util_python" = "xyes"; then
	if ! test -x $UTIL_PYTHON; then
		AC_MSG_ERROR([Unexecutable python found or given: $UTIL_PYTHON])
	fi
fi
AC_SUBST(UTIL_PYTHON)

]
)


#------------------------------------------------------------------------------
# TRILINOS_ROOT: See if the user gave us the location of trilinos
# then search $ccatut_trilinos_dirs.
# One of these directories must be
# present and contain the correct files, or else the user
# must give the directory that contains the correct files.
#------------------------------------------------------------------------------
AC_DEFUN(CCATUT_LIB_TRILINOS,
[
# Trilinos search paths
ccatut_trilinos_dirs="
    $TRILINOS_HOME
    $prefix/Trilinos-2.0a
    $CCATUT_HOME/Trilinos-2.0a
    $TOP/Trilinos-2.0a
    $CURRDIR_PARENT/Trilinos-2.0a
    $CURRDIR_GRANDPARENT/Trilinos-2.0a
    $CURRDIR_GREATGRANDPARENT/Trilinos-2.0a
    $CURRDIR_ANCESTOR/Trilinos-2.0a
    $HOME/Trilinos-2.0a
    $HOME/software/Trilinos-2.0a
    /home/alice/software/Trilinos-2.0a
    /usr/local/Trilinos-2.0a
    /home/local/Trilinos-2.0a
    $CURRDIR_PARENT/Trilinos
    $CURRDIR_GRANDPARENT/Trilinos
    $CURRDIR_GREATGRANDPARENT/Trilinos
    $CURRDIR_ANCESTOR/Trilinos
    $prefix/Trilinos
    $CCATUT_HOME/Trilinos
    $TOP/Trilinos
    $HOME/Trilinos
    $HOME/software/Trilinos
    /home/alice/CCA/Trilinos
    /home/alice/software/Trilinos
    /usr/local/Trilinos
    /home/local/Trilinos
"
AC_ARG_WITH(trilinos,
    [Location of trilinos:   
  --with-trilinos=TRILINOS_ROOT
                          The location of Trilinos
                          Give the full path: e.g.
                              --with-trilinos=/usr/local/Trilinos ] ,
    , [with_trilinos=yes])

case "$with_trilinos" in 
    no)
        # lUser input error
        with_trilinos=_searching
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_trilinos=_searching
        ;;
    *)
        TRILINOS_ROOT="$with_trilinos"
        ;;
esac

if test "$with_trilinos" = _searching ; then
    AC_MSG_CHECKING([for Trilinos distribution])
    for chome in $ccatut_trilinos_dirs ; do
        if test -d $chome ; then
            with_trilinos=$chome
            AC_MSG_RESULT([found $chome.])
            break
        fi
    done
fi
if test "$with_trilinos" = _searching ; then
    AC_MSG_RESULT([Cannot find Trilinos root directory.])
    AC_MSG_ERROR([Please install it and/or use --with-trilinos=TRILINOS_ROOT.])
fi
if test ! -f "$with_trilinos/adaptors/epetra_esi/src/Epetra_ESI_Object.h"  ; then
    AC_MSG_RESULT([No adaptors/epetra_esi/src/Epetra_ESI_Object.h.])
    AC_MSG_ERROR([Please install the version of Trilinos with ESI support.])
fi
TRILINOS_ROOT="$with_trilinos"
AC_SUBST(TRILINOS_ROOT)
]
)

#------------------------------------------------------------------------------
# PETSC_ROOT: See if the user gave us the location of PETSc
# then search $ccatut_petsc_dirs.
# One of these directories must be
# present and contain the correct files, or else the user
# must give the directory that contains the correct files.
#------------------------------------------------------------------------------
AC_DEFUN(CCATUT_LIB_PETSC,
[
# PETSc search paths
PETSC_VERSION="2.1.1"
ccatut_petsc_dirs="
    $PETSC_DIR
    $CCATUT_HOME/petsc-$PETSC_VERSION
    $TOP/petsc-$PETSC_VERSION
    $CURRDIR_PARENT/petsc-$PETSC_VERSION
    $CURRDIR_GRANDPARENT/petsc-$PETSC_VERSION
    $CURRDIR_GREATGRANDPARENT/petsc-$PETSC_VERSION
    $CURRDIR_ANCESTOR/petsc-$PETSC_VERSION
    $prefix/petsc-$PETSC_VERSION
    $HOME/petsc-$PETSC_VERSION
    $HOME/software/petsc-$PETSC_VERSION
    /usr/local/petsc-$PETSC_VERSION
    /home/local/petsc-$PETSC_VERSION
    $prefix/petsc
    $CCATUT_HOME/petsc
    $TOP/petsc
    $HOME/petsc
    $HOME/software/petsc
    /home/alice/CCA/petsc
    /usr/local/petsc
    /home/local/petsc"
AC_ARG_WITH(petsc,
    [Location of petsc:   
  --with-petsc=PETSC_ROOT
                          The location of PETSc
                          Give the full path: e.g.
                              --with-petsc=/usr/local/petsc ] ,
    , [with_petsc=yes])

case "$with_petsc" in 
    no)
        # lUser input error
        with_petsc=_searching
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_petsc=_searching
        ;;
    *)
        PETSC_ROOT="$with_petsc"
        ;;
esac

if test "$with_petsc" = _searching ; then
    AC_MSG_CHECKING([for PETSc distribution])
    for chome in $ccatut_petsc_dirs ; do
        if test -d $chome ; then
            with_petsc=$chome
            AC_MSG_RESULT([found $chome.])
            break
        fi
    done
fi
if test "$with_petsc" = _searching ; then
    AC_MSG_RESULT([Cannot find PETSc root directory.])
    AC_MSG_ERROR([Please install it and/or use --with-petsc=PETSC_ROOT.])
fi
if test ! -f "$with_petsc/include/esi/petsc/matrix.h"  ; then
    AC_MSG_RESULT([No include/esi/petsc/matrix.h in $with_petsc.])
    AC_MSG_ERROR([Please install the version of PETSc with ESI support.])
fi
if test "X$PETSC_ARCH" = X ; then
    PETSC_ARCH="`$with_petsc/bin/petscarch`"
fi 

PETSC_ROOT="$with_petsc"
AC_SUBST(PETSC_ROOT)
AC_SUBST(PETSC_ARCH)
])

#------------------------------------------------------------------------------
# TAO_ROOT: See if the user gave us the location of TAO
# then search $ccatut_tao_dirs.
# One of these directories must be
# present and contain the correct files, or else the user
# must give the directory that contains the correct files.
#------------------------------------------------------------------------------
AC_DEFUN(CCATUT_LIB_TAO,
[
TAO_VERSION="1.3"
ccatut_tao_dirs="
    $TAO_DIR
    $CCATUT_HOME/tao-$TAO_VERSION
    $TOP/tao-$TAO_VERSION
    $HOME/tao-$TAO_VERSION
    $CURRDIR_PARENT/tao-$TAO_VERSION
    $CURRDIR_GRANDPARENT/tao-$TAO_VERSION
    $CURRDIR_GREATGRANDPARENT/tao-$TAO_VERSION
    $CURRDIR_ANSCESTOR/tao-$TAO_VERSION
    $HOME/software/tao-$TAO_VERSION
    $prefix/tao-$TAO_VERSION
    /usr/local/tao-$TAO_VERSION
    /home/local/tao-$TAO_VERSION
    /home/software/tao-$TAO_VERSION
    $HOME/tao
    $CCATUT_HOME/tao
    $TOP/tao
    $CURRDIR_PARENT/tao
    $CURRDIR_GRANDPARENT/tao
    $CURRDIR_GREATGRANDPARENT/tao
    $CURRDIR_ANSCESTOR/tao
    $HOME/software/tao
    $prefix/tao
    /usr/local/tao
    /home/local/tao
    /home/software/tao
"
AC_ARG_WITH(tao,
    [Location of tao:   
  --with-tao=TAO_ROOT
                          The location of TAO
                          Give the full path: e.g.
                              --with-tao=/usr/local/tao ] ,
    , [with_tao=yes])

case "$with_tao" in 
    no)
        # lUser input error
        with_tao=_searching
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_tao=_searching
        ;;
    *)
        TAO_ROOT="$with_tao"
        ;;
esac

if test "$with_tao" = _searching ; then
    AC_MSG_CHECKING([for REQUIRED TAO distribution])
    for chome in $ccatut_tao_dirs ; do
        if test -d $chome ; then
            with_tao=$chome
            AC_MSG_RESULT([found $chome.])
            break
        fi
    done
fi
if test "$with_tao" = _searching ; then
    AC_MSG_RESULT([Cannot find TAO root directory.])
    AC_MSG_ERROR([Please install it and/or use --with-tao=TAO_ROOT.])
fi
if test ! -f "$with_tao/src/externaltao/esitao/esisolver/esiapplication.h"  ; then
    AC_MSG_RESULT([No src/externaltao/esitao/esisolver/esiapplication.h in $with_tao.])
    AC_MSG_ERROR([Please install the version of TAO with ESI support.])
fi
TAO_ROOT="$with_tao"
AC_SUBST(TAO_ROOT)
]
)


#------------------------------------------------------------------------------
# MXN_ROOT: See if the user gave us the location of Lsode
# then search $ccatut_mxn_dirs.
# One of these directories must be
# present and contain the correct files, or else the user
# must give the directory that contains the correct files.
#------------------------------------------------------------------------------
AC_DEFUN(CCATUT_SPEC_MXN,
[
ccatut_mxn_dirs="
    $CURRDIR_GRANDPARENT/jeeembo/CumulvsMxN
    $CURRDIR_GREATGRANDPARENT/jeeembo/CumulvsMxN
    $CURRDIR_ANCESTOR/jeeembo/CumulvsMxN
    $CCATUT_HOME/sandbox/jeeembo/CumulvsMxN
    $TOP/sandbox/jeeembo/CumulvsMxN
    $HOME/sandbox/jeeembo/CumulvsMxN
    $HOME/CumulvsMxN
    $HOME/cca/cca-sc01-demo/sandbox/jeembo/CumulvsMxN
    $HOME/CCA/sc_tut/ben/sandbox/jeeembo/CumulvsMxN
"
AC_ARG_WITH(mxn,
    [Location of lsode: 
  --with-mxn=MXN_ROOT   
                          The location of lsode integrator component
                          Give the full path: e.g.
                          --with-mxn=/usr/local/mxn ] ,
    , [with_mxn=yes])

case "$with_mxn" in
    no)
        # lUser input error
        with_mxn=_searching
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_mxn=_searching
        ;;
    *)
        MXN_ROOT="$with_mxn"
        ;;
esac

if test "$with_mxn" = _searching ; then
    AC_MSG_CHECKING([for REQUIRED mxn header distribution])
    for chome in $ccatut_mxn_dirs ; do
        if test -d $chome ; then
            with_mxn=$chome
            AC_MSG_RESULT([found $chome.])
            break
        fi
    done
fi
if test "$with_mxn" = _searching ; then
    AC_MSG_RESULT([Cannot find MxN specification root directory.])
    AC_MSG_ERROR([Please install it and/or use --with-mxn=MXN_ROOT.])
fi
if test ! -f "$with_mxn/MxNPort.h"  ; then
    AC_MSG_RESULT([No MxNPort.h in $with_mxn.])
    AC_MSG_ERROR([Please install the MXN component.])
fi
MXN_ROOT="$with_mxn"
AC_SUBST(MXN_ROOT)
]
)

#------------------------------------------------------------------------------
# VIZPROXY_ROOT: See if the user gave us the location of Lsode
# then search $ccatut_vizproxy_dirs.
# One of these directories must be
# present and contain the correct files, or else the user
# must give the directory that contains the correct files.
#------------------------------------------------------------------------------
AC_DEFUN(CCATUT_SPEC_VIZPROXY,
[
ccatut_vizproxy_dirs="
    $CURRDIR_GRANDPARENT/jeeembo/VizProxy
    $CURRDIR_GREATGRANDPARENT/jeeembo/VizProxy
    $CURRDIR_ANSCESTOR/jeeembo/VizProxy
    $CCATUT_HOME/sandbox/jeeembo/VizProxy
    $TOP/sandbox/jeeembo/VizProxy
    $HOME/CCA/sc_tut/ben/sandbox/jeeembo/VizProxy
    $HOME/cca/cca-sc01-demo/sandbox/jeembo/VizProxy
    $HOME/sandbox/jeeembo/VizProxy
"
AC_ARG_WITH(vizproxy,
    [Location of lsode: 
  --with-vizproxy=VIZPROXY_ROOT 
                          The location of lsode integrator component
                          Give the full path: e.g.
                          --with-vizproxy=/usr/local/vizproxy ] ,
    , [with_vizproxy=yes])

case "$with_vizproxy" in
    no)
        # lUser input error
        with_vizproxy=_searching
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_vizproxy=_searching
        ;;
    *)
        VIZPROXY_ROOT="$with_vizproxy"
        ;;
esac

if test "$with_vizproxy" = _searching ; then
    AC_MSG_CHECKING([for REQUIRED vizproxy header distribution])
    for chome in $ccatut_vizproxy_dirs ; do
        if test -d $chome ; then
            with_vizproxy=$chome
            AC_MSG_RESULT([found $chome.])
            break
        fi
    done
fi
if test "$with_vizproxy" = _searching ; then
    AC_MSG_RESULT([Cannot find Vizproxy specification root directory.])
    AC_MSG_ERROR([Please install it and/or use --with-vizproxy=VIZPROXY_ROOT.])
fi

VIZPROXY_ROOT="$with_vizproxy"
AC_SUBST(VIZPROXY_ROOT)
]
)

#------------------------------------------------------------------------------
# DADF_ROOT: See if the user gave us the location of Lsode
# then search $ccatut_dadf_dirs.
# One of these directories must be
# present and contain the correct files, or else the user
# must give the directory that contains the correct files.
#------------------------------------------------------------------------------
AC_DEFUN(CCATUT_SPEC_DADF,
[
ccatut_dadf_dirs="
    $CURRDIR_GRANDPARENT/bernhold/DistArrayDescriptorFactory
    $CURRDIR_GREATGRANDPARENT/bernhold/DistArrayDescriptorFactory
    $CURRDIR_ANSCESTOR/bernhold/DistArrayDescriptorFactory
    $CCATUT_HOME/sandbox/bernhold/DistArrayDescriptorFactory
    $TOP/sandbox/bernhold/DistArrayDescriptorFactory
    $HOME/CCA/sc_tut/ben/sandbox/bernhold/DistArrayDescriptorFactory
    $HOME/cca/cca-sc01-demo/sandbox/bernhold/DistArrayDescriptorFactory
    $HOME/sandbox/bernhold/DistArrayDescriptorFactory
"
AC_ARG_WITH(dadf,
    [Location of dadf: 
  --with-dadf=DADF_ROOT 
                          The location of DADF component
                          Give the full path: e.g.
                          --with-dadf=/usr/local/dadf ] ,
    , [with_dadf=yes])

case "$with_dadf" in
    no)
        # lUser input error
        with_dadf=_searching
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_dadf=_searching
        ;;
    *)
        DADF_ROOT="$with_dadf"
        ;;
esac

if test "$with_dadf" = _searching ; then
    AC_MSG_CHECKING([for REQUIRED dadf header distribution])
    for chome in $ccatut_dadf_dirs ; do
        if test -d $chome ; then
            with_dadf=$chome
            AC_MSG_RESULT([found $chome.])
            break
        fi
    done
fi
if test "$with_dadf" = _searching ; then
    AC_MSG_RESULT([Cannot find DADF specification root directory.])
    AC_MSG_ERROR([Please install it and/or use --with-dadf=DADF_ROOT.])
fi
if test ! -f "$with_dadf/DistArrayDescrFactoryPort.h"  ; then
    AC_MSG_RESULT([No DistArrayDescrFactoryPort.h in $with_dadf.])
    AC_MSG_ERROR([Please install the DADF component.])
fi
DADF_ROOT="$with_dadf"
AC_SUBST(DADF_ROOT)
]
)


#------------------------------------------------------------------------------
# LSODE_ROOT: See if the user gave us the location of Lsode
# then search $ccatut_lsode_dirs.
# One of these directories must be
# present and contain the correct files, or else the user
# must give the directory that contains the correct files.
#------------------------------------------------------------------------------
AC_DEFUN(CCATUT_SPEC_LSODE,
[
ccatut_lsode_dirs="
    $CURRDIR_GRANDPARENT/baallan/ode/odepackpp
    $CURRDIR_GREATGRANDPARENT/baallan/ode/odepackpp
    $CURRDIR_ANCESTOR/baallan/ode/odepackpp
    $CCATUT_HOME/sandbox/baallan/ode/odepackpp
    $TOP/sandbox/baallan/ode/odepackpp
    $HOME/sandbox/baallan/ode/odepackpp
    $HOME/CCA/sc_tut/ben/sandbox/baallan/ode/odepackpp
    $HOME/cca/cca-sc01-demo/sandbox/baallan/ode/odepackpp
    /home/cca/sandbox/baallan/ode/odepackpp
"
AC_ARG_WITH(lsode,
    [Location of lsode: 
  --with-lsode=LSODE_ROOT 
                          The location of lsode integrator component
                          Give the full path: e.g.
                          --with-lsode=/usr/local/lsode ] ,
    , [with_lsode=yes])

case "$with_lsode" in
    no)
        # lUser input error
        with_lsode=_searching
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_lsode=_searching
        ;;
    *)
        LSODE_ROOT="$with_lsode"
        ;;
esac

if test "$with_lsode" = _searching ; then
    AC_MSG_CHECKING([for optional lsode header distribution])
    for chome in $ccatut_lsode_dirs ; do
        if test -d $chome ; then
            with_lsode=$chome
            AC_MSG_RESULT([found $chome.])
            break
        fi
    done
fi
if test "$with_lsode" = _searching ; then
    AC_MSG_RESULT([Cannot find LSODE specification root directory.])
    AC_MSG_ERROR([Please install it and/or use --with-lsode=LSODE_ROOT.])
fi
if test ! -f "$with_lsode/ProblemLogger/ProblemLogger.h"  ; then
    AC_MSG_RESULT([No ProblemLogger/ProblemLogger.h in $with_lsode.])
    AC_MSG_ERROR([Please install the LSODE component.])
fi
LSODE_ROOT="$with_lsode"
AC_SUBST(LSODE_ROOT)
]
)

#------------------------------------------------------------------------------
# ESIFACTORY_ROOT: See if the user gave us the location of esifactory
# then search $ccatut_esifactory_dirs.
# One of these directories must be
# present and contain the correct files, or else the user
# must give the directory that contains the correct files.
#------------------------------------------------------------------------------
AC_DEFUN(CCATUT_SPEC_ESIFACTORY,
[
ccatut_esifactory_dirs="
  $CURRDIR_PARENT/norris
  $CURRDIR_GRANDPARENT/norris
  $CURRDIR_GREATGRANDPARENT/norris
  $CURRDIR_ANCESTOR/norris
  $CCATUT_HOME/sandbox/norris
  $TOP/sandbox/norris
  $HOME/sandbox/norris
  $HOME/cca/sandbox/norris
  $HOME/CCA/sandbox/norris
  $HOME/CCA/sc_tut/ben/sandbox/norris
"
AC_ARG_WITH(esifactory,
    [Location of esifactory:	
  --with-esifactory=ESIFACTORY_ROOT	
                          The location of esifactory
                          Give the full path: e.g.
                          --with-esifactory=/usr/local/esifactory ] ,
    , [with_esifactory=yes])

case "$with_esifactory" in
    no)
        # lUser input error
        with_esifactory=_searching
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_esifactory=_searching
        ;;
    *)
        ESIFACTORY_ROOT="$with_esifactory"
        ;;
esac

if test "$with_esifactory" = _searching ; then
    AC_MSG_CHECKING([for REQUIRED esifactory header distribution])
    for chome in $ccatut_esifactory_dirs ; do
        if test -d $chome ; then
            with_esifactory=$chome
            AC_MSG_RESULT([found $chome.])
            break
        fi
    done
fi
if test "$with_esifactory" = _searching ; then
    AC_MSG_RESULT([Cannot find ESIFACTORY specification root directory.])
    AC_MSG_ERROR([Please install it and/or use --with-esifactory=ESIFACTORY_ROOT.])
fi
if test ! -f "$with_esifactory/ports/esifactory/ESIFactory.h" ; then
    AC_MSG_RESULT([No esifactory/ESIFactory.h in $with_esifactory.])
    AC_MSG_ERROR([Please install esifactory.])
fi
ESIFACTORY_ROOT="$with_esifactory"
AC_SUBST(ESIFACTORY_ROOT)
]
)

#------------------------------------------------------------------------------
# LINEARSOLVER_ROOT: See if the user gave us the location of LinearSolver interface
# then search $ccatut_linearsolver_dirs.
# One of these directories must be
# present and contain the correct files, or else the user
# must give the directory that contains the correct files.
#------------------------------------------------------------------------------
AC_DEFUN(CCATUT_SPEC_LINEARSOLVER,
[
ccatut_ls_dirs="
  $CURRDIR_PARENT/norris
  $CURRDIR_GRANDPARENT/norris
  $CURRDIR_GREATGRANDPARENT/norris
  $CURRDIR_ANCESTOR/norris
  $CCATUT_HOME/sandbox/norris
  $TOP/sandbox/norris
  $HOME/sandbox/norris
  $HOME/cca/sandbox/norris
  $HOME/CCA/sandbox/norris
  $HOME/CCA/sc_tut/ben/sandbox/norris
"
AC_ARG_WITH(ls,
            [Location of Linear Solver interface specification:
             --with-ls = LinearSolverPort_HOME
                          The location of Linear Solver Ports. Give the full path: e.g.
                              --with-ls='/usr/local/LinearSolver' ] ,
           , [with_ls=no])

case "$with_ls" in
    no)
        # lUser input error
        with_ls=_searching
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_ls=_searching
        ;;
    *)
        LS_ROOT="$with_ls"
        ;;
esac

if test "$with_ls" = _searching ; then
    AC_MSG_CHECKING([for REQUIRED Linear Solver Port])
    for ls_home in $ccatut_ls_dirs ; do
        if test -d $ls_home ; then
            with_ls=$ls_home
            AC_MSG_RESULT([found $ls_home.])
            break
        fi
    done
fi
if test "$with_ls" = _searching ; then
    AC_MSG_RESULT([Cannot find Linear Solver Ports root directory.])
    AC_MSG_ERROR([Please install it and/or use --with-ls=LinearSolverPort_HOME.])
fi

if test ! -f "$with_ls/ports/linearsolver/LinearSolver.h"  ; then
    AC_MSG_RESULT([No ports/linearsolver/LinearSolver.h in $with_ls.])
    AC_MSG_ERROR([Please install a correct Linear Solver Port headers.])
fi

LS_ROOT="$with_ls"
AC_SUBST(LS_ROOT)
]
)

#------------------------------------------------------------------------------
# VTK_ROOT: See if the user gave us the location of Lsode
# then search $ccatut_vtk_dirs.
# One of these directories must be
# present and contain the correct files, or else the user
# must give the directory that contains the correct files.
#------------------------------------------------------------------------------
AC_DEFUN(CCATUT_LIB_VTK,
[
ccatut_vtk_dirs="
    /usr/lib
    /usr/local/lib
    $prefix
    $CCATUT_HOME/vtk
    $TOP/vtk
    /home/local/lib
    $HOME/vtk3.2-glMesa
    /home/freitag/vtk3.2-glMesa
    /home/FuturesLab/Software/Linux/vtk3.2-glMesa
    $HOME/vtk-3.12/vtk31
    $HOME/vtk31
    /home/freitag/vtk31
    /home/freitag/CCA/vtk3.2-glMesa
"
AC_ARG_WITH(vtk,
    [Location of lsode:	
  --with-vtk=VTK_ROOT	
                          The location of lsode integrator component
                          Give the full path: e.g.
                          --with-vtk=/usr/local/vtk ] ,
    , [with_vtk=yes])

case "$with_vtk" in
    no)
        # lUser input error
        with_vtk=_searching
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_vtk=_searching
        ;;
    *)
        VTK_ROOT="$with_vtk"
        ;;
esac

if test "$with_vtk" = _searching ; then
    AC_MSG_CHECKING([for REQUIRED vtk header distribution])
    for chome in $ccatut_vtk_dirs ; do
        if test -d $chome ; then
            with_vtk=$chome
            AC_MSG_RESULT([found $chome.])
            break
        fi
    done
fi
if test "$with_vtk" = _searching ; then
    AC_MSG_RESULT([Cannot find VTK specification root directory.])
    AC_MSG_ERROR([Please install it and/or use --with-vtk=VTK_ROOT.])
fi
if test ! -f "$with_vtk/graphics/libVTKGraphics.so" -a ! -f "$with_vtk/libVTKGraphics.so" ; then
    AC_MSG_RESULT([No graphics/libVTKGraphics.so in $with_vtk.])
    AC_MSG_ERROR([Please install the VTK 3.1.2 or higher.])
fi

VTK_ROOT="$with_vtk"
AC_SUBST(VTK_ROOT)
]
)

# MESA
#------------------------------------------------------------------------------
# MESA_ROOT: See if the user gave us the location of Lsode
# then search $ccatut_mesa_dirs.
# One of these directories must be
# present and contain the correct files, or else the user
# must give the directory that contains the correct files.
#------------------------------------------------------------------------------
AC_DEFUN(CCATUT_LIB_MESA,
[
ccatut_mesa_dirs="
    /usr/lib
    /usr/local/lib
    /home/local/lib
    /usr/local/Mesa
    /home/freitag/Mesa-3.5
    /home/freitag/CCA/Mesa-3.5
    /homes/FuturesLab/Software/Mesa-3.2.1/
    /home/freitag/Mesa-3.2.1
    $CCATUT_HOME/Mesa
    $HOME/Mesa-4.0
    /home/fretiag/Mesa-4.0
"
AC_ARG_WITH(mesa,
    [Location of lsode:	
  --with-mesa=MESA_ROOT	
                          The location of lsode integrator component
                          Give the full path: e.g.
                          --with-mesa=/usr/local/mesa ] ,
    , [with_mesa=yes])

case "$with_mesa" in
    no)
        # lUser input error
        with_mesa=_searching
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_mesa=_searching
        ;;
    *)
        MESA_ROOT="$with_mesa"
        ;;
esac

if test "$with_mesa" = _searching ; then
    AC_MSG_CHECKING([for REQUIRED mesa header distribution])
    for chome in $ccatut_mesa_dirs ; do
        if test -d $chome ; then
            with_mesa=$chome
            AC_MSG_RESULT([found $chome.])
            break
        fi
    done
fi
if test "$with_mesa" = _searching ; then
    AC_MSG_RESULT([Cannot find MESA specification root directory.])
    AC_MSG_ERROR([Please install it and/or use --with-mesa=MESA_ROOT.])
fi

MESA_ROOT="$with_mesa"
AC_SUBST(MESA_ROOT)
]
)

#------------------------------------------------------------------------------
# DOXYGEN_PATH: See if the user gave us the location of doxygen
# then search $ccatut_dox_dirs_dirs.
# One of these directories must be
# present and contain the correct files, or else the user
# must give the directory that contains the correct files.
#------------------------------------------------------------------------------
AC_DEFUN(CCATUT_PROG_DOXYGEN,
[
ccatut_dox_dirs="
    $prefix/bin/doxygen
    /usr/bin/doxygen
    /usr/local/bin/doxygen
    $CCATUT_HOME/doxygen
    $TOP/doxygen
    $HOME/doxygen/bin/doxygen
    $HOME/bin/doxygen
"
AC_ARG_WITH(dox, 
            [Location of doxygen:
             --with-dox=DoxygenLocation
             The location of doxygen. Give the full path:
                              --with-dox='/usr/local/bin/doxygen'],
    , [with_dox=_searching])

case "$with_dox" in
    no)
 	AC_MSG_WARN([Option '--without-dox'
	makes it impossible to produce source-based documentation.])
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_dox=_searching
        ;;
    *)
        DOXYGEN_PATH="$with_dox"
        ;;
esac

if test "$with_dox" = _searching ; then
    AC_MSG_CHECKING([for OPTIONAL doxygen])
    for dox in $ccatut_dox_dirs ; do
        if test -f $dox ; then
            with_dox=$dox
            AC_MSG_RESULT([found $dox.])
            break
        fi
    done
fi

if test "$with_dox" = _searching ; then
    AC_MSG_RESULT([Cannot find doxygen.])
    AC_MSG_WARN([Without doxygen, it is impossible to produce source-based 
	documentation.  If you wish to be able to generate this documentation,
	please re-run configure with a --with-dox=doxygen_path option.])
    with_dox="no"
fi

if test "$with_dox" = no ; then
   with_dox="@echo WARNING: doxygen not configured!"
fi

DOXYGEN_PATH="$with_dox"
AC_SUBST(DOXYGEN_PATH)
]
)

#------------------------------------------------------------------------------
# Find an OPTIONAL jdk1.2
#------------------------------------------------------------------------------
AC_DEFUN(CCATUT_PROG_JAVA,
[
# jdk for java2/swing
ccatut_java_dirs="
    $JAVA_HOME
    $JAVA_HM
    /usr/local/jdk1.2.2
    $HOME/jdk1.2.2
    /usr/local/jdk
    /opt/local/jdk1.2.2
    /opt/local/jdk
    $prefix/jdk1.2.2
    $prefix/jdk
"

# java_home

if test "$target_os" = "macosx" ; then
    # MacOSX comes with complete Java package installed
    AC_PATH_PROG(JAVA_HM, javac, , /usr/bin)
    JAVA_HM="/usr"
else
    AC_ARG_WITH(jdk12,
        [Location of jdk 1.2. Give the full path:
      --with-jdk12=JAVA_HOME] , , [with_jdk12=_searching])
    case "$with_jdk12" in
	no)
	    AC_MSG_WARN([Option '--without-jdk12' may result in reduced functionality.])
	    ;;
	yes)
	    with_jdk12=_searching
	    ;;
	*)
	    JAVA_HM="$with_jdk12"
	    ;;
    esac

    if test "$with_jdk12" = _searching ; then
        AC_MSG_RESULT([Searching for jdk 1.2 or later])
        for jhome in $ccatut_java_dirs ; do
            AC_PATH_PROG(JAVA_HM, javac, , $jhome/bin)
            if test ! -z "$JAVA_HM" ; then
                AC_MSG_RESULT([Found $JAVA_HM.])
                break
            fi
        done
    else
        AC_PATH_PROG(JAVA_HM, javac, , $with_jdk12/bin)
    fi
    if test -z "$JAVA_HM" ; then
	AC_MSG_RESULT([Cannot find jdk 1.2 or later.])
        AC_MSG_WARN([Without jdk 1.2, functionality may be reduced.  You may
	want to re-run configure with a --with-jdk12=JAVA_HOME option.])
    fi
    # find the jni header to get version
    jhome=`echo $JAVA_HM | sed 's/\/javac$//' | sed 's/\/bin$//'`
    java_header_file=$jhome/include/jni.h
    jni_h_version=`grep JDK1_2 $java_header_file | sed 's/#define //'`
    # or we could attempt 
    # version=`$JAVA_HM -version 2>&1 |grep \"1.2 | sed 's/java version "//' |sed 's/"//'`

    # check for java2-ness
    AC_EGREP_HEADER(JDK1_2, $java_header_file, [ JAVA_HM=$jhome], [ JAVA_HM=no_java_found ])
    if test ! "X$jni_h_version" = "XJDK1_2" ; then
        AC_MSG_ERROR([JDK {$jhome} is the wrong version, apparently.
                      Use --with-jdk12=JAVA_HOME for a jdk1.2 or compatible version,])
    fi
    JAVA_HM=$jhome
fi
AC_SUBST(JAVA_HM)
]
)


dnl CCAFE_AC_PREFIX(DEFAULT)
dnl --------------------------------------------------------------------
dnl Side effects: updates all the prefix related variables using
dnl DEFAULT if prefix has not been properly defined by now.
dnl fully expands the values, too.
dnl --------------------------------------------------------------------
AC_DEFUN(CCAFE_AC_PREFIX,
[
  if test -z "$1" ; then
    AC_MSG_ERROR([Ccafe_ac_prefix macro requires a default path.])
  fi
  if test -z "$prefix" -o "$prefix" = "NONE"; then
    prefix=$1;
  fi
  if test -z "$datarootdir" -o "$datarootdir" = "NONE/share" -o "$datarootdir" = '${prefix}/share' ; then
    datarootdir="$prefix/share";
  fi
  if test -z "$datadir" -o "$datadir" = "NONE/share" -o "$datadir" = '${prefix}/share' -o "$datadir" = '${datarootdir}' ; then
    datadir="$datarootdir";
  fi
  if test -z "$sysconfdir" -o "$sysconfdir" = "NONE/etc" -o "$sysconfdir" = '${prefix}/etc' ; then
    sysconfdir="$prefix/etc";
  fi
  if test -z "$sharedstatedir" -o "$sharedstatedir" = "NONE/com" -o "$sharedstatedir" = '${prefix}/com' ; then
    sharedstatedir="$prefix/com";
  fi
  if test -z "$localstatedir" -o "$localstatedir" = "NONE/var" -o "$localstatedir" = '${prefix}/var' ; then
    localstatedir="$prefix/var";
  fi
  if test -z "$includedir" -o "$includedir" = "NONE/include" -o "$includedir" = '${prefix}/include' ; then
    includedir="$prefix/include";
  fi
  if test -z "$infodir" -o "$infodir" = "NONE/info" -o "$infodir" = '${prefix}/info' ; then
    infodir="$prefix/info";
  fi
  if test -z "$mandir" -o "$mandir" = "NONE/man" -o "$mandir" = '${prefix}/man' ; then
    mandir="$prefix/man";
  fi
]
)

dnl --------------------------------------------------------------------
dnl requires prefix be define, or does nothing.
dnl --------------------------------------------------------------------
AC_DEFUN(CCAFE_AC_EXEC_PREFIX,
[
  if test -z "$1" ; then
    AC_MSG_ERROR([Ccafe_ac_exec_prefix macro requires a default path.])
  fi
  if test -z "$exec_prefix" -o "$exec_prefix" = "NONE"; then
     exec_prefix=$1;
  fi
  if test -z "$bindir" -o "$bindir" = "NONE/bin" -o "$bindir" = '${exec_prefix}/bin' ; then
    bindir="$exec_prefix/bin";
  fi
  if test -z "$sbindir" -o "$sbindir" = "NONE/sbin" -o "$sbindir" = '${exec_prefix}/sbin'; then
    sbindir="$exec_prefix/sbin";
  fi
  if test -z "$libexecdir" -o "$libexecdir" = "NONE/libexec" -o "$libexecdir" = '${exec_prefix}/libexec' ; then
    libexecdir="$exec_prefix/libexec";
  fi
  if test -z "$libdir" -o "$libdir" = "NONE/lib" -o "$libdir" = '${exec_prefix}/lib' ; then
    libdir="$exec_prefix/lib";
  fi
]
)


dnl --------------------------------------------------------------------
dnl define the sidl preamble, based on CCASPEC_BABEL_VERSION
dnl --------------------------------------------------------------------
AC_DEFUN(GOVCCA_SIDL_START,
[
# -----------------------------------------------------
# compute top of cca.sidl, given babel version.
# -----------------------------------------------------
GOVCCA_SIDL_START_0=" unsupported_babel_version. fix acsite.m4 and configure"
GOVCCA_SIDL_START_1="// package gov {"
GOVCCA_SIDL_START_2="// package cca version $CCASPEC_VERSION {"
GOVCCA_SIDL_START_3="//"
GOVCCA_SIDL_START_4="//"
GOVCCA_SIDL_START_5="//"

# this is better done with a case statement.
OBSOLETE=0
case "x$CCASPEC_BABEL_VERSION" in
  x0.7.*) OBSOLETE=1
          ;;
  x0.8.*) OBSOLETE=1
          ;;
  x0.9.*) OBSOLETE=1
          ;;
  x0.10.*) OBSOLETE=1
          ;;
  x0.11.*) OBSOLETE=1
          ;;
  x0.99.*) OBSOLETE=1
          ;;  
  x1.0.*) PREAMBLE_VER=09
          ;;  
  x1.1.*) OBSOLETE=1
          ;;  
  x1.2.*) PREAMBLE_VER=09
          ;;  
  x1.4.*) PREAMBLE_VER=09
          ;;  
  x$CUSTOM_BABEL_VERSION) PREAMBLE_VER=09
          ;;  
esac
if test "x$OBSOLETE" = "X1"; then
  AC_MSG_ERROR([obsolete babel $CCASPEC_BABEL_VERSION unsupported. Try 1.0.x or 1.4.x versions.])
fi
case "x$PREAMBLE_VER" in
  x07,x08)
    AC_MSG_ERROR([obsolete babel $CCASPEC_BABEL_VERSION unsupported.])
    ;;
  x09) 
    GOVCCA_SIDL_START_0=""
    GOVCCA_SIDL_START_1="package gov {"
    GOVCCA_SIDL_START_2="package cca version $CCASPEC_VERSION {"
    GOVCCA_SIDL_START_4=""
    GOVCCA_SIDL_START_5=""
    ;;
  *) AC_MSG_ERROR([babel $CCASPEC_BABEL_VERSION unsupported.])
    ;;
esac

# computed preamble
# -----------------------------------------------------
]
)


dnl CCAFE_CONFIG_ARGS(VAR)
dnl --------------------------------------------------------------------
dnl capture the ./configure arguments in VAR.
dnl --------------------------------------------------------------------
AC_DEFUN(CCAFE_CONFIG_ARGS,
[
  if test -z "$1" ; then
    AC_MSG_ERROR([Ccafe_config_args macro requires a variable name.])
  fi
  $1=[$]*
]
)



dnl    BABEL_PATH_TO_CONFIG_VER(VARIABLE, BINVAR, PATH, TEST_FILE,
dnl      [ RUN_IF_FOUND], [RUN_IF_NOT_FOUND])
dnl    Test for the presence of file(s) (TEST_FILE) in the given colon
dnl    separated list of directory paths (PATH).  If all the file 
dnl    is found, it sets VARIABLE to the matching PATH element and
dnl    BINVAR to script found.
dnl    The last two arguments are run if a path to the
dnl    files is found or not found respectively.
dnl Side effects:
dnl   If variable BABEL_PATH_TO_CONFIG is predefined to contain
dnl   the name of an appropriate executable, then we get
dnl   that as BINVAR and its root as VARIABLE.

AC_DEFUN(BABEL_PATH_TO_CONFIG_VER,
[

  
dnl AC_MSG_RESULT([entering babel_path_to_config_ver])
p2cv_var="$1"
p2cv_binvar="$2"
p2cv_path="$3"
p2cv_testFile="$4"
p2cv_config="no"
p2cv_ok=no

if test "x$BABEL_PATH_TO_CONFIG" != "x" ; then
  if test -x $BABEL_PATH_TO_CONFIG ; then
    p2cv_config=$BABEL_PATH_TO_CONFIG
    p2cv_path=`$BABEL_PATH_TO_CONFIG --query-var=prefix`
    p2cv_result=$p2cv_path
    $1=$p2cv_result
    $2=$p2cv_config
    p2cv_ok=yes
    if test -n '$5' ; then
      # if found
      $5 
    fi
dnl    AC_MSG_RESULT([found $BABEL_PATH_TO_CONFIG])
  else
    AC_MSG_WARN([Ignoring env BABEL_PATH_TO_CONFIG pointing to non-executable $BABEL_PATH_TO_CONFIG.])
  fi
fi

if test "$p2cv_ok" = "no" ; then

  p2cv_tmpfile=`pwd`/.p2cv_tmpfile

  # for path elements
  # if ! element/testfile exists, res=search
  # for file-* w/ver number, try highest number
  # and work down. ver must end in a digit

  p2cv_result=_searching
  p2cv_paths=`echo $p2cv_path|tr ":" " "`
  for chome in $p2cv_paths ; do
dnl    AC_MSG_RESULT([trying $chome])
    if test -x $chome/$p2cv_testFile ; then
        p2cv_result=$chome
        p2cv_config=$chome/$p2cv_testFile
        $1=$p2cv_result
        $2=$p2cv_config
        if test -n '$5' ; then
            # if found
              $5 
        fi
dnl        AC_MSG_RESULT([found basenamed file])
        break
    fi  

    if test -d $chome ; then
        pushd $chome > /dev/null
        flist="${p2cv_testFile}*"
        popd > /dev/null
        /bin/rm -f $p2cv_tmpfile
        for fname in $flist ; do
          echo $fname >> $p2cv_tmpfile
        done
        flist=`cat $p2cv_tmpfile | sort -n -r`
        /bin/rm -f $p2cv_tmpfile
        for fname in $flist ; do
            if test -x $chome/$fname ; then
                p2cv_result=$chome
                p2cv_config=$chome/$fname
                $1=$p2cv_result
                $2=$p2cv_config
                if test -n '$5' ; then
                    # if found
                  $5 
                fi
dnl                AC_MSG_RESULT([       found: $p2cv_result/$fname])
                break;
            fi
        done
    fi
  done
  # not found anywhere
  if test "$p2cv_result" = _searching ; then
dnl    AC_MSG_RESULT([        nothing found])
    p2cv_result=no
    if test -n '$6' ; then
      #if not found
        $6
    fi
  fi
  # end of search for config with ver.

dnl end of p2cv_ok no test
fi
dnl AC_MSG_RESULT([leaving babel_path_to_config_ver])
]
)

dnl BABEL_CONFIG_FIND(DISTROOT, PATH, TESTFILE, NOTFOUNDWARNING, CONFIGBIN)
dnl input
dnl DISTROOT- input: the variable to set with the result
dnl PATH- the directories to check for babel by finding babel-config
dnl TESTFILE- the script file we require to exist.
dnl
dnl Output/sideeffects
dnl DISTROOT becomes defined as  no, or a directory
dnl CONFIGBIN becomes defined as no, or the name of the babel-config script
dnl
dnl See if the user gave us the location of babel.
dnl This is a routine used by another macro that should be preferred.
dnl Use macro BABEL_CONFIG instead of BABEL_CONFIG_FIND.
dnl
dnl This macro does discovery and is reusable. 
dnl policy matters such as paths checked
dnl and fatal or not are specific to the configure that includes this macro.
dnl
dnl eg bABEL_CONFIG_FIND(BABEL_ROOT, testpaths, bin/babel-config, msg, BABEL_CONFIG_PROG)
AC_DEFUN(BABEL_CONFIG_FIND,
[
CCAFE_BABEL_TEST=""
CCAFE_BABEL=""
AC_ARG_WITH(babel,
    [
Location of babel installation:
  --with-babel=INSTALLED_PREFIX
            The location of babel.  Give the full path:
                  --with-babel='/where/is/babel/installed'
            Better to use --with-babel-config, however.
              ] ,
    , [with_babel=yes])

case "$with_babel" in
    no)
        CCAFE_BABEL="no"
        AC_MSG_WARN([babel disabled.
   Use --with-babel=/where/babel/installed if wanted.])
        ;;
    yes)
        #  User didn't give the option or didn't give useful
        #  information, search for it ourselves
        with_babel="yes"
        CCAFE_BABEL="yes"
  AC_MSG_CHECKING([babel])
        ;;
    *)
        CCAFE_BABEL="$with_babel"
	if ! test -d $with_babel ; then
		AC_MSG_WARN([Path specified in --with-babel does not exist.])
	fi
	AC_MSG_CHECKING([babel])
        ;;
esac


CCAFE_BABEL_TEST="$CCAFE_BABEL"
CCAFE_BABEL_CONFIG_TEST="no"
if test "$CCAFE_BABEL" != "no"; then
        CCAFE_BABEL_TEST=""
        BABEL_PATH_TO_CONFIG_VER(CCAFE_BABEL_TEST, CCAFE_BABEL_CONFIG_TEST, $with_babel:$2, $3,
                CCAFE_BABEL="$CCAFE_BABEL_TEST" 
                CCAFE_BABEL_CONFIG="$CCAFE_BABEL_CONFIG_TEST" ,
                CCAFE_BABEL_TEST="no"
                CCAFE_BABEL="no"
                CCAFE_BABEL_CONFIG_TEST=no
                CCAFE_BABEL_CONFIG=no
                [AC_MSG_WARN([$4])]
        )
fi

$1="$CCAFE_BABEL"
$5="$CCAFE_BABEL_CONFIG"
dnl AC_MSG_RESULT([root $CCAFE_BABEL , config $CCAFE_BABEL_CONFIG])


]
)

dnl BABEL_CONFIG(PATH, CONFIGBIN)
dnl input
dnl PATH- the directories to check for babel by finding babel-config
dnl CONFIGBIN- output variable set to the result found, or the empty string.
dnl
AC_DEFUN(BABEL_CONFIG,
[
AC_ARG_WITH(babel-config,
[
Location of babel-config program:
  --with-babel-config=/usr/local/bin/babel-config[version_number]
            Specify the particular babel config info script.
            This option overrides environment variable BABEL_PATH_TO_CONFIG.
] , , [with_babel_config=no])

case "$with_babel_config" in
    no)
        ;;
    yes)
        with_babel_config="no"
        AC_MSG_ERROR([--with-babel-config must be given the path of the script.])
        ;;
    *)
        if test -d $with_babel_config ; then
          AC_MSG_ERROR([--with-babel-config must be given the path of the script, not a directory.])
        fi
        if ! test -x $with_babel_config ; then
          AC_MSG_ERROR([--with-babel-config=$with_babel_config: $with_babel_config not executable])
        fi
        BABEL_PATH_TO_CONFIG=$with_babel_config
        ;;
esac

trybabeldirs="$1:/usr/local:/usr:/usr/local/babel:/usr/local/babel-0.9.8:/usr/local/babel-0.10.0:$HOME/babel"
BABEL_CONFIG_FIND(BC_INST_ROOT, $trybabeldirs, bin/babel-config, , BC_CONFIGBIN)

if test "x$BC_CONFIGBIN" != "xno" ; then
  $2="$BC_CONFIGBIN"
else
  $2=""
fi
BABEL_ROOT="$BC_INST_ROOT"

]
)

builtin(include,config/cca_comp_flags.m4)
builtin(include,config/llnl_libxml.m4)
builtin(include,config/ccafe_pushd.m4)
builtin(include,config/ccafe_shlib_suffix.m4)
builtin(include,config/cca_bundle_tag.m4)
builtin(include,config/ccafe_libtoolmake.m4)
builtin(include,config/cca_enable_mpi.m4)
builtin(include,config/cca_enable_contrib.m4)
builtin(include,config/cca_babel_branch_version.m4)
