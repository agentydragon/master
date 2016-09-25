import paths
from thirdparty.fuseki import fuseki
from prototype.lib import zk

# NOTE: must be absolute path
config_file_path = '/tmp/fuseki-config.ttl'
config.write_config(config_file_path,
                    paths.WORK_DIR + '/fuseki-datasets/wikidata',
                    paths.WORK_DIR + '/fuseki-datasets/dbpedia-sameas')

# TODO: not really Hador...
zk.set_wikidata_endpoint('hador:3030')
zk.set_dbpedia_endpoint('hador:3030')

print("Starting Wikidata Fuseki...", datetime.datetime.now())
fuseki.serve_forever(
    config = config_file_path,
    port = 3030
)
