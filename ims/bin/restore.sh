#!/bin/bash

# Restoring to default config values.
cp ../ims-default/cfg/*.cfg ../cfg/.
cp ../ims-default/cfg/*.xml ../cfg/.
cp ../ims-default/cfg/*.sql ../cfg/.

cp ../ims-default/bind/*.dnszone ../bind/.
cp ../ims-default/bind/named.conf.local ../bind/.
cp ../ims-default/bind/head ../bind/.

cp ../ims-default/FHoSS/deploy/*.xml ../FHoSS/deploy/.
cp ../ims-default/FHoSS/scripts/*.sql ../FHoSS/scripts/.

