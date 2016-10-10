# TODO: launch

from prototype.lib import pbs_util
import sys

job = pbs_util.Job(sys.argv[1])
print(job.get_state()['exec_host'])
