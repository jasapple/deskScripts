#!/bin/bash

exec >> logs/vpn.log
exec 2>&1

/opt/cisco/anyconnect/bin/vpn disconnect
