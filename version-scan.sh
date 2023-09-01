#!/bin/sh

SPECFILE=$(pwd)/unifi.spec

SOURCES=$( spectool -l -s 0 $SPECFILE )
DLURL=$( echo $SOURCES | grep -E '^Source0:\s+' | sed 's/^Source0://' )
SOURCEFILE=$(pwd)/$( echo $DLURL | sed 's/http.*\///' )
TEMPDIR=$( mktemp -d -t unifi_XXXXXXXXXX )
TEMPLIBDIR=$TEMPDIR/UniFi/lib
VERSION=$( grep -E '^Version:\s+' $SPECFILE | sed 's/^Version://' )
VERSIONFILE=$TEMPDIR/provides.list
if [ x"$VERSION" = x ]; then
  echo "Unable to determine the version to scan from $SPECFILE. Exiting!"
  exit 1
fi

echo DLURL is $DLURL
echo SOURCEFILE is $SOURCEFILE
echo TEMPDIR is $TEMPDIR
echo TEMPLIBDIR is $TEMPLIBDIR
echo VERSION is $VERSION

if [ ! -x /usr/bin/unzip ]; then
  echo "Unzip is required for this script. Exiting!"
  exit 2
fi

if [ ! -f $SOURCEFILE ]; then
  echo "Unable to find the required sourcefiles. Exiting!"
  exit 3
fi

echo -n "Extracting $SOURCEFILE to $TEMPDIR..."
unzip -q $SOURCEFILE -d $TEMPDIR
if [ $? -ne 0 ]; then
  echo "Failed to extract $SOURCEFILE to $TEMPDIR. Exiting!"
  exit 4
fi
echo "done!"

for file in `ls $TEMPLIBDIR/*.jar`; do
  
  # try the file name
  # get just the version, which is assumed to be -#[.#]+.jar
  if [ `echo $file | grep -` ]; then
    version=`echo $file | sed -e 's/\.jar$//' -e 's/.*-//' -e 's/\.RELEASE//'`
    determination="filename"
  fi
  
  # if not, check to see if implementation-version is set, if so, go with it
  if [ x${version} = x ]; then
    version=`unzip -p $file META-INF/MANIFEST.MF | grep Implementation-Version | sed -e 's/^Implementation-Version: //' -e 's/\r//'`
    determination="manifest"
  fi
  
  # if not, just give up, and say '9999'
  if [ x${version} = x ]; then
    version='9999'
    determination="fallback"
  fi
  
  library=`echo $file | sed -e 's/.*\///' -e 's/\.jar$//' -e "s/-$version//" -e 's/\.RELEASE//'`
  
  # create output for RPM packaging
  echo "Provides:       bundled(${library}) = ${version}" >> $VERSIONFILE
  
done

echo "Created provides list in $VERSIONFILE."

echo -n "Updating $SPECFILE with jar library versions..."
sed -i -n -e '1,/^### BEGIN AUTOMATION ###$/p' -e '/^### BEGIN AUTOMATION ###$/r '$VERSIONFILE -e '/^### END AUTOMATION ###$/,$p' $SPECFILE
echo "done!"
