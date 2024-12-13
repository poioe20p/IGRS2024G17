#!/bin/bash

# Initialization & global vars
# if you execute this script for the second time
# you should change these variables to the latest
# domain name and ip address
DDOMAIN="open-ims\.test"
DSDOMAIN="open-ims\\\.test"
DEFAULTIP="127\.0\.0\.1"
CONFFILES=`ls *.cfg *.xml *.sql *.properties 2>/dev/null`

# Interaction
printf "Domain Name:"
read domainname 
printf "IP Adress:"
read ip_address

# input domain is to be slashed for cfg regexes 
slasheddomain=`echo $domainname | sed 's/\./\\\\\\\\\./g'`

	if [ $# != 0 ] 
	then 
	printf "changing: "
	    for j in $* 
	    do
		printf "$j " 
	    done
	echo 
	else 
	printf "File to change [\"all\" for everything, \"exit\" to quit]:"
	# loop
	    while read filename ;
	    do
		    if [ "$filename" = "exit" ] 
		    then 
		    printf "exitting...\n"
		    break ;

			elif [ "$filename" = "all" ]
			then    
			    printf "changing: "
			   for i in $CONFFILES 
			   do
				printf "$i " 
			   done 
			   echo 
			   break;

				elif [ -w $filename ] 
				then
				    printf "changing $filename \n"
					else 
					printf "cannot access file $filename. skipping... \n" 
		    fi
		    printf "File to Change:"
	    done 
	fi
