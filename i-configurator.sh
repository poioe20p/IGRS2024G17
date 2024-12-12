#!/bin/bash

# Interaction
printf "Domain Name A:"
read domainnameA 
printf "IP Adress A:"
read ip_addressA

printf "Domain Name B:"
read domainnameB
printf "IP Adress B:"
read ip_addressB

printf "Your system is A or B [A/B]:"
read mysystem

if [ $mysystem = "A" ];
then
	domainname=$domainnameA
	ip_address=$ip_addressA
	visiteddomain=$domainnameB
elif [ $mysystem = "B" ];
then
	domainname=$domainnameB
	ip_address=$ip_addressB
	visiteddomain=$domainnameA
else
	printf "Error: choose A or B \n"
	exit
fi

echo "Domain A:" $domainnameA
echo "IP Adress A:" $ip_addressA
echo "Domain B:" $domainnameB
echo "IP Adress B:" $ip_addressB
echo "You are: " $mysystem
echo "Domain:" $domainname
echo "IP Adress:" $ip_address

cd ./ims/bin/
sudo ./restore.sh 

cd ../bind
sudo ./configurator-bind.sh $domainnameA $ip_addressA $domainnameB $ip_addressB  $ip_address

cd ../..


