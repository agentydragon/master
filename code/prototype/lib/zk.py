from prototype.lib import flags
from kazoo import client as kazoo_client

flags.add_argument('--zk_enabled', default=False, type=bool)

kz = kazoo_client.KazooClient()

def start():
    print('Connecting to ZooKeeper...')
    kz.start()

def force_connect():
    if kz.client_state == 'CONNECTED':
        return
    print('Force-connecting to ZooKeeper...')
    kz.start()

def maybe_connect():
    if kz.client_state == 'CONNECTED':
        return True

    if flags.parse_args().zk_enabled:
        print('Connecting to ZooKeeper by flag')
        start()
        return True

    print('WARN: Kazoo client not connected')
    return False

def get_wikidata_endpoint():
    if not maybe_connect():
        return

    wikidata_endpoint_node = '/user/prvak/thesis/wikidata-service'

    if kz.exists(wikidata_endpoint_node):
        return kz.get(wikidata_endpoint_node)[0].decode('UTF-8')

def get_dbpedia_endpoint():
    if not maybe_connect():
        return

    dbpedia_endpoint_node = '/user/prvak/thesis/dbpedia-service'

    if kz.exists(dbpedia_endpoint_node):
        return kz.get(dbpedia_endpoint_node)[0].decode('UTF-8')

def get_spotlight_endpoint():
    if not maybe_connect():
        return

    node = '/user/prvak/thesis/spotlight-annotators'

    if kz.exists(node):
        return kz.get(node)[0].decode('UTF-8')

def set_spotlight_endpoint(spotlight_endpoint):
    force_connect()

    node = '/user/prvak/thesis/spotlight-annotators'

    if kz.exists(node):
        kz.delete(node)

    kz.create(
        node,
        bytes(spotlight_endpoint, encoding='UTF-8'),
        makepath = True
    )
