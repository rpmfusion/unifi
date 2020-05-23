#!/bin/sh

for file in `ls $1/*.$2`; do
  
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
  echo "Provides:       bundled(${library}) = ${version}"
  
done
