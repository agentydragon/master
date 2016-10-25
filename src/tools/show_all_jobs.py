from src.prototype.lib import pbs_util

data = []
data.append(['Status', 'ID', 'Name', 'Machine', 'Runtime', 'Target runtime'])
for job in pbs_util.get_all_jobs():
    data.append([
        job['status'],
        job['jobid'],
        job['jobname'],
        job['job_machine'],
        job['runtime'],
        job['target_walltime']
    ])

import terminaltables
print(terminaltables.AsciiTable(data).table)
