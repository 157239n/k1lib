#!/bin/bash

echo 1; sleep 0.5
echo This message goes to stderr >&2
echo 2; sleep 0.5
echo $(</dev/stdin)
sleep 0.5; echo 3
