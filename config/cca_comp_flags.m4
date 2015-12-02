dnl
dnl cca_cxxflags_option(flagsToTest,varToAppendIfPass)
dnl
AC_DEFUN([CCA_CXXFLAGS_OPTION],
[
  AC_LANG_SAVE
  AC_LANG_CPLUSPLUS

  AC_MSG_CHECKING([if c++ compiler understands $1])
  OLDCXX="$CXX"
  CXX="$CXX $1" 
  AC_TRY_COMPILE(,,
    $2="${$2} $1"
    AC_MSG_RESULT(yes), AC_MSG_RESULT(no))
  CXX="$OLDCXX"
  AC_LANG_RESTORE
]
)

dnl
dnl cca_cflags_option(flagsToTest,varToAppendIfPass)
dnl
AC_DEFUN([CCA_CFLAGS_OPTION],
[
  AC_LANG_SAVE
  AC_LANG_C
  AC_MSG_CHECKING([if c compiler understands $1])
  OLDCC="$CC"
  CC="$CC $1" 
  AC_TRY_COMPILE(,,
    $2="${$2} $1"
    AC_MSG_RESULT(yes), AC_MSG_RESULT(no))
  CC="$OLDCC"
  AC_LANG_RESTORE

]
)
