import subprocess
import sys

JOBSCRIPT_HEADER = """
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
"""

def get_job_state(job):
    """
    Args:
        job (str) PBS job id
    """
    output = subprocess.check_output(["qstat", "-f", "-1", job])
    lines = output.split("\n")
    state = {}
    for line in lines:
        line = line.strip()
        if ' = ' in line:
            parts = line.split(" = ")
            if parts[0] == 'job_state':
                state['job_state'] = parts[1]
            if parts[0] == 'exec_host':
                state['exec_host'] = parts[1]
            if parts[0] == 'sched_nodespec':
                state['sched_nodespec'] = parts[1]
    return state

def launch(walltime, node_spec, job_name, script):
    """
    Returns:
        PBS job ID (str)
    """
    qsub_command = ['qsub',
                    '-l', 'walltime=' + walltime,
                    '-l', node_spec,
                    '-m', 'abe',
                    '-N', job_name]
    print(qsub_command)
    job_script = (JOBSCRIPT_HEADER + script)

    js_path = job_name + '.sh'
    with open(js_path, 'w') as jobscript_file:
        jobscript_file.write(job_script)
    #print(job_script)

    qsub_command.append(js_path)
    popen = subprocess.Popen(qsub_command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    stdoutdata, stderrdata = popen.communicate()
    if popen.returncode != 0:
        print('stdout:', stdoutdata)
        print('stderr:', stderrdata)
        print(popen.returncode)
        sys.exit(1)
    assert stderrdata == ''
    return stdoutdata.strip()

def launch_job(walltime, node_spec, job_name, job_command):
    launch(walltime, node_spec, job_name, ' '.join(job_command))