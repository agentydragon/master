from prototype.lib import pbs_util
import sys
import subprocess

extension = sys.argv[2]
assert extension in ['OU', 'ER']

job_id = sys.argv[1]
job = pbs_util.Job(job_id)
machine = print(job.get_state()['exec_host'].split('+')[0])

rv = subprocess.call([
    'ssh',
    machine,
    'tail -F /var/spool/torque/spool/' + job_id + '.' + extension,
])
sys.exit(rv)
