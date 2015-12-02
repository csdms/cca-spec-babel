
dnl macro CCA_BABEL_BRANCH_VERSION
dnl ------------------------------------------------------------------------------
dnl  CCASPEC_BABEL_SNAPSHOT defined as 1 or 0. 
dnl  if 1, CCASPEC_BABEL_BRANCH, CCASPEC_BABEL_BRANCH_MAJOR,
dnl CCASPEC_BABEL_BRANCH_MINOR, CCASPEC_BABEL_BRANCH_RELEASE
dnl defined per user input.
dnl ------------------------------------------------------------------------------
AC_DEFUN([CCA_BABEL_BRANCH_VERSION],
[
AC_ARG_WITH(babel-branch, [  --with-babel-branch=x.y.z    Branch of babel development to assume.
                     If using an official babel release, do not use this switch.],
              [babel_branch=$withval], [babel_branch=no])
CCASPEC_BABEL_SNAPSHOT=0
if test "X$babel_branch" = "Xyes"; then
  AC_MSG_ERROR([--with-babel-branch must be given a value (e.g. --with-babel-branch=1.4.0)])
fi
if test ! "X$babel_branch" = "Xno"; then
  CCASPEC_BABEL_SNAPSHOT=1
fi

if test "x$CCASPEC_BABEL_SNAPSHOT" = "x1"; then
  CCASPEC_BABEL_BRANCH=$babel_branch
  CCASPEC_BABEL_BRANCH_MAJOR=`echo $CCASPEC_BABEL_BRANCH | sed -e 's/\([[0-9]]*\)\.\([[0-9]]*\)\.\([[0-9]]*\)/\1/'`
  CCASPEC_BABEL_BRANCH_MINOR=`echo $CCASPEC_BABEL_BRANCH | sed -e 's/\([[0-9]]*\)\.\([[0-9]]*\)\.\([[0-9]]*\)/\2/'`
  CCASPEC_BABEL_BRANCH_PATCH=`echo $CCASPEC_BABEL_BRANCH | sed -e 's/\([[0-9]]*\)\.\([[0-9]]*\)\.\([[0-9]]*\)/\3/'`

fi

AC_SUBST(CCASPEC_BABEL_BRANCH)
AC_SUBST(CCASPEC_BABEL_BRANCH_MAJOR)
AC_SUBST(CCASPEC_BABEL_BRANCH_MINOR)
AC_SUBST(CCASPEC_BABEL_BRANCH_PATCH)
AC_SUBST(CCASPEC_BABEL_SNAPSHOT)

]
)

AC_DEFUN([CCA_BABEL_BRANCH_CHECK],
[
  babel_branch_error=0
  if test "x$CCASPEC_BABEL_BRANCH_MAJOR" = "x"; then
    babel_branch_error=1
  fi
  if test "x$CCASPEC_BABEL_BRANCH_MINOR" = "x"; then
    babel_branch_error=$babel_branch_error,2
  fi
  if test "x$CCASPEC_BABEL_BRANCH_PATCH" = "x"; then
    babel_branch_error=$babel_branch_error,3
  fi
  if test ! "x$babel_branch_error" = "x0"; then
     AC_MSG_ERROR([--with-babel-branch=$CCASPEC_BABEL_BRANCH is an invalid version string. (elements $babel_branch_error) Expected X.Y.Z format.])
  fi

])


AC_DEFUN([CCA_BABEL_BRANCH_FROM_RELEASE],
[
CCASPEC_BABEL_BRANCH=$1
CCASPEC_BABEL_BRANCH_MAJOR=$2
CCASPEC_BABEL_BRANCH_MINOR=$3
CCASPEC_BABEL_BRANCH_PATCH=$4
])

