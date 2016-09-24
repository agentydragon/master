from prototype.lib import pbs_util

job = pbs_util.launch(
    walltime = "02:00:00",
    node_spec = "nodes=1:brno:ppn=4,mem=4gb,scratch=200gb",
    job_name = "local_fuseki",
    script = "../cpulimit/cpulimit -l 400 local_fuseki/local_fuseki",
)
print(job.job_id)

# TODO: wait until it boots up
