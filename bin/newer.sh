# !bash
# A script to copy stuff if it is new.
# copies file list to target dir.
# actually just echos the list to copy.
tdir=""
name=$0
for x in $*; do
  tdir=$x;
done
if [ ! -d $tdir ] ; then
  echo "$0: Last argument must be a directory" >> /dev/stderr;
  exit 1
# else
#  echo "Target = $tdir" >> /dev/stderr;
fi
for i in $* ; do
  if [ "$tdir" = "$i" ] ; then
#    echo "$name done" >> /dev/stderr;
    echo ""
    break;
  fi;
  if [ -h $i ] ; then
    echo "input file $i is a symlink. ignored." >> /dev/stderr
    continue;
  fi
  if [ -h $tdir/$i ] ; then
    echo " target file $tdir/$i is a symlink. ignored." >> /dev/stderr
    continue;
  fi
  if [ -f $i -a -r $i ] ; then
    if [ -f $tdir/$i ] ; then
      if [ $i -nt $tdir/$i ] ; then
        echo  "$i "
      fi
    else 
      echo  "$i "
    fi
  fi
done
