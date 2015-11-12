#!/bin/bash

source $HOME/.bash_profile

declare -i numJobs=0

sh submitTH.sh C9H18_148_r003_C19_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_148_r004_C5_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_158_r004_C11_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_164_r015_C5_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_164_r018_C19_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_170_r006_C5_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_177_r010_C18_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_181_r006_C14_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_183_r016_C9_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_189_r009_C24_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_191_r007_C4_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_191_r016_C24_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_200_r017_C10_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_204_r015_C21_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_205_r015_C4_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_206_r002_C24_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_208_r011_C17_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_210_r008_C24_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_212_r016_C7_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_235_r002_C24_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_238_r006_C19_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_240_r001_C11_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_240_r004_C11_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_251_r005_C6_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_254_r016_C24_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_287_r010_C4_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_288_r017_C6_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
sh submitTH.sh C9H18_301_r010_C10_2_opt_B3L
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
Tianhe submission script generated successfully!
[Finished in 0.3s]