#!/usr/bin/python3

import pbs_util
import paths
import time

jobs = []

for i in range(3):
    port = i + 2222
    SCRIPT="""
    cd /storage/brno7-cerit/home/prvak/master/code
    /storage/brno7-cerit/home/prvak/bin/bazel run --script_path $SCRATCHDIR/script.sh spotlight:Spotlight
    $SCRATCHDIR/script.sh %d
    """ % port
    job_id = pbs_util.launch(walltime="24:00:00",
                             node_spec="nodes=1:brno:ppn=8,mem=16gb",
                             job_name="spotlight_%d" % (i + 1),
                             script=SCRIPT)
    print("port:", port)
    print(pbs_util.get_job_state(job_id))

    jobs.append({
        'port': port,
        'job_id': job_id
    })

while True:
    for job in jobs:
        job['state'] = pbs_util.get_job_state(job['job_id'])

    waiting = False
    for job in jobs:
        if job['state']['job_state'] == 'Q':
            print("job", job['job_id'], "still queued")
            waiting = True
            break
    if not waiting:
        break
    time.sleep(5)

print(jobs)

addresses = []
for job in jobs:
    exec_host = job['state']['exec_host'].split('+')[0].split('/')[0]
    address = 'http://' + exec_host + ':' + job['port'] + '/rest/annotate'
    addresses.append(address)

print("Addresses:", addresses)
