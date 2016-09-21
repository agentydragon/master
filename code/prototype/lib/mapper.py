from py import paths
from py import pbs_util
from py import file_util
import datetime

def launch_in_slices(job_name, items, slice_size,
                     slice_to_commandline,
                     slice_to_walltime=None,
                     cores=2):
    if not slice_size:
        slices = [items]
    else:
        slices = []
        for i in range(0, len(items), slice_size):
            slices.append(items[i:i+slice_size])

    now = datetime.datetime.now()
    log_base_dir = paths.LOG_PATH + "/" + job_name + "/" + now.strftime('%Y%m%d-%H%M%S')
    file_util.ensure_dir(log_base_dir)


    for i, slice_items in enumerate(slices):
        if slice_to_walltime:
            walltime = slice_to_walltime(slice_items)
        else:
            walltime = None

        if walltime is None:
            walltime = "04:00:00"

        launch_job_for_slice(i, job_name, log_base_dir,
                             slice_to_commandline(slice_items),
                             walltime_estimate=str(walltime),
                             cores=cores)


def launch_job_for_slice(slice_index, job_name, log_base_dir,
                         job_command,
                         walltime_estimate,
                         cores=2):
    job = pbs_util.launch_job(
        # TODO: parallelize on one node
        walltime=walltime_estimate,
        node_spec="nodes=1:brno:ppn=%d,mem=2gb" % (cores),
        job_name=job_name,
        job_command=job_command,
        output_path=(log_base_dir + ("/%04d.o" % slice_index)),
        error_path=(log_base_dir + ("/%04d.e" % slice_index))
    )
    print("Launched %s:" % job_name, job.job_id)
