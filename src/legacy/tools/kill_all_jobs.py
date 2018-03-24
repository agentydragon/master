from src.prototype.lib import pbs_util

for job in pbs_util.get_all_jobs():
    if job['status'] in ['Q', 'R']:
        pbs_util.Job(job['jobid']).kill()
