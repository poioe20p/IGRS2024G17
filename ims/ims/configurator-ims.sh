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
domainname=$1
ip_address=$2

# input domain is to be slashed for cfg regexes 
slasheddomain=`echo $domainname | sed 's/\./\\\\\\\\\./g'`

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
				sed -i -e "s/$DDOMAIN/$domainname/g" $i
				sed -i -e "s/$DSDOMAIN/$slasheddomain/g" $i
				sed -i -e "s/$DEFAULTIP/$ip_address/g" $i
				sudo cp $i /opt/OpenIMSCore/.
				
				printf "$i " 
			   done 
			   echo 
			   break;

				elif [ -w $filename ] 
				then
				    printf "changing $filename \n"
				    sed -i -e "s/$DDOMAIN/$domainname/g" $filename
				    sed -i -e "s/$DSDOMAIN/$slasheddomain/g" $filename
				    sed -i -e "s/$DEFAULTIP/$ip_address/g" $filename
				    sudo cp $filename /opt/OpenIMSCore/.

					else 
					printf "cannot access file $filename. skipping... \n" 
		    fi
		    printf "File to Change:"
	    done 

