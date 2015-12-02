#!/bin/sh
# A script to remove most of the useless crap
# that changes with every commit.
for i in $* ; do 
	if ! [ -f $i ] ; then
		echo "$0: $i is not regular file."
		continue
	fi
	/bin/rm -f .unstamp.$$i; \
	/bin/cat $i | grep -v '^// babel-version' | \
		grep -v '^// source-line' | \
		grep -v '^// source-url' | \
		grep -v '^// Babel Version' | \
		grep -v '^// Generated' | \
		grep -v '^// SIDL Created' > .unstamp.$i; \
	/bin/mv -f .unstamp.$i $i; \
done
