#!/usr/bin/tclsh
if {$argc == 2} {
	if {
		$argv == "-- -help" ||
		$argv == "-- --help" ||
		$argv == "-- --help" ||
		$argv == "-- -H" ||
		$argv == "-- --H" ||
		$argv == "-- -h" ||
		$argv == "-- --h" 
	} {
		puts "$argv0 usage: <inputFile> <sidl-package> [output_dir]"
		puts "Where inputFile is a Ccaffeine batch or gui script,"
		puts "and sidl-package is the name of the sidl package"
		puts "for which the output is generated. Optional output_dir"
		puts "is a path which will be prefixed to output file names."
	}
}
if {$argc != 3 && $argc != 4 } {
	puts stderr "$argv0 usage: <inputFile> <sidl-package> [output_dir]"
	exit 1
}

proc !!! {args} {
	puts stdout "// $args"
}

proc !! {args} {
	puts stdout "// $args"
}

proc ! {args} {
	puts stdout "\t\t// $args"
}

proc !code {x} {
	global bld_global
	flushConfigRequests
	puts $bld_global(file,BM_driverBody) "\t$x"
}

proc !header {x} {
	global bld_global
	puts $bld_global(file,PR_I) "$x"
}

global env
#parray env
############################################
# generate a block of component constuctor prototypes
# that the linker must satisfy somehow from user component
# libraries.
# @param  ofile is an output file such as obtained from tcl open.


#################################################
proc genIncludes {ofile} {
puts $ofile " // old genIncludes call. does nothing in babel."
return
puts $ofile "/* Generated file. Includes block */"
puts $ofile "/*---------------------------------------*/"
puts $ofile "#include \<neocca.hh\>"
puts $ofile "#include \<neoports.hh\>"
puts $ofile "#include \<neosupport.hh\>"
}


#################################################
#################################################

#
# Here we search paths
# and scan .cca files. Babel people who
# don't use a .cca file can just lump it.
proc findLoadingData { classAlias } {
	global bld_palette bld_global
	scanPath $classAlias
	set bld_palette(requested,$classAlias) 1
	lappend bld_palette(request-list) $classAlias
	if { [lsearch -exact $bld_palette(aliasList) $classAlias] == -1} {
		puts stderr "Warning: Faking .cca data for $classAlias. check factory output."
		lappend bld_palette(aliasList) $classAlias
		set bld_palette(cppname,$classAlias) $classAlias
		set m [mangle $classAlias]
		set bld_palette(ctor,$classAlias) create_$classAlias
		set bld_palette(filename,$classAlias) FAKE_DATA__MISSING.CCA_FILE
		set bld_palette(libtoollib,$classAlias) "" 
		set bld_palette(staticlib,$classAlias) "" 
		set bld_palette(sharedlib,$classAlias) "" 
		set bld_palette(classincfiles,$classAlias) "" 
		set bld_palette(classincdirs,$classAlias) "" 
		set bld_palette(classlibrary,$classAlias) "FAKE_DATA__MISSING.CCA_FILE.a" 
	}

}

# split the path, find .cca files, and load their data
proc scanPath {classAlias} {
	global bld_fileseen
	set bld_fileseen(.whatTheHeck) 1
	global bld_palette bld_global
	if { [lsearch -exact $bld_palette(aliasList) $classAlias] >= 0} {
		return
	}
	set plist [split $bld_palette(path) :]
#	puts $bld_palette(path)
	foreach d $plist {
		set flist ""
		if {[catch {set flist [glob $d/*.depl.cca] } err ]} {
			continue
		}
		set flist [lsort $flist]
		foreach f $flist {
			if {[info exists bld_fileseen($f)]} { continue }
	#		puts "scanning $f"
			scanFile $f
			set bld_fileseen($f) 1
		}
	}
}
# read a file almost the same ways as ccaffeine does,
# with some really ugly hacks to compensate for not
# using an xml package.
proc scanFile {fname} {
	if {![file readable $fname]} {
		return
	}
	if {[isOldFormat $fname]} {
		extractOldFile $fname
	}
	if {[isXMLCCAFormat $fname]} {
		extractXMLCCAFile $fname
	}
}

proc extractXMLCCAFile {fname} {
	global bld_global
	set names [exec $bld_global(SCAN_CCA_XML) $fname]
# puts stderr $fname
# puts stderr $names
	foreach i [split $names \n] {
		if {[llength $i] == 3} {
			# back compatibility mode
			set binding [lindex $i 0]
			set classname [lindex $i 1]
			set classalias [lindex $i 2]
			# set constructor [lindex $i 3]
			set constructor "babel-none"
			if { [string compare $binding "babel"]==0 } {
				policyAdd $classalias $constructor $classname $fname
			}
		}
		if {[llength $i] == 9} {
			set binding [lindex $i 0]
			set classname [lindex $i 1]
			set classalias [lindex $i 2]
			set classlibrary [lindex $i 3]
			set classincdirs [lindex $i 4]
			set classincfiles [lindex $i 5]
			set libtoollib [lindex $i 6]
			set sharedlib [lindex $i 7]
			set staticlib [lindex $i 8]
			set constructor "babel-none"
			if { [string compare $binding "babel"]==0 } {
				policyAdd $classalias $constructor $classname $fname $classlibrary $staticlib $libtoollib $sharedlib $classincdirs $classincfiles
			}
		}
	}
}


# read a ccaffeine format file roughly as framework/ComponentFactory does.
proc extractOldFile {fname} {
	global bld_palette
	set last_buildDate ""
	set last_builder ""
	set last_so_file ""
	set last_buildLocation ""
	set cmptType ""
	set last_lib ""
	set f [open $fname r]
	set line [gets $f]
	while { ![eof $f]} {
		gets $f line
		if {[string compare -length 1 $line "!"] == 0 || [string compare -length 1 $line "#"]} {
			# whack commments and metadata
			gets $f line
			continue; # could check and cache stuff here, e.g. binding type, lib location.
		}
		if { [llength $line] == 1 } {
			# do nothing. library location the user will deal with
		}
		if {  [llength $line] == 2 } {
			set ctor [lindex $line 0]
			set alias [lindex $line 1]
			set cppname [stripCreate $ctor]
			policyAdd $alias $ctor $cppname $fname
		}
		gets $f line
	}
}

# This is where we control whether
# we take last-found or first-found
# when searching the file path.
# remove the if-check to get last-found behavior.
# default is first-found.
proc policyAdd {alias ctor cppname filename {classlibrary ""} {staticlib ""} {libtoollib ""} {sharedlib ""} {classincdirs ""} {classincfiles ""} } {
	global bld_palette bld_global
	if {[lsearch $bld_palette(aliasList) $alias] != -1} {
		if {![info exists bld_palette(warned,$alias,$filename)] } {
			puts stderr "Warning: ignoring $alias in .cca file $filename"
			puts stderr "Warning: Found same class first in $bld_palette(filename,$alias)"
			set bld_palette(warned,$alias,$filename) 1
		}
		return
	}
	set bld_palette(ctor,$alias) $ctor
	set bld_palette(cppname,$alias) $cppname
	set bld_palette(filename,$alias) $filename
        set bld_palette(classlibrary,$alias) $classlibrary
        set bld_palette(staticlib,$alias) $staticlib
        set bld_palette(libtoollib,$alias) $libtoollib
        set bld_palette(sharedlib,$alias) $sharedlib
        set bld_palette(classincdirs,$alias) $classincdirs
        set bld_palette(classincfiles,$alias) $classincfiles
	lappend bld_palette(aliasList) $alias
	set bld_palette(requested,$alias) 0
}

proc stripCreate { ctor } {
	if { [string compare -length 7 $ctor "create_"] ==0} {
		return [string range $ctor 7 end]
	}
	return $ctor
}

# if the files does start with <
# it's assumed to be xml and therefore must be xml .cca
# this could get more complicated later.
proc isXMLCCAFormat {fname} {
	set f [open $fname r]
	set charOne [read $f 1]
	if { "$charOne" == "<" } {
		close $f
		return 1
	}
	close $f
	return 0
}

# if the files doesn't start with <
# it's assumed not to be xml and therefore must be ccaffeine.
proc isOldFormat {fname} {
	set f [open $fname r]
	set charOne [read $f 1]
	if { "$charOne" != "<" } {
		close $f
		return 1
	}
	close $f
	return 0
}
	

#################################################
#################################################


# @param  ofile is an output file such as obtained from tcl open.
# @param ns is the empty string or the name of a namespace(c++) to use
# when generating the repository/factory class for the
# set of components found in the global array variable bld_palette.
# @global bld_palette array with entries:
#   (aliasList) -- list entry: keys $k to rest of info.
#   (cppname,$k) -- c++ class for a given alias k
#   (ctor,$k) -- c constructor for alias k
#   (dtor,$k) -- c destructor for alias k, or if none use c++ delete.
#   (classlibrary,$k) libraryName
#   (staticlib,$k) static-archive
#   (libtoollib,$k) libtool-archive
#   (sharedlib,$k) shared-archive
#   (classincdirs,$k) include dirs path
#   (classincfiles,$k) headers path
#   (requested,$k) -- boolean flag whether we want to output or not.
proc genFactory {ofile ccifile ns} {
	global bld_palette
	global bld_global
	global env
	set hname $bld_global(cBaseName)

# init
puts $ofile "/* Generated custom factory implementation block */"
foreach i $bld_palette(request-list) {
	if { $bld_palette(requested,$i) == 0 } { # this check should be redundant
		continue;
	}
	puts $ofile "\taddDescription(\"$bld_palette(cppname,$i)\", \"$i\");"
}


# ctor list
puts $ccifile "/* Generated custom factory implementation block */"
foreach i $bld_palette(request-list) { 
	if { $bld_palette(requested,$i) == 0 } { # this check should be redundant
		continue;
	}
	puts $ccifile "\tif (className == \"$i\") \{"
	set cpname [colonMangle $bld_palette(cppname,$i)]
	puts $ccifile "\t\t$cpname x = "
	puts $ccifile "\t\t\t${cpname}::_create();"
	puts $ccifile "\t\tgov::cca::Component c = x;"
	puts $ccifile "\t\treturn c;"
	puts $ccifile "\t\}"
}
set incdirsseen(.whatTheHeck) 1
set incfilesseen(.whatTheHeck) 1
foreach i $bld_palette(request-list) {
# puts stderr "###  processing $i"
# set alias $i
# puts stderr "cppname $bld_palette(cppname,$alias)"
# puts stderr "filename $bld_palette(filename,$alias)"
# puts stderr "classlibrary $bld_palette(classlibrary,$alias)"
# puts stderr "staticlib $bld_palette(staticlib,$alias)"
# puts stderr "libtoollib $bld_palette(libtoollib,$alias)"
# puts stderr "sharedlib $bld_palette(sharedlib,$alias)"
# puts stderr "classincdirs $bld_palette(classincdirs,$alias)"
# puts stderr "classincfiles $bld_palette(classincfiles,$alias)"
	if { $bld_palette(requested,$i) == 0 } { # this check should be redundant
		continue;
	}
	puts $bld_global(file,MAKE) "\n# for $bld_palette(cppname,$i) from $bld_palette(filename,$i)"
	puts $bld_global(file,MAKE) "$bld_global(sidlpkg)_COMPONENT_LIBS += $bld_palette(classlibrary,$i)"
	puts $bld_global(file,MAKE) "$bld_global(sidlpkg)_COMPONENT_LIBS_STATIC += $bld_palette(staticlib,$i)"
	puts $bld_global(file,MAKE) "$bld_global(sidlpkg)_COMPONENT_LIBS_SHARED += $bld_palette(sharedlib,$i)"
	puts $bld_global(file,MAKE) "$bld_global(sidlpkg)_COMPONENT_LIBS_LIBTOOL += $bld_palette(libtoollib,$i)"

	foreach j [split $bld_palette(classincdirs,$i) : ] {
		set dname "[string trim $j]"
		if { [string length $dname ] > 0} {
			if { [info exists incdirsseen($dname)] } { continue; }
			puts $bld_global(file,MAKE) "$bld_global(sidlpkg)_COMPONENT_INCLUDES += -I$j"
			set incdirsseen($dname) 1
		}
	}
	puts $bld_global(file,PR_I) "\n/* for $bld_palette(cppname,$i) from $bld_palette(filename,$i): */"
	set suffix ".$env(CXX_HDR_SUFFIX)"
	foreach k [split $bld_palette(classincfiles,$i) : ] {
		set j [string trim $k]
		if { [string length $j ] > 0} {
			if { [info exists incfilesseen($j)] } { continue ; }
			puts $bld_global(file,PR_I) "#include \"${j}$suffix\""
			set incfilesseen($j) 1
		}
	}
}

}
# end genFactory

######################################
proc driverProlog {ofile scriptName} {
	global bld_global
	set hname $bld_global(cBaseName)
puts $ofile ""
puts $ofile "/* Generated custom driverProlog block */"
puts $ofile "/*---------------------------------------*/"
}

# @param  ofile is an output file such as obtained from tcl open.
# @param ns is the empty string or the name of a namespace(c++) to use
# when generating the repository/factory class for the
# set of components found in the global array variable bld_palette.
proc genFactoryHeader {ofile ns} {
  
	global bld_global
	set hname $bld_global(cBaseName)
	global bld_palette
puts $ofile "/* Generated custom FactoryHeader */"

}
# end genFactoryHeader

########################################33

proc genConfigRequests {} {
	global bld_global bld_param cids
	set ofile $bld_global(file,BM_driverBody)
puts $ofile "\t\{"
puts $ofile "\t\t$bld_global(sidlpkgCname)::StringMap data = $bld_global(sidlpkgCname)::StringMap::_create();"
	foreach i $bld_param(varlist) {
puts $ofile "\t\tdata.set(\"$i\" , \"$bld_param(val,$i)\");"
	}
puts $ofile "\t\tsetParameters(\"$bld_param(compCurr)\","
puts $ofile "\t\t\t\"$bld_param(portCurr)\","
puts $ofile "\t\t\t$cids($bld_param(compCurr)), bs, services, data);"
puts $ofile "\t\}"

}
# end genConfigRequests
########################################33
########################################33

proc testDriver {} {
	driverProlog stderr runH2
	driverEpilog stderr runH2
}

# test routine to create some palette data
proc testInitPalette {} {
	global bld_palette
	set bld_palette(aliasList) "fred barney joe"
	set bld_palette(cppname,fred) Fred
	set bld_palette(cppname,joe) ns1::Joe
	set bld_palette(cppname,barney) Barney
	set bld_palette(ctor,fred) create_Fred
	set bld_palette(ctor,joe) create_ns1_Joe
	set bld_palette(ctor,barney) create_Barney
	set bld_palette(dtor,barney) destroy_Barney

}

######################################

proc testFactory {} {
	testInitPalette
	genFactoryHeader stderr ANON
	genConstructorExtern stderr
	genFactory stderr ANON
}


proc testAll {} {
	testInitPalette
	genIncludes stdout
	genFactoryHeader stdout ANON
	driverProlog stdout runH2
	driverEpilog stdout runH2
	genConstructorExtern stdout
	genFactory stderr ANON
}
############################################
# here would be a good place to chekc for ./supp2neo.tcl and load if exists.

####################################
# the first set of functions map logged gui commands to 
# their BS equivalents and output them immediately.
# The script input must be well-formed, or
# the code may not compile/may not even transform properly.
####################################

proc commandCount {args} {}

# ignore the global screen size
proc setSize {x y} { }
proc setMaximum {args} { }
# ignore next gui cmponent location
proc setDropLocation {x y} { }
proc move {c x y} { }

# gov draft
# component must be the componentid variable name
# that goes with the component being called.
proc go {component port} {
	checkEofDone
	flushConfigRequests
	global bld_global cids
	set ofile $bld_global(file,BM_driverBody)
puts $ofile ""
puts $ofile "\tinvokeGo( \"${component}\", \"${port}\", $cids($component) , services, bs);"

}

# neo done
proc connect {u up p pp} {
	checkEofDone
	flushConfigRequests
	global connids cids bld_global
	set ofile $bld_global(file,BM_driverBody)
	set key "${u}_${up}_${p}_${pp}"
	set id [Simp_genConnID $key]
	set connids($key) $id
	set uid $cids($u)
	set pid $cids($p)

puts $ofile "\n\tgov::cca::ConnectionID"
puts $ofile "\t$id ="
puts $ofile "\t\tbs.connect(${uid}, \"${up}\", ${pid}, \"${pp}\");"
	lappend bld_global(connstack) $id
}

# neo done
proc disconnect {u up p pp} {
	flushConfigRequests
	global connids cids bld_global
	set ofile $bld_global(file,BM_driverBody)
	set key "${u}_${up}_${p}_${pp}"
	set id $connids($key)
	puts $ofile "\tbs.disconnect($id, 0);"
	unset connids($key)
}

# neo done
proc disconnectSlop { ofile } {
	flushConfigRequests
	global bld_global connids
puts $ofile "\t// Section to clean up connections the user didn't. reverse order."
	# collect the open connections in reverse order of making.
	set stack {}
	foreach i $bld_global(connstack) {
		if {[info exists connids($i)]} {
			set newstack [linsert $stack 0 $i]
			set stack $newstack
		}
	}
	foreach i $stack {
puts $ofile "\tbs.disconnect(${i}, 0);"
		unset connids($i)
	}
}

# neo done
proc parameters {newcomp newport var args} {
	configure $newcomp $newport $var $args
}

proc badComponentName { name } {
  set badNames "af services dummy pr myself bs data"
  if {[lsearch -exact $badNames $name] >= 0} {
	return 1
  }
  return 0
}

# logic:
# foreach param port set request seen, accumulate data
# until any other keyword or param port is processed.
# foreach param get request seen, do it immediately.
# bld_param(active) 0/1 already accumulated something
# bld_param(portCurr) port most recent
# bld_param(compCurr) component most recent
# bld_param(varlist) keys set so far
# for i in varlist:
# bld_param(val,$i) value for each key
# bld_param(type,$i) type for each key (not yet supported)
proc configure {newcomp newport var args} {
	checkEofDone
	# first handle special case of value request
	if {! [string length $args]} {
		genConfigReads $newcomp $newport $var
		return
	}
	global bld_global bld_param
	# handle already got a param
	if { $bld_param(active) } {
		if { $newcomp == $bld_param(compCurr) && $newport == $bld_param(portCurr) } {
			addParam $var $args
		} else {
			genConfigRequests
			startParamSet $newcomp $newport $var $args
		}
	} else {
		set bld_param(active) 1
		startParamSet $newcomp $newport $var $args
	}
	
}
# this must be identical to configure
proc parameter {newcomp newport var args} {
	checkEofDone
	# first handle special case of value request
	if {! [string length $args]} {
		genConfigReads $newcomp $newport $var
		return
	}
	global bld_global bld_param
	# handle already got a param
	if { $bld_param(active) } {
		if { $newcomp == $bld_param(compCurr) && $newport == $bld_param(portCurr) } {
			addParam $var $args
		} else {
			genConfigRequests
			startParamSet $newcomp $newport $var $args
		}
	} else {
		set bld_param(active) 1
		startParamSet $newcomp $newport $var $args
	}
	
}

# neo done
proc flushConfigRequests {} {
	global bld_global bld_param
	if {$bld_param(active)} {
		genConfigRequests
		set bld_param(active) 0
	}
}
	

# neo done
proc startParamSet {newcomp newport var val} {
	global bld_global bld_param
	set bld_param(compCurr) $newcomp
	set bld_param(portCurr) $newport
	set bld_param(varlist) $var
	set bld_param(val,$var) $val
}

# neo done
proc addParam { var val} {
	global bld_global bld_param
	lappend bld_param(varlist) $var
	set bld_param(val,$var) $val
}

proc genConfigReads { newcomp newport var } {
	global bld_global bld_param cids
	flushConfigRequests
	set ofile $bld_global(file,BM_driverBody)
puts $ofile "\t// the next function call returns a string."
puts $ofile "\tgetParameterValue($cids($newcomp),"
puts $ofile "\t\t\"$newport\", \"$var\", services, bs);"
}

# neo done
proc quit {args} {
	checkEofDone
	flushConfigRequests
	puts stdout "\n\t// quit $args \n"
	user_eof
}

# neo done
proc repository {verb args} {
	checkEofDone
	flushConfigRequests
	switch -- $verb {
	list {
	}
	get-ports {
		# do nothing. this will be taken care of
		# at link time by user.
	}
	get -
	get-global -
	get-lazy -
	get-lazy-global {
		# handle classes from .cca files
		findLoadingData "[lindex $args 0]"
	}
	}
}

# just internally accumulate the path with : separators
# path init/append/prepend/set arg
proc path {args} {
	checkEofDone
	global bld_palette env
	if { [llength $args] == 0} {
		# print path request; ignore it
		return
	}
	switch -- "[lindex $args 0]" {
	init {
		set bld_palette(path) $env(CCA_COMPONENT_PATH)
		set bld_palette(aliasList) {}
	}
	set {
		if { [llength $args] > 1} {
			set bld_palette(path) [lindex $args 1]
			set bld_palette(aliasList) {}
		}
	}
	append {
		if { [llength $args] > 1} {
			append bld_palette(path) ":[lindex $args 1]"
		}
	}
	prepend {
		if { [llength $args] > 1} {
			set val "[lindex $args 1]:"
			append val $bld_palette(path)
			set bld_palette(path) $val
		}
	}
	default {}
	}
}

proc display {args} {
	# gui thing we ignore
}

proc instantiate {type c} {
	pulldown $type $c
}

# neo done
proc pulldown {type c} {
	checkEofDone
	flushConfigRequests
	global bld_global cids
	set ofile $bld_global(file,BM_driverBody)
	set id [Simp_genCID $c]
	set cids($c) $id
	puts $ofile "\n\tgov::cca::ComponentID $id ="
	puts $ofile "\t\tbs.createInstance(\"$id\", \"$type\", dummy);"
	lappend bld_global(compstack) $id
}
	
# neo done
proc create {type c} {
	checkEofDone
	pulldown $type $c
}

# neo done
proc destroySlop { ofile } {
	flushConfigRequests
	global bld_global cids
puts $ofile "\n\t// Section to clean up components the user didn't. reverse order."
	set stack {}
	foreach i $bld_global(compstack) {
		if {[info exists cids($i)]} {
			set newstack [linsert $stack 0 $i]
			set stack $newstack
		}
	}
	foreach i $stack {
puts $ofile "\tbs.destroyInstance(${i}, 0.0);"
		unset cids($i)
	}
}
	
# gov done
proc checkEofDone {} {
	global bld_global
	if {$bld_global(eof_done) == 1} { 
		puts stderr "eof command found in middle of input. output maybe wrong."
		exit 1
	 }
}
# gov done
proc user_eof {} {
	global jname
	global bld_global
	if {$bld_global(eof_done) == 1} { return }
	set bld_global(eof_done) 1
	set ofile $bld_global(file,BM_driverBody)
	
# whack connections user missed, in reverse order.
	disconnectSlop $ofile
# whack components user missed, in reverse order.
	destroySlop $ofile
	genFactory $bld_global(file,PR_CTOR) $bld_global(file,PR_CCI) ""
}

####################################
# the second set of functions manages identifier mappings
####################################
# come up with unique in the existing list name from iname

proc Simp_genCID {iname} {
	global cids
	set n 2
	set testid $iname
	if { [badComponentName $testid] != 0 } {
	  set testid "${iname}_$n"
	}
	if { [llength [array get cids $testid]] == 0 } {
		return $testid
	}
	while {[llength [array get cids $testid]] != 0 } {
		incr n
		set testid "${iname}_$n"
	}
	return $testid
}

proc Simp_genConnID {iname} {
	global connids
	set testid $iname
	if { [llength [array get connids $testid]] == 0 } {
		return $testid
	}
	set n 2
	set testid "${iname}_$n"
	while {[llength [array get connids $testid]] != 0 } {
		incr n
		set testid "${iname}_$n"
	}
	return $testid
}

proc Simp_genCCD {iname} {
	global ccds
	set testid $iname
	if { [llength [array get ccds $testid]] == 0 } {
		return $testid
	}
	set n 2
	set testid "${iname}_$n"
	while {[llength [array get ccds $testid]] != 0 } {
		incr n
		set testid "${iname}_$n"
	}
	return $testid
}

proc Simp_Init {} {
	# arrays of c++ var name from string name
	global cids connids ccds bld_palette bld_param bld_global env
	set bld_palette(request-list) ""
	set bld_palette(aliasList) ""
	set bld_global(eof_done) 0
	set bld_param(active) 0
	set bld_param(varList) ""
	set ccds(-) 0
	set connids(-) 0
	set cids(-) 0
	if {[info exists env(SCAN_CCA_XML)]} {
		set bld_global(SCAN_CCA_XML) $env(SCAN_CCA_XML)
	} else {
		set bld_global(SCAN_CCA_XML) ./cca-spec-babel-scanCCAxml.exe
	}
}

proc colonMangle {cname} {
	regsub -all -- {\.} $cname {::} cname1
	return $cname1
}

proc barMangle {cname} {
	regsub -all -- {_} $cname {::} cname1
	return $cname1
}

proc mangle {fname} {
	regsub -all -- {\.} $fname {_} fname1
	regsub -all -- {-} $fname1 {_} fname2
	regsub -all -- {:} $fname2 {_} jname
	return "$jname"
}

####################################
# main
####################################

Simp_Init
# input
set fname [lindex $argv 1]
# sidl pkg prefix to become dir+prefix
set baseName [lindex $argv 2]
set bld_global(sidlpkg) $baseName
set bld_global(sidlpkgCname) [barMangle $baseName]
# sidl pkg from old usage
set cBaseName [file tail $baseName]
# get dir and prepend sidl pkg for output names
if { $argc == 4 } {
   set dirName [lindex $argv 3]
   set baseName "$dirName/$baseName"
}
set bld_global(baseName) $baseName
set jname $cBaseName
global jname fname
# debug get rid of h/cfile when no one writes to it directly.
set cfile stderr
set bld_global(file,BM_driverBody) [open "$bld_global(baseName).BabelMain.driverBody.guts.hh" "w+"]
set bld_global(file,PR_CTOR)  [open "$bld_global(baseName).PrivateRepository._ctor.guts.hh" "w+"]
set bld_global(file,PR_CCI)  [open "$bld_global(baseName).PrivateRepository.createComponentInstance.guts.hh" "w+"]
set bld_global(file,PR_I)  [open "$bld_global(baseName).PrivateRepository._includes.guts.hh" "w+"]
set bld_global(file,MAKE)  [open "$bld_global(baseName).make" "w+"]
set bld_global(hfile) stderr
set bld_global(cBaseName) $cBaseName
#exec cat $fname | egrep -v {^\!} | sed -e {s/^eof/user_eof/g} > $baseName.tmp1.tcl
exec cat $fname | sed -e {s/^eof/user_eof/g} > $baseName.tmp1.tcl
# force the finish if not found.
exec echo user_eof >> $baseName.tmp1.tcl
#exec cat $fname | egrep -v {^\!} > $baseName.tmp1.tcl
source $baseName.tmp1.tcl
exec /bin/rm $baseName.tmp1.tcl
close $bld_global(file,PR_CCI)
close $bld_global(file,PR_I)
close $bld_global(file,PR_CTOR)
close $bld_global(file,BM_driverBody)
close $bld_global(file,MAKE)
exit 0
