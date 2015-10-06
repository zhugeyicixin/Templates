#!/bin/csh
#
#$ -cwd
#$ -j y
#$ -S /bin/csh
#
echo 'submit 12:'
for entry in `find $@ -name *.job`
do
	echo $entry
	qsub -pe orte 4 $entry
done
