#!/bin/bash

clear

sudo apt-get update
sudo apt-get -y install subversion

sudo mkdir /opt/OpenIMSCore
cd /opt/OpenIMSCore

sudo mkdir FHoSS 
sudo svn checkout http://svn.berlios.de/svnroot/repos/openimscore/FHoSS/trunk FHoSS

sudo mkdir ser_ims 
sudo svn checkout http://svn.berlios.de/svnroot/repos/openimscore/ser_ims/trunk ser_ims

cd FHoSS 
sudo ant compile deploy 
cd ..

sudo apt-get -y install flex
sudo apt-get -y install bison
sudo apt-get -y install libcurl-ocaml-dev

cd ser_ims 
sudo make install-libs all 
cd ..

sudo cp ser_ims/cfg/*.cfg . 
sudo cp ser_ims/cfg/*.xml . 
sudo cp ser_ims/cfg/*.sh .

