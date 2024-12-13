#!/bin/bash

#sudo ./kill.fhoss.sh
#sudo ./kill.pcscf.sh
#sudo ./kill.icscf.sh
#sudo ./kill.scscf.sh
./stop.fhoss.sh
sudo killall ser
sudo killall opensips
