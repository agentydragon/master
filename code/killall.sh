#!/bin/bash
for id in $(qstat -u prvak | grep R | cut -d. -f1 | tail -n+2); do
	echo "Killing $id.arien.ics.muni.cz..."
	qdel $id.arien.ics.muni.cz
done
