#!/bin/bash

# Initialization & global vars
# if you execute this script for the second time
# you should change these variables to the latest
# domain name and ip address
DDOMAIN1="open-ims1\.test"
DSDOMAIN1="open-ims1\\\.test"

DDOMAIN2="open-ims2\.test"
DSDOMAIN2="open-ims2\\\.test"

DEFAULTIP="127\.0\.0\.1"

# Interaction
domainnameA=$1
ip_addressA=$2
domainnameB=$3
ip_addressB=$4
my_ip=$5

# input domain is to be slashed for cfg regexes 
slasheddomain=`echo $domainname | sed 's/\./\\\\\\\\\./g'`

printf "changing: open-ims1.dnszone"
sed -i -e "s/$DDOMAIN1/$domainnameA/g" ./open-ims1.dnszone
sed -i -e "s/$DSDOMAIN1/$slasheddomainA/g" ./open-ims1.dnszone
sed -i -e "s/$DEFAULTIP/$ip_addressA/g" ./open-ims1.dnszone

printf "changing: open-ims2.dnszone"
sed -i -e "s/$DDOMAIN2/$domainnameB/g" ./open-ims2.dnszone
sed -i -e "s/$DSDOMAIN2/$slasheddomainB/g" ./open-ims2.dnszone
sed -i -e "s/$DEFAULTIP/$ip_addressB/g" ./open-ims2.dnszone

printf "changing: named.conf.local"
sed -i -e "s/$DDOMAIN1/$domainnameA/g" ./named.conf.local
sed -i -e "s/$DDOMAIN2/$domainnameB/g" ./named.conf.local

sudo cp ./open-ims1.dnszone /etc/bind/.
sudo cp ./open-ims2.dnszone /etc/bind/.
sudo cp ./named.conf.local  /etc/bind/.

sudo echo >> "nameserver $my_ip" ./head 
sudo cp ./head /etc/resolvconf/resolv.conf.d/.

sudo service bind9 restart
