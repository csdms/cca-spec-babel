
dnl macro CCA_ENABLE_MPI
dnl ------------------------------------------------------------------------------
dnl  ENABLE_MPI defined as 1 or 0
dnl ------------------------------------------------------------------------------
AC_DEFUN([CCA_ENABLE_MPI],
[
AC_ARG_ENABLE(mpi, [  --enable-mpi=yes    Should mpi port be included?
                     (presently not quite in the standard officially).],
              [enable_mpi=$enableval], [enable_mpi=no])
ENABLE_MPI=0
if test ! "X$enable_mpi" = "Xyes"; then
  enable_mpi=no
fi
if test "X$enable_mpi" = "Xyes"; then
  ENABLE_MPI=1
fi

]
)
