import subprocess
import sys

def launch_job(walltime, node_spec, job_name, job_command):
    qsub_command = ['qsub',
                    '-l', 'walltime=' + walltime,
                    '-l', node_spec,
                    '-m', 'abe',
                    '-N', job_name]
    print(qsub_command)
    job_script = ("""
#!/bin/bash

# TODO HAX
export LANG=en_US.UTF-8
export LANGUAGE=
export LC_CTYPE="en_US.UTF-8"
export LC_NUMERIC="en_US.UTF-8"
export LC_TIME="en_US.UTF-8"
export LC_COLLATE="en_US.UTF-8"
export LC_MONETARY="en_US.UTF-8"
export LC_MESSAGES="en_US.UTF-8"
export LC_PAPER="en_US.UTF-8"
export LC_NAME="en_US.UTF-8"
export LC_ADDRESS="en_US.UTF-8"
export LC_TELEPHONE="en_US.UTF-8"
export LC_MEASUREMENT="en_US.UTF-8"
export LC_IDENTIFICATION="en_US.UTF-8"
export LC_ALL=
# ^-- TODO HAX

module add jdk-8
module add python34-modules-gcc

cd $PBS_O_WORKDIR
""" + (' '.join(job_command)))

    js_path = job_name + '.sh'
    with open(js_path, 'w') as jobscript_file:
        jobscript_file.write(job_script)
    print(job_script)

    qsub_command.append(js_path)
    popen = subprocess.Popen(qsub_command,
                             #stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    stdoutdata, stderrdata = popen.communicate()#job_script)
    print(stdoutdata)
    print(stderrdata)
    if popen.returncode != 0:
        print(popen.returncode)
        sys.exit(1)
