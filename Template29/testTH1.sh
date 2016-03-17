#!/bin/bash

source $HOME/.bash_profile

declare -i numJobs=0

sh submitTH.sh C10H20_514_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
