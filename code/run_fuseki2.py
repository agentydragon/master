import paths
from thirdparty.fuseki import fuseki

from kazoo import client as kazoo_client

print('Connecting to ZooKeeper...')
kz = kazoo_client.KazooClient()
kz.start()

node = '/user/prvak/thesis/dbpedia-service'

if kz.exists(node):
    kz.delete(node)

dbpedia_port = 3031

kz.create(
    node,
    bytes('hador:%d' % dbpedia_port, encoding='UTF-8'),
    makepath = True
)

fuseki.serve_forever(
    dataset_path = paths.WORK_DIR + '/fuseki-datasets/dbpedia-sameas',
    namespace = '/dbpedia-sameas',
    port = dbpedia_port
)
