#!/bin/bash

cd /k1a

pip install . >> /base/log 2>&1

cd /k1lib

pip install .[extras] >> /base/log 2>&1
python /k1lib/test-envs/test.py > "/k1lib/test-envs/test-outputs/$RANDOM" 2>&1

tail -f /dev/null

