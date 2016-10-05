import paths
import datetime
from thirdparty.fuseki import fuseki
import fuseki_config
from prototype.lib import zk

# NOTE: must be absolute path
config_file_path = '/tmp/fuseki-config.ttl'
fuseki_config.write_config(
    config_file_path,
    datasets = {
        'wikidata': '/scratch/prvak/wikidata',
        'dbpedia-sameas': paths.WORK_DIR + '/fuseki-datasets/dbpedia-sameas',
        # TODO: 'merged' when we merge it
    },
)

# TODO: not really Hador...
zk.set_wikidata_endpoint('http://hador:3030/wikidata/query')
zk.set_dbpedia_endpoint('http://hador:3030/dbpedia-sameas/query')

print("Starting Fuseki...", datetime.datetime.now())
fuseki.serve_forever(
    config = config_file_path,
    port = 3030
)
