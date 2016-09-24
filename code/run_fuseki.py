import paths
from thirdparty.fuseki import fuseki

from kazoo import client as kazoo_client

print('Connecting to ZooKeeper...')
kz = kazoo_client.KazooClient()
kz.start()

node = '/user/prvak/thesis/wikidata-service'

if kz.exists(node):
    kz.delete(node)

wikidata_port = 3030

kz.create(
    node,
    bytes('hador:%d' % wikidata_port, encoding='UTF-8'),
    makepath = True
)

fuseki.serve_forever(
    dataset_path = paths.WORK_DIR + '/fuseki-datasets/wikidata',
    namespace = '/wikidata',
    port = wikidata_port
)

fuseki.serve_forever(
    dataset_path = paths.WORK_DIR + '/fuseki-datasets/wikidata',
    namespace = '/wikidata',
    port = wikidata_port
)
