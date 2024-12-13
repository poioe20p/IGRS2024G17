#!/bin/bash

screen -S PRESENCE -d -m -h 10000 /bin/bash -c "opensips -f /home/igrs/Desktop/igrs-tools/ims/cfg/presence.cfg -E"
#sudo opensips -f /home/igrs/Desktop/ims/cfg/presence.cfg -E
