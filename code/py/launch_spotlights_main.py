#!/usr/bin/python3

import pbs_util
import paths

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
