
dnl macro CCAFE_HIDELIBTOOL
dnl ------------------------------------------------------------------------------
dnl  HIDELIBTOOL defined as @ or ""
dnl  show libtool in make or not? Useful in debugging our makefiles.
dnl ------------------------------------------------------------------------------
AC_DEFUN([CCAFE_HIDELIBTOOL],
[
AC_ARG_ENABLE(showlibtool, [  --enable-showlibtool    Should libtool invocations be printed?],
              [enable_showlibtool=$enableval], [enable_showlibtool=no])
HIDELIBTOOL=@
if test ! "X$enable_showlibtool" = "Xno"; then
  enable_showlibtool=yes
fi
if test "X$enable_showlibtool" = "Xyes"; then
  HIDELIBTOOL=
fi

]
)

dnl macro CCAFE_HIDECOMPILE
dnl ------------------------------------------------------------------------------
dnl  HIDECOMPILE defined as --quiet or ""
dnl  show libtool generated compiler invocations or not? 
dnl  Useful in debugging our makefiles.
dnl ------------------------------------------------------------------------------
AC_DEFUN([CCAFE_HIDECOMPILE],
[
AC_ARG_ENABLE(showcompile, [  --enable-showcompile    Should compiler invocations be printed?],
              [enable_showcompile=$enableval], [enable_showcompile=no])
HIDECOMPILE=--quiet
if test ! "X$enable_showcompile" = "Xno"; then
  enable_showcompile=yes
fi
if test "X$enable_showcompile" = "Xyes"; then
  HIDECOMPILE=
fi

]
)

