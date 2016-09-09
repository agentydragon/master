#!/bin/bash
echo "Killing queued jobs:"
for id in $(qstat -u prvak | grep Q | cut -d. -f1 | tail -n+2); do
	echo "Killing $id.arien.ics.muni.cz..."
	qdel $id.arien.ics.muni.cz
done

echo "Killing running jobs:"
for id in $(qstat -u prvak | grep R | cut -d. -f1 | tail -n+2); do
	echo "Killing $id.arien.ics.muni.cz..."
	qdel $id.arien.ics.muni.cz
done
