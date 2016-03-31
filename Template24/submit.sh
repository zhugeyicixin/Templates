#!/bin/sh

#print hello world in the console window

echo 'submit:'
for entry in `find $@ -name *.job`
do
	echo $entry
	bsub<$entry
done

