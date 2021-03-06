#!/bin/sh

DATE=`date`
CURRDIR=`pwd`
CCA_SPEC_VARS=${1} # cca spec variables
CLIENT_NAME=${2}  # name of this port, to be used in library name
CLIENT_DIR=${3}   # the location of the client Source code (w/o language)
PREFIX=${4}       # the directory in which to place libraries and include
                  # files in lib/ and include/ subdirectories
LANGUAGE=${5}     # optional language parameter

if [ "x${LANGUAGE}" != "x" ] ; then 
	CLIENT_DIR=${CLIENT_DIR}/${LANGUAGE}
fi

# Create the Makefile in the client directory
echo "#This file is automatically generated; do not edit." > ${CLIENT_DIR}/Makefile
echo "#${DATE}" >> ${CLIENT_DIR}/Makefile
echo "#--------------------------------------------------" \
	>> ${CLIENT_DIR}/Makefile


# Do simple substitution to set the specific port (client) name 
# (argument 2 of this script), and the top-level directory for the 
# client's Source code and then copy the Makefile template to the 
# client's directory.
sed -e "/@CLIENT_NAME@/ s/@CLIENT_NAME@/${CLIENT_NAME}/g" \
	-e "/@CCA_SPEC_VARS@/ s|@CCA_SPEC_VARS@|${CCA_SPEC_VARS}|g" \
	-e "/@LANGUAGE@/ s|@LANGUAGE@|${LANGUAGE}|g" \
	-e "/@PWD@/ s|@PWD@|${CURRDIR}|g" utils/Makefile_template.client \
		>> ${CLIENT_DIR}/Makefile


