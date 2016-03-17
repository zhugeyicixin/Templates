#!/bin/bash

source $HOME/.bash_profile

declare -i numJobs=0

sh submitTH.sh C10H20_502_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_503_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_504_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_505_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_506_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_507_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_508_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_509_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_510_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_511_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_642_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_643_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_644_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_645_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_646_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_647_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_648_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_649_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_650_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_651_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
