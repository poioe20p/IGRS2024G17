#!/bin/bash

#setkey -F
#setkey -FP

screen -S P-CSCF -d -m -h 10000 /bin/bash -c "LD_LIBRARY_PATH=/usr/local/lib/ser /opt/OpenIMSCore/ser_ims/ser -f /opt/OpenIMSCore/pcscf.cfg -D -D"

