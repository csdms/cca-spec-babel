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
		puts "$argv0 usage: <inputFile> <outputFile>"
		puts "Where inputFile is a header temporary with CTOR in it."
	}
}
if {$argc != 3} {
puts stderr "try ctor --help"
exit 1
}

set iname [lindex $argv 1]
set oname [lindex $argv 2]
set ifile [open $iname r]
set ofile [open $oname w+]
#puts stderr "Creating $oname."

# first line must be ctor as a comment after //
gets $ifile dat
set ctor [string trimleft $dat /]

while {![eof $ifile]} {
	gets $ifile dat
	set dat2 $dat
	set result [regsub -- {@CTORPY@} $dat $ctor dat2]
	if { $result != 0 } {
#		puts stderr "Matched $iname: $dat"
		#puts stderr "to get $dat2"
	}
	puts $ofile $dat2
}
	

close $ifile
close $ofile
exit 0
