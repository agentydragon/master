import paths
from prototype.lib import pbs_util
from prototype.lib import file_util
import datetime

def launch_in_slices(job_name, items, slice_size,
                     slice_to_commandline,
                     slice_to_walltime=None,
                     cores=2,
                     ram='2gb',
                     scratch='100mb'):
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

        commandline = slice_to_commandline(slice_items)
        commandline = [
            '../cpulimit/cpulimit',
            '--limit=' + str(CORES * 100),
            '--include-children',
        ] + commandline

        launch_job_for_slice(
            i, job_name, log_base_dir,
            commandline,
            walltime_estimate=str(walltime),
            cores=cores,
            ram=ram,
            scratch=scratch
        )


def launch_job_for_slice(slice_index, job_name, log_base_dir,
                         job_command,
                         walltime_estimate,
                         cores=2,
                         ram='2gb',
                         scratch='100mb'):
    job = pbs_util.launch_job(
        # TODO: parallelize on one node
        walltime=walltime_estimate,
        node_spec="nodes=1:brno:ppn=%d,mem=%s,scratch=%s" % (cores, ram, scratch),
        job_name=('%s_%d' % (job_name, slice_index)),
        job_command=job_command,
        output_path=(log_base_dir + ("/%04d.o" % slice_index)),
        error_path=(log_base_dir + ("/%04d.e" % slice_index))
    )
    print("Launched %s:" % job_name, job.job_id)
