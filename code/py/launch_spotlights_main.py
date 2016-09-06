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

class Job(object):
    def __init__(self, i):
        self.i = i
        self.port = None
        self.job_id = None
        self.state = None

    def start_new(self):
        port = self.i + 2222
        SCRIPT="""
        cd /storage/brno7-cerit/home/prvak/master/code
        /storage/brno7-cerit/home/prvak/bin/bazel run --script_path $SCRATCHDIR/script.sh spotlight:Spotlight
        $SCRATCHDIR/script.sh %d
        """ % port
        # 4: not enough
        # 10: not enough
        job_id = pbs_util.launch(walltime="24:00:00",
                                 node_spec="nodes=1:brno:ppn=12,mem=16gb",
                                 job_name="spotlight_%d" % (self.i + 1),
                                 script=SCRIPT)
        print("port:", port)

        self.port = port
        self.job_id = job_id

    def refresh_state(self):
        self.state = pbs_util.get_job_state(self.job_id)

    def get_address(self):
        exec_host = self.state['exec_host'].split('+')[0].split('/')[0]
        address = ('http://%s:%d/rest/annotate' % (exec_host, self.port))
        return address

    def kill(self):
        pbs_util.kill_job(self.job_id)

jobs = []
for i in range(args.num_servers):
    job = Job(i)
    job.start_new()
    jobs.append(job)

def kill_jobs():
    print("Killing remaining jobs")
    for job in jobs:
        job.kill()
atexit.register(kill_jobs)

while True:
    waiting = False
    for i, job in enumerate(jobs):
        job.refresh_state()

        if job.state['job_state'] == 'Q':
            print(job.job_id, "still queued, waiting 30 seconds")
            sys.stdout.flush()
            waiting = True
            continue

        if job.state['job_state'] == 'C':
            print(job.job_id, "completed. replacing by new job in 30 seconds.")
            sys.stdout.flush()
            job.start_new()
            waiting = True
            continue

        assert job.state['job_state'] == 'R'

        try:
            spotlight.annotate_text("Barack Obama is the president of the United States.",
                                    spotlight_endpoint=job.get_address())
        except:
            waiting = True
            print(job.job_id, 'not yet OK:', sys.exc_info()[0], 'waiting 30 seconds')
            print(sys.exc_info()[1])
            sys.stdout.flush()
            continue
        else:
            print(job.job_id, "running OK.")

    if not waiting:
        break
    time.sleep(30)

print("All Spotlight servers running.")

addresses = []
for i, job in enumerate(jobs):
    address = job.get_address()
    print('Address:', address, 'job_id:', job.job_id, 'i:', i)
    addresses.append(address)

print("Addresses:", ','.join(addresses))
sys.stdout.flush()
