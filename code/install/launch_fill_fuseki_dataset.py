from prototype.lib import pbs_util

# walltime: 168h
# mem: 24gb
# scratch: 200gb

pbs_util.launch_job(
    # walltime = '168h',
    walltime = '24h',
    # node_spec = 'nodes=1:brno:ppn=4,mem=24gb,scratch=200gb',
    node_spec = 'nodes=1:brno:ppn=4,mem=24gb,scratch=200gb',
    job_name = 'fill-fuseki-dataset',
    job_command = ['install/fill_fuseki_dataset'],
)
