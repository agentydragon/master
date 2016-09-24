import paths
from thirdparty import fuseki

from kazoo import client as kazoo_client

print('Connecting to ZooKeeper...')
kz = kazoo_client.KazooClient()
kz.start()

kz.ensure_path('/user/prvak/thesis')
kz.create(
    '/user/prvak/thesis/wikidata-service',
    b'hador:3030',
    makepath = True
)

fuseki.serve_forever(
    dataset_path = paths.WORK_DIR + '/fuseki-datasets/wikidata',
    namespace = '/wikidata'
)
