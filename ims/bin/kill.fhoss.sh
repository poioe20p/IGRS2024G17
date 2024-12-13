#!/bin/bash

ps fax | grep "\-S FHoSS -d" | grep -v "grep" | awk '{}{print $0; ;system( "kill -9 " $1);}'