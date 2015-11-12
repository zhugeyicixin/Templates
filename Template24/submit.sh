#!/bin/bash

export GAUSS_SCRDIR=/vol-th/home/you/scratch
export g09root=/vol-th/home/you/softwares/gaussian/g09D01

source $g09root/g09/bsd/g09.profile

cd /vol-th/home/you/hetanjin/newGroupAdditivityFrog2/test
yhrun -pTH_NET -c12 $g09root/g09/g09 $1 

