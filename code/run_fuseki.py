import paths
from thirdparty.fuseki import fuseki

from kazoo import client as kazoo_client

print('Connecting to ZooKeeper...')
kz = kazoo_client.KazooClient()
kz.start()

kz.ensure_path('/user/prvak/thesis')

node = '/user/prvak/thesis/wikidata-service'

if kz.exists(node):
    kz.delete(node)

kz.create(
    node,
    b'hador:3030',
    makepath = True
)

fuseki.serve_forever(
    dataset_path = paths.WORK_DIR + '/fuseki-datasets/wikidata',
    namespace = '/wikidata'
)
