import paths
import datetime
from thirdparty.fuseki import fuseki
import fuseki_config
from prototype.lib import zk

# NOTE: must be absolute path
config_file_path = '/tmp/fuseki-config.ttl'
fuseki_config.write_config(config_file_path,
                           # '/scratch/prvak/wikidata',
                           paths.WORK_DIR + '/fuseki-datasets/merged')

# TODO: not really Hador...
zk.set_wikidata_endpoint('http://hador:3030/merged/query')
zk.set_dbpedia_endpoint('http://hador:3030/merged/query')

print("Starting Wikidata Fuseki...", datetime.datetime.now())
fuseki.serve_forever(
    config = config_file_path,
    port = 3030
)
