#--------------------------------------------------------------------
# CCAFE_SHLIB_SUFFIX
#
#       Try to determine the proper shared library suffix.
#       SHLIB_SUFFIX -  Suffix to use for the names of dynamically loadable
#                       extensions.  An empty string means we don't know how
#                       to use shared libraries on this platform.
#--------------------------------------------------------------------
AC_DEFUN([CCAFE_GET_SHLIB_SUFFIX], [
    AC_MSG_CHECKING([system version (for dynamic loading)])
    if test -f /usr/lib/NextStep/software_version; then
        system=NEXTSTEP-`awk '/3/,/3/' /usr/lib/NextStep/software_version`
    else
        system=`uname -s`-`uname -r`
        if test "$?" -ne 0 ; then
            AC_MSG_RESULT([unknown (can't find uname command)])
            system=unknown
        else
            # Special check for weird MP-RAS system (uname returns weird
            # results, and the version is kept in special file).

            if test -r /etc/.relid -a "X`uname -n`" = "X`uname -s`" ; then
                system=MP-RAS-`awk '{print $3}' /etc/.relid`
            fi
            if test "`uname -s`" = "AIX" ; then
                system=AIX-`uname -v`.`uname -r`
            fi
            AC_MSG_RESULT($system)
        fi
    fi

    case $system in
	AIX-*)
	    SHLIB_SUFFIX=".so"
	    ;;
	BSD/OS-2.1*|BSD/OS-3*)
	    SHLIB_SUFFIX=".so"
	    ;;
	BSD/OS-4.*)
	    SHLIB_SUFFIX=".so"
	    ;;
	dgux*)
	    SHLIB_SUFFIX=".so"
	    ;;
	HP-UX-*)
	    SHLIB_SUFFIX=".sl"
	    ;;
	IRIX-4.*)
	    SHLIB_SUFFIX=".a"
	    ;;
	IRIX-5.*)
	    SHLIB_SUFFIX=".so"
	    ;;
	IRIX-6.*)
	    SHLIB_SUFFIX=".so"
	    ;;
	IRIX64-6*)
	    SHLIB_SUFFIX=".so"
	    ;;
	Linux*)
	    SHLIB_SUFFIX=".so"
	    ;;
	GNU*)
	    SHLIB_SUFFIX=".so"
	    ;;
	MP-RAS-*)
	    SHLIB_SUFFIX=".so"
	    ;;
	NetBSD-*|FreeBSD-*|OpenBSD-*)
		SHLIB_SUFFIX=".so"
	    ;;
	Rhapsody-*|Darwin-*|darwin-*)
	    SHLIB_SUFFIX=".dylib"
	    ;;
	NEXTSTEP-*)
	    SHLIB_SUFFIX=".so"
	    ;;
	OSF1-*)
	    SHLIB_SUFFIX=".so"
	    ;;
	QNX-6*)
	    SHLIB_SUFFIX=".so"
	    ;;
	RISCos-*)
	    SHLIB_SUFFIX=".a"
	    ;;
	SCO_SV-3.2*)
	    SHLIB_SUFFIX=".so"
	    ;;
	SINIX*5.4*)
	    SHLIB_SUFFIX=".so"
	    ;;
	SunOS-*)
	    SHLIB_SUFFIX=".so"
	    ;;
	ULTRIX-4.*)
	    SHLIB_SUFFIX=".a"
	    ;;
	UNIX_SV* | UnixWare-5*)
	    SHLIB_SUFFIX=".so"
    esac

])
