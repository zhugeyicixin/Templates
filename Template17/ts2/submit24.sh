#!/bin/csh
#
#$ -cwd
#$ -j y
#$ -S /bin/csh
#
echo 'submit 24:'
for entry in `find $@ -name *.job`
do
	echo $entry
	qsub -pe smp 24 $entry
done
