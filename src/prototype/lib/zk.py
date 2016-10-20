from src.prototype.lib import flags
from kazoo import client as kazoo_client

flags.add_argument('--zk_enabled', default=False, type=bool,
                   help='Enables Zookeeper service discovery.')

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

WIKIDATA_NODE = '/user/prvak/thesis/wikidata-service'

def get_wikidata_endpoint():
    if not maybe_connect():
        return

    if kz.exists(WIKIDATA_NODE):
        return kz.get(WIKIDATA_NODE)[0].decode('UTF-8')

def set_wikidata_endpoint(wikidata_endpoint):
    force_connect()

    if kz.exists(WIKIDATA_NODE):
        kz.delete(WIKIDATA_NODE)

    kz.create(
        WIKIDATA_NODE,
        bytes(wikidata_endpoint, encoding='UTF-8'),
        makepath = True
    )

DBPEDIA_NODE = '/user/prvak/thesis/dbpedia-service'

def get_dbpedia_endpoint():
    if not maybe_connect():
        return

    if kz.exists(DBPEDIA_NODE):
        return kz.get(DBPEDIA_NODE)[0].decode('UTF-8')

def set_dbpedia_endpoint(dbpedia_endpoint):
    force_connect()

    if kz.exists(DBPEDIA_NODE):
        kz.delete(DBPEDIA_NODE)

    kz.create(
        DBPEDIA_NODE,
        bytes(dbpedia_endpoint, encoding='UTF-8'),
        makepath = True
    )

SPOTLIGHT_NODE = '/user/prvak/thesis/spotlight-annotators'

def get_spotlight_endpoint():
    if not maybe_connect():
        return

    if kz.exists(SPOTLIGHT_NODE):
        return kz.get(SPOTLIGHT_NODE)[0].decode('UTF-8')

def set_spotlight_endpoint(spotlight_endpoint):
    force_connect()

    if kz.exists(SPOTLIGHT_NODE):
        kz.delete(SPOTLIGHT_NODE)

    kz.create(
        SPOTLIGHT_NODE,
        bytes(spotlight_endpoint, encoding='UTF-8'),
        makepath = True
    )
