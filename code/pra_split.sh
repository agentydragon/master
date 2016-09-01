#!/bin/bash

# cat pra-data | sort -R > pra-data-random
# head -n 5000000 pra-data-random > pra-data-random-background
# tail -n 538101 pra-data-random > pra-data-random-traintest

for X in P27 P21 P22 P25 P7 P9 P26 P451; do
# for X in P27; do
	echo "${X}..."
	cat /storage/brno7-cerit/home/prvak/data/pra-data | grep -P "\t$X\t" | cut -f1,3 | sed -e "s/$/\t1/" > /storage/brno7-cerit/home/prvak/pra/prvak/relation_metadata/no-such-file/relations/$X
done
