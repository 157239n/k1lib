#!/bin/bash

source ~/repos/tools/ips.sh

rm -f dist.pth
zip -r dist.pth . -x .git/\* -x test-envs/\* -x docs/\* -x build/\*

scp dist.pth kelvin@192.168.1.$ip2:/home/kelvin/repos/labs/k1lib/dist.pth
scp dist.pth kelvin@192.168.1.$ip3:/home/kelvin/repos/labs/k1lib/dist.pth
scp dist.pth kelvin@192.168.1.$ip4:/home/kelvin/repos/labs/k1lib/dist.pth

