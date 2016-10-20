from src.prototype.lib import pbs_util

# 2016-10-07: creating merged dataset took 25 000 seconds on Hador's HDD
# 2016-10-07: 48gb of RAM is not enough, just after finishing load phase. (sort phase limit applied)
# 2016-10-11: took 7:43:56 to finish, while running on screen in Hador

# walltime: 168h
# mem: 24gb
# scratch: 200gb

pbs_util.launch_job(
    # walltime = '168h',
    # walltime = '24h',
    walltime = '12h',
    # node_spec = 'nodes=1:brno:ppn=4,mem=24gb,scratch=200gb',
    # node_spec = 'nodes=1:brno:ppn=4,mem=48gb,scratch=500gb:ssd',
    # node_spec = 'nodes=1:brno:ppn=4,mem=60gb,scratch=500gb:ssd',
    node_spec = 'nodes=1:brno:ppn=4,mem=48gb,scratch=300gb:ssd',
    job_name = 'fill-fuseki-dataset',
    job_command = ['install/fill_fuseki_dataset'],
    #scratch_type = 'ssd',
)
