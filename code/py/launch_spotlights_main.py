import pbs_util
import paths


for i in range(5):
    port = i + 2222
    SCRIPT="""
    cd /storage/brno7-cerit/home/prvak/master/code
    /storage/brno7-cerit/home/prvak/bin/bazel run --script_path $SCRATCHDIR/script.sh spotlight:Spotlight
    $SCRATCHDIR/script.sh %d
    """ % port
    pbs_util.launch(walltime="24:00:00",
                    node_spec="nodes=1:brno:ppn=8,mem=16gb",
                    job_name="spotlight_%d" % (i + 1),
                    script=SCRIPT)
    print("port:", port)
