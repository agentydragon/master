from prototype.lib import pbs_util
from prototype.lib import file_util
import datetime
import paths

# walltime: 168h
# mem: 24gb
# scratch: 200gb

now = datetime.datetime.now()
log_base_dir = paths.LOG_PATH + "/" + 'fill-fuseki-dataset' + '/' + now.strftime('%Y%m%d-%H%M%S')
file_util.ensure_dir(log_base_dir)

pbs_util.launch_job(
    # walltime = '168h',
    walltime = '24h',
    # node_spec = 'nodes=1:brno:ppn=4,mem=24gb,scratch=200gb',
    node_spec = 'nodes=1:brno:ppn=4,mem=24gb,scratch=200gb',
    job_name = 'fill-fuseki-dataset',
    job_command = ['install/fill_fuseki_dataset'],
    output_path=(log_base_dir + "/stdout"),
    error_path=(log_base_dir + "/stderr")
)
