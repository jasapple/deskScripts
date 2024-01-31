#!/bin/bash

exec >> logs/instance_launcher.log
exec 2>&1

/opt/homebrew/bin/python3 instance.py $@
