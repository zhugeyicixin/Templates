#!/bin/bash

echo 'submit to Tianhe:'
for entry in `find $@ -name *.job`
do
	echo $entry
	yhbatch -pTH_NET -c 12 $entry
done
