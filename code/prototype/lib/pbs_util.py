import subprocess
import shlex
import sys
from prototype.lib import file_util
import paths
import datetime

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

class Job(object):
    def __init__(self, job_id):
        self.job_id = job_id

    def get_state(self):
        """
        Args:
            job (str) PBS job id
        """
        output = subprocess.check_output(["qstat", "-f", "-1", self.job_id]).decode('utf-8')
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

    def kill(self):
        print("Killing", self.job_id)
        subprocess.check_output(['qdel', self.job_id])

def launch(walltime, node_spec, job_name, script,
           error_path=None,
           output_path=None,
           save_jobscript_path=True):
    """
    Returns:
        PBS job ID (str)
    """
    qsub_command = ['qsub',
                    '-l', 'walltime=' + walltime,
                    '-l', node_spec,
                    '-m', 'abe', # Send mail when job terminates.
                    '-N', job_name
                    ]
    now = datetime.datetime.now()
    basedir = paths.LOG_PATH + "/" + job_name + "/" + now.strftime("%Y%m%d-%H%M%S")

    if error_path is None:
        error_path = basedir + "/stderr"
        file_util.ensure_dir(basedir)
    if output_path is None:
        output_path = basedir + "/stderr"
        file_util.ensure_dir(basedir)

    qsub_command.extend(['-e', error_path])
    qsub_command.extend(['-o', output_path])
    # print(qsub_command)
    job_script = (JOBSCRIPT_HEADER + script)

    if save_jobscript_path is True:
        save_jobscript_path = basedir + "/" + job_name + '.sh'
        file_util.ensure_dir(basedir)
    elif save_jobscript_path is None:
        save_jobscript_path = job_name + '.sh'

    with open(save_jobscript_path, 'w') as jobscript_file:
        jobscript_file.write(job_script)
    #print(job_script)

    qsub_command.append(save_jobscript_path)
    popen = subprocess.Popen(
        qsub_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdoutdata, stderrdata = popen.communicate()
    stdoutdata = stdoutdata.decode('utf-8')
    stderrdata = stderrdata.decode('utf-8')
    if popen.returncode != 0 or stderrdata != '':
        print('stdout:', stdoutdata)
        print('stderr:', stderrdata)
        print(popen.returncode)
        sys.exit(1)
    return Job(stdoutdata.strip())

# TODO: select error_path and output_path by default
def launch_job(walltime, node_spec, job_name, job_command,
               error_path=None,
               output_path=None,
               save_jobscript_path=True):
    assert isinstance(job_command, list)

    command = ' '.join(map(shlex.quote, job_command))
    return launch(
        walltime,
        node_spec,
        job_name,
        command,
        error_path=error_path,
        output_path=output_path,
        save_jobscript_path=save_jobscript_path,
    )
