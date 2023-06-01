#!/bin/bash

rm -f dist.pth
zip -r dist.pth . -x .git/\* -x test-envs/\* -x docs/\* -x build/\*

scp dist.pth kelvin@192.168.1.43:/home/kelvin/repos/labs/k1lib/dist.pth
scp dist.pth kelvin@192.168.1.53:/home/kelvin/repos/labs/k1lib/dist.pth
scp dist.pth kelvin@192.168.1.57:/home/kelvin/repos/labs/k1lib/dist.pth

