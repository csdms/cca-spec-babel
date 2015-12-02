#!/usr/bin/ruby

# usage: $0 <source directory> <destination directory>

# Synchronize given files over given directories

class SyncFiles 

  def initialize(srcDir, dstDir, file = nil)
    @files = [];
    @srcDir = srcDir
    @dstDir = dstDir
    @exclusive_mode = false
    return if ! file
    addSrcFiles(file)
  end

  def addSrcFiles(file)
    if file.kind_of? String
      @files << File.basename(file)
    end
    if file.kind_of? Regexp
      addSrcFilesByRE(file)
    end
    if file.kind_of? Array
      file.each {|f|
	addSrcFiles(f)
      }
    end
  end

  def newer?(srcFile, dstFile)
    return nil if ! File.exists?(srcFile)
    if ! File.exists?(dstFile)
      return nil if @exclusive_mode
      return true 
    end
    d = File.stat(dstFile) 
    s = File.stat(srcFile);
    ts = s.mtime;
    td = d.mtime;
    return true if ts > td
    return nil
  end

  # Add file names from the source dir that match this Regexp
  def addSrcFilesByRE(re)
    Dir.for_each(@srcDir) { |f|
      next if File.stat(f).dir?
      @files << f if re =~ f
    }
  end

  

  # Iterate over each newer file.  Full paths are given as strings for
  # each newer source file.
  def each_newer()
    new = []
    @files.each { |f|
      src = @srcDir+'/'+f
      dst = @dstDir+'/'+f
      yield src, dst if newer?(src, dst)
    }
  end

  # returns an array of [srcFilePath, dstFilePath] for all srcFile's
  # that are newer than the corresponding dstFile's.
  def getNewer
    files = []
    each_newer { |src,dst|
      files << [src, dst]
    }
    files
  end

  def setExclusive(tf)
    @exclusive_mode = tf
  end


  def SyncFiles.each_newer(srcDir, dstDir, file = nil) 
  end

  def SyncFiles.copy(srcPath, dstPath, file = nil)
  end

  # syncronize over the given filenames from the srcDir to the dstDir
  def sync(srcDir, dstDir)
  end
end


if $0 == __FILE__

  usage = "
#{$0} <source directory or files> <destination directory> [--regexp <pattern>] [--exclusive]

 Check to see if src files in the source directory are modified
 later than files in the destination directory, if so, print
 them on stdout.

 --regexp <pattern>  - The only files in the source directory 
                       matching the pattern will be compared.  The 
                       source *must* be a directory.

 --exclusive         - Normally it will assume that missing files in 
                       the destination are \"newer\".  Use of this 
                       switch will cause files present in the source 
                       but missing in the destination to be ignored.
"

  if ARGV.size < 2
    puts usage
    exit(-1)
  end
  exclusive = false
  regexp = nil
  require 'getoptlong'

  opt = GetoptLong.new(
		       ['--help', '-?', GetoptLong::NO_ARGUMENT],
		       ['--exclusive', '-x', GetoptLong::NO_ARGUMENT],
		       ['--regexp', '-r', GetoptLong::REQUIRED_ARGUMENT]
		       )
  opt.each_option do |name,arg|
    case name
    when '--help'
      puts usage
      exit(0)
    when '--regexp'
      regexp = Regexp.new(arg)
    when '--exclusive'
      exclusive = true
    end
  end
  

  siz = ARGV.size
  pathSrc = ARGV[0...(siz-1)]
  pathDst = ARGV[siz-1]
  fileSrc = []  # array of src files in the dest directory
  if pathSrc.size == 1 
    f = pathSrc[0]
    if ! FileTest.directory?(f) # is not a directory
      if regexp
	$stderr.puts "regexp can only be used when src dir is a "+
	  "single directory"
	$stderr.puts "Going away now, have a nice day ..."
	$stderr.puts usage
	exit(-1)
      end	
      if ! FileTest.file?(f)
	$stderr.puts ":-( Source file \""+f+"\" not a plain file"
	$stderr.puts "Going away now, have a nice day ..."
	$stderr.puts usage
	exit(-1)
      end
      dirSrc = File.dirname(pathSrc)
      fileSrc = File.basename(pathSrc)
    else # is a directory
      dirSrc = (pathSrc[0]).chomp('/') # remove trailing '/' if present
      if regexp
	Dir.foreach(dirSrc) { |f|
	  file = dirSrc+'/'+f
	  fileSrc << f if (FileTest.file?(file) && regexp =~ f)
	}
      else
	Dir.foreach(dirSrc) { |f|
	  file = dirSrc+'/'+f
	  fileSrc << f if FileTest.file?(file)
	}
      end
    end
  else  # pathSrc.size != 1
    if regexp
      $stderr.puts "regexp can only be used when source is a "+
	"single directory"
      $stderr.puts "Going away now, have a nice day ..."
      $stderr.puts usage
      exit(-1)
    end	
    theDir = nil
    pathSrc.each { |f|
      if ! FileTest.file?(f)
	$stderr.puts ":-( Source file \""+f+"\" not a plain file"
	$stderr.puts "Cannot compare directories recursively"
	$stderr.puts "Going away now, have a nice day ..."
	$stderr.puts usage
	exit(-1)
      end
      theDir = File.dirname(f) if ! theDir
      if theDir != File.dirname(f)
	$stderr.puts ":-( Can only compare one source directory at a time"
	$stderr.puts "we have at least two directories in the source arguments:"
	$stderr.puts "Directory 1: "+theDir+" and Direcory 2: "+File.dirname(f)
	$stderr.puts "Going away now, have a nice day ..."
	$stderr.puts usage
	exit(-1)
      end

      # At this point we have ensured the same src dir, and that
      # it is a plain file.  Load it in to the src file array
      
      fileSrc << File.basename(f)
    }
    dirSrc = theDir
  end
  if FileTest.directory?(pathDst)
    dirDst = pathDst
  else
    $stderr.puts ":-( Destination: "+pathDst+" must be a directory"
    $stderr.puts "Going away now, have a nice day ..."
    $stderr.puts usage
    exit(-1)
  end
  
  sf = SyncFiles.new(dirSrc, dirDst, fileSrc)
  sf.setExclusive(true) if exclusive
  sf.getNewer.each { |s,d|
    puts s
  }
end

