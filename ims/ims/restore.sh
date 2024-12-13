#!/bin/bash

# Restoring to default config values.
cp ../ims-default/cfg/*.cfg .
cp ../ims-default/cfg/*.xml .

cp ../ims-default/bind/*.dnszone ./bind/.
cp ../ims-default/bind/named.conf.local ./bind/.

cp ../ims-default/FoHSS/deploy/*.xml ./FoHSS/deploy/.
cp ../ims-default/FoHSS/scripts/*.sql ./FoHSS/scripts/.

