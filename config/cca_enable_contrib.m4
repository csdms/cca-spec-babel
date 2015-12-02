
dnl macro CCA_ENABLE_CONTRIB
dnl ------------------------------------------------------------------------------
dnl  ENABLE_CONTRIB defined as 1 or 0
dnl  show libtool in make or not? Useful in debugging our makefiles.
dnl ------------------------------------------------------------------------------
AC_DEFUN([CCA_ENABLE_CONTRIB],
[
AC_ARG_ENABLE(contrib, [  --enable-contrib=yes    Should contrib be included?
                     (presently should be avoided).],
              [enable_contrib=$enableval], [enable_contrib=no])
ENABLE_CONTRIB=0
if test ! "X$enable_contrib" = "Xyes"; then
  enable_contrib=no
fi
if test "X$enable_contrib" = "Xyes"; then
  ENABLE_CONTRIB=1
fi

]
)
