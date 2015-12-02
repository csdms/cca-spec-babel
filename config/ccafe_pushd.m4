dnl macro CCAFE_PUSHD
dnl --------------------------------------------------------------------
dnl define pushd and popd as bourne shell functions
dnl for stack up to 20 deep.
dnl Side effects:
dnl defines variables CCAFE_DIRSTACK*
dnl --------------------------------------------------------------------
AC_DEFUN([CCAFE_PUSHD],
[
# this is a bit of ugly bourne shell code to emulate pushd/popd up to 
# depth 20.
# if 1, print debugging info
CCAFE_DIRSTACK_DEBUG=0
# make noise like bash
CCAFE_DIRSTACK_VERBOSE=0
# where in the stack we presently are
CCAFE_DIRSTACK_DEPTH=0
# the old directory pushed on the stack
CCAFE_DIRSTACK_1=
CCAFE_DIRSTACK_2=
CCAFE_DIRSTACK_3=
CCAFE_DIRSTACK_4=
CCAFE_DIRSTACK_5=
CCAFE_DIRSTACK_6=
CCAFE_DIRSTACK_7=
CCAFE_DIRSTACK_8=
CCAFE_DIRSTACK_9=
CCAFE_DIRSTACK_10=
CCAFE_DIRSTACK_11=
CCAFE_DIRSTACK_12=
CCAFE_DIRSTACK_13=
CCAFE_DIRSTACK_14=
CCAFE_DIRSTACK_15=
CCAFE_DIRSTACK_16=
CCAFE_DIRSTACK_17=
CCAFE_DIRSTACK_18=
CCAFE_DIRSTACK_19=
CCAFE_DIRSTACK_20=
export CCAFE_DIRSTACK_DEBUG
export CCAFE_DIRSTACK_DEPTH
export CCAFE_DIRSTACK_VERBOSE
export CCAFE_DIRSTACK_1
export CCAFE_DIRSTACK_2
export CCAFE_DIRSTACK_3
export CCAFE_DIRSTACK_4
export CCAFE_DIRSTACK_5
export CCAFE_DIRSTACK_6
export CCAFE_DIRSTACK_7
export CCAFE_DIRSTACK_8
export CCAFE_DIRSTACK_9
export CCAFE_DIRSTACK_10
export CCAFE_DIRSTACK_11
export CCAFE_DIRSTACK_12
export CCAFE_DIRSTACK_13
export CCAFE_DIRSTACK_14
export CCAFE_DIRSTACK_15
export CCAFE_DIRSTACK_16
export CCAFE_DIRSTACK_17
export CCAFE_DIRSTACK_18
export CCAFE_DIRSTACK_19
export CCAFE_DIRSTACK_20

printdirstack() {
  if test $CCAFE_DIRSTACK_DEPTH -ge 20 ; then
    echo -n "$CCAFE_DIRSTACK_20 "
  fi
  if test $CCAFE_DIRSTACK_DEPTH -ge 19 ; then
    echo -n "$CCAFE_DIRSTACK_19 "
  fi
  if test $CCAFE_DIRSTACK_DEPTH -ge 18 ; then
    echo -n "$CCAFE_DIRSTACK_18 "
  fi
  if test $CCAFE_DIRSTACK_DEPTH -ge 17 ; then
    echo -n "$CCAFE_DIRSTACK_17 "
  fi
  if test $CCAFE_DIRSTACK_DEPTH -ge 16 ; then
    echo -n "$CCAFE_DIRSTACK_16 "
  fi
  if test $CCAFE_DIRSTACK_DEPTH -ge 15 ; then
    echo -n "$CCAFE_DIRSTACK_15 "
  fi
  if test $CCAFE_DIRSTACK_DEPTH -ge 14 ; then
    echo -n "$CCAFE_DIRSTACK_14 "
  fi
  if test $CCAFE_DIRSTACK_DEPTH -ge 13 ; then
    echo -n "$CCAFE_DIRSTACK_13 "
  fi
  if test $CCAFE_DIRSTACK_DEPTH -ge 12 ; then
    echo -n "$CCAFE_DIRSTACK_12 "
  fi
  if test $CCAFE_DIRSTACK_DEPTH -ge 11 ; then
    echo -n "$CCAFE_DIRSTACK_11 "
  fi
  if test $CCAFE_DIRSTACK_DEPTH -ge 10 ; then
    echo -n "$CCAFE_DIRSTACK_10 "
  fi
  if test $CCAFE_DIRSTACK_DEPTH -ge 9 ; then
    echo -n "$CCAFE_DIRSTACK_9 "
  fi
  if test $CCAFE_DIRSTACK_DEPTH -ge 8 ; then
    echo -n "$CCAFE_DIRSTACK_8 "
  fi
  if test $CCAFE_DIRSTACK_DEPTH -ge 7 ; then
    echo -n "$CCAFE_DIRSTACK_7 "
  fi
  if test $CCAFE_DIRSTACK_DEPTH -ge 6 ; then
    echo -n "$CCAFE_DIRSTACK_6 "
  fi
  if test $CCAFE_DIRSTACK_DEPTH -ge 5 ; then
    echo -n "$CCAFE_DIRSTACK_5 "
  fi
  if test $CCAFE_DIRSTACK_DEPTH -ge 4 ; then
    echo -n "$CCAFE_DIRSTACK_4 "
  fi
  if test $CCAFE_DIRSTACK_DEPTH -ge 3 ; then
    echo -n "$CCAFE_DIRSTACK_3 "
  fi
  if test $CCAFE_DIRSTACK_DEPTH -ge 2 ; then
    echo -n "$CCAFE_DIRSTACK_2 "
  fi
  if test $CCAFE_DIRSTACK_DEPTH -ge 1 ; then
    echo -n "$CCAFE_DIRSTACK_1 "
  fi

  if ! test "x$CCAFE_DIRSTACK_DEPTH" = "x0"; then
    echo ""
  fi
  return 0
}

pushd() {
  if test $[#] -ne 1 ; then
	echo "pushd: only one directory argument allowed." 1>&2
	return 1;
  fi
  if ! test -d $1 ; then
	echo "pushd: argument given is not a directory." 1>&2
	return 2;
  fi
  CCAFE_DIRSTACK_DEPTH=`expr $CCAFE_DIRSTACK_DEPTH + 1`
  ccafe_olddir=`pwd`
  cd $1
  case $CCAFE_DIRSTACK_DEPTH in
  1) CCAFE_DIRSTACK_1=$ccafe_olddir
    ;;
  2) CCAFE_DIRSTACK_2=$ccafe_olddir
    ;;
  3) CCAFE_DIRSTACK_3=$ccafe_olddir
    ;;
  4) CCAFE_DIRSTACK_4=$ccafe_olddir
    ;;
  5) CCAFE_DIRSTACK_5=$ccafe_olddir
    ;;
  6) CCAFE_DIRSTACK_6=$ccafe_olddir
    ;;
  7) CCAFE_DIRSTACK_7=$ccafe_olddir
    ;;
  8) CCAFE_DIRSTACK_8=$ccafe_olddir
    ;;
  9) CCAFE_DIRSTACK_9=$ccafe_olddir
    ;;
  10) CCAFE_DIRSTACK_10=$ccafe_olddir
    ;;
  11) CCAFE_DIRSTACK_11=$ccafe_olddir
    ;;
  12) CCAFE_DIRSTACK_12=$ccafe_olddir
    ;;
  13) CCAFE_DIRSTACK_13=$ccafe_olddir
    ;;
  14) CCAFE_DIRSTACK_14=$ccafe_olddir
    ;;
  15) CCAFE_DIRSTACK_15=$ccafe_olddir
    ;;
  16) CCAFE_DIRSTACK_16=$ccafe_olddir
    ;;
  17) CCAFE_DIRSTACK_17=$ccafe_olddir
    ;;
  18) CCAFE_DIRSTACK_18=$ccafe_olddir
    ;;
  19) CCAFE_DIRSTACK_19=$ccafe_olddir
    ;;
  20) CCAFE_DIRSTACK_20=$ccafe_olddir
    ;;
  *)
     echo "pushd: max stackdepth exceeded." 1>&2
     CCAFE_DIRSTACK_DEPTH=20
     cd $ccafe_olddir
     return
     ;;
  esac

  if test "x$CCAFE_DIRSTACK_DEBUG" = "x1" ; then
    echo "$CCAFE_DIRSTACK_DEPTH" 1>&2
  fi
  if test "x$CCAFE_DIRSTACK_VERBOSE" = "x1" ; then
    printdirstack
  fi
}

popd() {
  if test "x$CCAFE_DIRSTACK_DEPTH" = "x0"; then
	echo "popd: directory stack is empty." 1>&2
	return 0;
  fi
  case $CCAFE_DIRSTACK_DEPTH in
  1) cd $CCAFE_DIRSTACK_1
         CCAFE_DIRSTACK_1=""
     ;;
  2) cd $CCAFE_DIRSTACK_2
         CCAFE_DIRSTACK_2=""
     ;;
  3) cd $CCAFE_DIRSTACK_3
         CCAFE_DIRSTACK_3=""
     ;;
  4) cd $CCAFE_DIRSTACK_4
         CCAFE_DIRSTACK_4=""
     ;;
  5) cd $CCAFE_DIRSTACK_5
         CCAFE_DIRSTACK_5=""
     ;;
  6) cd $CCAFE_DIRSTACK_6
         CCAFE_DIRSTACK_6=""
     ;;
  7) cd $CCAFE_DIRSTACK_7
         CCAFE_DIRSTACK_7=""
     ;;
  8) cd $CCAFE_DIRSTACK_8
         CCAFE_DIRSTACK_8=""
     ;;
  9) cd $CCAFE_DIRSTACK_9
         CCAFE_DIRSTACK_9=""
     ;;
  10) cd $CCAFE_DIRSTACK_10
         CCAFE_DIRSTACK_10=""
     ;;
  11) cd $CCAFE_DIRSTACK_11
         CCAFE_DIRSTACK_11=""
     ;;
  12) cd $CCAFE_DIRSTACK_12
         CCAFE_DIRSTACK_12=""
     ;;
  13) cd $CCAFE_DIRSTACK_13
         CCAFE_DIRSTACK_13=""
     ;;
  14) cd $CCAFE_DIRSTACK_14
         CCAFE_DIRSTACK_14=""
     ;;
  15) cd $CCAFE_DIRSTACK_15
         CCAFE_DIRSTACK_15=""
     ;;
  16) cd $CCAFE_DIRSTACK_16
         CCAFE_DIRSTACK_16=""
     ;;
  17) cd $CCAFE_DIRSTACK_17
         CCAFE_DIRSTACK_17=""
     ;;
  18) cd $CCAFE_DIRSTACK_18
         CCAFE_DIRSTACK_=18""
     ;;
  19) cd $CCAFE_DIRSTACK_19
         CCAFE_DIRSTACK_19=""
     ;;
  20) cd $CCAFE_DIRSTACK_20
         CCAFE_DIRSTACK_20=""
     ;;
  *)
     echo "popd: max stackdepth exceeded at $CCAFE_DIRSTACK_DEPTH." 1>&2
     return 1
     ;;
  esac
  CCAFE_DIRSTACK_DEPTH=`expr $CCAFE_DIRSTACK_DEPTH - 1`
  return 0;
}
]
)

