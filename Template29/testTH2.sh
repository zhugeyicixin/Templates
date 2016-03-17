#!/bin/bash

source $HOME/.bash_profile

declare -i numJobs=0

sh submitTH.sh C10H20_515_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_517_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_546_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_547_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_550_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_570_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_576_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_592_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_636_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_637_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_638_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_704_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_713_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_715_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_739_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_744_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_809_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_835_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C10H20_837_4_opt_M06
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
