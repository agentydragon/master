#!/usr/bin/python3

import atexit
import spotlight
import pbs_util
import paths
import sys
import time

import argparse
parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('--num_servers', type=int, required=True)
args = parser.parse_args()

jobs = []

for i in range(args.num_servers):
    port = i + 2222
    SCRIPT="""
    cd /storage/brno7-cerit/home/prvak/master/code
    /storage/brno7-cerit/home/prvak/bin/bazel run --script_path $SCRATCHDIR/script.sh spotlight:Spotlight
    $SCRATCHDIR/script.sh %d
    """ % port
    # 4: not enough
    # 10: not enough
    job_id = pbs_util.launch(walltime="24:00:00",
                             node_spec="nodes=1:brno:ppn=12,mem=16gb",
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
            sys.stdout.flush()
            waiting = True
            break
        assert job['state']['job_state'] == 'R'
    if not waiting:
        break
    time.sleep(5)

print(jobs)

def kill_jobs():
    print("Killing remaining jobs")
    for job in jobs:
        pbs_util.kill_job(job['job_id'])
atexit.register(kill_jobs)

addresses = []
for i, job in enumerate(jobs):
    exec_host = job['state']['exec_host'].split('+')[0].split('/')[0]
    address = ('http://%s:%d/rest/annotate' % (exec_host, job['port']))

    print('Address:', address, 'job_id:', job['job_id'], 'i:', i)
    job['address'] = address

    addresses.append(address)

while True:
    all_ok = True
    for job in jobs:
        try:
            spotlight.annotate_text("Barack Obama is the president of the United States.",
                                    spotlight_endpoint=job['address'])
        except:
            print(job['address'], 'not yet OK:', sys.exc_info()[0])
            print(sys.exc_info()[1])
            sys.stdout.flush()
            all_ok = False
            break
    if all_ok:
        break
    time.sleep(30)

print("All Spotlight servers running.")

print("Addresses:", ','.join(addresses))
sys.stdout.flush()
