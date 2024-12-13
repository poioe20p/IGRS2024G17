#!/bin/bash

# Initialization & global vars
# if you execute this script for the second time
# you should change these variables to the latest
# domain name and ip address
DDOMAIN="open-ims\.test"
DSDOMAIN="open-ims\\\.test"
DEFAULTIP="127\.0\.0\.1"
CONFFILES=`ls *.cfg *.xml *.sql *.properties 2>/dev/null`

name=$1
echo $name
